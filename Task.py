class Task:
    n_task = 0
    task_list = []

    def __init__(self, wcet, period, memory_req, memory_active_ratio):
        self.wcet = wcet
        self.period = period
        self.memory_req = memory_req
        self.memory_active_ratio = memory_active_ratio

        self.det = 0
        self.det_remain = 0
        self.gap = 0

        Task.n_task += 1
        self.no = Task.n_task
        Task.task_list.append(self)

    @staticmethod
    def calculate_det(task):
        new_det = task.wcet /

    @staticmethod
    def get_real_execution_time(task):
        if task.det_remain < task.gap:
            return task.det_remain
        else: return task.gap




