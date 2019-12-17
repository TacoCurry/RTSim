from GA.Task import Tasks, Task
import sys
from GA.Processor import Processor
from GA.Memory import Memories
from GA.Solution import Solution


class InputUtils:
    @staticmethod
    def get_memories(file="__input/input_mem.txt"):
        memories = Memories()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get memories
                for i in range(2):
                    mem_info = f.readline().split()
                    memories.insert_memory(mem_info[0], int(mem_info[1]), float(mem_info[2]), float(mem_info[3]),
                                           float(mem_info[4]))

            return memories
        except FileNotFoundError:
            print("{}이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("{}의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)

    @staticmethod
    def get_processor(file="__input/input_processor.txt"):
        processor = Processor()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get n_cores
                n_core = int(f.readline())
                processor.n_core = n_core

                # get voltage/frequency mode
                n_mode = int(f.readline())
                for i in range(n_mode):
                    mode_info = f.readline().split()
                    processor.insert_mode(float(mode_info[0]), float(mode_info[1]), float(mode_info[2]))

            return processor
        except FileNotFoundError:
            print("{}이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("{}의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)

    @staticmethod
    def get_tasks(file="task_generated.txt"):
        tasks = Tasks()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get tasks
                n_tasks = int(f.readline())
                for i in range(n_tasks):
                    task_info = f.readline().split()
                    tasks.insert_task(
                        Task(int(task_info[0]), int(task_info[1]), float(task_info[2]), float(task_info[3])))
            return tasks
        except FileNotFoundError:
            print("{}이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("{}의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)

    @staticmethod
    def get_other_input(file="__input/input_ga.txt"):
        try:
            with open(file, "r", encoding='UTF8') as f:
                Solution.MAX_GENERATIONS = int(f.readline())
                Solution.POPULATIONS = int(f.readline())
                Solution.TRY_LIMIT = int(f.readline())
                Solution.UTIL_LIMIT_RATIO = float(f.readline())
                Solution.PENALTY_RATIO = float(f.readline())
                Solution.MUTATION_PROB = float(f.readline())
                Solution.K_ROULETTE_WHEEL_SELECTION = int(f.readline())
                temp = f.readline().split()
                Solution.MAX_RANKING_SELECTION, Solution.MIN_RANKING_SELECTION = int(temp[0]), int(temp[1])
        except FileNotFoundError:
            print("{}이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("{}의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)


class OutputUtils:
    @staticmethod
    def result_print(solution, file="ga_result.txt"):
        with open(file, "w+", encoding='UTF8') as f:
            for i in range(solution.tasks.n_task):
                f.write(str(solution.genes_processor[i]) + " " + str(solution.genes_memory[i]) + "\n")
            f.write("# processor_mode memory_type")
        return True

    @staticmethod
    def init_report(file="ga_report.txt"):
        with open(file, "w+", encoding='UTF8') as f:
            f.write("\n")

    @staticmethod
    def report_print(n_generation, solutions, file="ga_report.txt"):
        power_min = power_max = power_sum = solutions[0].power
        util_min = util_max = util_sum = solutions[0].utilization

        for solution in solutions[1:]:
            power_sum += solution.power
            util_sum += solution.utilization

            if solution.power > power_max:
                power_max = solution.power
            elif solution.power < power_min:
                power_min = solution.power

            if solution.utilization > util_max:
                util_max = solution.utilization
            elif solution.utilization < util_min:
                util_min = solution.utilization

        power_avg = power_sum / len(solutions)
        util_avg = util_sum / len(solutions)

        with open(file, "a", encoding='UTF8') as f:
            f.write("generation: {}, power_min: {}, power_avg: {}, power_max: {}, "
                    "util_min: {}, util_avg: {}, util_max: {}\n".format(n_generation, round(power_min, 5),
                                                                        round(power_avg, 5), round(power_max, 5),
                                                                        round(util_min, 5), round(util_avg, 5),
                                                                        round(util_max, 5)))
