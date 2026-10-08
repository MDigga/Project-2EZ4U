import csv

class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk_detik, t_selesai_detik=None, status="ANTRE"):
        self.oid = str(oid)
        self.pelanggan = str(pelanggan)
        self.resto = str(resto)
        self.menu = str(menu)
        self.harga = int(harga) if harga not in (None, "") else 0
        self.prioritas = int(prioritas) if prioritas not in (None, "") else 3
        self.t_masuk_detik = int(t_masuk_detik) if t_masuk_detik not in (None, "") else 0
        self.t_selesai_detik = int(t_selesai_detik) if t_selesai_detik not in (None, "") else None
        self.status = str(status) if status else "ANTRE"

    def __repr__(self):
        return f"<Pesanan {self.oid} | {self.pelanggan} | {self.menu} | Rp{self.harga:,} | Status: {self.status}>"

class Array:
    def __init__(self, capacity=200005):
        self.capacity = capacity
        self.count = 0
        self.data = [None] * self.capacity

    def get(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Indeks di luar jangkauan")
        return self.data[index]

    def tambah_reguler(self, pesanan):
        if self.count >= self.capacity:
            raise OverflowError("Array penuh! Kapasitas maksimum tercapai.")
        self.data[self.count] = pesanan
        self.count += 1

    def tambah_vip(self, pesanan):
        if self.count >= self.capacity:
            raise OverflowError("Array penuh! Kapasitas maksimum tercapai.")
        for i in range(self.count, 0, -1):
            self.data[i] = self.data[i - 1]
        self.data[0] = pesanan
        self.count += 1

    def tambah_prioritas(self, pesanan):
        if self.count >= self.capacity:
            raise OverflowError("Array penuh! Kapasitas maksimum tercapai.")
        target_idx = self.count // 2
        for i in range(self.count, target_idx, -1):
            self.data[i] = self.data[i - 1]
        self.data[target_idx] = pesanan
        self.count += 1

    def hapus(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Indeks di luar jangkauan")
        pesanan_dihapus = self.data[index]
        for i in range(index, self.count - 1):
            self.data[i] = self.data[i + 1]
        self.data[self.count - 1] = None
        self.count -= 1
        return pesanan_dihapus

    def __len__(self):
        return self.count

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def get(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Indeks di luar jangkauan")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def tambah_reguler(self, pesanan):
        new_node = Node(pesanan)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.count += 1

    def tambah_vip(self, pesanan):
        new_node = Node(pesanan)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.count += 1

    def tambah_prioritas(self, pesanan):
        if self.head is None or self.count == 0:
            self.tambah_reguler(pesanan)
            return

        target_idx = self.count // 2
        if target_idx == 0:
            self.tambah_vip(pesanan)
            return

        new_node = Node(pesanan)
        current = self.head
        for _ in range(target_idx - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.count += 1

    def hapus(self, index):
        if index < 0 or index >= self.count:
            raise IndexError("Indeks di luar jangkauan")

        if index == 0:
            pesanan_dihapus = self.head.data
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.count -= 1
            return pesanan_dihapus

        current = self.head
        for _ in range(index - 1):
            current = current.next

        pesanan_dihapus = current.next.data
        if current.next == self.tail:
            self.tail = current
        current.next = current.next.next
        self.count -= 1
        return pesanan_dihapus

    def __len__(self):
        return self.count

def muat_data_pesanan(filepath="data/pesanan.csv", capacity=200005):
    array_pesanan = Array(capacity=capacity)
    linked_pesanan = LinkedList()

    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            pesanan = Pesanan(
                oid=row[0],
                pelanggan=row[1],
                resto=row[2],
                menu=row[3],
                harga=row[4],
                prioritas=row[5],
                t_masuk_detik=row[6],
                t_selesai_detik=row[7] if len(row) > 7 and row[7] else None,
                status=row[8] if len(row) > 8 else "ANTRE"
            )
            array_pesanan.tambah_reguler(pesanan)
            linked_pesanan.tambah_reguler(pesanan)

    return array_pesanan, linked_pesanan