"""Unit test untuk perhitungan gizi (hitung_gizi.hitung)."""

import unittest

from hitung_gizi.hitung import format_hasil, hitung_gizi, hitung_porsi, total_gizi
from hitung_gizi.makanan import dapat


class TestHitungGizi(unittest.TestCase):
    def test_nasi_putih_150_gram(self):
        nasi = dapat("nasi putih")
        hasil = hitung_gizi(nasi, 150)
        self.assertEqual(hasil["energi"], 262.5)
        self.assertEqual(hasil["protein"], 4.5)
        self.assertEqual(hasil["karbo"], 60.0)
        self.assertEqual(hasil["lemak"], 0.4)

    def test_dua_butir_telur_rebus(self):
        telur = dapat("telur ayam rebus")
        hasil = hitung_porsi(telur, 2)
        self.assertEqual(hasil["gram"], 100)
        self.assertEqual(hasil["energi"], 155.0)
        self.assertEqual(hasil["protein"], 13.0)
        self.assertEqual(hasil["karbo"], 1.1)
        self.assertEqual(hasil["lemak"], 11.0)

    def test_satu_porsi_umum(self):
        nasi = dapat("nasi putih")
        hasil = hitung_porsi(nasi, 1)
        self.assertEqual(hasil["gram"], 150)
        self.assertEqual(hasil["energi"], 262.5)

    def test_tolak_gram_nol_dan_negatif(self):
        nasi = dapat("nasi putih")
        with self.assertRaises(ValueError):
            hitung_gizi(nasi, 0)
        with self.assertRaises(ValueError):
            hitung_gizi(nasi, -50)

    def test_tolak_porsi_nol_dan_negatif(self):
        telur = dapat("telur ayam rebus")
        with self.assertRaises(ValueError):
            hitung_porsi(telur, 0)
        with self.assertRaises(ValueError):
            hitung_porsi(telur, -1)

    def test_total_gizi_menjumlah(self):
        nasi = hitung_gizi(dapat("nasi putih"), 150)
        telur = hitung_porsi(dapat("telur ayam rebus"), 2)
        total = total_gizi([nasi, telur])
        self.assertEqual(total["energi"], 417.5)
        self.assertEqual(total["protein"], 17.5)
        self.assertEqual(total["karbo"], 61.1)
        self.assertEqual(total["lemak"], 11.4)

    def test_total_gizi_kosong(self):
        total = total_gizi([])
        self.assertEqual(total, {"energi": 0.0, "protein": 0.0,
                                 "karbo": 0.0, "lemak": 0.0})

    def test_format_hasil(self):
        nasi = dapat("nasi putih")
        teks = format_hasil(hitung_gizi(nasi, 150), nasi)
        self.assertIn("Nasi putih — 150 g (1 piring)", teks)
        self.assertIn("262.5 kkal", teks)
        self.assertIn("4.5 g", teks)


if __name__ == "__main__":
    unittest.main()
