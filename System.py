from abc import *
from CPU import NoneDVFSCPU, DVFSCPU
from Memory import Memory, Memories
import heapq
from Task import Task


class System(metaclass=ABCMeta):
    """super class of all POLICYs"""

    def __init__(self):
        self.name = None
        self.desc = None

        self.CPU = None
        self.memories = None

        self.end_sim_time = None
        self.verbose = None

        self.tasks = []
        self.wait = []
        self.queue = []

        self.sum_utils = 0
        self.n_utils = 0

        self.power_consumed_cpu_active = 0
        self.power_consumed_mem_active = 0
        self.power_consumed_cpu_idle = 0
        self.power_consumed_mem_idle = 0

    def run(self):
        # Console input
        self.end_sim_time = int(input("실행할 시뮬레이션 시간을 입력하세요(정수): "))
        verbose = int(input("상세 출력을 원하시면 1을 입력하세요: "))
        if verbose == 1:
            self.verbose = True
        else:
            self.verbose = False

        # Set input files
        self.set_processor()
        self.set_memory()
        self.set_tasks()
        self.setup_tasks()

        # Run simulator...
        time = 0
        prev_exec_task = None
        while time <= self.end_sim_time:
            print(f'time = {time}')
            if self.verbose:
                print(self.print_queue())

            if len(self.queue) == 0:
                # for cpu
                self.power_consumed_cpu_idle += self.CPU.cpufreqs[-1].power_idle
                # for mem
                for task in self.tasks:
                    self.power_consumed_mem_idle += task.memory_req * task.memory.power_idle

            else:
                exec_task = heapq.heappop(self.queue)[1]
                if prev_exec_task != exec_task:
                    self.reassign_task(exec_task)
                prev_exec_task = exec_task

                print(f'{time}부터 {time+1}까지 {exec_task.no} 실행')

                # for a task (1 unit 실행)
                wcet_scaled_cpu = 1/exec_task.cpu_frequency.wcet_scale
                wcet_scaled_mem = 1/exec_task.memory.wcet_scale
                wcet_scaled = wcet_scaled_cpu + wcet_scaled_mem
                self.power_consumed_cpu_active += exec_task.cpu_frequency.power_active * wcet_scaled_cpu / wcet_scaled
                self.power_consumed_cpu_idle += exec_task.cpu_frequency.power_idle * wcet_scaled_mem / wcet_scaled
                self.power_consumed_mem_active += \
                    exec_task.memory.power_active * exec_task.memory_req * exec_task.memory_active_ratio
                self.power_consumed_mem_idle += \
                    exec_task.memory.power_idle * exec_task.memory_req * (1 - exec_task.memory_active_ratio)
                exec_task.deadline -= 1
                exec_task.det_remain -= 1

                # for other tasks (전력 소모 계산 및 1초 흐르기)
                for i in range(len(self.queue)):
                    task = self.queue[i][1]
                    task.deadline -= 1
                    self.queue[i] = (task.calc_priority(), task)
                    self.power_consumed_mem_idle += task.memory_req * task.memory.power_idle
                heapq.heapify(self.queue)  # 재정렬 필요
                for tup in self.wait:
                    task = tup[1]
                    self.power_consumed_mem_idle += task.memory_req * task.memory.power_idle

                self.add_utilization()
                self.check_queued_tasks()

                # task 주기 끝났는지 확인해서 끝났으면 초기화 시키고 wait으로
                if exec_task.det_remain == 0:
                    exec_task.period_start += exec_task.period
                    exec_task.det_remain = exec_task.det
                    exec_task.deadline = exec_task.period
                    heapq.heappush(self.wait, (exec_task.period_start, exec_task))
                else:
                    heapq.heappush(self.queue, (exec_task.calc_priority(), exec_task))

            # 타임 1더하고 wait중에 타임이랑 같은 건 큐로 넣어줌,
            time += 1

            while len(self.wait) != 0:
                if self.wait[0][0] > time:
                    break
                task = heapq.heappop(self.wait)[1]
                heapq.heappush(self.queue, (task.calc_priority(), task))

        time -= 1
        self.result_print(time)

    def add_utilization(self):
        self.sum_utils += self.get_tasks_ndet()
        self.n_utils += 1

    def result_print(self, time: int):
        power_consumed_cpu = self.power_consumed_cpu_active + self.power_consumed_cpu_idle
        power_consumed_mem = self.power_consumed_mem_active + self.power_consumed_mem_idle
        power_consumed_active = self.power_consumed_cpu_active + self.power_consumed_mem_active
        power_consumed_idle = self.power_consumed_cpu_idle + self.power_consumed_mem_idle
        power_consumed = power_consumed_cpu + power_consumed_mem

        power_consumed_avg = power_consumed / time
        power_consumed_cpu_avg = power_consumed_cpu / time
        power_consumed_mem_avg = power_consumed_mem / time
        power_consumed_active_avg = power_consumed_active / time
        power_consumed_idle_avg = power_consumed_idle / time
        utilization = float(self.sum_utils) / self.n_utils * 100

        print(f'policy: {self.name}')
        print(f'simulation time elapsed: {time}')
        print(f'average power consumed: {power_consumed_avg}')
        print(f'CPU + MEM power consumed: {power_consumed_cpu_avg} + {power_consumed_mem_avg}')
        print(f'ACTIVE + IDLE power consumed: {power_consumed_active_avg} + {power_consumed_idle_avg}')
        print(f'utilzation: {utilization}%')

    @abstractmethod
    def assign_task(self, task) -> bool:
        pass

    @abstractmethod
    def reassign_task(self, task) -> bool:
        pass

    def set_processor(self, input_file="input_processor.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                n_frequency = int(f.readline())
                for i in range(n_frequency):
                    temp = f.readline().split()
                    self.CPU.insert_cpufreq(
                        wcet_scale=float(temp[0]), power_active=float(temp[1]), power_idle=float(temp[2]))
        except FileNotFoundError:
            System.error("processor 설정 파일을 찾을 수 없습니다.")

    def set_memory(self, input_file="input_mem.txt"):
        try:
            self.memories = Memories()
            with open(input_file, "r", encoding='UTF8') as f:
                for i in range(2):
                    temp = f.readline().split()
                    self.memories.insert_memory(memory_str=temp[0], capacity=int(temp[1]), wcet_scale=float(temp[2]),
                                                power_active=float(temp[3]), power_idle=float(temp[4]))
        except FileNotFoundError:
            System.error("memory 정보 파일을 찾을 수 없습니다.")

    def get_tasks_ndet(self) -> float:
        result = 0.0
        for task in self.tasks:
                result += float(task.det) / task.period
        return result

    def get_tasks_ndet_except(self, task_except) -> float:
        result = 0.0
        for task in self.tasks:
            if task.no != task_except.no:
                result += float(task.det) / task.period
        return result

    def is_schedule(self, task) -> bool:
        if self.get_tasks_ndet_except(task) + (task.det * 1.0 / task.period) <= 1:
            return True
        return False

    def setup_tasks(self) -> bool:
        for task in self.tasks:
            if not self.assign_task(task):
                raise Exception(task.no + ": insufficient memory")
            task.calc_det()
            if not self.is_schedule(task):
                raise Exception(task.no + ": unschedule task")
            heapq.heappush(self.queue, (task.calc_priority(), task))
        return True

    def set_tasks(self, input_file="input_tasks.txt"):
        # 일단 tasks 에 순서대로 담기
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                n_task = int(f.readline())
                for i in range(n_task):
                    temp = f.readline().split()
                    self.tasks.append(Task(wcet=int(temp[0]), period=int(temp[1]),
                                      mem_req=int(temp[2]), mem_active_ratio=float(temp[3])))
        except FileNotFoundError:
            System.error("task 정보 파일을 찾을 수 없습니다.")

    def check_queued_tasks(self):
        for task in self.tasks:
            task.check_task()

    def print_queue(self):
        temp = []
        while len(self.queue) > 0:
            tup = heapq.heappop(self.queue)
            str = tup[1].desc_task()
            print(f'priority:{tup[0]} /{str}')
            temp.append(tup)
        heapq.heapify(temp)
        self.queue = temp


class Dram(System):
    def __init__(self):
        super().__init__()
        self.name = "DRAM"
        self.desc = "No DVFS with dram(dram)"
        self.CPU = NoneDVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)
        return self.memories.assign_memory(task, Memory.TYPE_DRAM)

    def reassign_task(self, task) -> bool:
        return self.CPU.reassign_cpufreq(task, self)


class Hm(System):
    def __init__(self):
        super().__init__()
        self.name = "HM"
        self.desc = "Hybrid memory(hm)"
        self.CPU = NoneDVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)

        mem_types = [Memory.TYPE_DRAM, Memory.TYPE_LPM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                return True
        return False

    def reassign_task(self, task) -> bool:
        self.CPU.reassign_cpufreq(task, self)

        Memories.revoke_memory(task)

        mem_types = [Memory.TYPE_LPM, Memory.TYPE_DRAM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                task.calc_det()
                if self.is_schedule(task):
                    return True
                task.revert_det()
        return False


class DvfsDram(System):
    def __init__(self):
        super().__init__()
        self.name = "DVFS_DRAM"
        self.desc = "DVFS with dram(dvfs-dram)"
        self.CPU = DVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)
        if not self.memories.assign_memory(task, Memory.TYPE_DRAM):
            return False
        return True

    def reassign_task(self, task) -> bool:
        return self.CPU.reassign_cpufreq(task, self)


class DvfsHm(System):
    def __init__(self):
        super().__init__()
        self.name = "DVFS_HM"
        self.desc = "DVFS with hybrid memory(dvs-hm)"
        self.CPU = DVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)

        mem_types = [Memory.TYPE_DRAM, Memory.TYPE_LPM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                return True
        return False

    def reassign_task(self, task) -> bool:
        Memories.revoke_memory(task)

        mem_types = [Memory.TYPE_LPM, Memory.TYPE_DRAM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                if self.CPU.reassign_cpufreq(task, self):
                    return True
                Memories.revoke_memory(task)
        return False
