import Task;



class system:
    '''super class of all POLICYs'''
    def __init__(self):
        self.system_task = Task.Task()

    def assign_task(self,system_task):
        system_task.idx_cpufreq=1
        return 1;

    def reassign_task(self,system_task):
        return 1;

class policy_t:
    def __init__(self, name,desc,single_memtype, ):