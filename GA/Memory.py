class Memory:
    TYPE_NONE = 0
    TYPE_DRAM = 1
    TYPE_LPM = 2

    def __init__(self, capacity, wcet_scale, power_active, power_idle):
        self.type = None
        self.capacity = capacity
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle

    def get_type_str(self) -> str:
        if self.type == Memory.TYPE_DRAM:
            return "DRAM"
        elif self.type == Memory.TYPE_NONE:
            return "None"
        else:
            return "LPM"


class LPM(Memory):
    def __init__(self, capacity, wcet_scale, power_active, power_idle):
        super().__init__(capacity, wcet_scale, power_active, power_idle)
        self.type = Memory.TYPE_LPM


class DRAM(Memory):
    def __init__(self, capacity, wcet_scale, power_active, power_idle):
        super().__init__(capacity, wcet_scale, power_active, power_idle)
        self.type = Memory.TYPE_DRAM


class Memories:
    def __init__(self):
        self.list = []
        self.n_mem_types = 0
        self.total_capacity = 0

    def get_memory_by_type(self, memory_type):
        for memory in self.list:
            if memory.type == memory_type:
                return memory
        return None

    def get_memory(self, index):
        return self.list[index]

    def insert_memory(self, memory_str: str, capacity, wcet_scale, power_active, power_idle) -> bool:
        if memory_str.lower() == "lpm":
            self.list.append(LPM(capacity, wcet_scale, power_active, power_idle))
        elif memory_str.lower() == "dram":
            self.list.append(DRAM(capacity, wcet_scale, power_active, power_idle))
        else:
            return False
        self.n_mem_types += 1
        self.total_capacity += capacity
        return True
