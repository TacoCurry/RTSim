import Simulator
import Task


class Memory:
    memories = []
    total_capacity = 0
    TYPE_DRAM = 1
    TYPE_LPM = 2

    def __init__(self, memory_type, capacity, exec_scale, power_active, power_idle):
        self.type = memory_type
        self.capacity = capacity
        self.exec_scale = exec_scale
        self.power_active = power_active
        self.power_idle = power_idle
        self.remain_capacity = capacity

    @staticmethod
    def get_memory(memory_type):
        for memory in Memory.memories:
            if memory.type == memory_type:
                return memory
        return False

    @staticmethod
    def insert_memory(self, memory_type, capacity, wcet_scale, power_active, power_idle):
        Memory.memories.append(
            Memory(memory_type, capacity, wcet_scale, power_active, power_idle))
        Memory.total_capacity += capacity

    @staticmethod
    def assign_memory(task: Task.Task, memory_type):
        memory: Memory = Memory.get_memory(memory_type)
        if memory.remain_capacity >= task.memory_req:
            memory.remain_capacity -= task.memory_req
            task.memory = memory
            return True
        return False

    @staticmethod
    def revoke_memory(task: Task.Task):
        task.memory.remain_capacity += task.memory_req
        task.memory = None

    @staticmethod
    def init_memories():
        for memory in Memory.memories:
            memory.remain_capacity = memory.capacity
