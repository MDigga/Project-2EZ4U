import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
import time

class MainAppWindow(tk.Tk):
    def __init__(self, array_pesanan, linked_pesanan, manajer):
        super().__init__()
        self.title("2EZ4U Food Delivery - Struktur Data & Analisa Algoritma (EC234303)")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.array_pesanan = array_pesanan
        self.linked_pesanan = linked_pesanan
        self.manajer = manajer
        
        self.next_oid_num = 200001
        self._setup_ui()

    def _setup_ui(self):
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(main_paned, width=300)
        main_paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="NAVIGASI MENU", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=5, pady=5)
        
        menu_scroll = ttk.Scrollbar(left_frame)
        menu_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menu_listbox = tk.Listbox(left_frame, yscrollcommand=menu_scroll.set, font=("Arial", 10), selectmode=tk.SINGLE)
        self.menu_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        menu_scroll.config(command=self.menu_listbox.yview)

        menus = [
            "DATA: Load Ulang CSV",
            "--- M1: ARRAY ---",
            "ARRAY - Lihat Pesanan",
            "ARRAY - Tambah Pesanan Reguler",
            "ARRAY - Tambah Pesanan Prioritas",
            "ARRAY - Tambah Pesanan VIP",
            "ARRAY - Hapus Pesanan",
            "--- M1: LINKED LIST ---",
            "LINKEDLIST - Lihat Pesanan",
            "LINKEDLIST - Tambah Pesanan Reguler",
            "LINKEDLIST - Tambah Pesanan Prioritas",
            "LINKEDLIST - Tambah Pesanan VIP",
            "LINKEDLIST - Hapus Pesanan",
            "--- M2: STACK & QUEUE ---",
            "STACK - Postfix (Mesin Kasir)",
            "STACK - Undo",
            "STACK - Redo",
            "QUEUE - Enqueue",
            "QUEUE - Dequeue Naif",
            "QUEUE - Dequeue Circular",
            "--- M3: SORT & SEARCH ---",
            "SORT - Insertion Sort",
            "SORT - Merge Sort",
            "SEARCH - Linear Search",
            "SEARCH - Binary Search"
        ]
        for m in menus:
            self.menu_listbox.insert(tk.END, m)

        self.menu_listbox.bind("<<ListboxSelect>>", self.on_menu_select)

        right_container = ttk.Frame(main_paned)
        main_paned.add(right_container, weight=4)

        right_paned = ttk.PanedWindow(right_container, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)

        self.content_frame = ttk.Frame(right_paned)
        right_paned.add(self.content_frame, weight=3)

        bottom_frame = ttk.Labelframe(right_paned, text="COMMAND")
        right_paned.add(bottom_frame, weight=1)

        cmd_scroll = ttk.Scrollbar(bottom_frame)
        cmd_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.cmd_text = tk.Text(bottom_frame, height=6, yscrollcommand=cmd_scroll.set, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00")
        self.cmd_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cmd_scroll.config(command=self.cmd_text.yview)

        self.log_command("Aplikasi UI diinisialisasi. Siap digunakan.")

    def log_command(self, text, module="system", elapsed_ms=0.0):
        msg = f"> {text}\n  [{module}] {elapsed_ms:.2f} ms\n"
        self.cmd_text.insert(tk.END, msg)
        self.cmd_text.see(tk.END)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def on_menu_select(self, event):
        selection = self.menu_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        val = self.menu_listbox.get(idx)

        if "Load Ulang" in val:
            messagebox.showinfo("Info", "Gunakan app.py untuk memuat ulang data CSV.")
            return

        self.clear_content()

        if "ARRAY - Lihat Pesanan" in val:
            self.show_view_pesanan("Array")
        elif "ARRAY - Tambah Pesanan Reguler" in val:
            self.show_tambah_pesanan("Array", 3, "REGULER")
        elif "ARRAY - Tambah Pesanan Prioritas" in val:
            self.show_tambah_pesanan("Array", 2, "PRIORITAS")
        elif "ARRAY - Tambah Pesanan VIP" in val:
            self.show_tambah_pesanan("Array", 1, "VIP")
        elif "ARRAY - Hapus Pesanan" in val:
            self.show_hapus_pesanan("Array")
        elif "LINKEDLIST - Lihat Pesanan" in val:
            self.show_view_pesanan("LinkedList")
        elif "LINKEDLIST - Tambah Pesanan Reguler" in val:
            self.show_tambah_pesanan("LinkedList", 3, "REGULER")
        elif "LINKEDLIST - Tambah Pesanan Prioritas" in val:
            self.show_tambah_pesanan("LinkedList", 2, "PRIORITAS")
        elif "LINKEDLIST - Tambah Pesanan VIP" in val:
            self.show_tambah_pesanan("LinkedList", 1, "VIP")
        elif "LINKEDLIST - Hapus Pesanan" in val:
            self.show_hapus_pesanan("LinkedList")
        elif "STACK - Postfix" in val:
            self.show_stack_postfix()
        elif "STACK - Undo" in val:
            self.show_stack_undo()
        elif "STACK - Redo" in val:
            self.show_stack_redo()
        elif "QUEUE - Enqueue" in val:
            self.show_queue_enqueue()
        elif "QUEUE - Dequeue Naif" in val:
            self.show_queue_dequeue("naif")
        elif "QUEUE - Dequeue Circular" in val:
            self.show_queue_dequeue("circular")
        elif "SORT - Insertion Sort" in val:
            self.show_sort("insertion")
        elif "SORT - Merge Sort" in val:
            self.show_sort("merge")
        elif "SEARCH - Linear Search" in val:
            self.show_search("linear")
        elif "SEARCH - Binary Search" in val:
            self.show_search("binary")

    def show_view_pesanan(self, jenis):
        lbl = ttk.Label(self.content_frame, text=f"M1: Lihat Pesanan ({jenis})", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        control_frame = ttk.Frame(self.content_frame)
        control_frame.pack(anchor=tk.W, padx=10, pady=5)

        source = self.array_pesanan if jenis == "Array" else self.linked_pesanan
        total_data = len(source)
        page_size = 1000
        current_page = [0]
        max_pages = max(1, (total_data + page_size - 1) // page_size)

        sub_frame = ttk.Frame(self.content_frame)
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("No", "OID", "Pelanggan", "Resto", "Menu", "Harga", "Prioritas", "Status")
        tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=18)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.W)
        tree.column("No", width=60)
        tree.column("Harga", width=80)
        tree.column("Prioritas", width=60)

        scrollbar = ttk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        info_page_lbl = ttk.Label(control_frame, text="", font=("Arial", 10, "bold"))

        def load_page():
            for row in tree.get_children():
                tree.delete(row)
            
            start_idx = current_page[0] * page_size
            end_idx = min(start_idx + page_size, total_data)

            t0 = time.perf_counter()
            for i in range(start_idx, end_idx):
                p = source.get(i)
                tree.insert("", tk.END, values=(i+1, p.oid, p.pelanggan, p.resto, p.menu, f"Rp {p.harga:,}", p.prioritas, p.status))
            t1 = time.perf_counter()
            elapsed = (t1 - t0) * 1000

            info_page_lbl.config(text=f"Hal {current_page[0]+1}/{max_pages} | Data {start_idx+1:,} - {end_idx:,} dari {total_data:,}")
            e_page.delete(0, tk.END)
            e_page.insert(0, str(current_page[0] + 1))
            self.log_command(f"Menampilkan halaman {current_page[0]+1} dari {jenis}.", f"M1 - {jenis}", elapsed)

        def next_page():
            if (current_page[0] + 1) * page_size < total_data:
                current_page[0] += 1
                load_page()

        def prev_page():
            if current_page[0] > 0:
                current_page[0] -= 1
                load_page()

        def jump_page():
            try:
                target_p = int(e_page.get()) - 1
                if 0 <= target_p < max_pages:
                    current_page[0] = target_p
                    load_page()
                else:
                    messagebox.showerror("Error", f"Masukkan nomor halaman antara 1 dan {max_pages}")
            except ValueError:
                messagebox.showerror("Error", "Nomor halaman harus berupa angka bulat.")

        btn_prev = ttk.Button(control_frame, text="< Sebelumnya", command=prev_page)
        btn_prev.pack(side=tk.LEFT, padx=3)

        info_page_lbl.pack(side=tk.LEFT, padx=8)

        btn_next = ttk.Button(control_frame, text="Selanjutnya >", command=next_page)
        btn_next.pack(side=tk.LEFT, padx=3)

        ttk.Label(control_frame, text="   Loncat ke Hal:").pack(side=tk.LEFT, padx=2)
        e_page = ttk.Entry(control_frame, width=6)
        e_page.pack(side=tk.LEFT, padx=2)
        e_page.bind("<Return>", lambda event: jump_page())

        btn_go = ttk.Button(control_frame, text="Go", command=jump_page)
        btn_go.pack(side=tk.LEFT, padx=2)

        load_page()

    def show_tambah_pesanan(self, struktur_jenis, prioritas_val, prioritas_nama):
        lbl = ttk.Label(self.content_frame, text=f"{struktur_jenis}: Tambah Pesanan {prioritas_nama}", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Nama Pelanggan:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_pelanggan = ttk.Entry(form_frame, width=30)
        e_pelanggan.grid(row=0, column=1, pady=2)
        e_pelanggan.insert(0, "Pelanggan Baru")

        ttk.Label(form_frame, text="Restoran:").grid(row=1, column=0, sticky=tk.W, pady=2)
        e_resto = ttk.Entry(form_frame, width=30)
        e_resto.grid(row=1, column=1, pady=2)
        e_resto.insert(0, "kafe-teknik")

        ttk.Label(form_frame, text="Menu:").grid(row=2, column=0, sticky=tk.W, pady=2)
        e_menu = ttk.Entry(form_frame, width=30)
        e_menu.grid(row=2, column=1, pady=2)
        e_menu.insert(0, "nasi-goreng")

        ttk.Label(form_frame, text="Harga (Rp):").grid(row=3, column=0, sticky=tk.W, pady=2)
        e_harga = ttk.Entry(form_frame, width=30)
        e_harga.grid(row=3, column=1, pady=2)
        e_harga.insert(0, "15000")

        result_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10, "italic"))
        result_lbl.pack(anchor=tk.W, padx=10, pady=5)

        def do_tambah():
            try:
                pelanggan = e_pelanggan.get()
                resto = e_resto.get()
                menu = e_menu.get()
                harga = int(e_harga.get())
                
                self.next_oid_num += 1
                new_oid = f"0-{self.next_oid_num:06d}"
                
                from backend import m1_pesanan
                p = m1_pesanan.Pesanan(new_oid, pelanggan, resto, menu, harga, prioritas_val, 50000, None, "ANTRE")

                t0 = time.perf_counter()
                
                # SINKRONISASI OTOMATIS: Tambahkan ke ARRAY dan LINKED LIST sekaligus
                if prioritas_val == 1:
                    self.array_pesanan.tambah_vip(p)
                    self.linked_pesanan.tambah_vip(p)
                elif prioritas_val == 2:
                    self.array_pesanan.tambah_prioritas(p)
                    self.linked_pesanan.tambah_prioritas(p)
                else:
                    self.array_pesanan.tambah_reguler(p)
                    self.linked_pesanan.tambah_reguler(p)
                
                self.manajer.enqueue(p)

                target_struktur = self.array_pesanan if struktur_jenis == "Array" else self.linked_pesanan
                self.manajer.catat_order((p, target_struktur, struktur_jenis))
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                result_lbl.config(text=f"Berhasil menambahkan pesanan {p.oid} ({prioritas_nama}) ke M1 (Array & Linked List) & Antrean M2!")
                self.log_command(f"Tambah pesanan {p.oid} ({prioritas_nama}) disinkronkan ke Array, LinkedList, & Queue.", f"M1 & M2", elapsed)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="TAMBAH PESANAN", command=do_tambah).grid(row=4, column=1, sticky=tk.W, pady=10)

    def show_hapus_pesanan(self, struktur_jenis):
        lbl = ttk.Label(self.content_frame, text=f"{struktur_jenis}: Hapus Pesanan berdasarkan Indeks", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Indeks Pesanan (0 s.d. n-1):").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_idx = ttk.Entry(form_frame, width=15)
        e_idx.grid(row=0, column=1, pady=2)
        e_idx.insert(0, "0")

        result_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10))
        result_lbl.pack(anchor=tk.W, padx=10, pady=5)

        def do_hapus():
            try:
                idx = int(e_idx.get())
                t0 = time.perf_counter()
                source = self.array_pesanan if struktur_jenis == "Array" else self.linked_pesanan
                
                pesanan_dihapus = source.get(idx)
                
                # Hapus dari kedua struktur (Array & LinkedList) agar sinkron
                try:
                    for i in range(len(self.array_pesanan)):
                        if self.array_pesanan.get(i).oid == pesanan_dihapus.oid:
                            self.array_pesanan.hapus(i)
                            break
                except:
                    pass

                try:
                    for i in range(len(self.linked_pesanan)):
                        if self.linked_pesanan.get(i).oid == pesanan_dihapus.oid:
                            self.linked_pesanan.hapus(i)
                            break
                except:
                    pass

                self.manajer.catat_hapus_m1((pesanan_dihapus, idx, struktur_jenis, source))
                
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                result_lbl.config(text=f"Berhasil menghapus pesanan {pesanan_dihapus.oid} dari kedua struktur M1.")
                self.log_command(f"Hapus pesanan indeks {idx} di {struktur_jenis}.", f"M1 - {struktur_jenis}", elapsed)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="HAPUS", command=do_hapus).grid(row=1, column=1, sticky=tk.W, pady=10)

    def show_stack_postfix(self):
        lbl = ttk.Label(self.content_frame, text="M2: Stack Postfix (Mesin Kasir)", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=5)

        ttk.Label(form_frame, text="Struk Belanja (Infix):").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_expr = ttk.Entry(form_frame, width=50)
        e_expr.grid(row=0, column=1, pady=2)
        e_expr.insert(0, "(3*12000)+(2*8500)-5000")

        res_text = ttk.Label(self.content_frame, text="", font=("Arial", 11, "bold"))
        res_text.pack(anchor=tk.W, padx=10, pady=5)

        sub_frame = ttk.Frame(self.content_frame)
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("Langkah", "Token", "Tindakan", "Stack", "Output")
        tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=15)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)
        tree.column("Langkah", width=80)
        tree.column("Token", width=60)

        scrollbar = ttk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def hitung_postfix():
            for row in tree.get_children():
                tree.delete(row)
            try:
                expr = e_expr.get()
                t0 = time.perf_counter()
                from backend import m2_antrean
                postfix_str, total, langkah = m2_antrean.proses_kasir(expr)
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                res_text.config(text=f"Postfix: {postfix_str}  |  TOTAL: {m2_antrean.format_rupiah(total)}")
                for (kode, tok, tindakan, stack_val, out_val) in langkah:
                    tree.insert("", tk.END, values=(kode, tok, tindakan, stack_val, out_val))
                self.log_command(f"Evaluasi postfix '{expr}' = {total}", "M2 - stack", elapsed)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="HITUNG", command=hitung_postfix).grid(row=0, column=2, padx=5)

    def show_stack_undo(self):
        lbl = ttk.Label(self.content_frame, text="M2: Stack Undo (Batalkan Aksi Terakhir)", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        info_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 11))
        info_lbl.pack(anchor=tk.W, padx=10, pady=5)

        def do_undo():
            t0 = time.perf_counter()
            sukses, pesan = self.manajer.undo_last()
            t1 = time.perf_counter()
            elapsed = (t1 - t0) * 1000

            stats = dict(self.manajer.stats())
            info_lbl.config(text=f"{pesan}\nPanjang antrean: naif {stats['queue_len_naif']}, circular {stats['queue_len_circular']}. Undo tersisa: {stats['undo_depth']}, redo: {stats['redo_depth']}")
            self.log_command(pesan, "M2 - stack", elapsed)

        ttk.Button(self.content_frame, text="UNDO", command=do_undo).pack(anchor=tk.W, padx=10, pady=10)

    def show_stack_redo(self):
        lbl = ttk.Label(self.content_frame, text="M2: Stack Redo (Kerjakan Ulang Aksi)", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        info_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 11))
        info_lbl.pack(anchor=tk.W, padx=10, pady=5)

        def do_redo():
            t0 = time.perf_counter()
            sukses, pesan = self.manajer.redo_last()
            t1 = time.perf_counter()
            elapsed = (t1 - t0) * 1000

            stats = dict(self.manajer.stats())
            info_lbl.config(text=f"{pesan}\nPanjang antrean: naif {stats['queue_len_naif']}, circular {stats['queue_len_circular']}. Undo: {stats['undo_depth']}, redo: {stats['redo_depth']}")
            self.log_command(pesan, "M2 - stack", elapsed)

        ttk.Button(self.content_frame, text="REDO", command=do_redo).pack(anchor=tk.W, padx=10, pady=10)

    def show_queue_enqueue(self):
        lbl = ttk.Label(self.content_frame, text="M2: Queue Enqueue (Tambah Pesanan ke Belakang Antrean & M1)", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Nama Pelanggan:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_pel = ttk.Entry(form_frame, width=30)
        e_pel.grid(row=0, column=1, pady=2)
        e_pel.insert(0, "X2")

        res_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10))
        res_lbl.pack(anchor=tk.W, padx=10, pady=5)

        def do_enqueue():
            try:
                from backend import m1_pesanan
                self.next_oid_num += 1
                oid_unik = f"0-{self.next_oid_num:06d}"
                p = m1_pesanan.Pesanan(oid_unik, e_pel.get(), "kafe-teknik", "roti-bakar", 12000, 3, 28800, None, "ANTRE")
                
                t0 = time.perf_counter()
                self.array_pesanan.tambah_reguler(p)
                self.linked_pesanan.tambah_reguler(p)
                self.manajer.enqueue(p)
                
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                stats = dict(self.manajer.stats())
                res_lbl.config(text=f"{p.oid} masuk ke antrean M2 & tersinkronisasi ke M1.\nPanjang sekarang: naif {stats['queue_len_naif']}, circular {stats['queue_len_circular']}.")
                self.log_command(f"Queue enqueue {p.oid} terintegrasi M1 & M2", "M1 & M2", elapsed)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="ENQUEUE", command=do_enqueue).grid(row=1, column=1, sticky=tk.W, pady=10)

    def show_queue_dequeue(self, versi):
        lbl = ttk.Label(self.content_frame, text=f"M2: Queue Dequeue ({versi.upper()})", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Berapa kali dequeue:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_n = ttk.Entry(form_frame, width=15)
        e_n.grid(row=0, column=1, pady=2)
        e_n.insert(0, "1")

        res_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10))
        res_lbl.pack(anchor=tk.W, padx=10, pady=5)

        sub_frame = ttk.Frame(self.content_frame)
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("No", "OID", "Pelanggan", "Resto", "Menu", "Status")
        tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.W)

        scrollbar = ttk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def do_dequeue():
            for row in tree.get_children():
                tree.delete(row)
            try:
                n = int(e_n.get())
                t0 = time.perf_counter()
                keluar, geseran = self.manajer.dequeue(n, versi)
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                stats = dict(self.manajer.stats())
                if versi == "naif":
                    res_lbl.config(text=f"{len(keluar)} pesanan keluar dari antrean naif & status M1 jadi DONE. Total geseran: {geseran:,}.")
                    self.log_command(f"Queue dequeue naif ({n} pesanan, {geseran} geseran)", "M2 - queue naif", elapsed)
                else:
                    res_lbl.config(text=f"{len(keluar)} pesanan keluar dari circular queue & status M1 jadi DONE.")
                    self.log_command(f"Queue dequeue circular ({n} pesanan)", "M2 - queue circular", elapsed)

                for i, p in enumerate(keluar):
                    tree.insert("", tk.END, values=(i+1, p.oid, p.pelanggan, p.resto, p.menu, p.status))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="DEQUEUE", command=do_dequeue).grid(row=1, column=1, sticky=tk.W, pady=10)

    def show_sort(self, jenis):
        nama_sort = "Insertion Sort (O(n^2))" if jenis == "insertion" else "Merge Sort (O(n log n))"
        lbl = ttk.Label(self.content_frame, text=f"M3: Sort - {nama_sort}", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Jumlah baris diurutkan:").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_n = ttk.Entry(form_frame, width=15)
        e_n.grid(row=0, column=1, pady=2)
        e_n.insert(0, "1000")

        ttk.Label(form_frame, text="Diurutkan menurut:").grid(row=1, column=0, sticky=tk.W, pady=2)
        combo_kunci = ttk.Combobox(form_frame, values=["harga", "oid", "selesai"], width=15, state="readonly")
        combo_kunci.grid(row=1, column=1, pady=2)
        combo_kunci.set("harga")

        res_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10, "bold"))
        res_lbl.pack(anchor=tk.W, padx=10, pady=5)

        sub_frame = ttk.Frame(self.content_frame)
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("No", "OID", "Harga", "Selesai", "Resto", "Menu")
        tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=15)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor=tk.W)

        scrollbar = ttk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def do_sort():
            for row in tree.get_children():
                tree.delete(row)
            try:
                n = int(e_n.get())
                kunci = combo_kunci.get()
                
                data_copy = []
                limit = min(n, len(self.array_pesanan))
                for i in range(limit):
                    data_copy.append(self.array_pesanan.get(i))

                t0 = time.perf_counter()
                from backend import m3_Sort_search
                if jenis == "insertion":
                    sorted_data, comps, moves = m3_Sort_search.insertion_sort(data_copy, kunci)
                else:
                    sorted_data, comps, moves = m3_Sort_search.merge_sort(data_copy, kunci)
                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                res_lbl.config(text=f"{len(sorted_data)} pesanan diurutkan menurut {kunci}.\n{comps:,} perbandingan, {moves:,} pemindahan.")
                self.log_command(f"{nama_sort} ({n} baris, kunci {kunci}): {comps:,} perbandingan", f"M3 - {jenis}", elapsed)

                max_show = min(100, len(sorted_data))
                for i in range(max_show):
                    p = sorted_data[i]
                    selesai_str = str(p.t_selesai_detik) if p.t_selesai_detik else "-"
                    tree.insert("", tk.END, values=(i+1, p.oid, f"Rp {p.harga:,}", selesai_str, p.resto, p.menu))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="URUTKAN", command=do_sort).grid(row=2, column=1, sticky=tk.W, pady=10)

    def show_search(self, jenis):
        nama_search = "Linear Search (O(n))" if jenis == "linear" else "Binary Search (O(log n))"
        lbl = ttk.Label(self.content_frame, text=f"M3: Search - {nama_search}", font=("Arial", 12, "bold"))
        lbl.pack(anchor=tk.W, padx=10, pady=5)

        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(anchor=tk.W, padx=10, pady=10)

        ttk.Label(form_frame, text="Nomor Pesanan (OID):").grid(row=0, column=0, sticky=tk.W, pady=2)
        e_oid = ttk.Entry(form_frame, width=25)
        e_oid.grid(row=0, column=1, pady=2)
        e_oid.insert(0, "O-137442")

        res_lbl = ttk.Label(self.content_frame, text="", font=("Arial", 10, "bold"))
        res_lbl.pack(anchor=tk.W, padx=10, pady=5)

        sub_frame = ttk.Frame(self.content_frame)
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("Kolom", "Isi")
        tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=10)
        tree.heading("Kolom", text="Kolom")
        tree.heading("Isi", text="Isi")
        tree.column("Kolom", width=120, anchor=tk.W)
        tree.column("Isi", width=300, anchor=tk.W)

        scrollbar = ttk.Scrollbar(sub_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def do_search():
            for row in tree.get_children():
                tree.delete(row)
            try:
                target = e_oid.get().strip()
                t0 = time.perf_counter()
                from backend import m3_Sort_search
                
                data_list = []
                for i in range(len(self.array_pesanan)):
                    data_list.append(self.array_pesanan.get(i))

                pre_msg = ""
                if jenis == "linear":
                    idx, comps = m3_Sort_search.linear_search(data_list, target, "oid")
                else:
                    t_sort0 = time.perf_counter()
                    m3_Sort_search.merge_sort(data_list, "oid")
                    t_sort1 = time.perf_counter()
                    sort_time = (t_sort1 - t_sort0) * 1000
                    pre_msg = f"Daftar terurut oid dibangun dengan merge sort ({sort_time:.2f} ms). "
                    
                    idx, comps = m3_Sort_search.binary_search(data_list, target, "oid")

                t1 = time.perf_counter()
                elapsed = (t1 - t0) * 1000

                if idx != -1:
                    p = data_list[idx]
                    res_lbl.config(text=f"{pre_msg}Ditemukan pada indeks {idx:,} ({comps:,} perbandingan).")
                    self.log_command(f"{nama_search} target '{target}' ketemu ({comps:,} perbandingan)", f"M3 - {jenis}", elapsed)
                    
                    tree.insert("", tk.END, values=("oid", p.oid))
                    tree.insert("", tk.END, values=("pelanggan", p.pelanggan))
                    tree.insert("", tk.END, values=("resto", p.resto))
                    tree.insert("", tk.END, values=("menu", p.menu))
                    tree.insert("", tk.END, values=("harga", f"Rp {p.harga:,}"))
                    tree.insert("", tk.END, values=("prioritas", p.prioritas))
                    tree.insert("", tk.END, values=("masuk_detik", p.t_masuk_detik))
                    tree.insert("", tk.END, values=("status", p.status))
                else:
                    res_lbl.config(text=f"{pre_msg}Pesanan dengan OID '{target}' tidak ditemukan ({comps:,} perbandingan).")
                    self.log_command(f"{nama_search} target '{target}' tidak ditemukan", f"M3 - {jenis}", elapsed)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(form_frame, text="CARI", command=do_search).grid(row=1, column=1, sticky=tk.W, pady=10)
