# 2EZ4U APP

Proyek ini merupakan project dari mata kuliah struktur data dan algoritma dengan menggunakan bahasa Python tanpa memanfaatkan fungsi atau struktur data bawaan seperti dict, set, sorted(), .sort(), heapq, atau modul collections. Sistem ini dirancang untuk simulasi pemrosesan pesanan berkapasitas besar hingga 200.000 data.

## Ringkasan Modul Backend

### M1: Pengelolaan Pesanan 
- **Fixed Array**: Implementasi array berukuran tetap (*fixed capacity*) yang dialokasikan sejak awal tanpa mekanisme alokasi ulang atau perbesaran kapasitas (*resizing*). Jika kapasitas penuh, sistem akan menolak data baru dengan melempar OverflowError. Mendukung penyisipan pesanan Reguler di posisi belakang, Prioritas di tengah, dan VIP di posisi paling depan dengan pergeseran elemen **O(n)**.
- **Singly Linked List**: Implementasi senarai berantai menggunakan pointer head dan tail. Menawarkan keunggulan penyisipan VIP di posisi paling depan dengan kompleksitas waktu konstan **O(1)**.

### M2: Stack & Queue
- **Stack (Mesin Kasir Postfix)**: Mengubah ekspresi aritmetika belanja dari bentuk *infix* (misal: (3*12000)+(2*8500)-5000) menjadi *postfix* menggunakan *stack* operator, lalu mengevaluasinya secara akurat menggunakan *stack* angka.
- **Stack (Undo & Redo)**: Mencatat riwayat setiap aksi interaktif (seperti *enqueue*, *dequeue*, atau penambahan pesanan) ke dalam tumpukan *Undo* beserta kebalikannya, serta mendukung tombol *Redo*.
- **Queue (Antrean Naif vs Melingkar)**: 
  - **Antrean Naif**: Menggunakan larik biasa di mana operasi dequeue memaksa seluruh sisa elemen bergeser ke kiri bernilai **O(n)**.
  - **Antrean Melingkar (*Circular Queue*):** Menggunakan penunjuk front, rear, dan pencacah count dengan operasi modulo. Operasi dequeue memajukan penunjuk tanpa menggeser elemen bernilai konstan **O(1)**.

### M3: Sort & Search
- **Insertion Sort**: Pengurutan *in-place* dengan pengaman batas maksimal 20.000 baris untuk mencegah aplikasi mengalami *freeze*.
- **Merge Sort**: Algoritma *divide and conquer* yang sanggup mengurutkan seluruh 200.000 data CSV secara stabil dan efisien.
- **Linear Search**: Pencarian sekuensial dari depan tanpa syarat data terurut.
- **Binary Search**: Pencarian cepat yang menuntut data sudah terurut menurut kunci pencarian (misal berdasarkan oid).
- **Comparison Counter**: Setiap fungsi pengurutan dan pencarian dilengkapi penghitung perbandingan untuk analisis performa.

---

## Antarmuka Grafis & Pagination
Antarmuka dibangun menggunakan pustaka standar **Tkinter** yang dilengkapi:
1. **Navigasi Menu (Kiri)**: Daftar lengkap untuk mengakses pengujian M1, M2, dan M3.
2. **Pagination (Sistem Halaman)**: Memungkinkan penelusuran data hingga **200.000 baris** secara mulus tanpa *freeze* melalui tombol navigasi halaman (< Sebelumnya dan Selanjutnya > dengan kapasitas 1.000 data per halaman).
3. **Command Log (Bawah)**: Terminal interaktif bergaya retro yang mencatat setiap perintah, modul, jumlah perbandingan, serta waktu eksekusi presisi tinggi dalam milidetik (ms).

---

## Batasan & Aturan Teknis

1. **Dilarang Instant Function**: Tidak menggunakan dict, set, sorted(), .sort(), heapq, bisect, atau collections.
2. **Struktur Dasar**: Hanya menggunakan struktur list sebagai array primitif berukuran tetap, tuple, variabel skalar, serta perulangan dan kondisi standar.
3. **Akurasi Data**: Memastikan pengujian jujur antara jenis struktur data pada set data yang sama persis (200.000 baris CSV).
