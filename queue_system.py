class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop(0)
        else:
            return "Queue is empty"

    def peek(self):
        if not self.isEmpty():
            return self.items[0]
        else:
            return "Queue is empty"

    def size(self):
        return len(self.items)
