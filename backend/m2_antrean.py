def _tumbuh_larik(lama):
    kapasitas_baru = len(lama) * 2 if len(lama) > 0 else 8
    baru = [None] * kapasitas_baru
    for i in range(len(lama)):
        baru[i] = lama[i]
    return baru


def format_rupiah(angka):
    if isinstance(angka, float) and angka == int(angka):
        angka = int(angka)
    negatif = angka < 0
    teks = str(abs(angka))
    bagian_desimal = ""
    titik = -1
    for i in range(len(teks)):
        if teks[i] == ".":
            titik = i
    if titik != -1:
        bagian_desimal = teks[titik:]
        teks = teks[:titik]
    hasil = ""
    hitung = 0
    for i in range(len(teks) - 1, -1, -1):
        if hitung == 3:
            hasil = "." + hasil
            hitung = 0
        hasil = teks[i] + hasil
        hitung += 1
    return ("-" if negatif else "") + "Rp " + hasil + bagian_desimal

class Tumpukan:
    def __init__(self, capacity=8):
        self.data = [None] * capacity
        self.count = 0

    def push(self, x):
        if self.count == len(self.data):
            self.data = _tumbuh_larik(self.data)
        self.data[self.count] = x
        self.count += 1

    def pop(self):
        if self.count == 0:
            raise IndexError("Tumpukan kosong")
        self.count -= 1
        x = self.data[self.count]
        self.data[self.count] = None
        return x

    def peek(self):
        if self.count == 0:
            raise IndexError("Tumpukan kosong")
        return self.data[self.count - 1]

    def kosong(self):
        return self.count == 0

    def kosongkan(self):
        for i in range(self.count):
            self.data[i] = None
        self.count = 0

    def ke_list(self):
        """Salinan isi dari dasar ke puncak (untuk ditampilkan)."""
        hasil = [None] * self.count
        for i in range(self.count):
            hasil[i] = self.data[i]
        return hasil

    def __len__(self):
        return self.count

def _adalah_operator(t):
    return len(t) == 1 and t in "+-*/"


def _adalah_kurung(t):
    return t == "(" or t == ")"


def _prioritas_op(op):
    if op == "*" or op == "/":
        return 2
    return 1  # + dan -


def tokenisasi(ekspresi):
    tokens = []
    i = 0
    n = len(ekspresi)
    while i < n:
        c = ekspresi[i]
        if c == " " or c == "\t":
            i += 1
            continue
        if c in "()*/+":
            tokens.append(c)
            i += 1
            continue

        negatif = False
        if c == "-":
            sebelumnya_pembuka = (
                len(tokens) == 0 or tokens[-1] == "(" or _adalah_operator(tokens[-1])
            )
            ada_angka_setelahnya = i + 1 < n and (
                ekspresi[i + 1].isdigit() or ekspresi[i + 1] == "."
            )
            negatif = sebelumnya_pembuka and ada_angka_setelahnya
            if not negatif:
                tokens.append("-")
                i += 1
                continue

        if c.isdigit() or c == "." or negatif:
            j = i + 1
            while j < n and (ekspresi[j].isdigit() or ekspresi[j] == "."):
                j += 1
            tokens.append(ekspresi[i:j])
            i = j
            continue

        raise ValueError("Karakter tidak dikenal: '" + c + "'")
    return tokens


def _parse_angka(tok):
    try:
        if "." in tok:
            return float(tok)
        return int(tok)
    except ValueError:
        raise ValueError("Angka tidak valid: '" + tok + "'")


def _fmt_angka(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return str(x)


def _str_isi(items):
    if len(items) == 0:
        return "kosong"
    return " ".join(items)


def ke_postfix(ekspresi):
    tokens = tokenisasi(ekspresi)
    if len(tokens) == 0:
        raise ValueError("Ekspresi kosong")

    stack = Tumpukan()
    keluaran = []
    langkah = []
    nomor = [0]  

    def catat(token, tindakan):
        nomor[0] += 1
        langkah.append(
            ("1." + str(nomor[0]), token, tindakan,
             _str_isi(stack.ke_list()), _str_isi(keluaran))
        )

    for tok in tokens:
        if tok == "(":
            stack.push(tok)
            catat(tok, "push ( ke stack")
        elif tok == ")":
            while not stack.kosong() and stack.peek() != "(":
                keluaran.append(stack.pop())
            if stack.kosong():
                raise ValueError("Kurung tutup tanpa pasangan")
            stack.pop()  
            catat(tok, "pop sampai ( : *, lalu buang (")
        elif _adalah_operator(tok):
            dikeluarkan = []
            while (not stack.kosong() and stack.peek() != "("
                   and _prioritas_op(stack.peek()) >= _prioritas_op(tok)):
                op_atas = stack.pop()
                keluaran.append(op_atas)
                dikeluarkan.append(op_atas)
            stack.push(tok)
            if len(dikeluarkan) > 0:
                catat(tok, "pop " + " ".join(dikeluarkan)
                      + " (lebih/sama kuat), push " + tok)
            else:
                catat(tok, "push " + tok)
        else:
            _parse_angka(tok) 
            keluaran.append(tok)
            catat(tok, "operand, langsung ke output")

    sisa = []
    while not stack.kosong():
        atas = stack.pop()
        if atas == "(":
            raise ValueError("Kurung buka tanpa pasangan")
        keluaran.append(atas)
        sisa.append(atas)
    nomor[0] = 0
    langkah.append(("1.akhir", "-", "pop sisa stack: " + _str_isi(sisa),
                    "kosong", _str_isi(keluaran)))
    return keluaran, langkah


def hitung(postfix):
    if isinstance(postfix, str):
        postfix = tokenisasi_postfix(postfix)

    stack = Tumpukan()
    langkah = []
    nomor = 0
    for tok in postfix:
        nomor += 1
        kode = "2." + str(nomor)
        if _adalah_operator(tok):
            if len(stack) < 2:
                raise ValueError("Ekspresi tidak valid: operand kurang untuk '" + tok + "'")
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                r = a + b
            elif tok == "-":
                r = a - b
            elif tok == "*":
                r = a * b
            else:
                if b == 0:
                    raise ValueError("Pembagian dengan nol")
                if isinstance(a, int) and isinstance(b, int) and a % b == 0:
                    r = a // b
                else:
                    r = a / b
            stack.push(r)
            tindakan = ("pop " + _fmt_angka(b) + " dan " + _fmt_angka(a) + " -> "
                        + _fmt_angka(a) + tok + _fmt_angka(b) + " = " + _fmt_angka(r))
        else:
            stack.push(_parse_angka(tok))
            tindakan = "operand, push " + tok
        isi = stack.ke_list()
        teks = [None] * len(isi)
        for i in range(len(isi)):
            teks[i] = _fmt_angka(isi[i])
        langkah.append((kode, tok, tindakan, _str_isi(teks)))

    if len(stack) != 1:
        raise ValueError("Ekspresi tidak valid: sisa operand di stack")
    total = stack.pop()
    if isinstance(total, float) and total == int(total):
        total = int(total)
    return total, langkah


def tokenisasi_postfix(teks):
    tokens = []
    i = 0
    n = len(teks)
    while i < n:
        if teks[i] == " ":
            i += 1
            continue
        j = i
        while j < n and teks[j] != " ":
            j += 1
        tokens.append(teks[i:j])
        i = j
    return tokens


def proses_kasir(ekspresi):
    postfix, langkah1 = ke_postfix(ekspresi)
    total, langkah2 = hitung(postfix)
    gabungan = list(langkah1)
    for (kode, tok, tindakan, isi) in langkah2:
        gabungan.append((kode, tok, tindakan, isi, ""))
    return " ".join(postfix), total, gabungan


class AntreanNaif:
    def __init__(self, capacity=8):
        self.data = [None] * capacity
        self.count = 0
        self.total_geseran = 0

    def enqueue(self, x):
        if self.count == len(self.data):
            self.data = _tumbuh_larik(self.data)
        self.data[self.count] = x
        self.count += 1

    def dequeue(self):
        """Ambil indeks 0, lalu geser SEMUA sisa satu langkah ke kiri -> O(n)."""
        if self.count == 0:
            return None
        x = self.data[0]
        for i in range(1, self.count):
            self.data[i - 1] = self.data[i]
        self.total_geseran += self.count - 1
        self.data[self.count - 1] = None
        self.count -= 1
        return x

    def is_empty(self):
        return self.count == 0

    def hapus_belakang(self):
        if self.count == 0:
            return None
        x = self.data[self.count - 1]
        self.data[self.count - 1] = None
        self.count -= 1
        return x

    def tambah_depan_banyak(self, items):
        n = len(items)
        while self.count + n > len(self.data):
            self.data = _tumbuh_larik(self.data)
        for i in range(self.count - 1, -1, -1):
            self.data[i + n] = self.data[i]
        for j in range(n):
            self.data[j] = items[j]
        self.count += n

    def ke_list(self):
        hasil = [None] * self.count
        for i in range(self.count):
            hasil[i] = self.data[i]
        return hasil

    def capacity(self):
        return len(self.data)

    def __len__(self):
        return self.count


class AntreanMelingkar:
    def __init__(self, K=8):
        self.K = K
        self.data = [None] * K
        self.front = 0
        self.rear = 0      
        self.count = 0

    def _tumbuh(self):
        """Penuh -> kapasitas 2x; isi disalin berurutan dari front, front kembali 0."""
        K_baru = self.K * 2 if self.K > 0 else 8
        baru = [None] * K_baru
        for i in range(self.count):
            baru[i] = self.data[(self.front + i) % self.K]
        self.data = baru
        self.K = K_baru
        self.front = 0
        self.rear = self.count

    def enqueue(self, x):
        if self.count == self.K:
            self._tumbuh()
        self.data[self.rear] = x
        self.rear = (self.rear + 1) % self.K
        self.count += 1

    def dequeue(self):
        """Hanya front yang maju. Tidak ada elemen yang digeser -> O(1)."""
        if self.count == 0:
            return None
        x = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.K
        self.count -= 1
        return x

    def is_empty(self):
        return self.count == 0 

    def is_full(self):
        return self.count == self.K

    def hapus_belakang(self):
        if self.count == 0:
            return None
        self.rear = (self.rear - 1) % self.K
        x = self.data[self.rear]
        self.data[self.rear] = None
        self.count -= 1
        return x

    def tambah_depan_banyak(self, items):
        """Kembalikan `items` ke DEPAN antrean (bukan ke belakang!)."""
        n = len(items)
        while self.count + n > self.K:
            self._tumbuh()
        for j in range(n - 1, -1, -1):  
            self.front = (self.front - 1) % self.K
            self.data[self.front] = items[j]
            self.count += 1

    def ke_list(self):
        hasil = [None] * self.count
        for i in range(self.count):
            hasil[i] = self.data[(self.front + i) % self.K]
        return hasil

    def capacity(self):
        return self.K

    def __len__(self):
        return self.count


def _oid_dari(p):
    return p.oid


def _deskripsi_aksi(aksi):
    jenis, data, versi = aksi
    if jenis == "ORDER":
        return "ORDER " + data.oid
    if jenis == "ENQUEUE":
        return "ENQUEUE " + data.oid
    return "DEQUEUE x" + str(len(data)) + " (" + versi + ")"


class ManajerAntrean:

    def __init__(self, capacity=32768):
        self.naif = AntreanNaif(capacity)
        self.melingkar = AntreanMelingkar(capacity)
        self.undo_stack = Tumpukan()
        self.redo_stack = Tumpukan()

    def muat_dari_array(self, array_pesanan):
        jumlah = 0
        for i in range(len(array_pesanan)):
            p = array_pesanan.get(i)
            if p.status == "ANTRE":
                self.naif.enqueue(p)
                self.melingkar.enqueue(p)
                jumlah += 1
        return jumlah

    def _aksi_baru(self, aksi):
        self.undo_stack.push(aksi)
        self.redo_stack.kosongkan()    

    def enqueue(self, pesanan):
        self.naif.enqueue(pesanan)
        self.melingkar.enqueue(pesanan)
        self._aksi_baru(("ENQUEUE", pesanan, None))

    def _antrean(self, versi):
        if versi == "naif":
            return self.naif
        if versi == "circular":
            return self.melingkar
        raise ValueError("versi harus 'naif' atau 'circular'")

    def dequeue(self, n=1, versi="circular"):
        q = self._antrean(versi)
        geseran_awal = self.naif.total_geseran
        keluar = []
        for _ in range(n):
            x = q.dequeue()
            if x is None:
                break
            keluar.append(x)
        geseran = self.naif.total_geseran - geseran_awal if versi == "naif" else 0
        if len(keluar) > 0:
            self._aksi_baru(("DEQUEUE", keluar, versi))  
        return keluar, geseran

    def catat_order(self, pesanan):
        self._aksi_baru(("ORDER", pesanan, None))

    def undo_last(self):
        if self.undo_stack.kosong():
            return False, "Tidak ada aksi yang bisa dibatalkan."
        aksi = self.undo_stack.pop()
        jenis, data, versi = aksi
        if jenis == "ENQUEUE":
            self.naif.hapus_belakang()
            self.melingkar.hapus_belakang()
            pesan = "Pembatalan enqueue: " + data.oid + " dikeluarkan lagi dari belakang."
        elif jenis == "DEQUEUE":
            self._antrean(versi).tambah_depan_banyak(data)
            pesan = (str(len(data)) + " pesanan dikembalikan ke DEPAN antrean "
                     + versi + ".")
        else:
            data.status = "CANCEL"
            pesan = "Pesanan " + data.oid + " ditandai CANCEL."
        self.redo_stack.push(aksi)
        return True, pesan

    def redo_last(self):
        if self.redo_stack.kosong():
            return False, "Tumpukan redo kosong, tidak ada yang diulang."
        aksi = self.redo_stack.pop()
        jenis, data, versi = aksi
        if jenis == "ENQUEUE":
            self.naif.enqueue(data)
            self.melingkar.enqueue(data)
            pesan = "Enqueue dikerjakan lagi: " + data.oid + " masuk kembali ke belakang."
        elif jenis == "DEQUEUE":
            q = self._antrean(versi)
            for _ in range(len(data)):
                q.dequeue()
            pesan = (str(len(data)) + " pesanan keluar lagi dari antrean "
                     + versi + ".")
        else:  
            data.status = "ANTRE"
            pesan = "Pesanan " + data.oid + " kembali berstatus ANTRE."
        self.undo_stack.push(aksi)
        return True, pesan

    def history(self):
        """Daftar aksi dari yang terlama sampai yang terbaru (konsisten dengan undo)."""
        isi = self.undo_stack.ke_list()
        hasil = [None] * len(isi)
        for i in range(len(isi)):
            hasil[i] = _deskripsi_aksi(isi[i])
        return hasil

    def stats(self):
        return [
            ("queue_len_naif", len(self.naif)),
            ("queue_len_circular", len(self.melingkar)),
            ("queue_capacity_naif", self.naif.capacity()),
            ("queue_capacity_circular", self.melingkar.capacity()),
            ("total_geseran", self.naif.total_geseran),
            ("undo_depth", len(self.undo_stack)),
            ("redo_depth", len(self.redo_stack)),
        ]
