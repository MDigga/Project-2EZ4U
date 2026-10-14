def _ambil_nilai(item, kunci):
    if kunci == "selesai" or kunci == "t_selesai_detik":
        return item.t_selesai_detik if item.t_selesai_detik is not None else 0
    if hasattr(item, kunci):
        return getattr(item, kunci)
    return item


def insertion_sort(larik, kunci="harga"):
    n = len(larik)
    if n > 20000:
        raise ValueError("DITOLAK: Batas Insertion Sort adalah 20.000 baris. Gunakan Merge Sort untuk data penuh.")

    comparisons = 0
    moves = 0

    for i in range(1, n):
        key_item = larik[i]
        key_val = _ambil_nilai(key_item, kunci)
        j = i - 1
        
        while j >= 0:
            comparisons += 1
            curr_val = _ambil_nilai(larik[j], kunci)
            if curr_val > key_val:
                larik[j + 1] = larik[j]
                moves += 1
                j -= 1
            else:
                break
        
        larik[j + 1] = key_item
        moves += 1

    return larik, comparisons, moves


def merge_sort(larik, kunci="harga"):
    comparisons = [0]
    moves = [0]

    def _merge_sort_rec(sub):
        if len(sub) <= 1:
            return sub
        mid = len(sub) // 2
        kiri = _merge_sort_rec(sub[:mid])
        kanan = _merge_sort_rec(sub[mid:])
        return _merge(kiri, kanan)

    def _merge(kiri, kanan):
        hasil = []
        i = 0
        j = 0
        while i < len(kiri) and j < len(kanan):
            comparisons[0] += 1
            val_i = _ambil_nilai(kiri[i], kunci)
            val_j = _ambil_nilai(kanan[j], kunci)
            
            if val_i <= val_j:
                hasil.append(kiri[i])
                i += 1
            else:
                hasil.append(kanan[j])
                j += 1
            moves[0] += 1

        while i < len(kiri):
            hasil.append(kiri[i])
            i += 1
            moves[0] += 1

        while j < len(kanan):
            hasil.append(kanan[j])
            j += 1
            moves[0] += 1

        return hasil

    pos_sorted = _merge_sort_rec(larik)
    for idx in range(len(larik)):
        larik[idx] = pos_sorted[idx]

    return larik, comparisons[0], moves[0]


def linear_search(larik, target, kunci="oid"):
    comparisons = 0
    for i in range(len(larik)):
        comparisons += 1
        val = _ambil_nilai(larik[i], kunci)
        if val == target:
            return i, comparisons
    return -1, comparisons


def binary_search(larik, target, kunci="oid"):
    comparisons = 0
    lo = 0
    hi = len(larik) - 1

    while lo <= hi:
        comparisons += 1
        mid = (lo + hi) // 2
        val_mid = _ambil_nilai(larik[mid], kunci)

        if val_mid == target:
            return mid, comparisons
        elif val_mid < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1, comparisons