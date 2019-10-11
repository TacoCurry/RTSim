import math
from DoubleLinkedList import DoubleLinkedList, ListNode


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

    def get_ret(self):
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

    def desc_task(self):
        pass
        # task의 속성을 설명해주세요


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

        result += self.header.task.det
        node = self.header.after
        while node != self.header:
            result += node.task.det * 1.0 / node.task.period
            node = node.after
        return result

    def is_schedule(self, task: Task) -> bool:
        if self.get_tasks_ndet() + (task.det * 1.0 / task.period) <= 1:
            return True
        return False

    def setup_tasks(self, system) -> bool:
        # self(queue)를 temp_head에 복사하고 self는 init하기.
        temp_header = self.add_first(None)
        self.list_del_init(self.header)

        if not self.is_empty():
            raise Exception("for debug, not empty queue")

        node = temp_header.after
        while node != temp_header:
            node_next = node.after
            self.list_del_init(node)
            if not system.assign_task(node.task):
                raise Exception("insufficient memory")

            node.task.calc_det()
            if not self.is_schedule(node.task):
                raise Exception("unschedule task")

            # task 객체를 드립니다.
            self.requeue_task(node.task, 0)
            node = node_next
        return True

    def get_head_node(self):
        if self.is_empty():
            return None
        return self.header.after

    def pop_head_task(self):
        if self.is_empty():
            return None
        head_task = self.header.after
        self.list_del_init(head_task)
        return head_task.task

    def delay_tasks(self, task: Task, p_target: Task):
        target: Task = p_target
        next_target = None

        det_remain_saved = task.det_remain
        deadline_saved = task.deadline

        if target.node.after != self.header:
            next_target = target.node.after

        i = 0
        for i in range(task.det_remain):
            if target.deadline == target.det_remain:
                break
            if Task.is_preceding(target, task):
                break

            target.deadline -= 1
            task.det_remain -= 1
            task.deadline -= 1

            if next_target:
                target.gap -= 1
                if target.gap == 0:
                    if Task.is_preceding(target, next_target):
                        target.gap = self.delay_tasks(target, next_target)
                    else:
                        ListNode.change_node_task(target.node, next_target.node)
                        target.gap = next_target.gap
                        next_target.gap = self.delay_tasks(next_target, target)

                        temp = target
                        target = next_target
                        next_target = temp

        task.det_remain = det_remain_saved
        task.deadline = deadline_saved
        assert i != 0
        return i, target.node

    def apply_gap_head(self, gap_head: int):
        if self.is_empty():
            return
        node = self.get_head_node()
        while node != self.header:
            node.task.deadline -= gap_head
            if node.task.gap != 0:
                break
            node = node.after

    @staticmethod
    def get_new_start(self, task: Task, prev_task: Task, start: int) -> int:
        det_remain_saved = prev_task.det_remain
        deadline_saved = prev_task.deadline

        i = 0
        for i in range(prev_task.get_ret()):
            if task.deadline == task.det_remain:
                break
            if Task.is_preceding(task, prev_task):
                break
            prev_task.det_remain -= 1
            prev_task.deadline -= 1
            task.deadline -= 1
        prev_task.det_remain = det_remain_saved
        prev_task.deadline = deadline_saved
        return start + i

    def requeue_task(self, task: Task, ticks: int):
        if task.det_remain == 0:
            start = task.gap_head + task.deadline
            task.deadline += task.period
            task.det_remain = task.det
            task.deadline -= start
        else:
            start = 0
        node = self.header.after
        # while node != self.header:
        #     til = node.task
        #     if start < ticks | (start == ticks & Task.is_preceding(task, til)):
        #         if

    def schedule_task(self, task, system) -> (bool, int):
        pass
        # time = 0
        # time += task.gap_head

    def check_queued_tasks(self):
        pass

    def re_init_tasks(self):
        if self.is_empty():
            return
        node = self.header.after
        while node != self.header:
            task = node.task
            task.det = 0
            task.det_remain = 0
            task.gap_head = 0
            task.gap = 0
            task.deadline = 0
            node = node.after

    def show_queued_tasks(self):
        pass
        # 큐에 있는 태스크 보여주기
