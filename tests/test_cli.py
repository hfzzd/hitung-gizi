"""Unit test end-to-end untuk CLI, lewat subprocess di direktori /tmp.

Paket ditemukan lewat PYTHONPATH (akar repo), jadi test berjalan dari mana
saja tanpa harus memasang HitungGizi.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, PYTHONPATH=REPO_ROOT)

    def tearDown(self):
        self.tmp.cleanup()

    def _jalankan(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "hitung_gizi", *args],
            cwd=self.tmp.name, env=self.env,
            capture_output=True, text=True, timeout=30,
        )

    def test_cari(self):
        hasil = self._jalankan("cari", "nasi")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("Ditemukan 4 makanan", hasil.stdout)
        self.assertIn("Nasi putih", hasil.stdout)

    def test_cari_tidak_ada(self):
        hasil = self._jalankan("cari", "xyz")
        self.assertNotEqual(hasil.returncode, 0)
        self.assertIn("tidak ada makanan", hasil.stdout)

    def test_hitung_gram(self):
        hasil = self._jalankan("hitung", "nasi putih", "150")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("Nasi putih — 150 g", hasil.stdout)
        self.assertIn("262.5 kkal", hasil.stdout)
        self.assertIn("4.5 g", hasil.stdout)
        self.assertIn("0.4 g", hasil.stdout)

    def test_hitung_porsi(self):
        hasil = self._jalankan("hitung", "telur ayam rebus", "--porsi", "2")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("155 kkal", hasil.stdout)
        self.assertIn("2 x 1 butir", hasil.stdout)

    def test_hitung_tanpa_gram_pakai_satu_porsi(self):
        hasil = self._jalankan("hitung", "nasi putih")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("150 g (1 piring)", hasil.stdout)
        self.assertIn("262.5 kkal", hasil.stdout)

    def test_nama_tak_dikenal_exit_bukan_nol(self):
        hasil = self._jalankan("hitung", "pizza", "100")
        self.assertNotEqual(hasil.returncode, 0)
        self.assertIn("belum ada di database", hasil.stdout)

    def test_nama_mirip_diberi_saran(self):
        hasil = self._jalankan("hitung", "nasi puti", "100")
        self.assertNotEqual(hasil.returncode, 0)
        self.assertIn("Mungkin maksudmu", hasil.stdout)
        self.assertIn("Nasi putih", hasil.stdout)

    def test_hitung_gram_nol_exit_bukan_nol(self):
        hasil = self._jalankan("hitung", "nasi putih", "0")
        self.assertNotEqual(hasil.returncode, 0)

    def test_daftar(self):
        hasil = self._jalankan("daftar")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("Daftar makanan (46)", hasil.stdout)
        self.assertIn("Tempe goreng", hasil.stdout)

    def test_daftar_kategori(self):
        hasil = self._jalankan("daftar", "--kategori", "lauk")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("kategori lauk (14)", hasil.stdout)

    def test_daftar_kategori_tak_dikenal_exit_bukan_nol(self):
        hasil = self._jalankan("daftar", "--kategori", "xyz")
        self.assertNotEqual(hasil.returncode, 0)
        self.assertIn("tidak dikenal", hasil.stdout)

    def test_version(self):
        hasil = self._jalankan("--version")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("HitungGizi 0.1.0", hasil.stdout)


if __name__ == "__main__":
    unittest.main()
