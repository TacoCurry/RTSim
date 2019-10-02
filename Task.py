import Memory
import CPU

class Task:
    n_task = 0
    task_list = []

    def __init__(self, wcet, period, memory_req, memory_active_ratio):
        self.wcet = wcet
        self.period = period
        self.memory_req = memory_req
        self.memory_active_ratio = memory_active_ratio

        self.idx_cpufreq=0
        self.det = 0
        self.det_remain = 0
        self.gap = 0

        self.det_old = 0
        self.det_remain_old =0

        Task.n_task += 1
        self.no = Task.n_task
        Task.task_list.append(self)

    def set_memory(self, memory: Memory.Memory):
        self.memory: Memory.Memory = memory

    def set_cpu_frequency(self, cpu_frequency: CPU.CpuFrequency):
        self.cpu_frequency: CPU.CpuFrequency = cpu_frequency

    def revert_task_det(self,det,det_remain):
        self.det= self.det_old
        self.det_remain=self.det_remain_old


    @staticmethod
    def calculate_det(task):
        pass

    @staticmethod
    def get_real_execution_time(task):
        if task.det_remain < task.gap:
            return task.det_remain
        else:
            return task.gap

    @staticmethod
    def is_schedulable(task):
        pass

