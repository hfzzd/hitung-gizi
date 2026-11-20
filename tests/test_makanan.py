"""Unit test untuk database makanan (hitung_gizi.makanan)."""

import unittest

from hitung_gizi.makanan import KATEGORI, MAKANAN, berdasarkan_kategori, cari, dapat, semua


class TestDatabaseMakanan(unittest.TestCase):
    def test_jumlah_makanan_minimal_40(self):
        self.assertGreaterEqual(len(MAKANAN), 40)

    def test_semua_makanan_punya_data_lengkap(self):
        for makanan in MAKANAN:
            for kunci in ("nama", "kategori", "energi", "protein", "karbo",
                          "lemak", "porsi_g", "porsi"):
                self.assertIn(kunci, makanan)
            self.assertIn(makanan["kategori"], KATEGORI)
            self.assertGreater(makanan["porsi_g"], 0)

    def test_semua_terurut_berdasarkan_nama(self):
        nama = [m["nama"] for m in semua()]
        self.assertEqual(nama, sorted(nama))

    def test_cari_case_insensitive(self):
        hasil_kecil = cari("nasi")
        hasil_besar = cari("NASI")
        self.assertEqual(hasil_kecil, hasil_besar)
        self.assertEqual(len(hasil_kecil), 4)

    def test_cari_multi_kata(self):
        hasil = cari("telur rebus")
        self.assertEqual([m["nama"] for m in hasil], ["Telur ayam rebus"])
        # Satu kata saja memberi hasil yang lebih luas.
        self.assertGreater(len(cari("telur")), 1)

    def test_cari_tidak_ada_kosong(self):
        self.assertEqual(cari("xyz"), [])
        self.assertEqual(cari("pizza"), [])

    def test_dapat_exact(self):
        makanan = dapat("Nasi Putih")
        self.assertIsNotNone(makanan)
        self.assertEqual(makanan["nama"], "Nasi putih")
        self.assertEqual(makanan["kategori"], "pokok")

    def test_dapat_nama_tak_persis_kosong(self):
        self.assertIsNone(dapat("nasi puti"))
        self.assertIsNone(dapat("xyz"))

    def test_kategori_tak_dikenal_kosong(self):
        self.assertEqual(berdasarkan_kategori("xyz"), [])
        self.assertEqual(berdasarkan_kategori(""), [])

    def test_berdasarkan_kategori(self):
        lauk = berdasarkan_kategori("lauk")
        self.assertEqual(len(lauk), 14)
        self.assertTrue(all(m["kategori"] == "lauk" for m in lauk))


if __name__ == "__main__":
    unittest.main()
