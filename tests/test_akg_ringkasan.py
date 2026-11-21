"""Unit test AKG + ringkasan harian vs AKG (akg.py, ringkasan.py).

AKG mengacu pada Permenkes No. 28 Tahun 2019, usia 19–29 tahun.
Menu contoh (cocok hitungan tangan dari database TKPI):
nasi putih 150 g (262,5 kkal / 4,5 / 60 / 0,4) + ayam goreng 1 potong
(212,5 kkal / 23,8 / 0,8 / 11,9) + sayur bayam 1 mangkuk (25 kkal /
3 / 3,5 / 0,5) = total 500 kkal / protein 31,3 g / karbo 64,3 g /
lemak 12,8 g.

Persen vs AKG umum (2150/60/325/67): 23,3% / 52,2% / 19,8% / 19,1%.
Persen vs AKG pria (2650/65/430/75): 18,9% / 48,2% / 15,0% / 17,1%.
"""

import unittest

from hitung_gizi.akg import AKG, akg_untuk, status_persen
from hitung_gizi.catat import data_kosong, tambah_entri
from hitung_gizi.hitung import hitung_gizi, hitung_porsi
from hitung_gizi.makanan import dapat
from hitung_gizi.ringkasan import format_ringkasan, ringkasan_hari

TANGGAL = "2026-11-21"


def _menu_contoh():
    """Data satu hari: nasi putih + ayam goreng + sayur bayam."""
    data = data_kosong()
    tambah_entri(
        data, TANGGAL, hitung_gizi(dapat("nasi putih"), 150)
    )
    tambah_entri(
        data, TANGGAL, hitung_porsi(dapat("ayam goreng"), 1)
    )
    tambah_entri(
        data, TANGGAL, hitung_porsi(dapat("sayur bayam"), 1)
    )
    return data


class TestAKG(unittest.TestCase):
    def test_akg_umum(self):
        self.assertEqual(
            akg_untuk("umum"),
            {"energi": 2150, "protein": 60, "karbo": 325, "lemak": 67},
        )

    def test_akg_pria(self):
        self.assertEqual(
            akg_untuk("pria"),
            {"energi": 2650, "protein": 65, "karbo": 430, "lemak": 75},
        )

    def test_akg_wanita(self):
        self.assertEqual(
            akg_untuk("wanita"),
            {"energi": 2250, "protein": 60, "karbo": 360, "lemak": 65},
        )

    def test_profil_tak_dikenal(self):
        with self.assertRaises(ValueError):
            akg_untuk("anak")

    def test_akg_dikembalikan_sebagai_salinan(self):
        akg = akg_untuk("umum")
        akg["energi"] = 0
        self.assertEqual(AKG["umum"]["energi"], 2150)


class TestStatusPersen(unittest.TestCase):
    def test_kurang_di_bawah_80(self):
        self.assertEqual(status_persen(0), "kurang")
        self.assertEqual(status_persen(79.9), "kurang")

    def test_cukup_tepat_80(self):
        self.assertEqual(status_persen(80), "cukup")

    def test_cukup_tengah(self):
        self.assertEqual(status_persen(100), "cukup")

    def test_cukup_tepat_120(self):
        self.assertEqual(status_persen(120), "cukup")

    def test_lebih_di_atas_120(self):
        self.assertEqual(status_persen(120.1), "lebih")
        self.assertEqual(status_persen(200), "lebih")


class TestRingkasanHari(unittest.TestCase):
    def test_total_cocok_hitungan_tangan(self):
        ringkasan = ringkasan_hari(_menu_contoh(), TANGGAL)
        self.assertEqual(
            ringkasan["total"],
            {"energi": 500.0, "protein": 31.3, "karbo": 64.3,
             "lemak": 12.8},
        )
        self.assertEqual(ringkasan["jumlah_entri"], 3)

    def test_persen_akg_umum(self):
        ringkasan = ringkasan_hari(_menu_contoh(), TANGGAL)
        self.assertEqual(
            ringkasan["persen"],
            {"energi": 23.3, "protein": 52.2, "karbo": 19.8,
             "lemak": 19.1},
        )
        self.assertEqual(
            ringkasan["status"],
            {"energi": "kurang", "protein": "kurang",
             "karbo": "kurang", "lemak": "kurang"},
        )

    def test_persen_akg_pria(self):
        ringkasan = ringkasan_hari(_menu_contoh(), TANGGAL, "pria")
        self.assertEqual(
            ringkasan["persen"],
            {"energi": 18.9, "protein": 48.2, "karbo": 15.0,
             "lemak": 17.1},
        )
        self.assertEqual(ringkasan["profil"], "pria")

    def test_persen_akg_wanita(self):
        ringkasan = ringkasan_hari(_menu_contoh(), TANGGAL, "wanita")
        self.assertEqual(
            ringkasan["persen"]["energi"],
            round(500 / 2250 * 100, 1),
        )

    def test_hari_kosong_total_nol(self):
        ringkasan = ringkasan_hari(data_kosong(), TANGGAL)
        self.assertEqual(
            ringkasan["total"],
            {"energi": 0.0, "protein": 0.0, "karbo": 0.0, "lemak": 0.0},
        )
        self.assertEqual(
            ringkasan["persen"],
            {"energi": 0.0, "protein": 0.0, "karbo": 0.0, "lemak": 0.0},
        )
        self.assertEqual(ringkasan["jumlah_entri"], 0)
        self.assertTrue(
            all(status == "kurang" for status in ringkasan["status"].values())
        )

    def test_profil_tak_dikenal(self):
        with self.assertRaises(ValueError):
            ringkasan_hari(_menu_contoh(), TANGGAL, "anak")

    def test_tanggal_tak_valid(self):
        with self.assertRaises(ValueError):
            ringkasan_hari(_menu_contoh(), "2026-13-40")

    def test_format_ringkasan(self):
        teks = format_ringkasan(ringkasan_hari(_menu_contoh(), TANGGAL))
        self.assertIn("Ringkasan 2026-11-21 (3 makanan", teks)
        self.assertIn("profil AKG: umum", teks)
        self.assertIn("500 kkal", teks)
        self.assertIn("23.3% AKG", teks)
        self.assertIn("kurang", teks)


if __name__ == "__main__":
    unittest.main()
