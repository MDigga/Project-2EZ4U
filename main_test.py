from backend.m1_pesanan import Array, Pesanan

def test_fixed_array_capacity():
    arr = Array(capacity=2)
    p1 = Pesanan("1", "Budi", "Resto A", "Nasi Goreng", 20000, 3, 100)
    p2 = Pesanan("2", "Siti", "Resto B", "Mie Goreng", 15000, 3, 105)
    p3 = Pesanan("3", "Andi", "Resto C", "Ayam Goreng", 25000, 3, 110)

    arr.tambah_reguler(p1)
    arr.tambah_reguler(p2)

    try:
        arr.tambah_reguler(p3)
        print("TEST GAGAL: Array tidak membatasi kapasitas.")
    except OverflowError:
        print("TEST BERHASIL: Fixed Array berhasil menolak data saat penuh.")

if __name__ == "__main__":
    test_fixed_array_capacity()