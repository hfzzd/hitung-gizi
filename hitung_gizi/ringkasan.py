"""Ringkasan makan harian dibandingkan dengan AKG."""

from .akg import akg_untuk, status_persen
from .catat import entri_hari
from .hitung import total_gizi

LABEL = {
    "energi": ("Energi", "kkal"),
    "protein": ("Protein", "g"),
    "karbo": ("Karbohidrat", "g"),
    "lemak": ("Lemak", "g"),
}


def ringkasan_hari(data, tanggal, profil="umum"):
    """Ringkasan gizi satu tanggal: total, persen AKG, dan status.

    Mengembalikan dict dengan kunci ``tanggal``, ``profil``, ``total``,
    ``akg``, ``persen``, ``status``, dan ``jumlah_entri``.
    """
    akg = akg_untuk(profil)
    entri = entri_hari(data, tanggal)
    total = total_gizi(entri)
    persen = {
        kunci: round(total[kunci] / akg[kunci] * 100, 1)
        for kunci in total
    }
    return {
        "tanggal": tanggal,
        "profil": profil,
        "total": total,
        "akg": akg,
        "persen": persen,
        "status": {kunci: status_persen(persen[kunci]) for kunci in persen},
        "jumlah_entri": len(entri),
    }


def format_ringkasan(ringkasan):
    """Format ringkasan harian menjadi teks yang ramah dibaca."""
    baris = [
        f"Ringkasan {ringkasan['tanggal']} "
        f"({ringkasan['jumlah_entri']} makanan, profil AKG: "
        f"{ringkasan['profil']})"
    ]
    for kunci in ("energi", "protein", "karbo", "lemak"):
        label, satuan = LABEL[kunci]
        baris.append(
            f"  {label:<12}: {ringkasan['total'][kunci]:g} {satuan} "
            f"dari {ringkasan['akg'][kunci]:g} {satuan} "
            f"({ringkasan['persen'][kunci]:g}% AKG) — "
            f"{ringkasan['status'][kunci]}"
        )
    return "\n".join(baris)
