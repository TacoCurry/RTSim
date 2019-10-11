class Report:
    def __init__(self):
        self.policy_name = None
        self.power_consumed_avg = 0
        self.utilization = None
        self.power_consumed_cpu_avg = 0
        self.power_consumed_mem_avg = 0
        self.power_consumed_active_avg = 0
        self.power_consumed_idle_avg = 0
        self.sum_utils = 0
        self.n_utils = 0

    def cleanup_report(self):
        self.power_consumed_cpu_avg = 0
        self.power_consumed_mem_avg = 0
        self.power_consumed_active_avg = 0
        self.power_consumed_idle_avg = 0
        self.sum_utils = 0
        self.n_utils = 0

    def add_utilization(self, task_queue):
        self.sum_utils += task_queue.get_tasks_ndet()
        self.n_utils += 1

    def make_report(self, system):
        pass
        # ~~

    def print_result(self):
        pass
        # ~~
