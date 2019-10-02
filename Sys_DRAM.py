import System;
import Memory;

class Dram(System.system):

    name= "dram"
    desc="No DVS with dram"
    def assign_task(self, system_task):
        system_task.idx_cpufreq=1
        return Memory.assgign_mem(system_task, 2)

    def reassign_task(self,system_task):
        return True



