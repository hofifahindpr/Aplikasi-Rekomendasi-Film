class Node:
    def __init__ (self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__ (self):
        self.head = None
    
    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
    
    def delete(self, judul):
        current = self.head
        if current and current.data['judul'] == judul:
            self.head = current.next
            return True
        prev = None
        while current and current.data['judul'] != judul:
            prev = current
            current = current.next
        if current is None:
            return False
        prev.next = current.next
        return True
    
    def search(self, judul):
        current = self.head
        while current:
            if current.data['judul'].lower() == judul.lower():
                return current.data
            current = current.next
        return None
    
    def update(self, judul, data_baru):
        current =self.head
        while current:
            if current.data['judul'].lower() == judul.lower():
                current.data.update(data_baru)
                return True
            current = current.next
        return False
    
    def display(self):
        films = []
        current = self.head
        while current:
            films.append(current.data)
            current = current.next
        return films
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count