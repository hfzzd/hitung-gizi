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

    def test_hitung_gram_sama_dengan_porsi_tampil_label(self):
        hasil = self._jalankan("hitung", "nasi putih", "150")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("150 g (1 piring)", hasil.stdout)

    def test_hitung_gram_bukan_porsi_tanpa_label(self):
        hasil = self._jalankan("hitung", "nasi putih", "100")
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("Nasi putih — 100 g", hasil.stdout)
        self.assertNotIn("(1 piring)", hasil.stdout)

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


class TestCLICatat(unittest.TestCase):
    """End-to-end CLI catat/hari/ringkasan/hapus via subprocess.

    Catatan diisolasi ke berkas /tmp lewat env HITUNG_GIZI_DATA, jadi
    tidak menyentuh ~/.config/hitung-gizi/catatan.json.
    Menu yang dicatat (cocok hitungan tangan): nasi putih 150 g
    (262,5 kkal) + ayam goreng 1 potong (212,5 kkal) + sayur bayam
    1 mangkuk (25 kkal) = 500 kkal / protein 31,3 / karbo 64,3 /
    lemak 12,8; persen AKG umum 23,3% / 52,2% / 19,8% / 19,1%.
    """

    TANGGAL = "2026-11-21"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.jalur = os.path.join(self.tmp.name, "catatan.json")
        self.env = dict(
            os.environ,
            PYTHONPATH=REPO_ROOT,
            HITUNG_GIZI_DATA=self.jalur,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _jalankan(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "hitung_gizi", *args],
            cwd=self.tmp.name, env=self.env,
            capture_output=True, text=True, timeout=30,
        )

    def _catat_menu(self):
        self.assertEqual(
            self._jalankan(
                "catat", "nasi putih", "150",
                "--tanggal", self.TANGGAL,
            ).returncode, 0)
        self.assertEqual(
            self._jalankan(
                "catat", "ayam goreng", "--porsi", "1",
                "--tanggal", self.TANGGAL,
            ).returncode, 0)
        self.assertEqual(
            self._jalankan(
                "catat", "sayur bayam",
                "--tanggal", self.TANGGAL,
            ).returncode, 0)

    def test_alur_catat_hari_ringkasan_hapus(self):
        self._catat_menu()
        hari = self._jalankan("hari", self.TANGGAL)
        self.assertEqual(hari.returncode, 0)
        self.assertIn("Catatan makan 2026-11-21 (3 makanan)", hari.stdout)
        self.assertIn("1. Nasi putih — 150 g: 262.5 kkal", hari.stdout)
        self.assertIn("2. Ayam goreng — 85 g: 212.5 kkal", hari.stdout)
        self.assertIn("3. Sayur bayam — 100 g: 25 kkal", hari.stdout)
        self.assertIn(
            "Total: 500 kkal, protein 31.3 g, karbo 64.3 g, "
            "lemak 12.8 g", hari.stdout,
        )
        ringkasan = self._jalankan(
            "ringkasan", self.TANGGAL, "--profil", "umum")
        self.assertEqual(ringkasan.returncode, 0)
        self.assertIn("Ringkasan 2026-11-21 (3 makanan", ringkasan.stdout)
        self.assertIn("500 kkal dari 2150 kkal (23.3% AKG)", ringkasan.stdout)
        self.assertIn("31.3 g dari 60 g (52.2% AKG)", ringkasan.stdout)
        self.assertIn("kurang", ringkasan.stdout)
        hapus = self._jalankan(
            "hapus", "--tanggal", self.TANGGAL, "--nomor", "3")
        self.assertEqual(hapus.returncode, 0)
        self.assertIn("Dihapus dari 2026-11-21", hapus.stdout)
        self.assertIn("Sayur bayam", hapus.stdout)
        hari = self._jalankan("hari", self.TANGGAL)
        self.assertEqual(hari.returncode, 0)
        self.assertIn("Catatan makan 2026-11-21 (2 makanan)", hari.stdout)
        self.assertIn("Total: 475 kkal", hari.stdout)
        self.assertNotIn("Sayur bayam", hari.stdout)

    def test_ringkasan_profil_pria(self):
        self._catat_menu()
        ringkasan = self._jalankan(
            "ringkasan", self.TANGGAL, "--profil", "pria")
        self.assertEqual(ringkasan.returncode, 0)
        self.assertIn("500 kkal dari 2650 kkal (18.9% AKG)", ringkasan.stdout)
        self.assertIn("profil AKG: pria", ringkasan.stdout)

    def test_catat_makanan_tak_dikenal_exit_1(self):
        hasil = self._jalankan(
            "catat", "pizza", "100", "--tanggal", self.TANGGAL)
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("belum ada di database", hasil.stdout)

    def test_catat_tanggal_salah_exit_1(self):
        hasil = self._jalankan(
            "catat", "nasi putih", "150", "--tanggal", "2026-13-40")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("tidak valid", hasil.stdout)

    def test_hari_tanggal_salah_exit_1(self):
        hasil = self._jalankan("hari", "2026-13-40")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("tidak valid", hasil.stdout)

    def test_ringkasan_profil_tak_dikenal_exit_1(self):
        self._catat_menu()
        hasil = self._jalankan(
            "ringkasan", self.TANGGAL, "--profil", "anak")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("tidak dikenal", hasil.stdout)

    def test_hapus_nomor_tak_ada_exit_1(self):
        self._catat_menu()
        hasil = self._jalankan(
            "hapus", "--tanggal", self.TANGGAL, "--nomor", "9")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("tidak ada", hasil.stdout)

    def test_hari_kosong_exit_1(self):
        hasil = self._jalankan("hari", "2026-11-22")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Belum ada catatan makan pada 2026-11-22", hasil.stdout)

    def test_ringkasan_hari_kosong_exit_1(self):
        hasil = self._jalankan("ringkasan", "2026-11-22")
        self.assertEqual(hasil.returncode, 1)
        self.assertIn("Belum ada catatan makan pada 2026-11-22", hasil.stdout)

    def test_catat_tanpa_gram_pakai_satu_porsi(self):
        hasil = self._jalankan(
            "catat", "telur ayam rebus", "--tanggal", self.TANGGAL)
        self.assertEqual(hasil.returncode, 0)
        self.assertIn("Dicatat sebagai entri ke-1", hasil.stdout)
        self.assertIn("50 g (1 butir)", hasil.stdout)
        self.assertIn("77.5 kkal", hasil.stdout)


if __name__ == "__main__":
    unittest.main()
