import Task;


class System:
    """super class of all POLICYs"""
    def __init__(self,name,desc):
        self.task = Task.Task()
        self.name=name
        self.desc=desc

    def assign_task(self, task):
        pass
        # system_task.idx_cpufreq=1
        # return 1;

    def reassign_task(self,task):
        return 1;

