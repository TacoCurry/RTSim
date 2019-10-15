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
        power_consumed_cpu = system.CPU.power_consumed_cpu_active + system.CPU.power_consumed_cpu_idle
        power_consumed_mem = system.Memories.power_consumed_mem_active + system.Memories.power_consumed_mem_idle
        power_consumed_active = system.CPU.power_consumed_cpu_active + system.Memories.power_consumed_mem_active
        power_consumed_idle = system.CPU.power_consumed_cpu_idle +  system.Memories.power_consumed_mem_idle
        power_consumed = self.power_consumed_cpu + self.power_consumed_mem

        self.power_consumed_avg = float(power_consumed)/system.time
        self.power_consumed_cpu_avg = float(power_consumed_cpu)/system.time
        self.power_consumed_mem_avg = float(power_consumed_mem) / system.time
        self.power_consumed_active_avg = float(power_consumed_active)/ system.time
        self.power_consumed_idle_avg = float(power_consumed_idle)/system.time
        self.utilization = float(self.sum_utils)/self.n_utils*100

    def print_result(self):
        print("%10s %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf" %
              (self.policy_name, self.power_consumed_avg, self.utilization, self.power_consumed_cpu_avg,
               self.power_consumed_mem_avg, self.power_consumed_active_avg, self.power_consumed_idle_avg))
