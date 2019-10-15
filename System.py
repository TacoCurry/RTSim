from abc import *
from CPU import NoneDVFSCPU, DVFSCPU
from Memory import Memory, Memories
import sys
from Task import TaskQueue
from Report import Report


class System(metaclass=ABCMeta):
    """super class of all POLICYs"""

    def __init__(self):
        self.name = None
        self.CPU = None
        self.memories = None
        self.desc = None
        self.n_core = None
        self.end_sim_time = None
        self.task_queue = None
        self.report = None
        self.verbose = None
        self.time = None

    def run(self):
        self.end_sim_time = int(input("실행할 시뮬레이션 시간을 입력하세요(정수): "))

        verbose = int(input("상세 출력을 원하시면 1을 입력하세요:"))
        if verbose == 1:
            self.verbose = True
        else:
            self.verbose = False

        self.set_processor()
        self.set_memory()
        self.set_tasks()
        self.report = Report()
        # run simulator...
        self.time = 0
        while self.time <= self.end_sim_time:
            task = self.task_queue.pop_head_task()
            if not task:
                break
            if not self.task_queue.schedule_task(task, self):
                raise Exception("Simulation failed")
            self.task_queue.check_queued_tasks()
            self.report.add_utilization(self.task_queue)
            if self.verbose:
                self.task_queue.show_queued_tasks()
        self.report.make_report(self)
        self.report.print_result()

    @abstractmethod
    def assign_task(self, task) -> bool:
        pass

    @abstractmethod
    def reassign_task(self, task) -> bool:
        pass

    @staticmethod
    def error(msg: str):
        print(msg)
        sys.exit()

    def set_processor(self, input_file="input_processor.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                self.n_core = int(f.readline())
                n_frequency = int(f.readline())
                for i in range(n_frequency):
                    temp = f.readline().split()
                    self.CPU.insert_cpufreq(
                        wcet_scale=float(temp[0]), power_active=float(temp[1]), power_idle=float(temp[2]))
        except FileNotFoundError:
            System.error("processor 설정 파일을 찾을 수 없습니다.")
        # except:
        #     System.error("processor 파일의 형식이 잘못 되었습니다.")

    def set_memory(self, input_file="input_mem.txt"):
        try:
            self.memories = Memories()
            with open(input_file, "r", encoding='UTF8') as f:
                for i in range(2):
                    temp = f.readline().split()
                    self.memories.insert_memory(memory_str=temp[0], capacity=int(temp[1]), wcet_scale=float(temp[2]),
                                                power_active=float(temp[3]), power_idle=float(temp[4]))
        except FileNotFoundError:
            System.error("memory 정보 파일을 찾을 수 없습니다.")
        # except:
        #     System.error("memory 파일의 형식이 잘못 되었습니다.")

    def set_tasks(self, input_file="input_tasks.txt"):
        try:
            self.task_queue = TaskQueue()
            with open(input_file, "r", encoding='UTF8') as f:
                n_task = int(f.readline())
                for i in range(n_task):
                    temp = f.readline().split()
                    self.task_queue.insert_task(wcet=int(temp[0]), period=int(temp[1]),
                                                mem_req=int(temp[2]), mem_active_ratio=float(temp[3]))
            if not self.task_queue.setup_tasks(self):
                raise Exception("failed to setup tasks")
        except FileNotFoundError:
            System.error("task 정보 파일을 찾을 수 없습니다.")
        # except:
        #     System.error("task 파일의 형식이 잘못 되었습니다.")


class Dram(System):
    def __init__(self):
        super().__init__()
        self.name = "DRAM"
        self.desc = "No DVFS with dram(dram)"
        self.CPU = NoneDVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)
        return self.memories.assign_memory(task, Memory.TYPE_DRAM)

    def reassign_task(self, task) -> bool:
        return self.CPU.reassign_cpufreq(task)


class Hm(System):
    def __init__(self):
        super().__init__()
        self.name = "HM"
        self.desc = "Hybrid memory(hm)"
        self.CPU = NoneDVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)

        mem_types = [Memory.TYPE_DRAM, Memory.TYPE_LPM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                return True
        return False

    def reassign_task(self, task) -> bool:
        self.CPU.reassign_cpufreq(task)

        Memories.revoke_memory(task)

        mem_types = [Memory.TYPE_LPM, Memory.TYPE_DRAM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                task.calc_det()
                if task.is_schedulable():
                    return True
                task.revert_det()
        return False


class DvfsDram(System):
    def __init__(self):
        super().__init__()
        self.name = "DVFS_DRAM"
        self.desc = "DVFS with dram(dvfs-dram)"
        self.CPU = DVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)
        if not self.memories.assign_memory(task, Memory.TYPE_DRAM):
            return False
        return True

    def reassign_task(self, task) -> bool:
        return self.CPU.reassign_cpufreq(task)


class DvfsHm(System):
    def __init__(self):
        super().__init__()
        self.name = "DVFS_HM"
        self.desc = "DVFS with hybrid memory(dvs-hm)"
        self.CPU = DVFSCPU()

    def assign_task(self, task) -> bool:
        self.CPU.assign_cpufreq(task)

        mem_types = [Memory.TYPE_DRAM, Memory.TYPE_LPM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                return True
        return False

    def reassign_task(self, task) -> bool:
        Memories.revoke_memory(task)

        mem_types = [Memory.TYPE_LPM, Memory.TYPE_DRAM]
        for mem_type in mem_types:
            if self.memories.assign_memory(task, mem_type):
                if self.CPU.reassign_cpufreq(task):
                    return True
                Memories.revoke_memory(task)
        return False
