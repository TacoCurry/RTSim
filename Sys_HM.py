import System
import CPU
import Memory
import Task

class Hm(System.system):
    System.system.name = "hm"
    System.system.desc = "hybrid memory"

    def assign_task(self, task):
        mem_types = [Memory.Memory.TYPE_LPM, Memory.Memory.TYPE_DRAM]
        Task.Task.idx_cpufreq = 1
        for mem_type in mem_types:
            if(Memory.Memory.assign_memory(task, mem_type)):
                return True
        return False

    def reassign_task(self,task):
        mem_types = [Memory.Memory.TYPE_LPM, Memory.Memory.TYPE_DRAM]
        Memory.Memory.revoke_memory()
        for mem_type in mem_types:
           if Memory.Memory.assign_memory(task, mem_type):
                Task.Task.calculate_det(task)
                if Task.Task.is_schedulable(task):
                    return True
                Task.Task.revert_task_det(task)
        return False


