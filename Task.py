class Task:
    n_task = 0

    def __init__(self, wcet, period, mem_req, mem_active_ratio, cpu):
        self.wcet = wcet
        self.period = self.deadline = period
        self.memory_req = mem_req
        self.memory_active_ratio = mem_active_ratio

        Task.n_task = Task.n_task + 1
        self.no = Task.n_task

        self.cpu = cpu
        self.cpu_frequency = None
        self.memory = None

        self.det = 0
        self.det_remain = 0
        self.det_old = None
        self.det_remain_old = None

        self.period_start = 0

    def __lt__(self, other):
        return self.no < other.no

    def calc_priority(self) -> float:
        # min heap 사용을 위해 역수로 계산.
        return float(self.deadline)/self.det_remain

    def calc_det(self):
        new_det = self.wcet / (self.cpu_frequency.wcet_scale * self.memory.wcet_scale)

        self.det_old = self.det
        self.det = int(round(new_det))
        if self.det == 0:
            self.det = 1

        self.det_remain_old = self.det_remain
        if not self.det_remain:
            self.det_remain = self.det
        elif self.det_remain > 0 & self.det != self.det_old:
            self.det_remain = int(round(self.det_remain * (new_det / self.det_old)))

    def revert_det(self):
        self.det = self.det_old
        self.det_remain = self.det_remain_old

    def desc_task(self) -> str:
        return (f'    [no:{self.no}, wcet:{self.wcet}, period:{self.period}, ' +
                f'cpu_freq(scale):{self.cpu_frequency.wcet_scale}, memory:{self.memory.type}, ' +
                f'det:{self.det}, det_remain:{self.det_remain}, deadline:{self.deadline}]')

    def check_task(self):
        if self.det == 0:
            raise Exception(self.desc_task()+": zero det.")
        if self.det < self.det_remain:
            raise Exception(self.desc_task() + ": invalid det.")
        if self.deadline < 0:
            raise Exception(self.desc_task() + ": negative deadline")
        return True

    def revoke_memory(self):
        self.memory.used_capacity -= self.memory_req
        self.memory = None

    def exec_idle(self, time: int, update_deadline: bool):
        self.memory.power_consumed_idle += time * self.memory_req * self.memory.power_idle
        if update_deadline:
            self.deadline -= 1

    def exec_active(self, time: int):
        wcet_scaled_cpu = 1 / self.cpu_frequency.wcet_scale
        wcet_scaled_mem = 1 / self.memory.wcet_scale
        wcet_scaled = wcet_scaled_cpu + wcet_scaled_mem

        self.cpu.add_power_consumed_active(time * self.cpu_frequency.power_active * wcet_scaled_cpu / wcet_scaled)
        self.cpu.add_power_consumed_idle(time * self.cpu_frequency.power_idle * wcet_scaled_mem / wcet_scaled)
        self.memory.add_power_consumed_active(
            time * self.memory.power_active * self.memory_req * self.memory_active_ratio)
        self.memory.add_power_consumed_idle(
            time * self.memory.power_idle * self.memory_req * (1 - self.memory_active_ratio))

        self.deadline -= time
        self.det_remain -= time
