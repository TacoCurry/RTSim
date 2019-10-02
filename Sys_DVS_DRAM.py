import System
import CPU

dram_cpu = CPU.cpu

class Dvs_dram(System.system):
    def assign_task(self,system_task):
        system_task.idx_cpufreq=1
        if not assign_mem(system_task,2):
            return False

    def reassign_task(self,system_task):
        for i in range(cpu.n_cpufreq,1,-1):
            system_task.idx_cpufreq=i
            system_task.cal_task_det(system_task)

