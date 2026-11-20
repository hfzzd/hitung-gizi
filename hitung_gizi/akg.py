"""Angka Kecukupan Gizi (AKG) yang dianjurkan.

Mengacu pada Peraturan Menteri Kesehatan Nomor 28 Tahun 2019, Lampiran I,
untuk kelompok usia 19–29 tahun — kelompok yang paling dekat dengan
pengguna umum aplikasi ini. AKG adalah angka rata-rata untuk populasi,
bukan kebutuhan personal: kebutuhan tiap orang tetap dipengaruhi ukuran
tubuh, aktivitas, dan kondisi kesehatan.

Profil "umum" memakai rata-rata nasional (2.150 kkal, protein 60 g,
lemak 67 g, karbohidrat 325 g) dari peraturan yang sama.
"""

AKG = {
    "umum": {"energi": 2150, "protein": 60, "karbo": 325, "lemak": 67},
    "pria": {"energi": 2650, "protein": 65, "karbo": 430, "lemak": 75},
    "wanita": {"energi": 2250, "protein": 60, "karbo": 360, "lemak": 65},
}

PROFIL = tuple(AKG)


def akg_untuk(profil):
    """AKG untuk ``profil`` ("umum", "pria", atau "wanita")."""
    if profil not in AKG:
        raise ValueError(
            f"Profil '{profil}' tidak dikenal. Pilih: "
            + ", ".join(PROFIL)
            + "."
        )
    return dict(AKG[profil])


def status_persen(persen):
    """Status pemenuhan AKG dari persen: kurang / cukup / lebih.

    Batas mengikuti kebiasaan penilaian konsumsi gizi: di bawah 80%
    dianggap kurang, 80–120% cukup, di atas 120% lebih.
    """
    if persen < 80:
        return "kurang"
    if persen <= 120:
        return "cukup"
    return "lebih"
