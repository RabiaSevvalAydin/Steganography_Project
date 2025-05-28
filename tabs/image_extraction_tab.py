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
        
        # Sol panel - Görüntü önizlemeleri
        left_frame = ttk.LabelFrame(main_container, text="Görüntü Önizlemeleri", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Steganografik resim önizleme
        stego_label = ttk.Label(left_frame, text="Steganografik Resim:", font=('Arial', 10, 'bold'))
        stego_label.pack(pady=(0, 5))
        
        self.stego_image_preview = tk.Label(left_frame, bg="#f0f0f0", width=50, height=18, 
                                        text="Steganografik resim seçilmedi\n(İçinde gizli resim olan)")
        self.stego_image_preview.pack(pady=(0, 20))
        
        # Çıkarılan resim önizleme
        extracted_label = ttk.Label(left_frame, text="Çıkarılan Gizli Resim:", font=('Arial', 10, 'bold'))
        extracted_label.pack(pady=(0, 5))
        
        self.extracted_image_preview = tk.Label(left_frame, bg="#f0f0f0", width=50, height=18, 
                                            text="Çıkarılan resim burada görünecek")
        self.extracted_image_preview.pack()
        
        # Sağ panel - Kontroller
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.create_widgets(right_frame)
    
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
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="5")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=8, width=30, wrap=tk.WORD, font=('Arial', 8),
                           state=tk.DISABLED, bg="#f0f0f0")
        info_text.pack()
        
        # Bilgi metnini ekle
        info_content = ("• Steganografik resim, içinde gizli resim bulunan resimdir.\n\n"
                       "• Bu resim 'Resim Gizle' sekmesinde oluşturulmuş olmalıdır.\n\n"
                       "• Çıkarılan gizli resim otomatik olarak gösterilecektir.\n\n"
                       "• Çıkarılan resmi farklı formatlarda kaydedebilirsiniz.")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=15)
        
        # İşlem sonuç göstergesi
        self.result_var = tk.StringVar(value="Henüz işlem yapılmadı")
        result_label = ttk.Label(parent, textvariable=self.result_var, 
                                font=('Arial', 9, 'bold'), foreground='gray')
        result_label.pack(pady=5)
    
    def select_image(self):
        """Steganografik resim seçme fonksiyonu"""
        try:
            file_path = select_steganographic_image_for_extraction()
            
            if file_path:
                self.image_path = file_path
                self.steganographic_image = Image.open(file_path)
                
                # Steganografik resmi önizlemede göster
                display_image(self.steganographic_image, self.stego_image_preview, (400, 250))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Steganografik görüntü yüklendi")
                
                # Önceki çıkarılan resmi temizle
                self.extracted_image_preview.config(image="", text="Çıkarılan resim burada görünecek")
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
            
            # Çıkarılan resmi önizlemede göster
            display_image(self.extracted_image, self.extracted_image_preview, (400, 250))
            
            # Durum güncelle
            self.status_var.set("Gizli resim başarıyla çıkarıldı!")
            self.result_var.set("Resim başarıyla çıkarıldı! ✅")
            self.result_var.config = lambda **kwargs: None  # Renk değişimi için
            
            # Resim boyutları hakkında bilgi
            width, height = self.extracted_image.size
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
                
                messagebox.showinfo("Başarılı", 
                                  f"Çıkarılan resim başarıyla kaydedildi:\n{filename}\n\n"
                                  f"Dosya boyutu: {file_size_kb:.1f} KB\n"
                                  f"Resim boyutu: {self.extracted_image.size[0]}x{self.extracted_image.size[1]} piksel")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim kaydedilemedi")
