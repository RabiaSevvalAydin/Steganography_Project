import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    extract_text_from_image, 
    select_steganographic_image,
    save_text_to_file,
    display_image
)
import os

class TextExtractionTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.image_path = ""
        self.image = None
        self.extracted_text = ""
        self.create_tab()
    
    def create_tab(self):
        """Yazı çıkarma tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="🔍 Yazı Çıkar")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Görüntü önizleme
        left_frame = ttk.LabelFrame(main_container, text="Steganografik Görüntü", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Görüntü önizleme alanı
        self.image_preview = tk.Label(left_frame, bg="#f0f0f0", width=60, height=25, 
                                    text="Steganografik görüntü seçilmedi\n(İçinde gizli yazı olan resim)")
        self.image_preview.pack(pady=10)
        
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
        extract_button = ttk.Button(parent, text="🔓 Gizli Yazıyı Çıkar", 
                                   command=self.extract_text, width=30)
        extract_button.pack(pady=(0, 20))
        
        # Çıkarılan yazı bölümü
        text_label = ttk.Label(parent, text="Çıkarılan Gizli Yazı:", font=('Arial', 10, 'bold'))
        text_label.pack(pady=(0, 5))
        
        # Text widget frame
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.result_text = tk.Text(text_frame, height=10, width=35, wrap=tk.WORD, 
                                  state=tk.DISABLED, bg="#f5f5f5")
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Kaydet butonu
        save_button = ttk.Button(parent, text="💾 Yazıyı Dosyaya Kaydet", 
                                command=self.save_text, width=30)
        save_button.pack(pady=10)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="5")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=5, width=30, wrap=tk.WORD, font=('Arial', 8),
                           state=tk.DISABLED, bg="#f0f0f0")
        info_text.pack()
        
        # Bilgi metnini ekle
        info_content = ("• Steganografik resim, içinde gizli yazı bulunan resimdir.\n\n"
                       "• Bu resim genellikle 'Yazı Gizle' sekmesinde oluşturulmuş olmalıdır.\n\n"
                       "• Çıkarılan yazı otomatik olarak gösterilecektir.")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=10)
    
    def select_image(self):
        """Steganografik resim seçme fonksiyonu"""
        try:
            file_path = select_steganographic_image()
            
            if file_path:
                self.image_path = file_path
                self.image = Image.open(file_path)
                
                # Görüntüyü önizlemede göster
                display_image(self.image, self.image_preview, (450, 300))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Steganografik görüntü yüklendi")
                
                # Önceki çıkarılan yazıyı temizle
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete("1.0", tk.END)
                self.result_text.config(state=tk.DISABLED)
                self.extracted_text = ""
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Görüntü yüklenemedi")
    
    def extract_text(self):
        """Gizli yazıyı çıkarma fonksiyonu"""
        if not self.image:
            messagebox.showwarning("Uyarı", "Lütfen önce steganografik bir resim seçin!")
            return
        
        try:
            # Resimden gizli yazıyı çıkar
            self.extracted_text = extract_text_from_image(self.image)
            
            # Sonucu göster
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            
            if self.extracted_text.strip():
                self.result_text.insert("1.0", self.extracted_text)
                self.status_var.set("Gizli yazı başarıyla çıkarıldı!")
                messagebox.showinfo("Başarılı", f"Gizli yazı başarıyla çıkarıldı!\n\nÇıkarılan yazı {len(self.extracted_text)} karakter uzunluğunda.")
            else:
                self.result_text.insert("1.0", "Bu resimde gizli yazı bulunamadı.")
                self.status_var.set("Gizli yazı bulunamadı")
                messagebox.showinfo("Bilgi", "Bu resimde gizli yazı bulunamadı.\n\nLütfen steganografik bir resim seçtiğinizden emin olun.")
            
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı çıkarılamadı")
    
    def save_text(self):
        """Çıkarılan yazıyı dosyaya kaydetme fonksiyonu"""
        if not self.extracted_text.strip():
            messagebox.showwarning("Uyarı", "Kaydedilecek yazı bulunamadı!\nÖnce yazı çıkarma işlemi yapın.")
            return
        
        try:
            file_path = save_text_to_file(self.extracted_text)
            
            if file_path:
                filename = os.path.basename(file_path)
                self.status_var.set(f"Yazı kaydedildi: {filename}")
                messagebox.showinfo("Başarılı", f"Çıkarılan yazı başarıyla kaydedildi:\n{filename}\n\nKarakter sayısı: {len(self.extracted_text)}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı kaydedilemedi")
