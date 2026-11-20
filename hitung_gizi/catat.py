"""Catatan makan harian.

Catatan disimpan sebagai JSON di ``~/.config/hitung-gizi/catatan.json``
(env ``HITUNG_GIZI_DATA`` untuk menunjuk berkas lain, dipakai saat test):

    {"catatan": {"2026-11-21": [{"nama": ..., "gram": ..., "energi": ...,
                                 "protein": ..., "karbo": ..., "lemak": ...}]}}

Setiap entri menyimpan hasil hitung gizi (bukan hanya nama + gram) supaya
ringkasan hari lama tetap bisa dibaca walau database makanan berubah.
"""

import json
import os
from datetime import date

NAMA_BERKAS = "catatan.json"


def jalur_data(berkas=None):
    """Lokasi berkas catatan; ``berkas`` mengesampingkan lokasi bawaan."""
    if berkas:
        return berkas
    env = os.environ.get("HITUNG_GIZI_DATA")
    if env:
        return env
    return os.path.join(os.path.expanduser("~"), ".config",
                        "hitung-gizi", NAMA_BERKAS)


def data_kosong():
    """Struktur catatan kosong."""
    return {"catatan": {}}


def muat_data(berkas=None):
    """Muat catatan dari berkas; berkas yang belum ada = catatan kosong."""
    jalur = jalur_data(berkas)
    if not os.path.exists(jalur):
        return data_kosong()
    try:
        with open(jalur, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(
            f"Berkas catatan rusak atau tidak bisa dibaca ({jalur}): {exc}"
        ) from exc
    if not isinstance(data, dict) or not isinstance(data.get("catatan"), dict):
        raise ValueError(f"Berkas catatan tidak sesuai format ({jalur}).")
    return data


def simpan_data(data, berkas=None):
    """Simpan catatan ke berkas (buat direktorinya bila belum ada)."""
    jalur = jalur_data(berkas)
    direktori = os.path.dirname(jalur)
    if direktori:
        os.makedirs(direktori, exist_ok=True)
    with open(jalur, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def validasi_tanggal(teks):
    """Periksa teks tanggal YYYY-MM-DD; kembalikan teksnya bila valid."""
    try:
        tahun, bulan, hari = (int(bagian) for bagian in teks.split("-"))
        date(tahun, bulan, hari)
    except (ValueError, AttributeError):
        raise ValueError(
            f"Tanggal '{teks}' tidak valid. Pakai format YYYY-MM-DD, "
            "contoh: 2026-11-21."
        ) from None
    return teks


def hari_ini():
    """Tanggal hari ini sebagai teks YYYY-MM-DD."""
    return date.today().isoformat()


def tambah_entri(data, tanggal, hasil_hitung):
    """Tambah satu entri (hasil ``hitung_gizi``) ke tanggal tertentu.

    Mengembalikan nomor entri yang baru ditambahkan (mulai dari 1).
    """
    validasi_tanggal(tanggal)
    entri = {
        "nama": hasil_hitung["nama"],
        "gram": hasil_hitung["gram"],
        "energi": hasil_hitung["energi"],
        "protein": hasil_hitung["protein"],
        "karbo": hasil_hitung["karbo"],
        "lemak": hasil_hitung["lemak"],
    }
    hari = data["catatan"].setdefault(tanggal, [])
    hari.append(entri)
    return len(hari)


def entri_hari(data, tanggal):
    """Daftar entri pada tanggal tertentu (kosong bila belum ada)."""
    validasi_tanggal(tanggal)
    return list(data["catatan"].get(tanggal, []))


def hapus_entri(data, tanggal, nomor):
    """Hapus entri ke-``nomor`` (mulai dari 1) pada tanggal tertentu.

    Mengembalikan entri yang dihapus. Tanggal yang ikut kosong ikut
    dihapus dari catatan.
    """
    validasi_tanggal(tanggal)
    hari = data["catatan"].get(tanggal)
    if not hari:
        raise ValueError(f"Belum ada catatan makan pada {tanggal}.")
    if nomor < 1 or nomor > len(hari):
        raise ValueError(
            f"Nomor {nomor} tidak ada — {tanggal} hanya punya "
            f"{len(hari)} entri."
        )
    entri = hari.pop(nomor - 1)
    if not hari:
        del data["catatan"][tanggal]
    return entri


def tanggal_tercatat(data):
    """Semua tanggal yang punya catatan, terurut dari yang paling lama."""
    return sorted(data["catatan"])
