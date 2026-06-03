import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

BG_MAIN       = "#FFF0F5"
BG_CARD       = "#FFFFFF"
BG_HEADER     = "#F8A7C0"
BG_PANEL      = "#FFF5F8"
BG_BTN_PINK   = "#E91E8C"
BG_BTN_SOFT   = "#F48FB1"
BG_BTN_GRAY   = "#B0BEC5"
BG_BTN_PURPLE = "#CE93D8"
FG_HEADER     = "#FFFFFF"
FG_TITLE      = "#880E4F"
FG_LABEL      = "#AD1457"
FG_MUTED      = "#EC407A"
FG_TEXT       = "#4A0022"
BORDER        = "#F48FB1"
ACCENT        = "#E91E8C"


DEMO_FILMS = [
    {"id": 1,  "judul": "Inception",                   "genre": "Sci-Fi",    "tahun": 2010, "rating": 8.8},
    {"id": 2,  "judul": "Interstellar",                "genre": "Sci-Fi",    "tahun": 2014, "rating": 8.6},
    {"id": 3,  "judul": "The Dark Knight",             "genre": "Action",    "tahun": 2008, "rating": 9.0},
    {"id": 4,  "judul": "Parasite",                    "genre": "Thriller",  "tahun": 2019, "rating": 8.5},
    {"id": 5,  "judul": "Your Name",                   "genre": "Animation", "tahun": 2016, "rating": 8.4},
    {"id": 6,  "judul": "The Shawshank Redemption",    "genre": "Drama",     "tahun": 1994, "rating": 9.3},
    {"id": 7,  "judul": "Spirited Away",               "genre": "Animation", "tahun": 2001, "rating": 8.6},
    {"id": 8,  "judul": "The Matrix",                  "genre": "Sci-Fi",    "tahun": 1999, "rating": 8.7},
    {"id": 9,  "judul": "Avengers: Endgame",           "genre": "Action",    "tahun": 2019, "rating": 8.4},
    {"id": 10, "judul": "Joker",                       "genre": "Drama",     "tahun": 2019, "rating": 8.4},
    {"id": 11, "judul": "Get Out",                     "genre": "Horror",    "tahun": 2017, "rating": 7.7},
    {"id": 12, "judul": "Knives Out",                  "genre": "Thriller",  "tahun": 2019, "rating": 7.9},
]

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "films_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEMO_FILMS.copy()

def save_data(films):
    with open(DATA_FILE, "w") as f:
        json.dump(films, f, indent=2)


class CineRecApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 CineRec — Sistem Rekomendasi Film")
        self.geometry("1150x720")
        self.minsize(950, 620)
        self.configure(bg=BG_MAIN)

        self.films = load_data()
        self.favorit = []
        self.histori = []
        self.selected_id = None

        self._build_ui()
        self._refresh_cards()

    def _build_ui(self):
       
        header = tk.Frame(self, bg=BG_HEADER, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header,
                 text="🎬 CineRec — Sistem Rekomendasi Film",
                 font=("Helvetica", 20, "bold"),
                 fg=FG_HEADER, bg=BG_HEADER).pack(expand=True)

       
        tk.Frame(self, bg=ACCENT, height=3).pack(fill="x")

       
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="x", padx=14, pady=10)

        self._build_left(main)
        self._build_middle(main)
        self._build_right(main)

        
        tk.Frame(self, bg=BORDER, height=2).pack(fill="x", padx=14)

       
        canvas_frame = tk.Frame(self, bg=BG_MAIN)
        canvas_frame.pack(fill="both", expand=True, padx=14, pady=8)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Pink.Vertical.TScrollbar",
                         background=BG_BTN_SOFT,
                         troughcolor=BG_MAIN,
                         arrowcolor=ACCENT)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_MAIN,
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                  command=self.canvas.yview,
                                  style="Pink.Vertical.TScrollbar")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.card_frame = tk.Frame(self.canvas, bg=BG_MAIN)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.card_frame, anchor="nw")

        self.card_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _panel(self, parent, title):
        """Buat panel dengan shadow effect."""
        # Shadow frame
        shadow = tk.Frame(parent, bg="#F4A7B9")
        shadow.pack(side="left", fill="y", padx=(0, 10), pady=3)

        
        frame = tk.LabelFrame(shadow, text=f"  {title}  ",
                               font=("Helvetica", 10, "bold"),
                               fg=FG_TITLE, bg=BG_PANEL,
                               relief="flat", bd=0,
                               highlightthickness=2,
                               highlightbackground=BORDER,
                               highlightcolor=ACCENT)
        frame.pack(padx=(0, 3), pady=(0, 3), fill="both", expand=True,
                   ipadx=6, ipady=6)
        return frame

    def _build_left(self, parent):
        frame = self._panel(parent, "🎬 Kelola Data Film")

        fields = [("Judul Film", "judul"), ("Genre", "genre"),
                  ("Tahun", "tahun"), ("Rating (0-10)", "rating")]
        self.entries = {}

        for label, key in fields:
            tk.Label(frame, text=label, font=("Helvetica", 9, "bold"),
                     fg=FG_LABEL, bg=BG_PANEL).pack(anchor="w",
                                                     padx=12, pady=(8, 0))
            e = tk.Entry(frame, font=("Helvetica", 10),
                         relief="flat", bd=0, width=22,
                         bg="#FFFFFF", fg=FG_TEXT,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT,
                         insertbackground=ACCENT)
            e.pack(padx=12, pady=(2, 0), ipady=5)
            self.entries[key] = e

        btn_cfg = [
            ("➕  Tambah",  BG_BTN_PINK,   self._tambah),
            ("✏️   Update",  BG_BTN_SOFT,   self._update),
            ("🗑   Hapus",   "#E57373",      self._hapus),
            ("🔄  Reset",   BG_BTN_GRAY,   self._clear),
        ]
        for text, bg, cmd in btn_cfg:
            b = tk.Button(frame, text=text,
                          font=("Helvetica", 10, "bold"),
                          bg=bg, fg="white", relief="flat",
                          cursor="hand2", bd=0,
                          activebackground=ACCENT,
                          activeforeground="white",
                          command=cmd)
            b.pack(fill="x", padx=12, pady=(7, 0), ipady=7)

    def _build_middle(self, parent):
        
        shadow = tk.Frame(parent, bg="#F4A7B9")
        shadow.pack(side="left", fill="both", expand=True,
                    padx=(0, 10), pady=3)

        frame = tk.LabelFrame(shadow,
                               text="  🔍 Pencarian & Rekomendasi  ",
                               font=("Helvetica", 10, "bold"),
                               fg=FG_TITLE, bg=BG_PANEL,
                               relief="flat", bd=0,
                               highlightthickness=2,
                               highlightbackground=BORDER,
                               highlightcolor=ACCENT)
        frame.pack(padx=(0, 3), pady=(0, 3), fill="both", expand=True,
                   ipadx=6, ipady=6)

        def entry_field(lbl):
            tk.Label(frame, text=lbl, font=("Helvetica", 9, "bold"),
                     fg=FG_LABEL, bg=BG_PANEL).pack(anchor="w",
                                                     padx=12, pady=(10, 0))
            e = tk.Entry(frame, font=("Helvetica", 10),
                         relief="flat", bd=0,
                         bg="#FFFFFF", fg=FG_TEXT,
                         highlightthickness=1,
                         highlightbackground=BORDER,
                         highlightcolor=ACCENT,
                         insertbackground=ACCENT)
            e.pack(fill="x", padx=12, pady=(2, 0), ipady=5)
            return e

        self.search_entry = entry_field("Cari Film")

        tk.Button(frame, text="🔍  Cari",
                  font=("Helvetica", 10, "bold"),
                  bg=BG_BTN_PINK, fg="white", relief="flat",
                  cursor="hand2", activebackground=ACCENT,
                  command=self._cari).pack(fill="x", padx=12,
                                           pady=(8, 0), ipady=7)

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x",
                                                   padx=12, pady=10)

        tk.Label(frame, text="Filter Genre",
                 font=("Helvetica", 9, "bold"),
                 fg=FG_LABEL, bg=BG_PANEL).pack(anchor="w",
                                                 padx=12, pady=(0, 2))

        self.genre_var = tk.StringVar(value="Semua")
        genres = ["Semua", "Action", "Sci-Fi", "Drama",
                  "Comedy", "Horror", "Thriller", "Animation", "Romance"]

        style = ttk.Style()
        style.configure("Pink.TCombobox",
                         fieldbackground="#FFFFFF",
                         background=BG_BTN_SOFT,
                         foreground=FG_TEXT,
                         arrowcolor=ACCENT)

        genre_cb = ttk.Combobox(frame, textvariable=self.genre_var,
                                 values=genres, state="readonly",
                                 font=("Helvetica", 10),
                                 style="Pink.TCombobox")
        genre_cb.pack(fill="x", padx=12, pady=(0, 0), ipady=4)

        tk.Label(frame, text="Min Rating",
                 font=("Helvetica", 9, "bold"),
                 fg=FG_LABEL, bg=BG_PANEL).pack(anchor="w",
                                                 padx=12, pady=(10, 2))

        self.rating_var = tk.StringVar(value="7.0")
        tk.Entry(frame, textvariable=self.rating_var,
                 font=("Helvetica", 10), relief="flat", bd=0,
                 bg="#FFFFFF", fg=FG_TEXT,
                 highlightthickness=1,
                 highlightbackground=BORDER,
                 highlightcolor=ACCENT,
                 insertbackground=ACCENT).pack(fill="x", padx=12,
                                               pady=(0, 0), ipady=5)

        tk.Button(frame, text="✨  Cari Rekomendasi",
                  font=("Helvetica", 10, "bold"),
                  bg=BG_BTN_PINK, fg="white", relief="flat",
                  cursor="hand2", activebackground=ACCENT,
                  command=self._rekomendasi).pack(fill="x", padx=12,
                                                  pady=(8, 0), ipady=7)

        tk.Button(frame, text="🔄  Reset",
                  font=("Helvetica", 10, "bold"),
                  bg=BG_BTN_GRAY, fg="white", relief="flat",
                  cursor="hand2", activebackground="#90A4AE",
                  command=self._reset).pack(fill="x", padx=12,
                                            pady=(6, 0), ipady=7)

        self.status_label = tk.Label(frame, text="",
                                     font=("Helvetica", 9, "italic"),
                                     fg=ACCENT, bg=BG_PANEL,
                                     wraplength=200, justify="left")
        self.status_label.pack(padx=12, pady=(8, 4), anchor="w")

    def _build_right(self, parent):
        frame = self._panel(parent, "💖 Akses Cepat")

        btns = [
            ("⭐  Tambah Favorit", BG_BTN_PINK,   self._tambah_favorit),
            ("❤️   Lihat Favorit",  BG_BTN_SOFT,   self._lihat_favorit),
            ("🕐  Lihat Histori",   BG_BTN_GRAY,   self._lihat_histori),
            ("📋  Semua Film",      BG_BTN_SOFT,   self._reset),
            ("🎲  Acak Film",       BG_BTN_PURPLE, self._acak_film),
        ]

        for text, bg, cmd in btns:
            tk.Button(frame, text=text,
                      font=("Helvetica", 10, "bold"),
                      bg=bg, fg="white", relief="flat",
                      cursor="hand2", width=17,
                      activebackground=ACCENT,
                      activeforeground="white",
                      command=cmd).pack(padx=12, pady=(8, 0), ipady=7)

    
    def _refresh_cards(self, films=None):
        for w in self.card_frame.winfo_children():
            w.destroy()

        data = films if films is not None else self.films

        if not data:
            tk.Label(self.card_frame,
                     text="Tidak ada film ditemukan. 🎬🚫",
                     font=("Helvetica", 11, "italic"),
                     fg=FG_MUTED, bg=BG_MAIN).pack(pady=20)
            return

        genre_colors = {
            "Sci-Fi":    ("#EDE7F6", "#7E57C2"),
            "Action":    ("#FCE4EC", "#E91E63"),
            "Drama":     ("#E8F5E9", "#43A047"),
            "Horror":    ("#F3E5F5", "#8E24AA"),
            "Thriller":  ("#FFF8E1", "#FB8C00"),
            "Animation": ("#FCE4EC", "#F06292"),
            "Comedy":    ("#E0F7FA", "#00ACC1"),
            "Romance":   ("#FCE4EC", "#E91E63"),
        }

        cols = 6
        for i, film in enumerate(data):
            row, col = divmod(i, cols)

            # Shadow frame
            shadow = tk.Frame(self.card_frame, bg="#F4A7B9")
            shadow.grid(row=row, column=col, padx=6, pady=6)

            card = tk.Frame(shadow, bg=BG_CARD,
                            width=158, height=115, cursor="hand2")
            card.pack(padx=(0, 3), pady=(0, 3))
            card.pack_propagate(False)

            badge_bg, badge_fg = genre_colors.get(
                film["genre"], ("#FCE4EC", "#E91E63"))

            
            tk.Frame(card, bg=badge_fg, height=4).pack(fill="x")

            tk.Label(card, text=film["judul"],
                     font=("Helvetica", 9, "bold"),
                     fg=FG_TEXT, bg=BG_CARD,
                     wraplength=140, justify="left").pack(
                anchor="w", padx=8, pady=(6, 2))

            tk.Label(card, text=f"  {film['genre']}  ",
                     font=("Helvetica", 8),
                     fg=badge_fg, bg=badge_bg).pack(anchor="w", padx=8)

            tk.Label(card,
                     text=f"⭐ {film['rating']}  •  {film['tahun']}",
                     font=("Helvetica", 8),
                     fg="#AD1457", bg=BG_CARD).pack(
                anchor="w", padx=8, pady=(4, 0))

            for w in [card, shadow] + card.winfo_children():
                w.bind("<Button-1>",
                       lambda e, f=film: self._select_film(f))

    def _select_film(self, film):
        self.selected_id = film["id"]
        for key in ["judul", "genre", "tahun", "rating"]:
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, str(film[key]))
        if film not in self.histori:
            self.histori.append(film)
        self.status_label.config(
            text=f"🎬 Dipilih: {film['judul']}", fg=ACCENT)

    # CRUD
    def _tambah(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Peringatan", "Harap isi semua field!")
            return
        try:
            float(data["rating"])
            int(data["tahun"])
        except ValueError:
            messagebox.showerror("Error",
                                 "Tahun harus angka!\nRating harus angka desimal!")
            return
        new_id = max((f["id"] for f in self.films), default=0) + 1
        film = {"id": new_id, "judul": data["judul"],
                "genre": data["genre"],
                "tahun": int(data["tahun"]),
                "rating": float(data["rating"])}
        self.films.append(film)
        save_data(self.films)
        self._clear()
        self._refresh_cards()
        self.status_label.config(
            text=f"✅ '{film['judul']}' ditambahkan!", fg="#43A047")

    def _update(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan",
                                   "Klik film yang ingin diupdate dulu!")
            return
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Peringatan", "Harap isi semua field!")
            return
        for f in self.films:
            if f["id"] == self.selected_id:
                f["judul"]  = data["judul"]
                f["genre"]  = data["genre"]
                f["tahun"]  = int(data["tahun"])
                f["rating"] = float(data["rating"])
                break
        save_data(self.films)
        self._clear()
        self._refresh_cards()
        self.status_label.config(text="✅ Film berhasil diupdate!", fg="#43A047")

    def _hapus(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan",
                                   "Klik film yang ingin dihapus dulu!")
            return
        film = next((f for f in self.films
                     if f["id"] == self.selected_id), None)
        if film and messagebox.askyesno(
                "Konfirmasi", f"Hapus film '{film['judul']}'?"):
            self.films = [f for f in self.films
                          if f["id"] != self.selected_id]
            save_data(self.films)
            self._clear()
            self._refresh_cards()
            self.status_label.config(
                text="🗑 Film berhasil dihapus!", fg="#E57373")

    def _clear(self):
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.selected_id = None
        self.status_label.config(text="")

    
    def _cari(self):
        q = self.search_entry.get().strip().lower()
        if not q:
            self._refresh_cards()
            return
        hasil = [f for f in self.films
                 if q in f["judul"].lower() or q in f["genre"].lower()]
        self._refresh_cards(hasil)
        self.status_label.config(
            text=f"🔍 {len(hasil)} film ditemukan untuk '{q}'",
            fg=ACCENT)

    def _rekomendasi(self):
        genre = self.genre_var.get()
        try:
            min_rating = float(self.rating_var.get())
        except ValueError:
            min_rating = 7.0
        hasil = [f for f in self.films
                 if (genre == "Semua" or f["genre"] == genre)
                 and float(f["rating"]) >= min_rating]
        hasil.sort(key=lambda x: float(x["rating"]), reverse=True)
        self._refresh_cards(hasil)
        self.status_label.config(
            text=f"✨ {len(hasil)} rekomendasi ditemukan!", fg="#7E57C2")

    def _reset(self):
        self.search_entry.delete(0, tk.END)
        self.genre_var.set("Semua")
        self.rating_var.set("7.0")
        self._refresh_cards()
        self.status_label.config(text="")

   
    def _tambah_favorit(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan",
                                   "Klik film dulu untuk ditambah ke favorit!")
            return
        film = next((f for f in self.films
                     if f["id"] == self.selected_id), None)
        if film and film not in self.favorit:
            self.favorit.append(film)
            self.status_label.config(
                text=f"⭐ '{film['judul']}' ditambah ke favorit!", fg="#FB8C00")
        else:
            self.status_label.config(
                text="Film sudah ada di favorit.", fg="#888888")

    def _lihat_favorit(self):
        if not self.favorit:
            messagebox.showinfo("Favorit", "Belum ada film favorit! 🌸")
            return
        self._refresh_cards(self.favorit)
        self.status_label.config(
            text=f"❤️ {len(self.favorit)} film favorit", fg="#E91E63")

    def _lihat_histori(self):
        if not self.histori:
            messagebox.showinfo("Histori", "Belum ada histori! 🌸")
            return
        self._refresh_cards(self.histori)
        self.status_label.config(
            text=f"🕐 {len(self.histori)} film di histori", fg="#90A4AE")

    def _acak_film(self):
        acak = random.sample(self.films, min(6, len(self.films)))
        self._refresh_cards(acak)
        self.status_label.config(text="🎲 Film acak untukmu! 🎬", fg="#CE93D8")

    
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


if __name__ == "__main__":
    app = CineRecApp()
    app.mainloop()