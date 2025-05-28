import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    extract_image_from_image, 
    select_steganographic_image_for_extraction,
    save_image_to_file,
    display_image
)
import os

class ImageExtractionTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.image_path = ""
        self.steganographic_image = None
        self.extracted_image = None
        self.create_tab()
    
    def create_tab(self):
        """Resim çıkarma tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="🎨 Resim Çıkar")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - SCROLLABLE Görüntü önizlemeleri
        left_outer_frame = ttk.LabelFrame(main_container, text="Görüntü Önizlemeleri", padding="5")
        left_outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas ve Scrollbar oluştur
        canvas = tk.Canvas(left_outer_frame, bg="#f8f8f8")
        scrollbar = ttk.Scrollbar(left_outer_frame, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = ttk.Frame(canvas)
        
        # Canvas'ı yapılandır
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            # Canvas genişliğini scrollable_frame'e uygula
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Canvas window oluştur ve referansını sakla
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Canvas ve scrollbar'ı yerleştir
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scroll desteği
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Scrollable frame içine resim önizlemelerini ekle
        self.create_image_previews(scrollable_frame)
        
        # Sağ panel - Kontroller (SABİT GENİŞLİK)
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        right_frame.configure(width=280)
        
        self.create_widgets(right_frame)
    
    def create_image_previews(self, parent):
        """Resim önizlemelerini oluştur (tam genişlik)"""
        
        # Steganografik resim önizleme
        stego_label = ttk.Label(parent, text="Steganografik Resim (Giriş):", font=('Arial', 10, 'bold'))
        stego_label.pack(fill=tk.X, pady=(5, 2))
        
        stego_frame = tk.Frame(parent, bg="#f0f0f0", relief="sunken", bd=1, height=250)
        stego_frame.pack(fill=tk.X, pady=(0, 15))
        stego_frame.pack_propagate(False)
        
        self.stego_image_preview = tk.Label(stego_frame, bg="#f0f0f0", 
                                          text="Steganografik resim seçilmedi\n(İçinde gizli resim olan ana resim)\n\nBuraya yüklenecek resim tam ekran görünecek",
                                          font=('Arial', 9), fg='gray')
        self.stego_image_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Çıkarılan resim önizleme
        extracted_label = ttk.Label(parent, text="Çıkarılan Gizli Resim (Çıkış):", font=('Arial', 10, 'bold'))
        extracted_label.pack(fill=tk.X, pady=(5, 2))
        
        extracted_frame = tk.Frame(parent, bg="#f0f0f0", relief="sunken", bd=1, height=250)
        extracted_frame.pack(fill=tk.X, pady=(0, 15))
        extracted_frame.pack_propagate(False)
        
        self.extracted_image_preview = tk.Label(extracted_frame, bg="#f0f0f0", 
                                               text="Çıkarılan gizli resim burada görünecek\n(Steganografik resimden çıkarılan orijinal resim)\n\nİşlem sonrası burada görünecek",
                                               font=('Arial', 9), fg='gray')
        self.extracted_image_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="İşlem Bilgisi", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, font=('Arial', 9),
                           state=tk.DISABLED, bg="#f9f9f9")
        info_text.pack(fill=tk.X)
        
        # Bilgi metnini ekle
        info_content = ("• Steganografik resim, içinde gizli resim bulunan resimdir.\n\n"
                       "• Bu resim 'Resim Gizle' sekmesinde oluşturulmuş olmalıdır.\n\n"
                       "• Çıkarılan gizli resim otomatik olarak gösterilecektir.\n\n"
                       "• Çıkarılan resmi farklı formatlarda kaydedebilirsiniz.")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Resim seçme butonu
        select_button = ttk.Button(parent, text="📁 Steganografik Resim Seç", 
                                  command=self.select_image, width=30)
        select_button.pack(pady=(0, 15))
        
        # Dosya yolu gösterme
        self.file_path_var = tk.StringVar(value="Dosya seçilmedi")
        path_label = ttk.Label(parent, textvariable=self.file_path_var, 
                              wraplength=250, font=('Arial', 8))
        path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Çıkar butonu
        extract_button = ttk.Button(parent, text="🔓 Gizli Resmi Çıkar", 
                                   command=self.extract_image, width=30)
        extract_button.pack(pady=(0, 20))
        
        # Kaydet butonu
        save_button = ttk.Button(parent, text="💾 Çıkarılan Resmi Kaydet", 
                                command=self.save_image, width=30)
        save_button.pack(pady=(0, 20))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)
        
        # İşlem durumu göstergesi
        status_frame = ttk.LabelFrame(parent, text="İşlem Durumu", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=(0, 5))
        
        # İşlem sonuç göstergesi
        self.result_var = tk.StringVar(value="Henüz işlem yapılmadı")
        result_label = ttk.Label(status_frame, textvariable=self.result_var, 
                                font=('Arial', 9, 'bold'), foreground='gray')
        result_label.pack(pady=5)
        
        # İstatistik göstergesi
        stats_frame = ttk.LabelFrame(parent, text="İstatistikler", padding="10")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_var = tk.StringVar(value="Henüz resim yüklenmedi")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, 
                               font=('Arial', 8), foreground='darkgreen')
        stats_label.pack()
    
    def select_image(self):
        """Steganografik resim seçme fonksiyonu"""
        try:
            file_path = select_steganographic_image_for_extraction()
            
            if file_path:
                self.image_path = file_path
                self.steganographic_image = Image.open(file_path)
                
                # Steganografik resmi önizlemede göster (daha büyük boyut)
                display_image(self.steganographic_image, self.stego_image_preview, (600, 240))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Steganografik görüntü yüklendi")
                
                # İstatistikleri güncelle
                width, height = self.steganographic_image.size
                file_size = os.path.getsize(file_path) / 1024
                self.stats_var.set(f"Boyut: {width}x{height}\nDosya: {file_size:.1f} KB\nFormat: {self.steganographic_image.mode}")
                
                # Önceki çıkarılan resmi temizle
                self.extracted_image_preview.config(image="", 
                                                   text="Çıkarılan gizli resim burada görünecek\n(Steganografik resimden çıkarılan orijinal resim)\n\nİşlem sonrası burada görünecek")
                self.extracted_image = None
                self.result_var.set("Henüz işlem yapılmadı")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Görüntü yüklenemedi")
    
    def extract_image(self):
        """Gizli resmi çıkarma fonksiyonu"""
        if not self.steganographic_image:
            messagebox.showwarning("Uyarı", "Lütfen önce steganografik bir resim seçin!")
            return
        
        try:
            # Resimden gizli resmi çıkar
            self.extracted_image = extract_image_from_image(self.steganographic_image)
            
            # Çıkarılan resmi önizlemede göster (daha büyük boyut)
            display_image(self.extracted_image, self.extracted_image_preview, (600, 240))
            
            # Durum güncelle
            self.status_var.set("Gizli resim başarıyla çıkarıldı!")
            self.result_var.set("Resim başarıyla çıkarıldı! ✅")
            
            # Resim boyutları hakkında bilgi
            width, height = self.extracted_image.size
            self.stats_var.set(f"Çıkarılan: {width}x{height}\nFormat: {self.extracted_image.mode}\nDurum: Hazır")
            
            messagebox.showinfo("Başarılı", 
                              f"Gizli resim başarıyla çıkarıldı!\n\n"
                              f"Çıkarılan resim boyutu: {width}x{height} piksel\n"
                              f"Resim formatı: {self.extracted_image.mode}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Resim çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim çıkarılamadı")
            self.result_var.set("İşlem başarısız! ❌")
    
    def save_image(self):
        """Çıkarılan resmi kaydetme fonksiyonu"""
        if not self.extracted_image:
            messagebox.showwarning("Uyarı", "Kaydedilecek çıkarılan resim bulunamadı!\nÖnce resim çıkarma işlemi yapın.")
            return
        
        try:
            file_path = save_image_to_file(self.extracted_image)
            
            if file_path:
                filename = os.path.basename(file_path)
                self.status_var.set(f"Resim kaydedildi: {filename}")
                
                # Dosya boyutu bilgisi
                file_size = os.path.getsize(file_path)
                file_size_kb = file_size / 1024
                
                # İstatistikleri güncelle
                width, height = self.extracted_image.size
                self.stats_var.set(f"Kaydedildi: {width}x{height}\nDosya: {file_size_kb:.1f} KB\nKonum: Kaydedildi")
                
                messagebox.showinfo("Başarılı", 
                                  f"Çıkarılan resim başarıyla kaydedildi:\n{filename}\n\n"
                                  f"Dosya boyutu: {file_size_kb:.1f} KB\n"
                                  f"Resim boyutu: {self.extracted_image.size[0]}x{self.extracted_image.size[1]} piksel")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim kaydedilemedi")
