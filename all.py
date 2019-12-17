from RTSim.System import Dram, Hm, DvfsDram, DvfsHm, GA
from GA.inout import InputUtils, OutputUtils
from GA.Solution import Solution
from TaskGen.Input import InputUtils as tgInput
from TaskGen.Generation import GenTask


def taskgen():
    tgInput.set_memory()
    tgInput.set_processor()
    tgInput.set_tasks()
    GenTask.gen_task(1)


def ga_run():
    # from files
    Solution.memories = InputUtils.get_memories()
    Solution.processor = InputUtils.get_processor()
    Solution.tasks = InputUtils.get_tasks()
    InputUtils.get_other_input()

    # Initiate ga_report.txt
    OutputUtils.init_report()

    # 1. Make initial solution set
    Solution.set_random_seed()
    solutions = [Solution.get_random_solution() for i in range(Solution.POPULATIONS)]
    solutions.sort()  # Sort solutions by score

    for i in range(Solution.MAX_GENERATIONS):
        if i != 0 and i % 100 == 0:
            OutputUtils.report_print(i, solutions)

        get_new_solution = False
        for j in range(Solution.TRY_LIMIT):
            # 2. Select two solution
            solution1_index, solution1 = Solution.select_solution_using_ranking_selection(solutions)
            solution2_index, solution2 = Solution.select_solution_using_ranking_selection(solutions)
            solutions.insert(solution2_index, solution2)
            solutions.insert(solution1_index, solution1)

            # 3. Crossover
            new_solution = Solution.crossover(solution1, solution2)
            new_solution.mutation()

            # 4. Check Validity
            new_solution.calc_memory_used()
            new_solution.calc_memory_with_most_tasks()
            if new_solution.check_memory() and new_solution.check_utilization():
                get_new_solution = True
                break

        if get_new_solution:
            # Replace worst solution into new solution
            solutions[-1] = new_solution
            solutions.sort()
            continue
        else:
            raise Exception("{}번째 generation 이후, solution 교배 불가".format(i + 1))

    # 5. Print result
    for solution in solutions:
        if solution.is_schedule():
            print("power: {}, utilization: {}".format(solution.power, solution.utilization))
            OutputUtils.result_print(solution)
            break


num = int(input("몇 번 반복?: "))
for i in range(num):
    print("==================================")
    print("# {}회".format(i+1))

    # Generate Task
    print("\n1.TaskGen")
    taskgen()

    # GA
    print("\n2.GA")
    ga_run()

    # RTsim
    print("\n3.RTsim")
    system = 6
    end_sim_time = 10000
    verbose = 0
    Dram(end_sim_time, verbose).run()
    Hm(end_sim_time, verbose).run()
    DvfsDram(end_sim_time, verbose).run()
    DvfsHm(end_sim_time, verbose).run()
    GA(end_sim_time, verbose).run()
    print("==================================")
