class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        """เพิ่มไอเท็มลงใน stack"""
        self.items.append(item)

    def pop(self):
        """นำไอเท็มตัวล่าสุดออกจาก stack"""
        if not self.is_empty():
            return self.items.pop()
        else:
            return "Stack is empty"

    def peek(self):
        """ดูไอเท็มตัวล่าสุดโดยไม่นำออก"""
        if not self.is_empty():
            return self.items[-1]
        else:
            return "Stack is empty"

    def size(self):
        """ตรวจสอบจำนวนไอเท็มใน stack"""
        return len(self.items)

    def clear(self):
        """ล้าง stack ทั้งหมด"""
        self.items.clear()