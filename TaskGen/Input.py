from TaskGen.Memory import Memories
from TaskGen.Utility import ErrorMsg
from TaskGen.Utility import Variables


class InputUtils:
    @staticmethod
    def set_memory(input_file="__input/input_mem.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                mem1 = Memories()
                temp = f.readline().split()
                mem1.insert_memory(mem_type=temp[0], capacity=int(temp[1]), wcet_scale=float(temp[2]),
                                   power_active=float(temp[3]), power_idle=float(temp[4]))
                mem2 = Memories()
                temp = f.readline().split()
                mem2.insert_memory(mem_type=temp[0], capacity=int(temp[1]), wcet_scale=float(temp[2]),
                                   power_active=float(temp[3]), power_idle=float(temp[4]))
        except FileNotFoundError:
            ErrorMsg.error("task 정보 파일을 찾을 수 없습니다.")

        print("=======================================================")
        print("This is the memory Input")
        print("type capacity, wcet_scale, power_active, power_idle")
        print(mem1.mem_type, mem1.capacity, mem1.wcet_scale, mem1.power_active, mem1.power_idle)
        print(mem2.mem_type, mem2.capacity, mem2.wcet_scale, mem2.power_active, mem2.power_idle)

        Memories.mem_list.append(mem1)
        Memories.mem_list.append(mem2)

    @staticmethod
    def set_tasks(input_file="__input/input_taskgen.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                Variables.n_tasks = int(f.readline())

                temp = f.readline().split()
                Variables.wcet_min = int(temp[0])
                Variables.wcet_max = int(temp[1])
                Variables.mem_total = int(temp[2])
                Variables.util_cpu = float(temp[3]) * Variables.n_cores
                Variables.total_mem_usage = int(temp[4])
                print("=======================================================")
                print("This is the Task Generation Input")

                print("n_cores  n_tasks")
                print(Variables.n_cores, Variables.n_tasks)

                print("wcet_min, wcet_max, mem_total, util_cpu, util_target")
                print(Variables.wcet_min, Variables.wcet_max, Variables.mem_total, Variables.util_cpu,
                      Variables.total_mem_usage)

        except FileNotFoundError:
            ErrorMsg.error("task 정보 파일을 찾을 수 없습니다.")

    @staticmethod
    def set_processor(input_file="__input/input_processor.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                Variables.n_cores = int(f.readline())
        except FileNotFoundError:
            ErrorMsg.error("task 정보 파일을 찾을 수 없습니다.")
