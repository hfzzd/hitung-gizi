# HitungGizi

Kalkulator gizi makanan Indonesia di terminal — tanpa internet, tanpa akun.

Cari makanan Indonesia, hitung kalori dan makronutrien (protein, karbohidrat,
lemak) per porsi, lalu catat makan harianmu dan bandingkan dengan kebutuhan
harian acuan (AKG).

Versi 0.2.0 — Day-2: catat makan harian + ringkasan vs AKG.

## Kenapa

Aplikasi gizi yang populer datanya didominasi makanan Barat. HitungGizi memakai
makanan yang memang kita makan sehari-hari — nasi putih, tempe goreng, soto
ayam, gado-gado, pisang — dengan nilai gizi per 100 gram yang mengacu pada
Tabel Komposisi Pangan Indonesia (TKPI) dan dibulatkan agar mudah dipakai.

## Cara pakai

### Cari dan hitung

```bash
python3 -m hitung_gizi cari nasi
python3 -m hitung_gizi hitung "nasi putih" 150
python3 -m hitung_gizi hitung "telur ayam rebus" --porsi 2
python3 -m hitung_gizi daftar
python3 -m hitung_gizi daftar --kategori lauk
```

Contoh hasil:

```
$ python3 -m hitung_gizi hitung "nasi putih" 150
Nasi putih — 150 g (1 piring)
  Energi     : 262.5 kkal
  Protein    : 4.5 g
  Karbohidrat: 60 g
  Lemak      : 0.4 g
```

Tanpa GRAM, dipakai satu porsi umum; berat yang bukan satu porsi tidak
menampilkan label porsi supaya tidak menyesatkan:

```
$ python3 -m hitung_gizi hitung "nasi putih"
Nasi putih — 150 g (1 piring)
  Energi     : 262.5 kkal
  Protein    : 4.5 g
  Karbohidrat: 60 g
  Lemak      : 0.4 g

$ python3 -m hitung_gizi hitung "nasi putih" 100
Nasi putih — 100 g
  Energi     : 175 kkal
  Protein    : 3 g
  Karbohidrat: 40 g
  Lemak      : 0.3 g
```

### Catat makan harian (Day-2)

`catat` menyimpan makanan ke log hari ini; tanpa `--tanggal`, dipakai tanggal
hari ini. Tanpa GRAM, dipakai satu porsi umum — sama seperti `hitung`.

```bash
python3 -m hitung_gizi catat "nasi putih" 150 --tanggal 2026-11-21
python3 -m hitung_gizi catat "ayam goreng" --tanggal 2026-11-21
python3 -m hitung_gizi catat "sayur bayam" --tanggal 2026-11-21
```

```
$ python3 -m hitung_gizi catat "ayam goreng" --tanggal 2026-11-21
Dicatat sebagai entri ke-2 pada 2026-11-21:
Ayam goreng — 85 g (1 potong)
  Energi     : 212.5 kkal
  Protein    : 23.8 g
  Karbohidrat: 0.8 g
  Lemak      : 11.9 g
```

Lihat isi log hari itu dengan `hari`, bandingkan dengan AKG dengan
`ringkasan`, dan hapus entri yang salah catat dengan `hapus`:

```bash
python3 -m hitung_gizi hari 2026-11-21
python3 -m hitung_gizi ringkasan 2026-11-21
python3 -m hitung_gizi ringkasan 2026-11-21 --profil pria
python3 -m hitung_gizi hapus --tanggal 2026-11-21 --nomor 3
```

```
$ python3 -m hitung_gizi hari 2026-11-21
Catatan makan 2026-11-21 (3 makanan):
  1. Nasi putih — 150 g: 262.5 kkal, protein 4.5 g, karbo 60 g, lemak 0.4 g
  2. Ayam goreng — 85 g: 212.5 kkal, protein 23.8 g, karbo 0.8 g, lemak 11.9 g
  3. Sayur bayam — 100 g: 25 kkal, protein 3 g, karbo 3.5 g, lemak 0.5 g
Total: 500 kkal, protein 31.3 g, karbo 64.3 g, lemak 12.8 g

$ python3 -m hitung_gizi ringkasan 2026-11-21
Ringkasan 2026-11-21 (3 makanan, profil AKG: umum)
  Energi      : 500 kkal dari 2150 kkal (23.3% AKG) — kurang
  Protein     : 31.3 g dari 60 g (52.2% AKG) — kurang
  Karbohidrat : 64.3 g dari 325 g (19.8% AKG) — kurang
  Lemak       : 12.8 g dari 67 g (19.1% AKG) — kurang
AKG mengacu pada Permenkes No. 28 Tahun 2019 (usia 19–29 tahun);
angka ini acuan rata-rata populasi, bukan kebutuhan personal.
```

Setelah `hapus --nomor 3`, tersisa 2 entri dengan total 475 kkal,
protein 28.3 g, karbo 60.8 g, lemak 12.3 g. Angka-angka di atas sudah
dicocokkan dengan hitungan tangan (nasi putih 262.5 + ayam goreng 212.5 +
sayur bayam 25 = 500 kkal).

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `cari KATA` | Cari makanan berdasarkan nama |
| `hitung NAMA [GRAM]` | Hitung gizi untuk berat tertentu (gram); tanpa GRAM memakai porsi umum |
| `hitung NAMA --porsi N` | Hitung gizi untuk N porsi umum |
| `daftar [--kategori K]` | Tampilkan semua makanan, bisa difilter per kategori |
| `catat NAMA [GRAM] [--tanggal T]` | Catat makanan ke log hari ini (atau tanggal T) *(Day-2)* |
| `hari [TANGGAL]` | Tampilkan catatan makan hari itu *(Day-2)* |
| `ringkasan [TANGGAL] [--profil P]` | Ringkasan gizi hari itu vs AKG, profil `umum`/`pria`/`wanita` *(Day-2)* |
| `hapus --tanggal T --nomor N` | Hapus entri ke-N dari tanggal T *(Day-2)* |

## AKG acuan

Angka Kecukupan Gizi (AKG) mengikuti Permenkes No. 28 Tahun 2019,
kelompok usia 19–29 tahun:

| Profil | Energi | Protein | Karbohidrat | Lemak |
| --- | --- | --- | --- | --- |
| umum (rata-rata nasional) | 2150 kkal | 60 g | 325 g | 67 g |
| pria | 2650 kkal | 65 g | 430 g | 75 g |
| wanita | 2250 kkal | 60 g | 360 g | 65 g |

Status tiap gizi di ringkasan: **kurang** di bawah 80% AKG, **cukup**
80–120% AKG, **lebih** di atas 120% AKG. AKG adalah acuan rata-rata
populasi, bukan kebutuhan personal — kebutuhan tiap orang berbeda menurut
aktivitas, berat badan, dan kondisi kesehatan.

## Di mana catatan disimpan

Catatan makan disimpan sebagai JSON di `~/.config/hitung-gizi/catatan.json`
(satu berkas untuk semua tanggal). Setiap entri menyimpan hasil hitung
gizinya, jadi ringkasan lama tetap terbaca walau database makanan berubah.

Untuk test atau memakai lokasi lain, atur variabel lingkungan
`HITUNG_GIZI_DATA` ke path berkas JSON lain:

```bash
HITUNG_GIZI_DATA=/tmp/catatan-test.json python3 -m hitung_gizi catat "nasi putih" 150
```

## Data gizi

- Nilai per 100 gram, mengacu pada TKPI (dibulatkan ke satu desimal).
- Setiap makanan punya porsi umum (mis. 1 piring nasi = 150 g, 1 butir telur = 50 g)
  supaya menghitung tidak perlu timbangan.
- Nilai gizi adalah perkiraan untuk makanan rumahan pada umumnya; cara masak
  (digoreng, direbus, dipanggang) memengaruhi angka sebenarnya.
- `contoh/contoh-makanan.txt` berisi contoh menu sehari beserta angka
  gizinya (total 1669 kkal).

## Rencana

- [x] Day-1: database makanan Indonesia + pencarian + hitung gizi per porsi + CLI dasar + unit test + README lengkap
- [x] Day-2: catat makan harian + ringkasan vs AKG

## Menjalankan test

```bash
python3 -m unittest discover -s tests
```

82 test (32 Day-1: 10 database makanan, 8 perhitungan gizi, 14 CLI
end-to-end; 50 Day-2: 21 catatan makan, 19 AKG + ringkasan, 10 CLI
catat/hari/ringkasan/hapus) — semuanya harus lolos sebelum push.

## Lisensi

MIT — lihat [LICENSE](LICENSE).
