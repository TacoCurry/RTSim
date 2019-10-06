from abc import *


class CpuFrequency:
    def __init__(self, wcet_scale, power_active, power_idle):
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle


class CPU(metaclass=ABCMeta):
    MAX_CPU_FREQS = 15

    def __init__(self):
        self.cpufreqs = []
        self.n_cpufreqs = 0

    def insert_cpufreq(self, wcet_scale, power_active, power_idle) -> bool:
        if self.n_cpufreqs >= CPU.MAX_CPU_FREQS:
            return False

        self.n_cpufreqs += 1
        self.cpufreqs.append(CpuFrequency(wcet_scale, power_active, power_idle))
        self.sort_cpufreq()
        return True

    def sort_cpufreq(self):
        self.cpufreqs.sort(key=lambda object: object.wcet_scale, reverse=True)

    def assign_cpufreq(self, task):
        task.cpu_frequency = self.cpufreqs[0]

    @abstractmethod
    def reassign_cpufreq(self, task) -> bool:
        pass


class NoneDVFSCPU(CPU):
    def reassign_cpufreq(self, task) -> bool:
        return True


class DVFSCPU(CPU):
    def reassign_cpufreq(self, task) -> bool:
        for cpufreq in self.cpufreqs:
            task.cpu_frequency = cpufreq
            task.calc_det()
            if task.is_schedulable():
                return True
            task.revert_det()
        return False



