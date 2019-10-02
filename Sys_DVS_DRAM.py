import System
import CPU
import Memory
import Task

class Dvs_Dram(System.system):
    System.system.name = "dvsdram"
    System.system.desc = "DVS with dram(dvs-dram)"

    def assign_task(self, task: Task.Task):
        Task.Task.idx_cpufreq=1
        if not Memory.Memory.assign_memory(task, Memory.Memory.TYPE_DRAM):
            return False

    def reassign_task(self, task: Task.Task):
        for i in range(CPU.CPU.n_cpufreqs,1,-1):
            Task.Task.idx_cpufreq=1
            Task.cal_task_det(task)
            if(Task.Task.is_schedulable(task)):
                return True
            Task.Task.revert_task_det(task)
        return False



