import math


class Task:
    n_task = 0
    tasks = []

    def __init__(self, wcet, period, mem_req, mem_active_ratio):
        self.wcet = wcet
        self.period = period
        self.memory_req = mem_req
        self.memory_active_ratio = mem_active_ratio

        self.no = None
        self.cpufreq = None
        self.memory = None

        self.det = None
        self.det_remain = None
        self.det_old = None
        self.det_remain_old = None

        self.gap = None



    def set_memory(self, memory):
        self.memory = memory

    def set_cpu_frequency(self, cpu_frequency):
        self.cpu_frequency = cpu_frequency



    @staticmethod
    def insert_task(wcet: int, period: int, mem_req: int, mem_active_ratio: float):
        task = Task(wcet, period, mem_req, mem_active_ratio)
        Task.n_task += 1
        task.no = Task.n_task
        Task.tasks.append(task)

    @staticmethod
    def calc_task_det(task):
        new_det = task.wcet / (task.cpufreq.wcet_scale * task.memory.wcet_scale)

        task.det_old = task.det
        task.det = int(round(new_det))
        if task.det == 0:
            task.det = 1

        task.det_remain_old = task.det_remain
        if task.det_remain > 0 & task.det != task.det_old:
            task.det_remain = int(round(task.det_remain * (new_det / task.det_old)))

    @staticmethod
    def revert_task_det(task):
        task.det = task.det_old
        task.det_remain = task.det_remain_old

    @staticmethod
    def get_tasks_ndet() -> float:
        result = 0.0
        for task in Task.tasks:
            result += task.det * 1.0 / task.period
        return result

    @staticmethod
    def is_schedulable(task) -> bool:
        if Task.get_tasks_ndet() + (task.det * 1.0 / task.period) <= 1:
            return True
        return False

    @staticmethod
    def set_tasks() -> bool:
        pass


    @staticmethod
    def get_real_execution_time(task):
        if task.det_remain < task.gap:
            return task.det_remain
        else:
            return task.gap



