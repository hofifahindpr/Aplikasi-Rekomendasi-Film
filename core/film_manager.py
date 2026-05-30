import json
import os
from struktur.linked_list import LinkedList
from struktur.stack import Stack
from struktur.queue import Queue

class FilmManager:
    def __init__ (self):
        self.films = LinkedList()
        self.history = Stack()
        self.whatchlist = Queue()
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'films.json')
        self.load_data()
    