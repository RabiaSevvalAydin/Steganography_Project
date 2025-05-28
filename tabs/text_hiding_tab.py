import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    embed_text_to_image, 
    extract_text_from_image, 
    select_input_image,
    display_image
)
import os

class TextHidingTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.input_image_path = ""
        self.input_image = None
        self.output_image = None
        self.create_tab()
    
    def create_tab(self):
        """Yazı gizleme tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="📝 Yazı Gizle")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - Görüntü önizleme
        left_frame = ttk.LabelFrame(main_container, text="Görüntü Önizleme", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Görüntü önizleme alanı
        self.image_preview = tk.Label(left_frame, bg="#f0f0f0", width=60, height=25, 
                             text="Resim seçilmedi\n(Yazının gizleneceği resim)")
        self.image_preview.pack(pady=10)
        
        # Sağ panel - Kontroller
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        self.create_widgets(right_frame)
    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Resim seçme butonu
        select_button = ttk.Button(parent, text="📁 Resim Seç", 
                                  command=self.select_image, width=25)
        select_button.pack(pady=(0, 15))
        
        # Dosya yolu gösterme
        self.file_path_var = tk.StringVar(value="Dosya seçilmedi")
        path_label = ttk.Label(parent, textvariable=self.file_path_var, 
                              wraplength=200, font=('Arial', 8))
        path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Gizlenecek yazı bölümü
        text_label = ttk.Label(parent, text="Gizlenecek Yazı:", font=('Arial', 10, 'bold'))
        text_label.pack(pady=(0, 5))
        
        # Text widget frame
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.text_entry = tk.Text(text_frame, height=8, width=30, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar.set)
        
        self.text_entry.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # İşlem butonları
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        hide_button = ttk.Button(button_frame, text="🔒 Yazıyı Gizle", 
                                command=self.hide_text, width=25)
        hide_button.pack(pady=5)
        
        extract_button = ttk.Button(button_frame, text="🔓 Yazıyı Çıkar", 
                                   command=self.extract_text, width=25)
        extract_button.pack(pady=5)
        
        save_button = ttk.Button(button_frame, text="💾 Resmi Kaydet", 
                                command=self.save_image, width=25)
        save_button.pack(pady=5)
        
        # Durum göstergesi
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=5)
    
    def select_image(self):
        """Resim seçme fonksiyonu"""
        try:
            file_path = select_input_image()
            
            if file_path:
                self.input_image_path = file_path
                self.input_image = Image.open(file_path)
                
                # Görüntüyü önizlemede göster - BÜYÜK BOYUT
                display_image(self.input_image, self.image_preview, (450, 300))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Görüntü başarıyla yüklendi")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Görüntü yüklenemedi")

    
    def hide_text(self):
        """Yazı gizleme fonksiyonu"""
        if not self.input_image:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        text_to_hide = self.text_entry.get("1.0", tk.END).strip()
        if not text_to_hide:
            messagebox.showwarning("Uyarı", "Lütfen gizlenecek yazıyı girin!")
            return
        
        try:
            # Yazıyı resme gizle
            self.output_image = embed_text_to_image(self.input_image, text_to_hide)
            
            # Sonucu önizlemede göster
            display_image(self.output_image, self.image_preview, (400, 300))
            
            self.status_var.set("Yazı başarıyla gizlendi!")
            messagebox.showinfo("Başarılı", "Yazı resme başarıyla gizlendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı gizleme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı gizlenemedi")
    
    def extract_text(self):
        """Yazı çıkarma fonksiyonu"""
        if not self.input_image:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        try:
            # Resimden yazıyı çıkar
            extracted_text = extract_text_from_image(self.input_image)
            
            if extracted_text.strip():
                # Çıkarılan yazıyı text widget'a yaz
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert("1.0", extracted_text)
                
                self.status_var.set("Yazı başarıyla çıkarıldı!")
                messagebox.showinfo("Başarılı", "Gizli yazı başarıyla çıkarıldı!")
            else:
                messagebox.showinfo("Bilgi", "Bu resimde gizli yazı bulunamadı.")
                self.status_var.set("Gizli yazı bulunamadı")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı çıkarılamadı")
    
    def save_image(self):
        """İşlenmiş resmi kaydetme fonksiyonu"""
        if not hasattr(self, 'output_image') or self.output_image is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek işlenmiş resim bulunamadı!\nÖnce yazı gizleme işlemi yapın.")
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
