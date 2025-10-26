# Weighted Interval Scheduling

## Deskripsi Proyek

Implementasi pemilihan jadwal kelas pada satu ruang untuk memaksimalkan total jumlah (unweighted) atau total bobot (weighted) interval.

**Dua metode yang dibandingkan:**

1. **Baseline (Unweighted)** — Greedy berdasarkan earliest finish time (activity selection)
2. **Optimized (Weighted)** — Weighted Interval Scheduling menggunakan Dynamic Programming + binary search untuk fungsi `p(j)`

## Struktur Direktori
```
interval_scheduling/
├── simple_schedule.py           # Skrip utama
├── data/
│   └── my_intervals.csv         # Dataset contoh (input)
└── results/
    ├── greedy_selected.csv      # Hasil pilihan Greedy
    └── dp_selected.csv           # Hasil pilihan DP berbobot
```

## Instalasi dan Setup

### Prasyarat
- Python 3.x

### Persiapan Dataset

Simpan dataset CSV di folder `data/` (contoh: `my_intervals.csv`).

**Kolom yang diperlukan:**
- **Waktu mulai & selesai**: `start`, `end`, `stime`, `etime`, `start_time`, atau `end_time`
- **Bobot (opsional)**: `weight` (untuk weighted interval scheduling)

## Format CSV

### Format Minimal (Unweighted)
```csv
start,end
08:00,09:00
09:00,10:30
10:00,11:00
```

### Format dengan Bobot (Weighted)
```csv
start,end,weight
08:00,09:00,1.0
09:00,10:30,2.5
10:00,11:00,3.0
```

**Catatan:** Program akan otomatis mendeteksi dan mengonversi format waktu (string tanggal/waktu).

## Cara Menjalankan

### Opsi 1: Dengan Argumen
```bash
python simple_schedule.py data/my_intervals.csv
```

### Opsi 2: Tanpa Argumen (Interactive)
```bash
python simple_schedule.py
```

Program akan meminta input path file CSV.

## Output yang Dihasilkan

### Terminal
- **Hasil Greedy**: Daftar interval terpilih + jumlah total
- **Hasil DP**: Daftar interval terpilih + total bobot optimal
- **Perbandingan**: 
  - Perbandingan total bobot (jika bobot tidak semuanya 1)
  - Notifikasi kontradiksi jika DP > Greedy (menunjukkan Greedy tidak optimal untuk kasus berbobot)

### File CSV
- `results/greedy_selected.csv` — Interval yang dipilih oleh algoritma Greedy
- `results/dp_selected.csv` — Interval yang dipilih oleh algoritma DP

## Ringkasan Algoritma

### 1. Greedy (Earliest-Finish)

**Cara kerja:**
- Pilih interval dengan waktu selesai terkecil yang tidak bertabrakan
- Optimal untuk memaksimalkan **jumlah interval** saat semua bobot sama

**Kompleksitas:**
- Sorting: O(n log n)
- Selection: O(n)
- **Total: O(n log n)**

**Kapan digunakan:**
- Semua bobot = 1 (tujuan: maksimalkan jumlah)
- Dataset besar (cepat dan efisien)

### 2. Weighted Interval Scheduling (DP + Binary Search)

**Cara kerja:**
1. Urutkan interval berdasarkan waktu selesai
2. Hitung `p(j)` = indeks interval terakhir yang tidak bertabrakan dengan `j` menggunakan binary search
3. DP rekursif: `OPT(j) = max(weight[j] + OPT(p(j)), OPT(j-1))`
4. Memberikan solusi optimal untuk total bobot maksimum

**Kompleksitas:**
- Sorting: O(n log n)
- Komputasi `p(j)`: O(n log n) (binary search untuk setiap interval)
- DP: O(n)
- **Total: O(n log n)**

**Kapan digunakan:**
- Interval memiliki bobot/keuntungan berbeda
- Membutuhkan hasil optimal (bukan hanya heuristik)
- Bersedia membayar biaya komputasi lebih untuk akurasi

## Perbandingan Metode

| Aspek | Greedy | Weighted DP |
|-------|--------|-------------|
| **Optimal untuk** | Unweighted (jumlah max) | Weighted (bobot max) |
| **Kompleksitas** | O(n log n) | O(n log n) |
| **Kecepatan** | Sangat cepat | Sedikit lebih lambat |
| **Akurasi** | Optimal jika bobot = 1 | Selalu optimal |

## Catatan Debugging

### Kontradiksi DP > Greedy
Jika program menampilkan **DP total weight > Greedy total weight**, ini adalah bukti bahwa:
- Greedy **tidak optimal** untuk kasus berbobot
- DP memberikan solusi yang lebih baik untuk memaksimalkan total bobot

### Verifikasi Hasil
- Periksa file CSV di folder `results/` untuk analisis lebih lanjut
- Pastikan tidak ada interval yang bertabrakan dalam hasil yang dipilih

## Contoh Kasus

### Input (Weighted)
```csv
start,end,weight
08:00,10:00,5
09:00,11:00,6
10:00,12:00,5
11:00,13:00,3
```

### Hasil
- **Greedy** (earliest finish): Mungkin memilih `[08:00-10:00, 10:00-12:00, 11:00-13:00]` → Total weight = 13
- **DP** (optimal): Memilih `[09:00-11:00, 11:00-13:00]` → Total weight = 9

Atau sebaliknya tergantung strategi optimal untuk dataset spesifik.

## Pernyataan Keaslian (Untuk Laporan UTS)

> **Pernyataan Keaslian**
> 
> Kami menyatakan bahwa kode dan laporan ini adalah hasil kerja kelompok kami. Ide algoritma yang digunakan adalah materi umum yang dipelajari (Greedy Activity Selection, Weighted Interval Scheduling dengan DP); implementasi, eksperimen, dan analisis dilakukan oleh anggota tim: [Nama1, Nama2, Nama3]. Jika ada penggunaan sumber eksternal (paper, blog, AI), kami mencantumkan referensi dan menjelaskan bagian yang diadaptasi.

**Jika menggunakan bantuan AI:**
> Bagian kode X dihasilkan atau dibantu oleh AI (ChatGPT) dan telah saya modifikasi, verifikasi, dan pahami sepenuhnya.

## Referensi

Wajib dicantumkan dalam bibliografi laporan UTS:

1. Kleinberg, J., & Tardos, E. *Algorithm Design* — Chapter on Activity Selection / Greedy Algorithms.

2. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* — Dynamic Programming reference.

3. Wikipedia — Activity selection problem. https://en.wikipedia.org/wiki/Activity_selection_problem

4. Wikipedia — Weighted interval scheduling. https://en.wikipedia.org/wiki/Interval_scheduling#Weighted_interval_scheduling

5. Jika ada kutipan kode/struktur dari tutorial tertentu, sebutkan URL dan tanggal akses dalam laporan.

---

**Catatan:** Pastikan semua referensi di atas dicantumkan dalam laporan UTS Anda, tidak hanya di README.

## Lisensi

Proyek ini dibuat untuk keperluan akademik (UTS). Penggunaan di luar konteks akademik harus seizin pembuat.
