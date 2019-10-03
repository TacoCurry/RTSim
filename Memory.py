class Memory:
    mems = []
    n_mem_types = 0
    total_capacity = 0

    TYPE_NONE = 0
    TYPE_DRAM = 1
    TYPE_LPM = 2

    def __init__(self, memory_type, capacity, wcet_scale, power_active, power_idle):
        self.type = memory_type
        self.capacity = capacity
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle

        self.used_capacity = 0
        self.n_tasks = 0

    @staticmethod
    def get_memory(mem_type):
        for memory in Memory.mems:
            if memory.type == mem_type:
                return memory
        return None

    @staticmethod
    def insert_memory(memstr, capacity, wcet_scale, power_active, power_idle) -> bool:
        if memstr == "lpm":
            Memory.mems.append(
                Memory(Memory.TYPE_LPM, capacity, wcet_scale, power_active, power_idle))
        elif memstr == "dram":
            Memory.mems.append(
                Memory(Memory.TYPE_DRAM, capacity, wcet_scale, power_active, power_idle))
        else:
            return False
        Memory.n_mem_types += 1
        Memory.total_capacity += capacity
        return True

    @staticmethod
    def assign_memory(task, memory_type) -> bool:
        memory: Memory = Memory.get_memory(memory_type)
        if memory.capacity - memory.used_capacity >= task.memory_req:
            memory.used_capacity += task.memory_req
            task.memory = memory
            return True
        return False

    @staticmethod
    def revoke_memory(task):
        task.memory.used_capacity -= task.memory_req
        task.memory = None

    @staticmethod
    def init_memories():
        Memory.total_capacity = 0
        for memory in Memory.mems:
            memory.used_capacity = 0
            Memory.total_capacity += memory.capacity

