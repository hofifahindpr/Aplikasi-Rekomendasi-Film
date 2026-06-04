import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from struktur.linked_list import LinkedList
from struktur.stack import Stack
from struktur.queue import Queue

class FilmManager:
    def __init__ (self):
        self.films = LinkedList()
        self.riwayat = Stack()
        self.watchlist = Queue()
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'films.json')
        self.load_data()
    
    def load_data(self):
        with open (self.data_path, 'r') as file:
            data = json.load(file)
            for film in data['films']:
                self.films.insert(film)
    
    def save_data(self):
        try:
            data = {'films': self.films.display()}
            with open(self.data_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Gagal menyimpan data: {e}")
            return False
    
    def tambah_film(self, film): #create
        if self.films.search(film['judul']):
            return False, "Film sudah ada!"
        
        self.films.insert(film)
        self.save_data()
        return True, "Film berhasil ditambahkan."
    
    def semua_films(self): #read
        return self.films.display()
    
    def get_film(self, judul):
        film = self.films.search(judul)
        if film:
            return True, film
        return False, "Film tidak ditemukan!"
    
    def edit_film(self, judul, data_baru): #update
        hasil = self.films.update(judul, data_baru)
        if hasil:
            self.save_data()
            return True, "Film berhasil diupdate!"
        return False, "Film tidak ditemukan!"
    
    def hapus_film(self, judul): #delete
        hasil = self.films.delete(judul)
        if hasil:
            self.save_data()
            return True, "Film berhasil dihapus!"
        return False, "Film tidak ditemukan!"
    
    def tambah_riwayat(self, judul): #riwayat
        film = self.films.search(judul)
        if film:
            self.riwayat.push(film)
            return True, "Film ditambahkan ke riwayat!"
        return False, "Film tidak ditemukan!"

    def get_riwayat(self):
        return self.riwayat.display()
    
    def tambah_watchlist(self, judul): #watchlist
        film = self.films.search(judul)
        if film:
            if self.watchlist.is_in_queue(judul):
                return False, "Film sudah ada di watchlist!"
            self.watchlist.enqueue(film)
            return True, "Film ditambahkan ke watchlist!"
        return False, "Film tidak ditemukan!"
    
    def get_watchlist(self):
        return self.watchlist.display()
    
    def hapus_watchlist(self, judul):
        hasil = self.watchlist.remove(judul)
        if hasil:
            return True, "Film dihapus dari watchlist!"
        return False, "Film tidak ada di watchlist!"