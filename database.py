import sqlite3

# --- Veritabanı Bağlantısı ---
conn = sqlite3.connect("urunler.db")
cursor = conn.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS urunler(
                barkod INTEGER PRIMARY KEY,
                urunIsmi TEXT NOT NULL,
                fiyat FLOAT,
                marka TEXT,
                kategori TEXT)
               """)
conn.commit()

def urunEkle(barkod, urunAd, fiyat, marka, kategori):
    cursor.execute("""
                INSERT INTO urunler(barkod,urunIsmi,fiyat,marka,kategori)
                VALUES(?,?,?,?,?)""", (barkod, urunAd, fiyat, marka, kategori))
    conn.commit()

def urunListele():
    cursor.execute("SELECT * FROM urunler ORDER BY kategori ASC, urunIsmi ASC")
    return cursor.fetchall()

def urunGuncelleme(barkod, fiyat):
    cursor.execute("UPDATE urunler SET fiyat=? WHERE barkod=?", (fiyat, barkod))
    conn.commit()
    return cursor.rowcount

def urunSilme(barkod):
    cursor.execute("DELETE FROM urunler WHERE barkod=?", (barkod,))
    conn.commit()
    return cursor.rowcount

def urunBilgi(barkod):
    cursor.execute("SELECT barkod, urunIsmi, fiyat, marka, kategori FROM urunler WHERE barkod = ?", (barkod,))
    bilgi = cursor.fetchone()
    if bilgi:
        return bilgi
    else:
        return None
