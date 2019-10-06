import math
from DoubleLinkedList import DoubleLinkedList, ListNode


class TaskQueue(DoubleLinkedList):
    def __init__(self):
        super().__init__()
        self.n_task = 0

    def insert_task(self, wcet: int, period: int, mem_req: int, mem_active_ratio: float):
        task = Task(wcet, period, mem_req, mem_active_ratio)
        self.n_task += 1
        task.no = self.n_task
        task.node = self.add_last(task)

    def get_tasks_ndet(self) -> float:
        result = 0.0
        if self.n_task == 0:
            return result

        result += self.header.item.det
        node = self.header.after
        while node != self.header:
            result += node.item.det * 1.0 / node.item.period
            node = node.after
        return result

    def is_schedule(self, task) -> bool:
        if self.get_tasks_ndet() + (task.det * 1.0 / task.period) <= 1:
            return True
        sum_ndet=0
        if(task is not None):
            sum_ndet += (task.det*1.0/task.period)
        if(sum_ndet>1):
            return False

    def setup_tasks(self, system) -> bool:
        # self(queue)를 temp_head에 복사하고 self는 init하기.
        temp_header = self.add_first(None)
        self.list_del_init(self.header)

        if not self.is_empty():
            raise Exception("debug, not empty queue")

        node = temp_header.after
        while node != temp_header:
            node_next = node.after
            self.list_del_init(node)
            if not system.assign_task(node.item):
                raise Exception("insufficient memory")

            node.item.calc_det()
            if not self.is_schedule(node.item):
                raise Exception("unschedule task")

            self.requeue_task(node.item, 0)
            node = node_next
        return True

    def get_head_task(self):
        pass
        # 이게 task를 반환해야하는지 노드를 반환해야 하는지 잘 모르겠으니 나중에 짜겠어요
        # if self.is_empty():
        #     return None
        # return self.header.after.item

    def pop_head_task(self):
        pass
        # 이게 task를 반환해야하는지 노드를 반환해야 하는지 잘 모르겠으니 나중에 짜겠어요
        # if self.is_empty():
        #     return None
        # head_task = self.header.after
        # self.list_del_init(head_task)
        # return head_task.item

    def delay_tasks(self):
        pass

    def requeue_task(self, task, tick):
        pass

    def apply_gap_head(self, gap_head):

        """head=get_head_task()"""

        pass
    
    def get_new_start(self):
        pass

    def schedule_task(self,task)-> bool:
        pass

    def check_queed_tasks(self):
        pass

    def reinit_tasks(self):
        pass


class Task:
    n_task = 0
    tasks = []

    def __init__(self, wcet, period, mem_req, mem_active_ratio):
        self.wcet = wcet
        self.period = period
        self.memory_req = mem_req
        self.memory_active_ratio = mem_active_ratio

        self.no = None
        self.cpu_frequency = None
        self.memory = None

        self.det = None
        self.det_remain = None
        self.det_old = None
        self.det_remain_old = None

        self.deadline = None
        self.gap_head = None
        self.gap = None

        self.node = None

    def calc_det(self):
        new_det = self.wcet / (self.cpufreq.wcet_scale * self.memory.wcet_scale)

        self.det_old = self.det
        self.det = int(round(new_det))
        if self.det == 0:
            self.det = 1

        self.det_remain_old = self.det_remain
        if self.det_remain > 0 & self.det != self.det_old:
            self.det_remain = int(round(self.det_remain * (new_det / self.det_old)))

    def revert_det(self):
        self.det = self.det_old
        self.det_remain = self.det_remain_old

    def get_real_execution_time(self):
        if self.det_remain < self.gap:
            return self.det_remain
        else:
            return self.gap

    @staticmethod
    def is_preceding(task, task_cmp) -> bool:
        etr = (task.det_remain * 1.0) / task.deadline
        etr_cmp = (task_cmp.det_remain * 1.0) / task_cmp.deadline

        if etr > etr_cmp:
            return True
        elif etr < etr_cmp:
            return False
        elif task.no < task_cmp.no:
            return True
        return False


