from re import search
import time
from backend import m1_pesanan
from backend import m2_antrean
from backend import m3_Sort_search
from Frontend.ui import MainAppWindow

if __name__ == "__main__":
    print("Memuat data pesanan dari CSV...")
    array_pesanan, linked_pesanan = m1_pesanan.muat_data_pesanan("data/pesanan.csv")
    manajer = m2_antrean.ManajerAntrean()
    manajer.muat_dari_array(array_pesanan)
    print("Data berhasil dimuat. Membuka antarmuka aplikasi...")

    app = MainAppWindow(array_pesanan, linked_pesanan, manajer)
    app.mainloop()
