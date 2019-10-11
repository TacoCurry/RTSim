class ListNode:
    def __init__(self, task):
        self.task = task
        self.before: ListNode = None
        self.after: ListNode = None

    @staticmethod
    def change_node_task(node1, node2):
        temp = node1.task
        node1.task = node2.task
        node2.task = temp

        node1.task.node = node1
        node2.task.node = node2


class DoubleLinkedList:
    def __init__(self):
        dummy = ListNode(None)
        dummy.before = dummy.after = dummy
        self.header: ListNode = dummy
        # self.tail: ListNode = dummy

    def add_last(self, task) -> ListNode:
        new_node = ListNode(task)
        new_node.before = self.header.before
        new_node.after = self.header
        self.header.before.after = new_node
        self.header.before = new_node
        return new_node

    def add_first(self, task) -> ListNode:
        new_node = ListNode(task)
        new_node.before = self.header
        new_node.after = self.header.after
        self.header.after.before = new_node
        self.header.after = new_node
        return new_node

    # def add(self, pos, item):
    #     pass
    #
    # def delete(self, pos):
    #     pass
    #
    # def clear(self):
    #     pass
    #
    # def replace(self, pos, item):
    #     pass

    def is_in_list(self, task) -> bool:
        if self.is_empty():
            return False

        node = self.header.after
        while node != self.header:
            if node.task == task:
                return True
            node = node.after
        return False

    # def get_entry(self, pos) -> int:
    #     pass
    #
    # def get_length(self) -> int:
    #     pass

    def is_empty(self) -> bool:
        if self.header.after == self.header:
            return True
        return False

    # def is_full(self) -> bool:
    #     pass
    #
    # def display(self):
    #     pass

    @staticmethod
    def list_del_init(node):
        node.before.after = node.after
        node.after.before = node.before
        node.before = node.after = node
