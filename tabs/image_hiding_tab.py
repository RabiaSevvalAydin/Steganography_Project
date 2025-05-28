import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    embed_image_to_image, 
    select_input_image, 
    select_second_image,
    display_image
)
import os

class ImageHidingTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.main_image_path = ""
        self.secret_image_path = ""
        self.main_image = None
        self.secret_image = None
        self.result_image = None
        self.create_tab()
    
    def create_tab(self):
        """Resim gizleme tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="🎨 Resim Gizle")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Görüntü önizlemeleri (EXPAND=True)
        left_frame = ttk.LabelFrame(main_container, text="Görüntü Önizlemeleri", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Ana resim önizleme - DİNAMİK BOYUT
        main_label = ttk.Label(left_frame, text="Ana Resim (Örtü):", font=('Arial', 10, 'bold'))
        main_label.pack(pady=(0, 5))
        
        # Frame içinde label (daha iyi kontrol için)
        main_frame = tk.Frame(left_frame, bg="#f0f0f0", relief="sunken", bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.main_image_preview = tk.Label(main_frame, bg="#f0f0f0", 
                                        text="Ana resim seçilmedi\n(Gizli resmin üzerine bindirilecek resim)",
                                        font=('Arial', 9), fg='gray')
        self.main_image_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Gizli resim önizleme - DİNAMİK BOYUT
        secret_label = ttk.Label(left_frame, text="Gizlenecek Resim:", font=('Arial', 10, 'bold'))
        secret_label.pack(pady=(0, 5))
        
        secret_frame = tk.Frame(left_frame, bg="#f0f0f0", relief="sunken", bd=2)
        secret_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.secret_image_preview = tk.Label(secret_frame, bg="#f0f0f0", 
                                            text="Gizlenecek resim seçilmedi\n(Ana resmin içine gizlenecek resim)",
                                            font=('Arial', 9), fg='gray')
        self.secret_image_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sonuç resim önizleme - DİNAMİK BOYUT
        result_label = ttk.Label(left_frame, text="Sonuç (Steganografik Resim):", font=('Arial', 10, 'bold'))
        result_label.pack(pady=(0, 5))
        
        result_frame = tk.Frame(left_frame, bg="#f0f0f0", relief="sunken", bd=2)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_image_preview = tk.Label(result_frame, bg="#f0f0f0", 
                                        text="Steganografik resim burada görünecek\n(İşlem sonrası oluşan resim)",
                                        font=('Arial', 9), fg='gray')
        self.result_image_preview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sağ panel - Kontroller (SABİT GENİŞLİK)
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)  # Boyut sabitlenmesi için
        right_frame.configure(width=280)   # Sabit genişlik
        
        self.create_widgets(right_frame)

    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Ana resim seçme
        main_button = ttk.Button(parent, text="📁 Ana Resmi Seç (Örtü)", 
                                command=self.select_main_image, width=25)
        main_button.pack(pady=(0, 10))
        
        self.main_file_var = tk.StringVar(value="Ana resim seçilmedi")
        main_path_label = ttk.Label(parent, textvariable=self.main_file_var, 
                                   wraplength=200, font=('Arial', 8))
        main_path_label.pack(pady=(0, 15))
        
        # Gizli resim seçme
        secret_button = ttk.Button(parent, text="🔒 Gizlenecek Resmi Seç", 
                                  command=self.select_secret_image, width=25)
        secret_button.pack(pady=(0, 10))
        
        self.secret_file_var = tk.StringVar(value="Gizli resim seçilmedi")
        secret_path_label = ttk.Label(parent, textvariable=self.secret_file_var, 
                                     wraplength=200, font=('Arial', 8))
        secret_path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)
        
        # Gizle butonu
        hide_button = ttk.Button(parent, text="🔐 Resmi Gizle", 
                                command=self.hide_image, width=25)
        hide_button.pack(pady=(0, 15))
        
        # Kaydet butonu
        save_button = ttk.Button(parent, text="💾 Steganografik Resmi Kaydet", 
                                command=self.save_result, width=25)
        save_button.pack(pady=(0, 20))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="5")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=6, width=25, wrap=tk.WORD, font=('Arial', 8),
                           state=tk.DISABLED, bg="#f0f0f0")
        info_text.pack()
        
        # Bilgi metnini ekle
        info_content = ("• Ana resim: Gizli resmin üzerine bindirilecek görüntü\n\n"
                       "• Gizli resim: Ana resmin içine saklanacak görüntü\n\n"
                       "• Sonuç: Her iki resmi de içeren steganografik görüntü")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=15)
    
    def select_main_image(self):
        """Ana resim seçme fonksiyonu"""
        try:
            file_path = select_input_image()
            
            if file_path:
                self.main_image_path = file_path
                self.main_image = Image.open(file_path)
                
                # Ana resmi önizlemede göster - DİNAMİK BOYUT (max 600x350)
                display_image(self.main_image, self.main_image_preview, (600, 350))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.main_file_var.set(f"Ana: {filename}")
                self.status_var.set(f"Ana resim yüklendi ({self.main_image.size[0]}x{self.main_image.size[1]})")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ana resim yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Ana resim yüklenemedi")
    
    def select_secret_image(self):
        """Gizli resim seçme fonksiyonu"""
        try:
            file_path = select_second_image()
            
            if file_path:
                self.secret_image_path = file_path
                self.secret_image = Image.open(file_path)
                
                # Gizli resmi önizlemede göster - DİNAMİK BOYUT (max 600x350)
                display_image(self.secret_image, self.secret_image_preview, (600, 350))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.secret_file_var.set(f"Gizli: {filename}")
                self.status_var.set(f"Gizli resim yüklendi ({self.secret_image.size[0]}x{self.secret_image.size[1]})")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Gizli resim yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Gizli resim yüklenemedi")

    def hide_image(self):
        """Resim gizleme işlemi"""
        if not self.main_image or not self.secret_image:
            messagebox.showwarning("Uyarı", "Lütfen hem ana resmi hem de gizlenecek resmi seçin!")
            return
        
        try:
            # Resmi gizle
            self.result_image = embed_image_to_image(self.main_image, self.secret_image)
            
            # Sonuç resmi önizlemede göster - DİNAMİK BOYUT (max 600x350)
            display_image(self.result_image, self.result_image_preview, (600, 350))
            
            self.status_var.set("Resim başarıyla gizlendi!")
            
            # Boyut bilgisi
            main_size = self.main_image.size
            secret_size = self.secret_image.size
            result_size = self.result_image.size
            
            messagebox.showinfo("Başarılı", 
                            f"Resim gizleme işlemi tamamlandı!\n\n"
                            f"Ana resim: {main_size[0]}x{main_size[1]}\n"
                            f"Gizli resim: {secret_size[0]}x{secret_size[1]}\n"
                            f"Sonuç resim: {result_size[0]}x{result_size[1]}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Resim gizleme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim gizlenemedi")
            
    def save_result(self):
        """Sonuç resmini kaydetme fonksiyonu"""
        if not self.result_image:
            messagebox.showwarning("Uyarı", "Kaydedilecek steganografik resim bulunamadı!\nÖnce resim gizleme işlemi yapın.")
            return
        
        try:
            from functions.steganography_functions import save_image_to_file
            file_path = save_image_to_file(self.result_image)
            
            if file_path:
                filename = os.path.basename(file_path)
                self.status_var.set(f"Kaydedildi: {filename}")
                
                # Dosya boyutu bilgisi
                file_size = os.path.getsize(file_path)
                file_size_kb = file_size / 1024
                
                messagebox.showinfo("Başarılı", 
                                  f"Steganografik resim başarıyla kaydedildi:\n{filename}\n\n"
                                  f"Dosya boyutu: {file_size_kb:.1f} KB\n"
                                  f"Resim boyutu: {self.result_image.size[0]}x{self.result_image.size[1]} piksel")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim kaydedilemedi")
