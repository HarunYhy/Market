import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database import urunEkle, urunListele, urunGuncelleme, urunSilme, urunBilgi

# --- Arayüz Sınıfı ---
class MarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Otomasyonu")
        self.root.geometry("800x600")
        # Pencereyi işletim sisteminde tam ekran (maximized) olarak başlatır
        self.root.state('zoomed')
        
        # Tema ve Stil Ayarları
        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        # Arayüzü ayırt edilebilir ve modern yapmak için özel renk ayarları
        self.style.configure(".", background="#f4f4f9", foreground="#2f3542", font=("Helvetica", 10))
        self.style.configure("TFrame", background="#f4f4f9")
        self.style.configure("TLabelframe", background="#f4f4f9", borderwidth=2)
        self.style.configure("TLabelframe.Label", font=("Helvetica", 11, "bold"), background="#f4f4f9", foreground="#2f3542")
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#ced6e0", foreground="#2f3542")
        self.style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", rowheight=25, borderwidth=1)
        self.style.map("Treeview", background=[("selected", "#1e90ff")], foreground=[("selected", "white")])
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), background="#dfe4ea", padding=5)
        self.style.map("TButton", background=[("active", "#ced6e0")])
            
        self.sepet = {}  # barkod: [urunAd, marka, adet, fiyat]
        
        self.create_widgets()

    def create_widgets(self):
        # Sekmeler için Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sepet Sekmesi (İlk Sekme)
        self.tab_sepet = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sepet, text="Sepet İşlemleri")

        # Ürün Yönetimi Sekmesi (İkinci Sekme)
        self.tab_urun = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_urun, text="Ürün Yönetimi")
        
        self.setup_sepet_tab()
        self.setup_urun_tab()

    def setup_urun_tab(self):
        # Sol taraf form
        form_frame = ttk.LabelFrame(self.tab_urun, text="Ürün İşlemleri")
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ttk.Label(form_frame, text="Barkod:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ent_barkod = ttk.Entry(form_frame)
        self.ent_barkod.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Ürün Adı:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ent_urun_ad = ttk.Entry(form_frame)
        self.ent_urun_ad.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Fiyat:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.ent_fiyat = ttk.Entry(form_frame)
        self.ent_fiyat.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Marka:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ent_marka = ttk.Entry(form_frame)
        self.ent_marka.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Kategori:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.ent_kategori = ttk.Entry(form_frame)
        self.ent_kategori.grid(row=4, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Ekle", command=self.ui_urun_ekle).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Güncelle", command=self.ui_urun_guncelle).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sil", command=self.ui_urun_sil).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Temizle", command=self.ui_form_temizle).pack(side="left", padx=5)
        
        # Sağ taraf Liste
        list_frame = ttk.LabelFrame(self.tab_urun, text="Ürün Listesi")
        list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        columns = ("barkod", "urun_ismi", "fiyat", "marka", "kategori")
        self.tree_urunler = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree_urunler.heading("barkod", text="Barkod")
        self.tree_urunler.heading("urun_ismi", text="Ürün Adı")
        self.tree_urunler.heading("fiyat", text="Fiyat")
        self.tree_urunler.heading("marka", text="Marka")
        self.tree_urunler.heading("kategori", text="Kategori")
        
        self.tree_urunler.column("barkod", width=80)
        self.tree_urunler.column("urun_ismi", width=150)
        self.tree_urunler.column("fiyat", width=80)
        self.tree_urunler.column("marka", width=100)
        self.tree_urunler.column("kategori", width=100)
        
        self.tree_urunler.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_urunler.bind('<<TreeviewSelect>>', self.ui_urun_sec)
        
        self.ui_liste_yenile()

    def setup_sepet_tab(self):
        # Sepete ekleme alanı
        top_frame = ttk.Frame(self.tab_sepet)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(top_frame, text="Barkod:").pack(side="left", padx=5)
        self.ent_sepet_barkod = ttk.Entry(top_frame, width=15)
        self.ent_sepet_barkod.pack(side="left", padx=5)
        self.ent_sepet_barkod.bind("<Return>", lambda event: self.ui_sepete_ekle())
        
        ttk.Label(top_frame, text="Adet:").pack(side="left", padx=5)
        self.ent_sepet_adet = ttk.Entry(top_frame, width=5)
        self.ent_sepet_adet.pack(side="left", padx=5)
        self.ent_sepet_adet.insert(0, "1")
        
        ttk.Button(top_frame, text="Sepete Ekle", command=self.ui_sepete_ekle).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Sepetten Çıkar", command=self.ui_sepetten_cikar).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Adeti Güncelle", command=self.ui_sepet_adet_guncelle).pack(side="left", padx=5)
        
        # Sepet Listesi
        list_frame = ttk.LabelFrame(self.tab_sepet, text="Sepettekiler")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("barkod", "urun_ismi", "marka", "adet", "birim_fiyat", "toplam")
        self.tree_sepet = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree_sepet.heading("barkod", text="Barkod")
        self.tree_sepet.heading("urun_ismi", text="Ürün Adı")
        self.tree_sepet.heading("marka", text="Marka")
        self.tree_sepet.heading("adet", text="Adet")
        self.tree_sepet.heading("birim_fiyat", text="Birim Fiyat")
        self.tree_sepet.heading("toplam", text="Toplam Fiyat")
        
        self.tree_sepet.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_sepet.bind('<<TreeviewSelect>>', self.ui_sepet_sec)
        
        # Alt Kısım
        bottom_frame = ttk.Frame(self.tab_sepet)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        self.lbl_genel_toplam = ttk.Label(bottom_frame, text="Genel Toplam: 0.00 TL", font=("Arial", 14, "bold"))
        self.lbl_genel_toplam.pack(side="left")
        
        ttk.Button(bottom_frame, text="Sepeti Boşalt", command=self.ui_sepet_temizle).pack(side="right", padx=5)
        ttk.Button(bottom_frame, text="Alışverişi Tamamla", command=self.ui_alisveris_tamamla).pack(side="right", padx=5)

    # --- Ürün Yönetimi Metotları ---
    def ui_liste_yenile(self):
        for item in self.tree_urunler.get_children():
            self.tree_urunler.delete(item)
            
        urunler = urunListele()
        for u in urunler:
            self.tree_urunler.insert("", "end", values=u)

    def ui_form_temizle(self):
        self.ent_barkod.config(state="normal")
        self.ent_barkod.delete(0, tk.END)
        self.ent_urun_ad.delete(0, tk.END)
        self.ent_fiyat.delete(0, tk.END)
        self.ent_marka.delete(0, tk.END)
        self.ent_kategori.delete(0, tk.END)

    def ui_urun_sec(self, event):
        selected = self.tree_urunler.selection()
        if selected:
            item = self.tree_urunler.item(selected[0])
            values = item['values']
            
            self.ui_form_temizle()
            self.ent_barkod.insert(0, values[0])
            self.ent_barkod.config(state="readonly")
            self.ent_urun_ad.insert(0, values[1])
            self.ent_fiyat.insert(0, values[2])
            self.ent_marka.insert(0, values[3])
            self.ent_kategori.insert(0, values[4])

    def ui_urun_ekle(self):
        try:
            barkod = int(self.ent_barkod.get())
            ad = self.ent_urun_ad.get().title()
            fiyat = float(self.ent_fiyat.get())
            marka = self.ent_marka.get().title()
            kategori = self.ent_kategori.get().title()
            
            if not ad or not marka or not kategori:
                messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")
                return
                
            urunEkle(barkod, ad, fiyat, marka, kategori)
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi.")
            self.ui_liste_yenile()
            self.ui_form_temizle()
        except ValueError:
            messagebox.showerror("Hata", "Barkod tam sayı, fiyat ondalıklı veya tam sayı olmalıdır.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu barkoda sahip bir ürün zaten var.")

    def ui_urun_guncelle(self):
        try:
            barkod_str = self.ent_barkod.get()
            if not barkod_str:
                return
            barkod = int(barkod_str)
            fiyat = float(self.ent_fiyat.get())
            
            etkilenen = urunGuncelleme(barkod, fiyat)
            if etkilenen > 0:
                messagebox.showinfo("Başarılı", "Ürün fiyatı güncellendi.")
            else:
                messagebox.showwarning("Hata", "Bu barkoda ait ürün bulunamadı.")
            self.ui_liste_yenile()
            self.ui_form_temizle()
        except ValueError:
            messagebox.showerror("Hata", "Lütfen barkod ve fiyatı kontrol ediniz.")

    def ui_urun_sil(self):
        try:
            barkod_str = self.ent_barkod.get()
            if not barkod_str:
                messagebox.showwarning("Uyarı", "Lütfen silinecek ürünü listeden seçin veya barkodunu girin.")
                return
            barkod = int(barkod_str)
            cevap = messagebox.askyesno("Onay", f"{barkod} barkodlu ürünü silmek istediğinize emin misiniz?")
            if cevap:
                etkilenen = urunSilme(barkod)
                if etkilenen > 0:
                    messagebox.showinfo("Başarılı", "Ürün silindi.")
                else:
                    messagebox.showwarning("Hata", "Bu barkoda ait ürün bulunamadı.")
                self.ui_liste_yenile()
                self.ui_form_temizle()
        except ValueError:
             messagebox.showerror("Hata", "Lütfen geçerli bir barkod numarası girin.")

    # --- Sepet Metotları ---
    def ui_sepet_sec(self, event):
        selected = self.tree_sepet.selection()
        if selected:
            item = self.tree_sepet.item(selected[0])
            values = item['values']
            
            self.ent_sepet_barkod.delete(0, tk.END)
            self.ent_sepet_barkod.insert(0, values[0])
            
            self.ent_sepet_adet.delete(0, tk.END)
            self.ent_sepet_adet.insert(0, values[3])

    def ui_sepet_adet_guncelle(self):
        try:
            barkod = int(self.ent_sepet_barkod.get())
            adet_str = self.ent_sepet_adet.get()
            adet = int(adet_str) if adet_str else 1
            if adet <= 0:
                if barkod in self.sepet:
                    del self.sepet[barkod]
            else:
                if barkod in self.sepet:
                    self.sepet[barkod][2] = adet
                else:
                    messagebox.showerror("Hata", "Ürün sepette yok!")
            
            self.ent_sepet_barkod.delete(0, tk.END)
            self.ent_sepet_adet.delete(0, tk.END)
            self.ent_sepet_adet.insert(0, "1")
            self.ui_sepet_yenile()
        except ValueError:
             messagebox.showerror("Hata", "Geçerli bir barkod ve adet giriniz.")

    def ui_sepet_yenile(self):
        for item in self.tree_sepet.get_children():
            self.tree_sepet.delete(item)
            
        genel_toplam = 0
        for b_kod, x in self.sepet.items():
            toplam_fiyat = x[2] * x[3]
            genel_toplam += toplam_fiyat
            self.tree_sepet.insert("", "end", values=(b_kod, x[0], x[1], x[2], f"{x[3]:.2f}", f"{toplam_fiyat:.2f}"))
            
        self.lbl_genel_toplam.config(text=f"Genel Toplam: {genel_toplam:.2f} TL")

    def ui_sepete_ekle(self):
        try:
            barkod = int(self.ent_sepet_barkod.get())
            adet_str = self.ent_sepet_adet.get()
            adet = int(adet_str) if adet_str else 1
            if adet <= 0:
                messagebox.showwarning("Uyarı", "Adet 0'dan büyük olmalıdır.")
                return

            if barkod in self.sepet:
                self.sepet[barkod][2] += adet
            else:
                bilgi = urunBilgi(barkod)
                if bilgi:
                    self.sepet[barkod] = [bilgi[1], bilgi[3], adet, bilgi[2]]
                else:
                    messagebox.showerror("Hata", "Ürün bulunamadı!")
            
            self.ent_sepet_barkod.delete(0, tk.END)
            self.ent_sepet_adet.delete(0, tk.END)
            self.ent_sepet_adet.insert(0, "1")
            self.ui_sepet_yenile()
        except ValueError:
             messagebox.showerror("Hata", "Geçerli bir barkod ve adet giriniz.")

    def ui_sepetten_cikar(self):
        try:
            barkod = int(self.ent_sepet_barkod.get())
            adet_str = self.ent_sepet_adet.get()
            adet = int(adet_str) if adet_str else 1
            if adet <= 0:
                messagebox.showwarning("Uyarı", "Adet 0'dan büyük olmalıdır.")
                return

            if barkod in self.sepet:
                self.sepet[barkod][2] -= adet
                if self.sepet[barkod][2] <= 0:
                    del self.sepet[barkod]
            else:
                messagebox.showerror("Hata", "Ürün sepette yok!")
                
            self.ent_sepet_barkod.delete(0, tk.END)
            self.ent_sepet_adet.delete(0, tk.END)
            self.ent_sepet_adet.insert(0, "1")
            self.ui_sepet_yenile()
        except ValueError:
             messagebox.showerror("Hata", "Geçerli bir barkod ve adet giriniz.")

    def ui_sepet_temizle(self):
        self.sepet.clear()
        self.ui_sepet_yenile()

    def ui_alisveris_tamamla(self):
        if not self.sepet:
            messagebox.showwarning("Uyarı", "Sepet boş!")
            return
            
        fis = " MARKET FİŞİ \n" + "-"*40 + "\n"
        genel_toplam = 0
        for b, x in self.sepet.items():
            toplam_f = x[2] * x[3]
            genel_toplam += toplam_f
            fis += f"{x[0][:15]:<15} {x[2]}x{x[3]:.2f} = {toplam_f:.2f}\n"
            
        fis += "-"*40 + f"\nTOPLAM: {genel_toplam:.2f} TL"
        
        messagebox.showinfo("Alışveriş Tamamlandı", fis)
        self.ui_sepet_temizle()

if __name__ == "__main__":
    root = tk.Tk()
    app = MarketApp(root)
    root.mainloop()
