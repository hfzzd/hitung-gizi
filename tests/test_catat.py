"""Unit test modul catatan makan harian (catat.py).

Nilai gizi yang dipakai di sini cocok hitungan tangan dari database
(TKPI): nasi putih 150 g = 262,5 kkal / protein 4,5 / karbo 60 /
lemak 0,4; ayam goreng 1 potong (85 g) = 212,5 kkal / protein 23,8 /
karbo 0,8 / lemak 11,9; sayur bayam 1 mangkuk (100 g) = 25 kkal /
protein 3 / karbo 3,5 / lemak 0,5.
"""

import json
import os
import tempfile
import unittest

from hitung_gizi.catat import (
    data_kosong,
    entri_hari,
    hapus_entri,
    jalur_data,
    muat_data,
    simpan_data,
    tambah_entri,
    tanggal_tercatat,
    validasi_tanggal,
)
from hitung_gizi.hitung import hitung_gizi, hitung_porsi
from hitung_gizi.makanan import dapat

TANGGAL = "2026-11-21"


def _hasil(nama, gram=None, porsi=None):
    makanan = dapat(nama)
    if porsi is not None:
        return hitung_porsi(makanan, porsi)
    return hitung_gizi(makanan, gram)


class TestValidasiTanggal(unittest.TestCase):
    def test_tanggal_valid(self):
        self.assertEqual(validasi_tanggal("2026-11-21"), "2026-11-21")

    def test_bulan_tak_valid(self):
        with self.assertRaises(ValueError):
            validasi_tanggal("2026-13-40")

    def test_hari_tak_valid(self):
        with self.assertRaises(ValueError):
            validasi_tanggal("2026-02-30")

    def test_format_salah(self):
        with self.assertRaises(ValueError):
            validasi_tanggal("21-11-2026")

    def test_teks_kosong(self):
        with self.assertRaises(ValueError):
            validasi_tanggal("")


class TestTambahEntri(unittest.TestCase):
    def test_tambah_kembalikan_nomor_urut(self):
        data = data_kosong()
        nomor = tambah_entri(data, TANGGAL, _hasil("nasi putih", gram=150))
        self.assertEqual(nomor, 1)
        nomor = tambah_entri(data, TANGGAL, _hasil("ayam goreng", porsi=1))
        self.assertEqual(nomor, 2)

    def test_entri_menyimpan_hasil_hitung(self):
        data = data_kosong()
        tambah_entri(data, TANGGAL, _hasil("nasi putih", gram=150))
        entri = entri_hari(data, TANGGAL)
        self.assertEqual(len(entri), 1)
        self.assertEqual(entri[0]["nama"], "Nasi putih")
        self.assertEqual(entri[0]["gram"], 150)
        self.assertEqual(entri[0]["energi"], 262.5)
        self.assertEqual(entri[0]["protein"], 4.5)
        self.assertEqual(entri[0]["karbo"], 60.0)
        self.assertEqual(entri[0]["lemak"], 0.4)

    def test_tambah_tanggal_tak_valid(self):
        data = data_kosong()
        with self.assertRaises(ValueError):
            tambah_entri(data, "2026-13-40", _hasil("nasi putih", gram=150))

    def test_entri_hari_kosong(self):
        data = data_kosong()
        self.assertEqual(entri_hari(data, TANGGAL), [])

    def test_entri_hari_tanggal_tak_valid(self):
        data = data_kosong()
        with self.assertRaises(ValueError):
            entri_hari(data, "2026-02-30")

    def test_tanggal_tercatat_terurut(self):
        data = data_kosong()
        tambah_entri(data, "2026-11-22", _hasil("nasi putih", gram=150))
        tambah_entri(data, "2026-11-20", _hasil("nasi putih", gram=150))
        self.assertEqual(
            tanggal_tercatat(data), ["2026-11-20", "2026-11-22"]
        )


class TestHapusEntri(unittest.TestCase):
    def setUp(self):
        self.data = data_kosong()
        tambah_entri(self.data, TANGGAL, _hasil("nasi putih", gram=150))
        tambah_entri(self.data, TANGGAL, _hasil("ayam goreng", porsi=1))
        tambah_entri(self.data, TANGGAL, _hasil("sayur bayam", porsi=1))

    def test_hapus_tengah(self):
        entri = hapus_entri(self.data, TANGGAL, 2)
        self.assertEqual(entri["nama"], "Ayam goreng")
        sisa = entri_hari(self.data, TANGGAL)
        self.assertEqual(len(sisa), 2)
        self.assertEqual(sisa[0]["nama"], "Nasi putih")
        self.assertEqual(sisa[1]["nama"], "Sayur bayam")

    def test_hapus_terakhir_hapus_tanggal(self):
        hapus_entri(self.data, TANGGAL, 1)
        hapus_entri(self.data, TANGGAL, 1)
        hapus_entri(self.data, TANGGAL, 1)
        self.assertEqual(tanggal_tercatat(self.data), [])
        self.assertEqual(entri_hari(self.data, TANGGAL), [])

    def test_hapus_nomor_tak_ada(self):
        with self.assertRaises(ValueError):
            hapus_entri(self.data, TANGGAL, 4)

    def test_hapus_nomor_nol(self):
        with self.assertRaises(ValueError):
            hapus_entri(self.data, TANGGAL, 0)

    def test_hapus_tanggal_kosong(self):
        with self.assertRaises(ValueError):
            hapus_entri(self.data, "2026-11-22", 1)

    def test_hapus_tanggal_tak_valid(self):
        with self.assertRaises(ValueError):
            hapus_entri(self.data, "2026-13-40", 1)


class TestSimpanMuat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.jalur = os.path.join(self.tmp.name, "catatan.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_berkas_belum_ada_kosong(self):
        self.assertEqual(muat_data(self.jalur), data_kosong())

    def test_simpan_lalu_muat(self):
        data = data_kosong()
        tambah_entri(data, TANGGAL, _hasil("nasi putih", gram=150))
        tambah_entri(data, TANGGAL, _hasil("ayam goreng", porsi=1))
        simpan_data(data, self.jalur)
        self.assertEqual(muat_data(self.jalur), data)

    def test_berkas_rusak_ditolak(self):
        with open(self.jalur, "w", encoding="utf-8") as f:
            f.write("{ini bukan json")
        with self.assertRaises(ValueError):
            muat_data(self.jalur)

    def test_format_salah_ditolak(self):
        with open(self.jalur, "w", encoding="utf-8") as f:
            json.dump({"bukan": "catatan"}, f)
        with self.assertRaises(ValueError):
            muat_data(self.jalur)

    def test_jalur_data_env(self):
        os.environ["HITUNG_GIZI_DATA"] = self.jalur
        try:
            self.assertEqual(jalur_data(), self.jalur)
        finally:
            del os.environ["HITUNG_GIZI_DATA"]


if __name__ == "__main__":
    unittest.main()
