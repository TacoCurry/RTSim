import System;
import Memory;
import Task;
class Dram(System.system):

    System.system.name= "dram"
    System.system.desc="No DVS with dram"
    def assign_task(self, task):
        Task.Task.idx_cpufreq=1
        return Memory.Memory.assign_memory(task, Memory.Memory.TYPE_DRAM)

    def reassign_task(self,task):
        return True



