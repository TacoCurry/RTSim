class ListNode:
    def __init__(self, item):
        self.item = item
        self.before: ListNode = None
        self.after: ListNode = None


class DoubleLinkedList:
    def __init__(self):
        self.head: ListNode = None
        self.tail: ListNode = None

    def add_last(self, item):
        new_node = ListNode(item)
        if self.is_empty():
            self.head = self.tail = new_node
            new_node.before = new_node.after = new_node
        else:
            new_node.before = self.tail
            new_node.after = self.head
            self.tail.after = self.head.before = new_node
            self.tail = new_node

    def add_first(self, item):
        new_node = ListNode(item)
        if self.is_empty():
            self.head = self.tail = new_node
            new_node.before = new_node.after = new_node
        else:
            new_node.before = self.tail
            new_node.after = self.head
            self.tail.after = self.head.before = new_node
            self.head = new_node

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

    def is_in_list(self, item) -> bool:
        if self.head.item == item:
            return True

        node = self.head.after
        while node != self.head:
            if node.item == item:
                return True
            node = node.after

        return False

    # def get_entry(self, pos) -> int:
    #     pass
    #
    # def get_length(self) -> int:
    #     pass

    def is_empty(self) -> bool:
        if self.head is None:
            return True
        return False

    # def is_full(self) -> bool:
    #     pass
    #
    # def display(self):
    #     pass
