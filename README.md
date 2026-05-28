# Aplikasi-Rekomendasi-Film

Aplikasi berbasis Desktop (GUI) menggunakan Python yang dirancang untuk mengelola daftar film, melacak riwayat tontonan, dan memberikan rekomendasi film berdasarkan preferensi pengguna. Proyek ini dibuat untuk memenuhi Ujian Akhir Praktikum (UAP) pada mata kuliah "Algoritma dan Struktur Data Dasar".

---

# Fitur Utama
* Manajemen Data Film (CRUD): Tambah, edit, dan hapus data film secara *real-time* yang tersimpan dalam format JSON.
* Sistem Rekomendasi: Memberikan rekomendasi film berdasarkan genre dan keterkaitan antar-film.
* Fitur Pencarian & Pengurutan: Cari film berdasarkan judul/genre, serta urutkan berdasarkan rating atau tahun rilis.
* Riwayat & Watchlist: Fitur simpan daftar tontonan (Watchlist) dan riwayat film yang sudah ditonton.

---

# 🛠️ Implementasi Struktur Data & Algoritma
Proyek ini mengimplementasikan beberapa konsep dasar Algoritma dan Struktur Data Dasar:
* Linked List: Digunakan untuk menyimpan daftar utama film.
* Stack: Digunakan untuk mencatat riwayat tontonan (history).
* Queue: Digunakan untuk antrean daftar tontonan (watchlist).
* Graph: Digunakan untuk memetakan hubungan/relasi antar-film berdasarkan kesamaan genre.
* Algoritma Searching & Sorting: Menggunakan metode pencarian dan pengurutan efisien untuk menampilkan data film.

---

# Pembagian Tugas
* ERNI MAYASARI - 2517052003
  * Tanggung Jawab: Struktur Data & Backend (`linked_list.py`, `stack.py`, `queue.py`, `graph.py`, `film_manager.py`)
* HOFIFAH INDAR PARAWANSA - 2517052018
  * Tanggung Jawab: Algoritma & Rekomendasi (`sorting.py`, `searching.py`, `recommender.py`, GitHub Management)
* BUNGA PERMATA SARI - 2517052031
  * Tanggung Jawab: Desain UI/GUI (`home.py`, `crud_ui.py`, `rekomendasi_ui.py` menggunakan `tkinter`)
* MAIMUNA YULIANTI - 2517052026
  * Tanggung Jawab: Data & Dokumentasi (`main.py`, Dokumentasi Laporan BAB 1, 2, 3, `films.json`, )
