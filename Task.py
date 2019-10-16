class Task:
    n_task = 0

    def __init__(self, wcet, period, mem_req, mem_active_ratio):
        self.wcet = wcet
        self.period = self.deadline = period
        self.memory_req = mem_req
        self.memory_active_ratio = mem_active_ratio

        Task.n_task = Task.n_task + 1
        self.no = Task.n_task

        self.cpu_frequency = None
        self.memory = None

        self.det = 0
        self.det_remain = 0
        self.det_old = None
        self.det_remain_old = None

        self.period_start = 0

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
        return f'[no:{self.no}, wcet:{self.wcet}, period:{self.period}, ' \
               f'cpu_freq(scale):{self.cpu_frequency.wcet_scale}, memory:{self.memory.type}, ' \
               f'det:{self.det}, det_remain:{self.det_remain}, deadline:{self.deadline}]'

    def check_task(self):
        if self.det == 0:
            raise Exception(self.desc_task()+": zero det.")
        if self.det < self.det_remain:
            raise Exception(self.desc_task() + ": invalid det.")
        if self.deadline < 0:
            raise Exception(self.desc_task() + ": negative deadline")
        return True
