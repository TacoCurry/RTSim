import sys
from CPU import CPU
from Memory import Memory
from Task import Task
from System import System
from Sys_DVFS_HM import DVFS_HM
from Sys_DVFS_DRAM import DVFS_DRAM
from Sys_HM import HM
from Sys_DRAM import DRAM


class Simulator:
    n_core: int = 0
    policy: System = None
    end_sim_time: int = None

    @staticmethod
    def errmsg(message):
        print(message)
        sys.exit()

    @staticmethod
    def run():
        # Set simulator
        Simulator.set_policy(int(input("policy를 선택하세요.\n[1]DRAM, [2]HM. [3]DVFS_DRAM, [4]DVFS_HM : ")))
        Simulator.set_end_sim_time(input("실행할 시뮬레이션 시간을 입력하세요: "))
        Simulator.set_processor()
        Simulator.set_memory()
        Simulator.load_tasks()

        # run simulator


    @staticmethod
    def set_policy(policy_num: int):
        if policy_num == 1:
            Simulator.policy = DRAM()
        elif policy_num == 2:
            Simulator.policy = HM()
        elif policy_num == 3:
            Simulator.policy = DVFS_DRAM()
        elif policy_num == 4:
            Simulator.policy = DVFS_HM()
        else:
            Simulator.errmsg("올바른 policy를 선택하세요")

    @staticmethod
    def set_processor(input_file="input_processor.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                Simulator.n_core = int(f.readline())
                n_frequency = int(f.readline())
                for i in range(n_frequency):
                    temp = f.readline().split()
                    CPU.insert_cpufreq(
                        wcet_scale=float(temp[0]), power_active=float(temp[1]), power_idle=float(temp[2]))
        except FileNotFoundError:
            Simulator.errmsg("processor 정보 파일을 찾을 수 없습니다.")
        except:
            Simulator.errmsg("processor 파일의 형식이 잘못 되었습니다.")

    @staticmethod
    def set_memory(input_file="input_mem.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                for i in range(2):
                    temp = f.readline().split()
                    Memory.insert_memory(memstr=temp[0], capacity=int(temp[1]), wcet_scale=float(temp[2]),
                                         power_active=float(temp[3]), power_idle=float(temp[4]))
        except FileNotFoundError:
            Simulator.errmsg("memory 정보 파일을 찾을 수 없습니다.")
        except:
            Simulator.errmsg("memory 파일의 형식이 잘못 되었습니다.")

    @staticmethod
    def load_tasks(input_file="input_tasks.txt"):
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                n_task = int(f.readline())
                for i in range(n_task):
                    temp = f.readline().split()
                    Task.insert_task(wcet=temp[0], period=temp[1], memory_req=temp[2], memory_active_ratio=temp[3])
        except FileNotFoundError:
            Simulator.errmsg("task 정보 파일을 찾을 수 없습니다.")
        except:
            Simulator.errmsg("task 파일의 형식이 잘못 되었습니다.")


