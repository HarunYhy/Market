# Market Otomasyonu (Market Automation System)

Proje, SQLite veritabanı altyapısı ve Python **Tkinter** grafik arayüzü (GUI) kullanılarak geliştirilmiş modern bir market satış ve stok/ürün yönetim otomasyonudur.

---

## 📌 Özellikler

### 🛒 1. Sepet ve Satış İşlemleri
* **Barkodlu Satış:** Ürün barkodu ve adet girilerek hızlıca sepete ekleme.
* **Klavye Desteği:** Barkod alanında `Enter` tuşuna basarak hızlı ürün ekleme.
* **Sepet Yönetimi:** Sepetteki ürünlerin adetini güncelleme, ürünü sepetten çıkarma veya sepeti tamamen boşaltma.
* **Otomatik Hesaplama:** Ürünlerin birim fiyatı, toplam fiyatı ve genel sepet tutarının anlık hesaplanması.
* **Alışveriş Tamamlama & Fiş:** Alışveriş tamamlandığında detaylı özet fiş gösterimi.

### 📦 2. Ürün ve Stok Yönetimi
* **Ürün Ekleme:** Barkod, ürün adı, fiyat, marka ve kategori bilgileriyle yeni ürün kaydı.
* **Ürün Güncelleme:** Seçilen ürünün fiyat bilgisi güncellemesi.
* **Ürün Silme:** Onay mekanizmalı ürün silme işlemi.
* **Dinamik Listeleme:** Kayıtlı ürünlerin kategori ve ürün adına göre sıralı listelenmesi.
* **Form Temizleme & Seçim:** Tablodan ürün seçildiğinde otomatik form doldurma.

---

## 🛠️ Teknolojiler ve Gereksinimler

* **Dil:** Python 3.x
* **Arayüz (GUI):** `tkinter`, `tkinter.ttk`
* **Veritabanı:** SQLite3 (`urunler.db`)

*Herhangi bir dış kütüphane kurulumu gerektirmez, Python dahili kütüphaneleri ile çalışır.*

---

## 📂 Proje Yapısı

```text
Market-main/
│
├── database.py   # SQLite veritabanı bağlantısı, tablo oluşturma ve CRUD fonksiyonları
├── market.py     # Tkinter GUI arayüzü, sepet yönetimi ve uygulama ana döngüsü
└── urunler.db    # Otomatik oluşturulan SQLite veritabanı dosyası
```

---

## 🚀 Çalıştırma

Projeyi çalıştırmak için ana dizinde terminal veya komut satırında aşağıdaki komutu uygulayın:

```bash
python market.py
```

---

## 💡 Veritabanı Şeması (`urunler`)

| Kolon Adı | Veri Tipi | Açıklama |
| :--- | :--- | :--- |
| `barkod` | INTEGER (PRIMARY KEY) | Ürünün benzersiz barkod numarası |
| `urunIsmi` | TEXT (NOT NULL) | Ürün adı |
| `fiyat` | FLOAT | Ürünün satış fiyatı |
| `marka` | TEXT | Ürünün markası |
| `kategori` | TEXT | Ürünün ait olduğu kategori |
