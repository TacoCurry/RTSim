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
        self.used_capacity = 0


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
        self.power_consumed_mem_active = 0
        self.power_consumed_mem_idle = 0

    def get_memory(self, memory_type):
        for memory in self.list:
            if memory.type == memory_type:
                return memory
        return None

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

    def assign_memory(self, task, memory_type) -> bool:
        memory: Memory = self.get_memory(memory_type)
        if memory.capacity - memory.used_capacity >= task.memory_req:
            memory.used_capacity += task.memory_req
            task.memory = memory
            return True
        return False

    @staticmethod
    def revoke_memory(task):
        task.memory.used_capacity -= task.memory_req
        task.memory = None

    def init_memories(self):
        self.total_capacity = 0
        for memory in self.list:
            memory.used_capacity = 0
            self.total_capacity += memory.capacity