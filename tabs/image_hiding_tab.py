import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    embed_image_to_image, 
    extract_image_from_image, 
    select_input_image,
    select_second_image,
    display_image
)
import os

class ImageHidingTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.main_image_path = ""
        self.hidden_image_path = ""
        self.main_image = None
        self.hidden_image = None
        self.output_image = None
        self.create_tab()
    
    def create_tab(self):
        """Resim gizleme tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="🖼️ Resim Gizle")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Görüntü önizlemeleri
        left_frame = ttk.LabelFrame(main_container, text="Görüntü Önizlemeleri", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Ana resim önizleme
        main_label = ttk.Label(left_frame, text="Ana Resim:", font=('Arial', 10, 'bold'))
        main_label.pack(pady=(0, 5))
        
        self.main_image_preview = tk.Label(left_frame, bg="#e0e0e0", width=40, height=15, 
                                          text="Ana resim seçilmedi")
        self.main_image_preview.pack(pady=(0, 15))
        
        # Gizlenecek resim önizleme
        hidden_label = ttk.Label(left_frame, text="Gizlenecek Resim:", font=('Arial', 10, 'bold'))
        hidden_label.pack(pady=(0, 5))
        
        self.hidden_image_preview = tk.Label(left_frame, bg="#e0e0e0", width=40, height=15, 
                                            text="Gizlenecek resim seçilmedi")
        self.hidden_image_preview.pack(pady=(0, 15))
        
        # Sonuç önizleme
        result_label = ttk.Label(left_frame, text="Sonuç:", font=('Arial', 10, 'bold'))
        result_label.pack(pady=(0, 5))
        
        self.result_preview = tk.Label(left_frame, bg="#e0e0e0", width=40, height=15, 
                                      text="İşlem sonucu burada görünecek")
        self.result_preview.pack()
        
        # Sağ panel - Kontroller
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.create_widgets(right_frame)
    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Ana resim seçme
        main_image_button = ttk.Button(parent, text="📁 Ana Resim Seç", 
                                      command=self.select_main_image, width=25)
        main_image_button.pack(pady=(0, 10))
        
        # Ana resim dosya yolu
        self.main_file_var = tk.StringVar(value="Ana resim seçilmedi")
        main_path_label = ttk.Label(parent, textvariable=self.main_file_var, 
                                   wraplength=200, font=('Arial', 8))
        main_path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Gizlenecek resim seçme
        hidden_image_button = ttk.Button(parent, text="🖼️ Gizlenecek Resim Seç", 
                                        command=self.select_hidden_image, width=25)
        hidden_image_button.pack(pady=(0, 10))
        
        # Gizlenecek resim dosya yolu
        self.hidden_file_var = tk.StringVar(value="Gizlenecek resim seçilmedi")
        hidden_path_label = ttk.Label(parent, textvariable=self.hidden_file_var, 
                                     wraplength=200, font=('Arial', 8))
        hidden_path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)
        
        # İşlem butonları
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        hide_button = ttk.Button(button_frame, text="🔒 Resmi Gizle", 
                                command=self.hide_image, width=25)
        hide_button.pack(pady=5)
        
        extract_button = ttk.Button(button_frame, text="🔓 Resmi Çıkar", 
                                   command=self.extract_image, width=25)
        extract_button.pack(pady=5)
        
        save_button = ttk.Button(button_frame, text="💾 Sonucu Kaydet", 
                                command=self.save_image, width=25)
        save_button.pack(pady=5)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=15)
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="5")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=6, width=25, wrap=tk.WORD, font=('Arial', 8))
        info_text.pack()
        info_text.insert("1.0", "• Ana resim, gizlenecek resmi içerecek olan resimdir.\n\n"
                                "• Gizlenecek resim, ana resim içine saklanacak resimdir.\n\n"
                                "• Gizlenecek resim otomatik olarak ana resim boyutuna uyarlanır.")
        info_text.config(state=tk.DISABLED)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=10)
    
    def select_main_image(self):
        """Ana resim seçme fonksiyonu"""
        try:
            file_path = select_input_image()
            
            if file_path:
                self.main_image_path = file_path
                self.main_image = Image.open(file_path)
                
                # Ana resmi önizlemede göster
                display_image(self.main_image, self.main_image_preview, (300, 200))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.main_file_var.set(f"Ana resim: {filename}")
                self.status_var.set("Ana resim yüklendi")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ana resim yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Ana resim yüklenemedi")
    
    def select_hidden_image(self):
        """Gizlenecek resim seçme fonksiyonu"""
        try:
            file_path = select_second_image()
            
            if file_path:
                self.hidden_image_path = file_path
                self.hidden_image = Image.open(file_path)
                
                # Gizlenecek resmi önizlemede göster
                display_image(self.hidden_image, self.hidden_image_preview, (300, 200))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.hidden_file_var.set(f"Gizlenecek: {filename}")
                self.status_var.set("Gizlenecek resim yüklendi")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Gizlenecek resim yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Gizlenecek resim yüklenemedi")
    
    def hide_image(self):
        """Resim gizleme fonksiyonu"""
        if not self.main_image:
            messagebox.showwarning("Uyarı", "Lütfen önce ana resmi seçin!")
            return
        
        if not self.hidden_image:
            messagebox.showwarning("Uyarı", "Lütfen gizlenecek resmi seçin!")
            return
        
        try:
            # Resmi ana resme gizle
            self.output_image = embed_image_to_image(self.main_image, self.hidden_image)
            
            # Sonucu önizlemede göster
            display_image(self.output_image, self.result_preview, (300, 200))
            
            self.status_var.set("Resim başarıyla gizlendi!")
            messagebox.showinfo("Başarılı", "Resim ana resme başarıyla gizlendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Resim gizleme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim gizlenemedi")
    
    def extract_image(self):
        """Gizli resmi çıkarma fonksiyonu"""
        if not self.main_image:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        try:
            # Resimden gizli resmi çıkar
            extracted_image = extract_image_from_image(self.main_image)
            
            # Çıkarılan resmi önizlemede göster
            display_image(extracted_image, self.result_preview, (300, 200))
            
            # Çıkarılan resmi sakla
            self.output_image = extracted_image
            
            self.status_var.set("Gizli resim başarıyla çıkarıldı!")
            messagebox.showinfo("Başarılı", "Gizli resim başarıyla çıkarıldı!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Resim çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim çıkarılamadı")
    
    def save_image(self):
        """İşlenmiş resmi kaydetme fonksiyonu"""
        if not hasattr(self, 'output_image') or self.output_image is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek işlenmiş resim bulunamadı!\nÖnce resim gizleme veya çıkarma işlemi yapın.")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Resmi Kaydet",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                self.output_image.save(file_path)
                filename = os.path.basename(file_path)
                self.status_var.set(f"Resim kaydedildi: {filename}")
                messagebox.showinfo("Başarılı", f"Resim başarıyla kaydedildi:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim kaydedilemedi")
