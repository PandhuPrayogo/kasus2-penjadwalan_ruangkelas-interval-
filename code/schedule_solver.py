#!/usr/bin/env python3
"""
simple_schedule.py

Versi sederhana untuk Kasus 2 — Penjadwalan Ruang Kelas (Interval).

Fungsi:
- greedy earliest-finish (unweighted) -> memaksimalkan jumlah interval
- weighted interval scheduling (DP + binary search p(j)) -> memaksimalkan total bobot

Usage:
  python simple_schedule.py path/to/file.csv

CSV minimal harus memiliki dua kolom yang menyatakan waktu mulai dan selesai,
contoh header: start,end
Opsional: kolom 'weight' jika ingin bobot berbeda.

Jika header berbeda (mis. 'stime','etime' atau tanggal string), program mencoba deteksi sederhana.
"""

import sys
import os
import pandas as pd
from bisect import bisect_right
from datetime import datetime

# ---------- util sederhana untuk baca CSV ----------
def load_intervals(path):
    """
    Baca CSV dan kembalikan list intervals: [(start_num, end_num, weight, raw_row_dict), ...]
    start_num/end_num berbentuk float (timestamp) atau numeric.
    Expect: CSV with columns like 'start','end' or similar. If weight absent, default=1.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    df = pd.read_csv(path)
    # normalize column names
    cols = {c.lower(): c for c in df.columns}

    # cari kolom start/end
    start_col = None
    end_col = None
    weight_col = None
    for name in ('start','stime','start_time','begin','from','s'):
        if name in cols:
            start_col = cols[name]; break
    for name in ('end','etime','end_time','finish','to','e'):
        if name in cols:
            end_col = cols[name]; break
    for name in ('weight','w','value','score'):
        if name in cols:
            weight_col = cols[name]; break

    # fallback: pakai dua kolom pertama sebagai start/end
    if start_col is None or end_col is None:
        cand = df.columns.tolist()
        if len(cand) >= 2:
            start_col = start_col or cand[0]
            end_col = end_col or cand[1]
        else:
            raise ValueError("CSV harus memiliki minimal 2 kolom untuk start & end")

    # parse start/end ke numeric (timestamp jika string datetime)
    def to_num_series(series):
        # coba numeric langsung
        try:
            s = pd.to_numeric(series, errors='coerce')
            if s.notna().sum() > 0:
                return s.astype(float)
        except:
            pass
        # coba parse datetime
        try:
            parsed = pd.to_datetime(series, errors='coerce')
            if parsed.notna().sum() > 0:
                return parsed.astype('int64')/1e9  # convert to seconds
        except:
            pass
        # terakhir, coerce to numeric (may be NaN)
        return pd.to_numeric(series, errors='coerce').astype(float)

    s_series = to_num_series(df[start_col])
    e_series = to_num_series(df[end_col])
    if weight_col:
        w_series = pd.to_numeric(df[weight_col], errors='coerce').fillna(1.0).astype(float)
    else:
        w_series = pd.Series([1.0]*len(df))

    intervals = []
    for i, (s,e,w) in enumerate(zip(s_series, e_series, w_series)):
        if pd.isna(s) or pd.isna(e):
            continue
        s_f = float(s); e_f = float(e)
        if s_f > e_f:
            s_f, e_f = e_f, s_f
        intervals.append((s_f, e_f, float(w), dict(df.iloc[i])))
    if len(intervals) == 0:
        raise ValueError("Tidak ditemukan interval valid pada file.")
    return intervals

# ---------- Greedy earliest-finish ----------
def greedy_earliest_finish(intervals):
    # pilih berdasarkan waktu selesai terkecil
    arr = sorted(intervals, key=lambda iv: (iv[1], iv[0]))
    selected = []
    last_end = -1e18
    for iv in arr:
        if iv[0] >= last_end:
            selected.append(iv)
            last_end = iv[1]
    return selected

# ---------- Weighted Interval Scheduling (DP + binary search p(j)) ----------
def weighted_interval_scheduling(intervals):
    # sort by finish time
    arr = sorted(intervals, key=lambda iv: (iv[1], iv[0]))
    n = len(arr)
    starts = [iv[0] for iv in arr]
    ends = [iv[1] for iv in arr]
    weights = [iv[2] for iv in arr]

    # compute p[j]: index of rightmost interval i < j with end[i] <= start[j]; -1 jika tidak ada
    p = []
    for j in range(n):
        i = bisect_right(ends, starts[j]) - 1
        p.append(i)

    # DP: M[j] = optimal total weight for arr[0..j]
    M = [0.0] * n
    take = [False] * n
    for j in range(n):
        incl = weights[j] + (M[p[j]] if p[j] != -1 else 0.0)
        excl = M[j-1] if j-1 >= 0 else 0.0
        if incl > excl:
            M[j] = incl
            take[j] = True
        else:
            M[j] = excl
            take[j] = False

    # reconstruct solution
    selected = []
    j = n-1
    while j >= 0:
        if take[j]:
            selected.append(arr[j])
            j = p[j]
        else:
            j -= 1
    selected.reverse()
    return selected, M[n-1] if n>0 else 0.0

# ---------- helper prettify ----------
def human_readable(iv):
    s,e,w,raw = iv
    # jika nilai tampak seperti timestamp (besar), ubah jadi datetime
    def maybe_dt(x):
        if x > 1e9:  # timestamp seconds
            return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")
        # else tampilkan sebagai angka integer jika cocok
        if float(x).is_integer():
            return str(int(x))
        return f"{x:.3f}"
    return f"[{maybe_dt(s)} -> {maybe_dt(e)}] w={w}"

# ---------- Main (CLI simple) ----------
def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = "studikasus2/data/flight_data_2024_sample20.csv"
    print(f"Loading file: {path}")
    intervals = load_intervals(path)

    # Greedy (unweighted)
    greedy_sel = greedy_earliest_finish(intervals)
    print("\n--- Hasil Greedy (earliest-finish) ---")
    print(f"Jumlah terpilih: {len(greedy_sel)}")
    for iv in greedy_sel:
        print(" ", human_readable(iv))

    # DP weighted
    dp_sel, dp_weight = weighted_interval_scheduling(intervals)
    print("\n--- Hasil DP (weighted optimal) ---")
    print(f"Total bobot terpilih: {dp_weight:.3f}")
    for iv in dp_sel:
        print(" ", human_readable(iv))

    # jika bobot tidak semua sama, perlihatkan kontradiksi jika ada
    weights_set = set(round(iv[2],6) for iv in intervals)
    if len(weights_set) > 1:
        greedy_weight = sum(iv[2] for iv in greedy_sel)
        print("\n--- Perbandingan bobot ---")
        print(f"Greedy total weight: {greedy_weight:.3f}")
        print(f"DP    total weight: {dp_weight:.3f}")
        if dp_weight > greedy_weight + 1e-9:
            print("=> KONTRADIKSI: Greedy tidak optimal untuk kasus berbobot.")
        else:
            print("=> Greedy menghasilkan bobot sama/lebih baik pada dataset ini.")
    else:
        print("\nCatatan: dataset tampaknya unweighted (semua bobot = 1). Greedy optimal untuk count.")

    # Simpan hasil sederhana
    out_dir = "results"
    os.makedirs(out_dir, exist_ok=True)
    # save selected sets to CSV for laporan
    def save_list(lst, fname):
        import csv
        with open(os.path.join(out_dir, fname), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['start','end','weight'])
            for iv in lst:
                w.writerow([iv[0], iv[1], iv[2]])
    save_list(greedy_sel, "greedy_selected.csv")
    save_list(dp_sel, "dp_selected.csv")
    print(f"\nHasil disimpan di folder '{out_dir}' (greedy_selected.csv, dp_selected.csv).")

if __name__ == "__main__":
    main()
