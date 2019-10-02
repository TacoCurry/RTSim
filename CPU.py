import Simulator


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
    def insert_cpufreq(wcet_scale, power_active, power_idle):
        if CPU.n_cpufreqs >= CPU.MAX_CPU_FREQS:
            Simulator.Simulator.errmsg("CPU frequency 모드가 너무 많습니다.")
            return False
        if CPU.n_cpufreqs>0 & CPU.cpufreqs[CPU.n_cpufreqs-1].wcet_scale<wcet_scale:
            Simulator.Simulator.errmsg("CPU frequency는 내림차순으로 입력되어야 합니다.")
            return False

        CPU.n_cpufreqs += 1
        CPU.cpufreqs.append(
            CpuFrequency(wcet_scale, power_active, power_idle))
        return True

    @staticmethod
    def sort_cpufreq():
        pass




