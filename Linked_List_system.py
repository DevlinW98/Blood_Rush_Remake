# Node class to store data and the reference to the next node
class Node:
    def __init__(self, data):
        self.data = data  # Stores data
        self.next = None  # Points to the next node

# LinkedList class to handle operations like inserting and displaying nodes
class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the linked list

    # Method to insert a new node at the end of the linked list
    def append(self, data):
        new_node = Node(data)
        if self.head is None:  # If the list is empty, new node becomes the head
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Traverse to the last node
                current = current.next
            current.next = new_node  # Set the new node as the next of the last node

    # Method to display the linked list
    def display(self):
        current = self.head
        while current:  # Traverse the list until the last node
            print(current.data, end=" -> ")
            current = current.next
        print("None")  # Indicates the end of the list
    
    def isEmpty(self):
        return self.head == None

    def get_head_data(self):
        return self.head
    
    def size(self):
        count = 0
        current = self.head
        while current is not None:  # วนลูปจนกว่าจะถึง node สุดท้าย
            count += 1  # นับจำนวน node
            current = current.next  # ไปยัง node ถัดไป
        return count  # คืนค่าจำนวน node
    
    def pop_front(self):
        if not self.isEmpty():
            node = self.head
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return node.data

    
linked_list = LinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)

linked_list.display()

print(linked_list.size())