import random


class Solution:
    processor = None
    memories = None
    tasks = None

    # Constants
    MAX_GENERATIONS = None
    POPULATIONS = None
    TRY_LIMIT = None
    UTIL_LIMIT_RATIO = None
    PENALTY_RATIO = None
    MUTATION_PROB = None
    K_ROULETTE_WHEEL_SELECTION = None  # for Roulette-wheel selection
    MAX_RANKING_SELECTION = None  # for Ranking selection
    MIN_RANKING_SELECTION = None

    def __init__(self):
        self.genes_processor = []
        self.genes_memory = []

        # For memory balance
        self.n_tasks_for_each_memory = None
        self.used_capacity_for_each_memory = None
        self.memory_with_most_tasks = None

        self.utilization = None
        self.power = None
        self.score = None

    def __lt__(self, other):
        # Sort in descending order of scores
        return self.score < other.score

    def is_schedule(self):
        if self.utilization <= Solution.processor.n_core:
            return True
        return False

    """
    ------------------------------------------------------------------------------
    Memory
    """

    def calc_memory_with_most_tasks(self):
        # Find a memory with the most tasks
        max_n_tasks = self.n_tasks_for_each_memory[0]
        max_index = 0
        for i in range(1, Solution.memories.n_mem_types):
            if self.n_tasks_for_each_memory[i] > max_n_tasks:
                max_n_tasks = self.n_tasks_for_each_memory[i]
                max_index = i
        self.memory_with_most_tasks = max_index

    def calc_memory_used(self):
        # Calculate memory usages for each task
        self.n_tasks_for_each_memory = [0 for i in range(Solution.memories.n_mem_types)]
        self.used_capacity_for_each_memory = [0 for i in range(Solution.memories.n_mem_types)]

        for i in range(self.tasks.n_task):
            self.n_tasks_for_each_memory[self.genes_memory[i]] += 1
            self.used_capacity_for_each_memory[self.genes_memory[i]] += self.tasks.get_task(i).mem_req

    def check_memory(self):
        # Check memory capacity for each memory
        for i in range(Solution.memories.n_mem_types):
            if self.used_capacity_for_each_memory[i] > Solution.memories.get_memory(i).capacity:
                return False
        return True

    def adjust_memory(self):
        # Balance memory by moving a task placed in the most frequent memory to another memory.
        replace_index = random.randint(0, self.n_tasks_for_each_memory[self.memory_with_most_tasks]-1)
        while True:
            new_mem_type = random.randint(0, Solution.memories.n_mem_types - 1)
            if new_mem_type != self.memory_with_most_tasks:
                break

        for i in range(len(self.genes_memory)):
            if self.genes_memory[i] == self.memory_with_most_tasks:
                if replace_index == 0:
                    # Replace (replace_index)-th task of most frequent memory into new_mem_type
                    self.genes_memory[i] = new_mem_type

                    self.n_tasks_for_each_memory[self.memory_with_most_tasks] -= 1
                    self.used_capacity_for_each_memory[self.memory_with_most_tasks] -= self.tasks.get_task(i).mem_req

                    self.n_tasks_for_each_memory[new_mem_type] += 1
                    self.used_capacity_for_each_memory[new_mem_type] += self.tasks.get_task(i).mem_req

                    self.calc_memory_with_most_tasks()
                    break
                replace_index -= 1

    """
    --------------------------------------------------------------
    Utilization and power
    """

    def check_utilization(self):
        # Check utilization using UTIL_LIMIT_RATIO
        util_sum = 0
        power_sum = 0

        for i in range(Solution.tasks.n_task):
            task = Solution.tasks.get_task(i)
            processor_mode = Solution.processor.get_mode(self.genes_processor[i])
            memory = Solution.memories.get_memory(self.genes_memory[i])

            wcet_scaled_processor = 1 / processor_mode.wcet_scale
            wcet_scaled_memory = 1 / memory.wcet_scale
            det = task.wcet * max(wcet_scaled_memory, wcet_scaled_processor)
            det = int(round(det))
            if det == 0:
                det = 1

            if det > task.period:
                return False  # deadline ncc

            # Calc util
            util_sum += det / task.period

            # Calc active power for processor
            processor_power_unit = (processor_mode.power_active * wcet_scaled_processor +
                                    processor_mode.power_idle * wcet_scaled_memory) / \
                                   (wcet_scaled_memory + wcet_scaled_processor)
            power_sum += processor_power_unit * det / task.period

            # Calc power for memory
            power_sum += task.mem_req * (task.mem_active_ratio * memory.power_active +
                                         (1 - task.mem_active_ratio) * memory.power_idle) * det / task.period \
                         + task.mem_req * memory.power_idle * (1 - det / task.period)

        n_core = Solution.processor.n_core
        if util_sum > n_core * (1 + Solution.UTIL_LIMIT_RATIO):
            return False

        # Calc idle power for processor
        if util_sum < n_core:
            power_sum += Solution.processor.modes[-1].power_idle * (Solution.processor.n_core - util_sum)

        self.utilization = util_sum
        self.power = power_sum
        self.score = power_sum
        if util_sum >= Solution.processor.n_core:
            # Apply penalty for score
            self.score += power_sum * (util_sum - n_core) * Solution.PENALTY_RATIO
        return True

    def adjust_utilization(self):
        if random.random()*(Solution.processor.n_mode + Solution.memories.n_mem_types) < Solution.processor.n_mode:
            if not self.adjust_utilization_by_processor():
                if not self.adjust_utilization_by_memory():
                    return False
        else:
            if not self.adjust_utilization_by_memory():
                if not self.adjust_utilization_by_processor():
                    return False
        return True

    def adjust_utilization_by_memory(self):
        # Move a random task in LPM to DRAM
        index_end = index = random.randint(0, Solution.tasks.n_task-1)

        while True:
            index = (index + 1) % Solution.tasks.n_task
            if self.genes_memory[index] > 0:
                # Remove a task from LPM
                self.n_tasks_for_each_memory[self.genes_memory[index]] -= 1
                self.used_capacity_for_each_memory[self.genes_memory[index]] -= self.tasks.get_task(index).mem_req
                # Add a task to DRAM
                self.genes_memory[index] -= 1
                self.n_tasks_for_each_memory[self.genes_memory[index]] += 1
                self.used_capacity_for_each_memory[self.genes_memory[index]] += self.tasks.get_task(index).mem_req
                # Update memory with most tasks
                self.calc_memory_with_most_tasks()
                return True

            if index == index_end:
                break

        return False

    def adjust_utilization_by_processor(self):
        # Change a random task to higher processor voltage/frequency mode
        index_end = index = random.randint(0, Solution.tasks.n_task - 1)

        while True:
            index = (index + 1) % Solution.tasks.n_task
            if self.genes_processor[index] > 0:
                self.genes_processor[index] -= 1
                return True
            if index == index_end:
                break
        return False

    """
    ----------------------------------------------------------
    For making initial solution set in GA
    """

    @staticmethod
    def set_random_seed():
        random.seed()  # Set seed using current time

    @staticmethod
    def get_random_solution():
        solution = Solution()

        # Set random attributes
        solution.genes_processor = []
        solution.genes_memory = []
        for j in range(Solution.tasks.n_task):
            solution.genes_processor.append(random.randint(0, Solution.processor.n_mode - 1))
            solution.genes_memory.append(random.randint(0, Solution.memories.n_mem_types - 1))

        # Try making valid solution
        solution.calc_memory_used()
        solution.calc_memory_with_most_tasks()
        for i in range(Solution.TRY_LIMIT):
            if not solution.check_memory():
                solution.adjust_memory()
                continue
            if solution.check_utilization():
                return solution
            if not solution.adjust_utilization():
                raise Exception("random solution 생성 불가")

        # 생성을 반복해도 valid한 solution 을 만들지 못할 경우
        raise Exception("random solution 생성 불가")

    """
    ----------------------------------------------------------
    For Crossover in GA
    """

    @staticmethod
    def select_solution(sum_fitness, fitness_list, solutions):
        point = random.random() * sum_fitness
        temp = 0
        for i in range(len(fitness_list)):
            temp += fitness_list[i]
            if point < temp:
                break
        return i, solutions.pop(i)

    @staticmethod
    def select_solution_using_roulette_wheel(solutions):
        # 1. Calculate fitness using formula "fi = (Cw - Ci) + ( Cw - Cb ) / (k - 1)"
        worst_score = solutions[-1].score
        best_score = solutions[0].score
        constant = (worst_score - best_score) / (Solution.K_ROULETTE_WHEEL_SELECTION - 1)

        fitness_list = []
        sum_fitness = 0
        for solution in solutions:
            fitness = worst_score - solution.score + constant
            sum_fitness += fitness
            fitness_list.append(fitness)

        return Solution.select_solution(sum_fitness, fitness_list, solutions)

    @staticmethod
    def select_solution_using_ranking_selection(solutions):
        # Calculate fitness using Ranking Selection
        diff = Solution.MIN_RANKING_SELECTION - Solution.MAX_RANKING_SELECTION
        n = len(solutions)
        fitness_list = []
        sum_fitness = 0
        for i in range(1, len(solutions) + 1):
            fitness = Solution.MAX_RANKING_SELECTION + (i - 1) * diff / (n - 1)
            sum_fitness += fitness
            fitness_list.append(fitness)

        # Select
        return Solution.select_solution(sum_fitness, fitness_list, solutions)

    @staticmethod
    def crossover(solution1, solution2):
        n_task = Solution.tasks.n_task

        crossover_point_processor = random.randint(0, n_task)
        crossover_point_memory = random.randint(0, n_task)

        new_solution = Solution()
        new_solution.genes_processor = solution1.genes_processor[:crossover_point_processor] + \
                                       solution2.genes_processor[crossover_point_processor:]
        new_solution.genes_memory = solution1.genes_memory[:crossover_point_memory] + \
                                    solution2.genes_memory[crossover_point_memory:]
        return new_solution

    def mutation(self):
        if random.random() > Solution.MUTATION_PROB:
            return

        n_task = Solution.tasks.n_task

        # processor
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_processor[point1]
        self.genes_processor[point1] = self.genes_processor[point2]
        self.genes_processor[point2] = temp

        # memory
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_memory[point1]
        self.genes_memory[point1] = self.genes_memory[point2]
        self.genes_memory[point2] = temp
