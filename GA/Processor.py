class ProcessorMode:
    def __init__(self, wcet_scale, power_active, power_idle):
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle

    def __lt__(self, other):
        return self.wcet_scale > other.wcet_scale


class Processor:
    MAX_CPU_MODE = 15

    def __init__(self):
        self.n_core = None
        self.modes = []
        self.n_mode = 0

    def insert_mode(self, wcet_scale: float, power_active: float, power_idle: float) -> bool:
        if self.n_mode >= Processor.MAX_CPU_MODE:
            return False
        self.modes.append(ProcessorMode(wcet_scale, power_active, power_idle))
        self.n_mode += 1
        return True

    def get_mode(self, index):
        return self.modes[index]

