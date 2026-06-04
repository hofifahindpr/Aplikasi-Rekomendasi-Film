import tkinter as tk
from tkinter import ttk, messagebox

from core.film_manager import FilmManager
from algoritma.searching import search_by_title, search_by_genre
from algoritma.sorting import sort_by_rating, sort_by_title, sort_by_year


class CineRecGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 CineRec - Sistem Rekomendasi Film")
        self.root.geometry("1350x760")
        self.root.configure(bg="#FFE4EC")
        self.manager = FilmManager()
        self.setup_ui()
        self.load_movies()


    def setup_ui(self):
        self._make_header()
        main = tk.Frame(self.root, bg="#FFE4EC")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_panel   = self._panel(main, side="left",  width=280)
        self.center_panel = self._panel(main, side="left",  expand=True)
        self.right_panel  = self._panel(main, side="right", width=220)

        self.build_crud_panel()
        self.build_search_panel()
        self.build_quick_panel()
        self.build_movie_table()

    def _make_header(self):
        h = tk.Frame(self.root, bg="#FF6FA5", height=70)
        h.pack(fill="x")
        tk.Label(h, text="🎬 CineRec - Sistem Rekomendasi Film",
                 font=("Arial", 22, "bold"), bg="#FF6FA5", fg="white").pack(pady=15)

    def _panel(self, parent, side, width=None, expand=False):
        kw = dict(bg="white", bd=2, relief="ridge")
        if width:
            kw["width"] = width
        f = tk.Frame(parent, **kw)
        f.pack(side=side, fill="both" if expand else "y", expand=expand, padx=8)
        return f


    def build_crud_panel(self):
        self._section_label(self.left_panel, "🎬 Kelola Data Film")
        fields = ["Judul", "Genre", "Tahun", "Rating", "Sutradara"]
        entries = [self._entry(self.left_panel, f) for f in fields]
        self.title_entry, self.genre_entry, self.year_entry, \
            self.rating_entry, self.director_entry = entries

        btns = [
            ("➕ Tambah Film",  "#FF69B4", self.add_movie),
            ("✏️ Update Film",  "#FFA6C9", self.update_movie),
            ("🗑 Hapus Film",   "#FF8A80", self.delete_movie),
        ]
        for text, color, cmd in btns:
            tk.Button(self.left_panel, text=text, bg=color, fg="white",
                      font=("Arial", 11, "bold"), command=cmd
                      ).pack(fill="x", padx=20, pady=5)

    def build_search_panel(self):
        self._section_label(self.center_panel, "🔍 Search & Filter")

        self.search_entry = tk.Entry(self.center_panel, font=("Arial", 12))
        self.search_entry.pack(fill="x", padx=20)

        tk.Button(self.center_panel, text="Cari Film", bg="#FF69B4", fg="white",
                  font=("Arial", 11, "bold"), command=self.search_movie).pack(pady=8)

        tk.Label(self.center_panel, text="Filter Genre", bg="white").pack()

        self.genre_var = tk.StringVar(value="Semua")
        ttk.Combobox(self.center_panel, textvariable=self.genre_var, state="readonly",
                     values=["Semua","Action","Drama","Sci-Fi",
                             "Thriller","Comedy","Animation"]).pack(pady=5)

        tk.Button(self.center_panel, text="Filter Genre", bg="#CE93D8", fg="white",
                  font=("Arial", 11, "bold"), command=self.filter_genre).pack(pady=8)

    def build_quick_panel(self):
        self._section_label(self.right_panel, "⚡ Quick Access")
        btns = [
            ("⭐ Rating Tertinggi", self.sort_rating),
            ("📅 Tahun Terbaru",    self.sort_year),
            ("🔤 Urut A-Z",         self.sort_title),
            ("🎬 Semua Film",       self.load_movies),
        ]
        for text, cmd in btns:
            tk.Button(self.right_panel, text=text, command=cmd
                      ).pack(fill="x", padx=20, pady=5)

    def build_movie_table(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("judul", "genre", "tahun", "rating")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, font=("Arial", 16, "bold"),
                 bg="white", fg="#E91E63").pack(pady=10)

    def _entry(self, parent, label):
        tk.Label(parent, text=label, bg="white").pack(anchor="w", padx=20)
        e = tk.Entry(parent)
        e.pack(fill="x", padx=20, pady=5)
        return e

    def show_movies(self, films):
        self.tree.delete(*self.tree.get_children())
        for f in films:
            self.tree.insert("", "end",
                             values=(f["judul"], f["genre"], f["tahun"], f["rating"]))

    def load_movies(self):
        self.show_movies(self.manager.semua_films())

    def search_movie(self):
        self.show_movies(search_by_title(self.manager.semua_films(), self.search_entry.get()))

    def filter_genre(self):
        g = self.genre_var.get()
        films = self.manager.semua_films() if g == "Semua" \
            else search_by_genre(self.manager.semua_films(), g)
        self.show_movies(films)

    def sort_rating(self): self.show_movies(sort_by_rating(self.manager.semua_films()))
    def sort_year(self):   self.show_movies(sort_by_year(self.manager.semua_films()))
    def sort_title(self):  self.show_movies(sort_by_title(self.manager.semua_films()))

    def add_movie(self):
        try:
            film = {
                "judul":     self.title_entry.get().strip(),
                "genre":     self.genre_entry.get().strip(),
                "tahun":     int(self.year_entry.get()),
                "rating":    float(self.rating_entry.get()),
                "sutradara": self.director_entry.get().strip()
            }
            if not film["judul"]:
                raise ValueError("Judul tidak boleh kosong.")
            _, msg = self.manager.tambah_film(film)
            messagebox.showinfo("Info", msg)
            self.load_movies()
        except ValueError as e:
            messagebox.showerror("Input Error", f"Data tidak valid: {e}")

    def update_movie(self):
        messagebox.showinfo("Info", "Klik edit manual di JSON dulu ya")

    def delete_movie(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Peringatan", "Masukkan judul film yang akan dihapus.")
            return
        _, msg = self.manager.hapus_film(title)
        messagebox.showinfo("Info", msg)
        self.load_movies()


def run_app():
    root = tk.Tk()
    CineRecGUI(root)
    root.mainloop()