# HitungGizi

Kalkulator gizi makanan Indonesia di terminal — tanpa internet, tanpa akun.

Cari makanan Indonesia, hitung kalori dan makronutrien (protein, karbohidrat,
lemak) per porsi, lalu catat makan harianmu dan bandingkan dengan kebutuhan
harian acuan (AKG).

## Kenapa

Aplikasi gizi yang populer datanya didominasi makanan Barat. HitungGizi memakai
makanan yang memang kita makan sehari-hari — nasi putih, tempe goreng, soto
ayam, gado-gado, pisang — dengan nilai gizi per 100 gram yang mengacu pada
Tabel Komposisi Pangan Indonesia (TKPI) dan dibulatkan agar mudah dipakai.

## Cara pakai

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
  Energi   : 263 kkal
  Protein  : 4,5 g
  Karbohidrat: 60,0 g
  Lemak    : 0,5 g
```

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `cari KATA` | Cari makanan berdasarkan nama |
| `hitung NAMA [GRAM]` | Hitung gizi untuk berat tertentu (gram); tanpa GRAM memakai porsi umum |
| `hitung NAMA --porsi N` | Hitung gizi untuk N porsi umum |
| `daftar [--kategori K]` | Tampilkan semua makanan, bisa difilter per kategori |
| `catat NAMA [GRAM]` | Catat makanan ke log hari ini *(Day-2)* |
| `ringkasan` | Ringkasan gizi hari ini vs AKG *(Day-2)* |

## Data gizi

- Nilai per 100 gram, mengacu pada TKPI (dibulatkan ke satu desimal).
- Setiap makanan punya porsi umum (mis. 1 piring nasi = 150 g, 1 butir telur = 50 g)
  supaya menghitung tidak perlu timbangan.
- Nilai gizi adalah perkiraan untuk makanan rumahan pada umumnya; cara masak
  (digoreng, direbus, dipanggang) memengaruhi angka sebenarnya.

## Rencana

- [x] Day-1: database makanan Indonesia + pencarian + hitung gizi per porsi + CLI dasar
- [ ] Day-2: catat makan harian + ringkasan vs AKG + unit test + README lengkap

## Menjalankan test

```bash
python3 -m unittest discover -s tests
```

## Lisensi

MIT — lihat [LICENSE](LICENSE).
