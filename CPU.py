
class CpuFrequency:
    def __init__(self, wcet_scale, power_active, power_idle):
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle


class CPU:
    cpufreqs = []
    n_cpufreqs = 0
    MAX_CPU_FREQS = 15

    @staticmethod
    def insert_cpufreq(wcet_scale, power_active, power_idle) -> bool:
        if CPU.n_cpufreqs >= CPU.MAX_CPU_FREQS:
            return False
        if CPU.n_cpufreqs > 0 & CPU.cpufreqs[CPU.n_cpufreqs-1].wcet_scale < wcet_scale:
            return False

        CPU.n_cpufreqs += 1
        CPU.cpufreqs.append(CpuFrequency(wcet_scale, power_active, power_idle))
        return True

    @staticmethod
    def sort_cpufreq():
        pass




