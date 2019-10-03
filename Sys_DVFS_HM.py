import System
import CPU
import Memory
import Task


class DVFS_HM(System.System):
    System.System.name= "dvshm"
    System.System.desc= "DVS with hybrid memory(dvs-hm)"

    def assign_task(self, task):
        mem_types = [Memory.Memory.TYPE_LPM, Memory.Memory.TYPE_DRAM]
        for mem_type in mem_types:
            Memory.Memory.assign_memory(task, mem_type)
            Task.Task.calculate_det(task)
            if Task.Task.is_schedulable(task):
                return True
            Task.Task.revert_task_det(task)
        return False

    def reassign_task(self,task):
        mem_types = [Memory.Memory.TYPE_LPM, Memory.Memory.TYPE_LPM]
        Memory.Memory.revoke_memory()
        for mem_type in mem_types:
            if(Memory.Memory.assign_memory(task,mem_type)):
                for j in range(CPU.CPU.n_cpufreqs,0,-1):
                    Task.Task.idx_cpufreq = j
                    Task.Task.calculate_det(task)
                    if Task.Task.is_schedulable(task):
                        return True;
                    Task.Task.revert_task_det(task)
                Memory.Memory.revoke_memory()
        return False
