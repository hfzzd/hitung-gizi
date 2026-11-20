"""Antarmuka baris perintah HitungGizi.

Perintah:
  cari KATA                 Cari makanan berdasarkan nama.
  hitung NAMA [GRAM]        Hitung gizi untuk berat tertentu (gram);
                            tanpa GRAM memakai 1 porsi umum.
  hitung NAMA --porsi N     Hitung gizi untuk N porsi umum.
  daftar [--kategori K]     Tampilkan semua makanan, bisa difilter
                            per kategori.
  --version                 Tampilkan versi HitungGizi.
"""

import argparse
import sys

from . import __version__
from .hitung import format_hasil, hitung_gizi, hitung_porsi
from .makanan import KATEGORI, berdasarkan_kategori, cari, dapat, semua


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
    makanan = dapat(args.nama)
    if makanan is None:
        print(f"Maaf, '{args.nama}' belum ada di database HitungGizi.")
        mirip = _saran_mirip(args.nama)
        if mirip:
            print("Mungkin maksudmu salah satu ini?")
            for m in mirip:
                print("  " + _format_makanan(m))
        else:
            print("Coba cari dulu dengan: python3 -m hitung_gizi cari <kata>")
            print("atau lihat semua makanan dengan: python3 -m hitung_gizi daftar")
        return 1
    if args.gram is not None and args.porsi is not None:
        print("Maaf, pilih salah satu: berat dalam gram atau jumlah porsi, "
              "bukan keduanya.")
        return 2
    try:
        if args.porsi is not None:
            hasil = hitung_porsi(makanan, args.porsi)
            tampil = dict(makanan)
            if args.porsi > 1:
                tampil["porsi"] = f"{args.porsi:g} x {makanan['porsi']}"
        elif args.gram is not None:
            hasil = hitung_gizi(makanan, args.gram)
            # Label porsi umum hanya bila beratnya sama persis dengan
            # satu porsi, kalau tidak label itu menyesatkan.
            tampil = makanan if args.gram == makanan["porsi_g"] else None
        else:
            hasil = hitung_porsi(makanan, 1)
            tampil = makanan
    except ValueError as exc:
        print(f"Maaf, {exc}")
        return 1
    print(format_hasil(hasil, tampil))
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
