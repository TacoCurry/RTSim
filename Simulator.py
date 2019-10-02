import CPU
import Task
import sys
import Memory


class Simulator:
    def __init__(self):
        self.policy_num = input("policy를 선택하세요.\n[1]DRAM, [2]HM. [3]DVS_DRAM, [4]HM : ")
        self.max_simulation_time = input("실행할 시뮬레이션 시간을 입력하세요: ")
        self.set_processor()
        self.set_memory()
        self.tasks = []
        self.load_tasks()

    def set_processor(self, input_file="input_processor.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                self.n_core = int(f.readline())
                n_frequency = int(f.readline())
                for i in range(n_frequency):
                    temp = f.readline().split()
                    CPU.CPU.insert_cpufreq(
                        wcet_scale=float(temp[0]), power_active=float(temp[1]), power_idle=float(temp[2]))
        except FileNotFoundError:
            print("processor 정보 파일을 찾을 수 없습니다.")
            sys.exit(0)


    def set_memory(self, input_file="input_mem.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                for i in range(2):
                    temp = f.readline().split()
                    if temp[0] == "dram":
                        Memory.Memory.insert_memory(
                            Memory.Memory.TYPE_DRAM, capacity=int(temp[1]), wcet_scale=float(temp[2]),
                            power_active=float(temp[3]), power_idle=float(temp[4]))
                    elif temp[0] == "lpm":
                        Memory.Memory.insert_memory(
                            Memory.Memory.TYPE_LPM, capacity=int(temp[1]), wcet_scale=float(temp[2]),
                            power_active=float(temp[3]), power_idle=float(temp[4]))
        except FileNotFoundError:
            print("memory 정보 파일을 찾을 수 없습니다.")
            sys.exit(0)

    def load_tasks(self, input_file="input_tasks.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                n_task = int(f.readline())
                for i in range(n_task):
                    temp = f.readline().split()
                    self.tasks.append(
                        Task.Task(
                            wcet=temp[0], period=temp[1], memory_req=temp[2], memory_active_ratio=temp[3]))
        except FileNotFoundError:
            print("task 정보 파일을 찾을 수 없습니다.")
            sys.exit(0)

    @staticmethod
    def errmsg(message):
        print(message)
        sys.exit(0)
