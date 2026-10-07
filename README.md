# 2EZ4U APP

Proyek ini merupakan project dari mata kuliah struktur data dan algoritma dengan menggunakan bahasa Python tanpa memanfaatkan fungsi atau struktur data bawaan seperti dict, set, sorted(), .sort(), heapq, atau modul collections. Sistem ini dirancang untuk simulasi pemrosesan pesanan berkapasitas besar hingga 200.000 data.

## Ringkasan Modul Backend

### M1: Pengelolaan Pesanan 
* **Fixed Array**: Implementasi array berukuran tetap (fixed capacity) yang dialokasikan sejak awal tanpa mekanisme alokasi ulang atau perbesaran kapasitas (resizing). Jika kapasitas penuh, sistem akan menolak data baru dengan melempar OverflowError. Mendukung penyisipan pesanan Reguler di posisi belakang, Prioritas di tengah, dan VIP di posisi paling depan dengan pergeseran elemen O(n).
* **Singly Linked List**: Implementasi senarai berantai menggunakan pointer head dan tail. Menawarkan keunggulan penyisipan VIP di posisi paling depan dengan kompleksitas waktu konstan O(1).

## Analisis Algoritma - M1
-Fitur / Operasi,Fixed Array,Singly Linked List

1.Lihat Pesanan

2.Tambah Reguler

3.Tambah Prioritas

4.Tambah VIP 

5.Hapus Pesanan

## Batasan

1. **Dilarang Instant Function**: Tidak menggunakan dict, set, sorted(), .sort(), heapq, bisect, atau collections.
2. **Struktur Dasar**: Hanya menggunakan struktur list sebagai array primitif berukuran tetap, tuple, variabel skalar, serta perulangan dan kondisi standar.
3. **Akurasi Data**: Memastikan pengujian jujur antara dua jenis struktur data pada set data yang sama persis (200.000 baris CSV).
