"""Antarmuka baris perintah HitungGizi.

Perintah:
  cari KATA                 Cari makanan berdasarkan nama.
  hitung NAMA [GRAM]        Hitung gizi untuk berat tertentu (gram);
                            tanpa GRAM memakai 1 porsi umum.
  hitung NAMA --porsi N     Hitung gizi untuk N porsi umum.
  daftar [--kategori K]     Tampilkan semua makanan, bisa difilter
                            per kategori.
  catat NAMA [GRAM]         Catat makanan yang dimakan hari ini
                            (atau --tanggal YYYY-MM-DD).
  hari [TANGGAL]            Tampilkan catatan makan satu tanggal.
  ringkasan [TANGGAL]       Ringkasan gizi satu tanggal vs AKG
                            (--profil umum/pria/wanita).
  hapus --tanggal T --nomor N
                            Hapus satu entri catatan.
  --version                 Tampilkan versi HitungGizi.
"""

import argparse
import sys

from . import __version__
from .akg import PROFIL
from .catat import (
    entri_hari,
    hapus_entri,
    hari_ini,
    muat_data,
    simpan_data,
    tambah_entri,
    validasi_tanggal,
)
from .hitung import format_hasil, hitung_gizi, hitung_porsi, total_gizi
from .makanan import KATEGORI, berdasarkan_kategori, cari, dapat, semua
from .ringkasan import format_ringkasan, ringkasan_hari


def _format_makanan(makanan):
    """Satu baris ringkas: nama + kategori + energi/100 g + porsi."""
    return (
        f"{makanan['nama']} ({makanan['kategori']}) — "
        f"{makanan['energi']:g} kkal/100 g, "
        f"{makanan['porsi']} ({makanan['porsi_g']:g} g)"
    )


def _cmd_cari(args):
    hasil = cari(args.kata)
    if not hasil:
        print(f"Maaf, tidak ada makanan yang cocok dengan '{args.kata}'.")
        print("Coba kata yang lebih pendek, misalnya 'nasi' atau 'ayam'.")
        return 1
    print(f"Ditemukan {len(hasil)} makanan untuk '{args.kata}':")
    for makanan in hasil:
        print("  " + _format_makanan(makanan))
    return 0


def _saran_mirip(nama):
    """Hasil cari() untuk nama yang tidak ditemukan, bila ada."""
    return cari(nama)


def _cmd_hitung(args):
    makanan = _makanan_atau_pesan(args.nama)
    if makanan is None:
        return 1
    try:
        hasil, tampil = _hitung_dari_args(makanan, args.gram, args.porsi)
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    print(format_hasil(hasil, tampil))
    return 0


def _makanan_atau_pesan(nama):
    """Makanan dari ``dapat()``; bila tidak ada, cetak pesan ramah."""
    makanan = dapat(nama)
    if makanan is not None:
        return makanan
    print(f"Maaf, '{nama}' belum ada di database HitungGizi.")
    mirip = _saran_mirip(nama)
    if mirip:
        print("Mungkin maksudmu salah satu ini?")
        for m in mirip:
            print("  " + _format_makanan(m))
    else:
        print("Coba cari dulu dengan: python3 -m hitung_gizi cari <kata>")
        print("atau lihat semua makanan dengan: python3 -m hitung_gizi daftar")
    return None


def _hitung_dari_args(makanan, gram, porsi):
    """Hitung gizi dari argumen gram/porsi; kembalikan (hasil, tampil).

    ``tampil`` adalah makanan untuk label porsi umum, atau None bila
    beratnya bukan satu porsi umum (supaya label tidak menyesatkan).
    """
    if gram is not None and porsi is not None:
        raise ValueError(
            "pilih salah satu: berat dalam gram atau jumlah porsi, "
            "bukan keduanya."
        )
    if porsi is not None:
        hasil = hitung_porsi(makanan, porsi)
        tampil = dict(makanan)
        if porsi > 1:
            tampil["porsi"] = f"{porsi:g} x {makanan['porsi']}"
        return hasil, tampil
    if gram is not None:
        hasil = hitung_gizi(makanan, gram)
        # Label porsi umum hanya bila beratnya sama persis dengan
        # satu porsi, kalau tidak label itu menyesatkan.
        tampil = makanan if gram == makanan["porsi_g"] else None
        return hasil, tampil
    return hitung_porsi(makanan, 1), makanan


def _muat_atau_pesan():
    """Muat catatan; bila berkas rusak, cetak pesan ramah."""
    try:
        return muat_data(), None
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return None, 1


def _tanggal_atau_hari_ini(args):
    """Tanggal dari argumen, atau hari ini bila tidak diisi."""
    tanggal = getattr(args, "tanggal", None) or hari_ini()
    try:
        return validasi_tanggal(tanggal), None
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return None, 1


def _cmd_catat(args):
    makanan = _makanan_atau_pesan(args.nama)
    if makanan is None:
        return 1
    try:
        hasil, tampil = _hitung_dari_args(makanan, args.gram, args.porsi)
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    tanggal, kode = _tanggal_atau_hari_ini(args)
    if kode is not None:
        return kode
    data, kode = _muat_atau_pesan()
    if kode is not None:
        return kode
    nomor = tambah_entri(data, tanggal, hasil)
    simpan_data(data)
    print(f"Dicatat sebagai entri ke-{nomor} pada {tanggal}:")
    print(format_hasil(hasil, tampil))
    return 0


def _format_entri(nomor, entri):
    """Satu baris ringkas untuk satu entri catatan harian."""
    return (
        f"{nomor}. {entri['nama']} — {entri['gram']:g} g: "
        f"{entri['energi']:g} kkal, protein {entri['protein']:g} g, "
        f"karbo {entri['karbo']:g} g, lemak {entri['lemak']:g} g"
    )


def _cmd_hari(args):
    tanggal, kode = _tanggal_atau_hari_ini(args)
    if kode is not None:
        return kode
    data, kode = _muat_atau_pesan()
    if kode is not None:
        return kode
    entri = entri_hari(data, tanggal)
    if not entri:
        print(f"Belum ada catatan makan pada {tanggal}.")
        print("Catat dengan: python3 -m hitung_gizi catat <nama> [gram]")
        return 1
    print(f"Catatan makan {tanggal} ({len(entri)} makanan):")
    for nomor, item in enumerate(entri, start=1):
        print("  " + _format_entri(nomor, item))
    total = total_gizi(entri)
    print(
        f"Total: {total['energi']:g} kkal, protein {total['protein']:g} g, "
        f"karbo {total['karbo']:g} g, lemak {total['lemak']:g} g"
    )
    return 0


def _cmd_ringkasan(args):
    tanggal, kode = _tanggal_atau_hari_ini(args)
    if kode is not None:
        return kode
    data, kode = _muat_atau_pesan()
    if kode is not None:
        return kode
    if not entri_hari(data, tanggal):
        print(f"Belum ada catatan makan pada {tanggal}.")
        print("Catat dengan: python3 -m hitung_gizi catat <nama> [gram]")
        return 1
    try:
        ringkasan = ringkasan_hari(data, tanggal, args.profil)
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    print(format_ringkasan(ringkasan))
    print("AKG mengacu pada Permenkes No. 28 Tahun 2019 (usia 19–29 tahun);")
    print("angka ini acuan rata-rata populasi, bukan kebutuhan personal.")
    return 0


def _cmd_hapus(args):
    try:
        tanggal = validasi_tanggal(args.tanggal)
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    data, kode = _muat_atau_pesan()
    if kode is not None:
        return kode
    try:
        entri = hapus_entri(data, tanggal, args.nomor)
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    simpan_data(data)
    print(f"Dihapus dari {tanggal}:")
    print("  " + _format_entri(args.nomor, entri))
    return 0


def _cmd_daftar(args):
    if args.kategori is None:
        daftar = semua()
        print(f"Daftar makanan ({len(daftar)}):")
        for makanan in daftar:
            print("  " + _format_makanan(makanan))
        return 0
    daftar = berdasarkan_kategori(args.kategori)
    if not daftar:
        print(f"Maaf, kategori '{args.kategori}' tidak dikenal.")
        print("Kategori yang tersedia: " + ", ".join(KATEGORI))
        return 1
    print(f"Daftar makanan kategori {args.kategori} ({len(daftar)}):")
    for makanan in daftar:
        print("  " + _format_makanan(makanan))
    return 0


def _buat_parser():
    parser = argparse.ArgumentParser(
        prog="hitung_gizi",
        description="HitungGizi — kalkulator gizi makanan Indonesia di terminal.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"HitungGizi {__version__}",
    )
    sub = parser.add_subparsers(dest="perintah")

    p_cari = sub.add_parser("cari", help="cari makanan berdasarkan nama")
    p_cari.add_argument("kata", help="kata kunci nama makanan")
    p_cari.set_defaults(func=_cmd_cari)

    p_hitung = sub.add_parser("hitung", help="hitung gizi satu makanan")
    p_hitung.add_argument("nama", help="nama makanan (persis seperti di daftar)")
    p_hitung.add_argument("gram", nargs="?", type=float,
                          help="berat dalam gram (tanpa ini: 1 porsi umum)")
    p_hitung.add_argument("--porsi", type=float, metavar="N",
                          help="hitung untuk N porsi umum")
    p_hitung.set_defaults(func=_cmd_hitung)

    p_daftar = sub.add_parser("daftar", help="tampilkan semua makanan")
    p_daftar.add_argument("--kategori", metavar="K",
                          help="filter per kategori: " + ", ".join(KATEGORI))
    p_daftar.set_defaults(func=_cmd_daftar)

    p_catat = sub.add_parser("catat", help="catat makanan yang dimakan")
    p_catat.add_argument("nama", help="nama makanan (persis seperti di daftar)")
    p_catat.add_argument("gram", nargs="?", type=float,
                         help="berat dalam gram (tanpa ini: 1 porsi umum)")
    p_catat.add_argument("--porsi", type=float, metavar="N",
                         help="catat N porsi umum")
    p_catat.add_argument("--tanggal", metavar="T",
                         help="tanggal YYYY-MM-DD (bawaan: hari ini)")
    p_catat.set_defaults(func=_cmd_catat)

    p_hari = sub.add_parser("hari", help="tampilkan catatan makan satu tanggal")
    p_hari.add_argument("tanggal", nargs="?", metavar="T",
                        help="tanggal YYYY-MM-DD (bawaan: hari ini)")
    p_hari.set_defaults(func=_cmd_hari)

    p_ringkasan = sub.add_parser("ringkasan", help="ringkasan gizi vs AKG")
    p_ringkasan.add_argument("tanggal", nargs="?", metavar="T",
                            help="tanggal YYYY-MM-DD (bawaan: hari ini)")
    p_ringkasan.add_argument("--profil", default="umum", metavar="P",
                            help="profil AKG: " + ", ".join(PROFIL)
                            + " (bawaan: umum)")
    p_ringkasan.set_defaults(func=_cmd_ringkasan)

    p_hapus = sub.add_parser("hapus", help="hapus satu entri catatan")
    p_hapus.add_argument("--tanggal", required=True, metavar="T",
                         help="tanggal entri (YYYY-MM-DD)")
    p_hapus.add_argument("--nomor", required=True, type=int, metavar="N",
                         help="nomor entri seperti di perintah 'hari'")
    p_hapus.set_defaults(func=_cmd_hapus)

    return parser


def main(argv=None):
    """Titik masuk CLI; mengembalikan kode keluar (0 = sukses)."""
    parser = _buat_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
