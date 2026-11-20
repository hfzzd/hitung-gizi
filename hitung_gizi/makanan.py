"""Database makanan Indonesia.

Nilai gizi per 100 gram, mengacu pada Tabel Komposisi Pangan Indonesia
(TKPI) dan dibulatkan ke satu desimal. Angka adalah perkiraan untuk makanan
rumahan pada umumnya — cara masak memengaruhi nilai sebenarnya.

Setiap makanan punya porsi umum (``porsi_g`` + ``porsi``) supaya menghitung
tidak perlu timbangan: mis. 1 piring nasi putih = 150 g.
"""

MAKANAN = [
    # --- Makanan pokok ---
    {"nama": "Nasi putih", "kategori": "pokok", "energi": 175, "protein": 3.0, "karbo": 40.0, "lemak": 0.3, "porsi_g": 150, "porsi": "1 piring"},
    {"nama": "Nasi merah", "kategori": "pokok", "energi": 165, "protein": 3.5, "karbo": 35.0, "lemak": 1.5, "porsi_g": 150, "porsi": "1 piring"},
    {"nama": "Nasi uduk", "kategori": "pokok", "energi": 180, "protein": 3.4, "karbo": 31.0, "lemak": 4.5, "porsi_g": 150, "porsi": "1 piring"},
    {"nama": "Nasi goreng", "kategori": "pokok", "energi": 250, "protein": 6.0, "karbo": 40.0, "lemak": 7.0, "porsi_g": 200, "porsi": "1 piring"},
    {"nama": "Mie instan rebus", "kategori": "pokok", "energi": 170, "protein": 3.5, "karbo": 26.0, "lemak": 5.5, "porsi_g": 200, "porsi": "1 bungkus (masak)"},
    {"nama": "Mie goreng", "kategori": "pokok", "energi": 240, "protein": 6.0, "karbo": 34.0, "lemak": 9.0, "porsi_g": 200, "porsi": "1 piring"},
    {"nama": "Bihun goreng", "kategori": "pokok", "energi": 200, "protein": 5.0, "karbo": 30.0, "lemak": 7.0, "porsi_g": 200, "porsi": "1 piring"},
    {"nama": "Roti tawar putih", "kategori": "pokok", "energi": 248, "protein": 8.0, "karbo": 46.0, "lemak": 3.5, "porsi_g": 60, "porsi": "2 lembar"},
    {"nama": "Kentang rebus", "kategori": "pokok", "energi": 89, "protein": 1.9, "karbo": 20.0, "lemak": 0.1, "porsi_g": 150, "porsi": "1 buah sedang"},
    {"nama": "Ubi jalar rebus", "kategori": "pokok", "energi": 90, "protein": 1.3, "karbo": 21.0, "lemak": 0.1, "porsi_g": 150, "porsi": "1 buah sedang"},
    {"nama": "Singkong rebus", "kategori": "pokok", "energi": 146, "protein": 0.8, "karbo": 37.0, "lemak": 0.3, "porsi_g": 150, "porsi": "1 potong"},
    {"nama": "Jagung rebus", "kategori": "pokok", "energi": 96, "protein": 3.4, "karbo": 21.0, "lemak": 1.5, "porsi_g": 150, "porsi": "1 buah"},
    # --- Lauk ---
    {"nama": "Ayam goreng", "kategori": "lauk", "energi": 250, "protein": 28.0, "karbo": 1.0, "lemak": 14.0, "porsi_g": 85, "porsi": "1 potong"},
    {"nama": "Ayam panggang", "kategori": "lauk", "energi": 190, "protein": 27.0, "karbo": 0.0, "lemak": 8.0, "porsi_g": 85, "porsi": "1 potong"},
    {"nama": "Telur ayam rebus", "kategori": "lauk", "energi": 155, "protein": 13.0, "karbo": 1.1, "lemak": 11.0, "porsi_g": 50, "porsi": "1 butir"},
    {"nama": "Telur dadar", "kategori": "lauk", "energi": 200, "protein": 11.0, "karbo": 1.5, "lemak": 16.0, "porsi_g": 60, "porsi": "1 butir"},
    {"nama": "Ikan lele goreng", "kategori": "lauk", "energi": 220, "protein": 20.0, "karbo": 2.0, "lemak": 14.0, "porsi_g": 100, "porsi": "1 ekor"},
    {"nama": "Ikan bandeng goreng", "kategori": "lauk", "energi": 200, "protein": 20.0, "karbo": 1.0, "lemak": 12.0, "porsi_g": 100, "porsi": "1 potong"},
    {"nama": "Ikan tongkol", "kategori": "lauk", "energi": 115, "protein": 22.0, "karbo": 0.0, "lemak": 2.5, "porsi_g": 100, "porsi": "1 potong"},
    {"nama": "Udang goreng", "kategori": "lauk", "energi": 200, "protein": 20.0, "karbo": 3.0, "lemak": 11.0, "porsi_g": 100, "porsi": "5 ekor"},
    {"nama": "Tempe goreng", "kategori": "lauk", "energi": 220, "protein": 19.0, "karbo": 8.0, "lemak": 11.0, "porsi_g": 50, "porsi": "1 potong"},
    {"nama": "Tahu goreng", "kategori": "lauk", "energi": 120, "protein": 10.0, "karbo": 3.0, "lemak": 7.0, "porsi_g": 50, "porsi": "1 potong"},
    {"nama": "Daging sapi", "kategori": "lauk", "energi": 250, "protein": 26.0, "karbo": 0.0, "lemak": 15.0, "porsi_g": 100, "porsi": "1 potong"},
    {"nama": "Sate ayam", "kategori": "lauk", "energi": 220, "protein": 25.0, "karbo": 5.0, "lemak": 11.0, "porsi_g": 100, "porsi": "5 tusuk"},
    {"nama": "Rendang sapi", "kategori": "lauk", "energi": 350, "protein": 18.0, "karbo": 4.0, "lemak": 28.0, "porsi_g": 100, "porsi": "1 porsi kecil"},
    {"nama": "Bakso sapi", "kategori": "lauk", "energi": 150, "protein": 12.0, "karbo": 10.0, "lemak": 7.0, "porsi_g": 100, "porsi": "5 butir"},
    # --- Sayur & hidangan berkuah ---
    {"nama": "Sayur bayam", "kategori": "sayur", "energi": 25, "protein": 3.0, "karbo": 3.5, "lemak": 0.5, "porsi_g": 100, "porsi": "1 mangkuk"},
    {"nama": "Kangkung tumis", "kategori": "sayur", "energi": 60, "protein": 3.0, "karbo": 5.0, "lemak": 4.0, "porsi_g": 100, "porsi": "1 porsi"},
    {"nama": "Sayur sop", "kategori": "sayur", "energi": 50, "protein": 2.0, "karbo": 8.0, "lemak": 1.0, "porsi_g": 150, "porsi": "1 mangkuk"},
    {"nama": "Capcay", "kategori": "sayur", "energi": 100, "protein": 5.0, "karbo": 10.0, "lemak": 5.0, "porsi_g": 150, "porsi": "1 porsi"},
    {"nama": "Gado-gado", "kategori": "sayur", "energi": 150, "protein": 6.0, "karbo": 12.0, "lemak": 9.0, "porsi_g": 200, "porsi": "1 porsi"},
    {"nama": "Soto ayam", "kategori": "sayur", "energi": 120, "protein": 10.0, "karbo": 8.0, "lemak": 5.0, "porsi_g": 250, "porsi": "1 mangkuk"},
    {"nama": "Pecel", "kategori": "sayur", "energi": 130, "protein": 6.0, "karbo": 12.0, "lemak": 7.0, "porsi_g": 150, "porsi": "1 porsi"},
    # --- Buah ---
    {"nama": "Pisang", "kategori": "buah", "energi": 89, "protein": 1.1, "karbo": 23.0, "lemak": 0.3, "porsi_g": 100, "porsi": "1 buah"},
    {"nama": "Apel", "kategori": "buah", "energi": 52, "protein": 0.3, "karbo": 14.0, "lemak": 0.2, "porsi_g": 100, "porsi": "1 buah"},
    {"nama": "Jeruk", "kategori": "buah", "energi": 47, "protein": 0.9, "karbo": 12.0, "lemak": 0.1, "porsi_g": 100, "porsi": "1 buah"},
    {"nama": "Mangga", "kategori": "buah", "energi": 60, "protein": 0.8, "karbo": 15.0, "lemak": 0.4, "porsi_g": 100, "porsi": "1 buah"},
    {"nama": "Pepaya", "kategori": "buah", "energi": 43, "protein": 0.5, "karbo": 11.0, "lemak": 0.1, "porsi_g": 100, "porsi": "1 buah"},
    {"nama": "Alpukat", "kategori": "buah", "energi": 160, "protein": 2.0, "karbo": 9.0, "lemak": 15.0, "porsi_g": 100, "porsi": "1 buah"},
    # --- Minuman ---
    {"nama": "Susu sapi full cream", "kategori": "minuman", "energi": 61, "protein": 3.2, "karbo": 4.8, "lemak": 3.3, "porsi_g": 200, "porsi": "1 gelas"},
    {"nama": "Teh manis", "kategori": "minuman", "energi": 40, "protein": 0.0, "karbo": 10.0, "lemak": 0.0, "porsi_g": 200, "porsi": "1 gelas"},
    {"nama": "Kopi susu gula", "kategori": "minuman", "energi": 60, "protein": 1.0, "karbo": 10.0, "lemak": 2.0, "porsi_g": 200, "porsi": "1 gelas"},
    {"nama": "Jus alpukat gula", "kategori": "minuman", "energi": 120, "protein": 1.0, "karbo": 20.0, "lemak": 4.0, "porsi_g": 200, "porsi": "1 gelas"},
    # --- Camilan ---
    {"nama": "Kerupuk", "kategori": "camilan", "energi": 400, "protein": 4.0, "karbo": 60.0, "lemak": 15.0, "porsi_g": 25, "porsi": "1 genggam"},
    {"nama": "Bakwan goreng", "kategori": "camilan", "energi": 200, "protein": 4.0, "karbo": 25.0, "lemak": 10.0, "porsi_g": 50, "porsi": "1 buah"},
    {"nama": "Tahu isi goreng", "kategori": "camilan", "energi": 150, "protein": 6.0, "karbo": 15.0, "lemak": 8.0, "porsi_g": 50, "porsi": "1 buah"},
]

KATEGORI = ["pokok", "lauk", "sayur", "buah", "minuman", "camilan"]


def semua():
    """Semua makanan, diurutkan berdasarkan nama."""
    return sorted(MAKANAN, key=lambda m: m["nama"])


def berdasarkan_kategori(kategori):
    """Makanan dalam satu kategori, diurutkan berdasarkan nama."""
    kategori = kategori.strip().lower()
    return [m for m in semua() if m["kategori"] == kategori]


def cari(kata):
    """Cari makanan berdasarkan nama.

    Semua kata kunci harus muncul (sebagai substring) di nama makanan,
    tanpa memperhatikan huruf besar/kecil. Hasil diurutkan berdasarkan nama.
    """
    token = [t for t in kata.strip().lower().split() if t]
    if not token:
        return []
    hasil = []
    for m in MAKANAN:
        nama = m["nama"].lower()
        if all(t in nama for t in token):
            hasil.append(m)
    return sorted(hasil, key=lambda m: m["nama"])


def dapat(nama):
    """Cari satu makanan dengan nama persis (tanpa memperhatikan huruf).

    Mengembalikan dict makanan, atau None bila tidak ada.
    """
    target = nama.strip().lower()
    for m in MAKANAN:
        if m["nama"].lower() == target:
            return m
    return None
