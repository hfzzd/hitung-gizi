"""Hitung gizi makanan untuk berat atau jumlah porsi tertentu."""


def hitung_gizi(makanan, gram):
    """Hitung gizi ``makanan`` untuk ``gram`` gram.

    Mengembalikan dict dengan energi (kkal), protein, karbo, dan lemak
    (gram), dibulatkan ke satu desimal.
    """
    if gram <= 0:
        raise ValueError("Berat harus lebih dari 0 gram.")
    faktor = gram / 100.0
    return {
        "nama": makanan["nama"],
        "gram": gram,
        "energi": round(makanan["energi"] * faktor, 1),
        "protein": round(makanan["protein"] * faktor, 1),
        "karbo": round(makanan["karbo"] * faktor, 1),
        "lemak": round(makanan["lemak"] * faktor, 1),
    }


def hitung_porsi(makanan, jumlah_porsi):
    """Hitung gizi untuk ``jumlah_porsi`` porsi umum makanan."""
    if jumlah_porsi <= 0:
        raise ValueError("Jumlah porsi harus lebih dari 0.")
    return hitung_gizi(makanan, makanan["porsi_g"] * jumlah_porsi)


def total_gizi(daftar_hasil):
    """Jumlahkan gizi dari beberapa hasil hitung_gizi."""
    total = {"energi": 0.0, "protein": 0.0, "karbo": 0.0, "lemak": 0.0}
    for hasil in daftar_hasil:
        for kunci in total:
            total[kunci] += hasil[kunci]
    return {kunci: round(nilai, 1) for kunci, nilai in total.items()}


def format_hasil(hasil, makanan=None):
    """Format satu hasil hitung menjadi teks yang ramah dibaca."""
    baris = [f"{hasil['nama']} — {hasil['gram']:g} g"]
    if makanan is not None:
        baris[0] += f" ({makanan['porsi']})"
    baris.append(f"  Energi     : {hasil['energi']:g} kkal")
    baris.append(f"  Protein    : {hasil['protein']:g} g")
    baris.append(f"  Karbohidrat: {hasil['karbo']:g} g")
    baris.append(f"  Lemak      : {hasil['lemak']:g} g")
    return "\n".join(baris)
