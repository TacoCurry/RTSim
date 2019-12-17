class Task:
    def __init__(self, wcet, period, mem_req, mem_active_ratio, read_ratio=0.5):
        self.wcet = wcet
        self.period = period
        self.mem_req = mem_req
        self.mem_active_ratio = mem_active_ratio
        self.read_ratio = read_ratio


class Tasks:
    def __init__(self):
        self.n_task = 0
        self.list = []

    def insert_task(self, task):
        self.list.append(task)
        self.n_task += 1

    def get_task(self, index):
        return self.list[index]
