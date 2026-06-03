class Queue:
    def __init__(self):
        self.items =[]
    
    def enqueue(self, data):
        self.items.append(data)
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]
    
    def size(self):
        return len(self.items)
    
    def is_in_queue(self, judul):
        for item in self.items:
            if item['judul'].lower() == judul.lower():
                return True
        return False
    
    def remove(self, judul):
        for i, item in enumerate(self.items):
            if item['judul'].lower() == judul.lower():
                self.items.pop(i)
                return True
        return False