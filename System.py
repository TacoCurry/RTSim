import Task;



class system:
    '''super class of all POLICYs'''
    def __init__(self,name,desc):
        self.system_task = Task.Task()
        self.name=name
        self.desc=desc

    def assign_task(self, system_task: Task.Task):
        pass
        # system_task.idx_cpufreq=1
        # return 1;

    def reassign_task(self,system_task):
        return 1;

