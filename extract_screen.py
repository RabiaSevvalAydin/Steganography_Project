import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
from utils import extract_text_from_image, extract_image_from_image

class ExtractScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Değişkenler
        self.input_image_path = ""
        self.input_image = None
        self.extracted_image = None
        self.extract_mode = tk.StringVar(value="text")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Ana başlık ve geri butonu
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        home_button = tk.Button(header_frame, text="Ana Sayfa", command=self.controller.show_home_screen)
        home_button.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text="Veri Çıkarma", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Ana içerik
        content_frame = tk.Frame(self, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel - Görüntüler
        left_frame = tk.Frame(content_frame, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Görüntü önizleme alanları
        preview_frame = tk.Frame(left_frame, bg="#f0f0f0")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ana görüntü önizleme
        self.input_preview_label = tk.Label(preview_frame, text="Steganografi Görüntüsü", bg="#f0f0f0")
        self.input_preview_label.pack(pady=(0, 5))
        
        self.input_preview = tk.Label(preview_frame, bg="#e0e0e0", width=40, height=15)
        self.input_preview.pack(pady=(0, 5))
        
        # Çıkarılan görüntü önizleme
        self.extracted_preview_label = tk.Label(preview_frame, text="Çıkarılan Görüntü", bg="#f0f0f0")
        self.extracted_preview_label.pack(pady=(0, 5))
        
        self.extracted_preview = tk.Label(preview_frame, bg="#e0e0e0", width=40, height=10)
        self.extracted_preview.pack(pady=(0, 5))
        
        # Sağ panel - Kontroller
        right_frame = tk.Frame(content_frame, bg="#f0f0f0", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Kontrol bölgesi
        control_frame = tk.LabelFrame(right_frame, text="Kontrol Paneli", bg="#f0f0f0", padx=10, pady=10)
        control_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dosya seçme
        self.input_button = tk.Button(control_frame, text="Steganografi Görüntüsü Seç", 
                                     command=self.select_input_image, width=25)
        self.input_button.pack(pady=(10, 5))
        
        # Çıkarma modu seçimi
        mode_frame = tk.Frame(control_frame, bg="#f0f0f0")
        mode_frame.pack(pady=10)
        
        self.text_mode = tk.Radiobutton(mode_frame, text="Metin Çıkar", variable=self.extract_mode, 
                                        value="text", command=self.toggle_mode, bg="#f0f0f0")
        self.text_mode.pack(side=tk.LEFT, padx=5)
        
        self.image_mode = tk.Radiobutton(mode_frame, text="Görüntü Çıkar", variable=self.extract_mode, 
                                         value="image", command=self.toggle_mode, bg="#f0f0f0")
        self.image_mode.pack(side=tk.LEFT, padx=5)
        
        # Metin çıktı alanı
        self.text_frame = tk.Frame(control_frame, bg="#f0f0f0")
        self.text_frame.pack(fill=tk.X, pady=5)
        
        self.message_label = tk.Label(self.text_frame, text="Çıkarılan Metin:", bg="#f0f0f0")
        self.message_label.pack(anchor="w", pady=(0, 5))
        
        self.message_text = tk.Text(self.text_frame, height=6, width=30)
        self.message_text.pack(fill=tk.X)
        
        # İşlem butonları
        buttons_frame = tk.Frame(control_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=20)
        
        self.extract_button = tk.Button(buttons_frame, text="Veriyi Çıkar", 
                                       command=self.extract_data, width=25)
        self.extract_button.pack(pady=5)
        
        # Kaydetme butonu (görüntü çıkarma için)
        self.save_button = tk.Button(control_frame, text="Çıkarılan Görüntüyü Kaydet", 
                                    command=self.save_image, width=25)
        self.save_button.pack(pady=10)
        self.save_button.pack_forget()  # Başlangıçta gizli
    
    def toggle_mode(self):
        if self.extract_mode.get() == "text":
            self.text_frame.pack(fill=tk.X, pady=5)
            self.save_button.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.save_button.pack(pady=10)
    
    def select_input_image(self):
        file_path = filedialog.askopenfilename(
            title="Steganografi Görüntüsünü Seç",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        
        if file_path:
            self.input_image_path = file_path
            self.input_image = Image.open(file_path)
            self.display_image(self.input_image, self.input_preview, (300, 200))
            self.controller.update_status(f"Steganografi görüntüsü yüklendi: {os.path.basename(file_path)}")
    
    def display_image(self, img, label, size):
        # Görüntüyü yeniden boyutlandır
        img = img.resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # Referansı koru
    
    def extract_data(self):
        if not self.input_image_path:
            messagebox.showerror("Hata", "Lütfen önce bir steganografi görüntüsü seçin!")
            return
        
        try:
            mode = self.extract_mode.get()
            
            if mode == "text":
                # Metni çıkar
                message = extract_text_from_image(self.input_image)
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", message)
                self.controller.update_status("Metin başarıyla çıkarıldı!")
                
            else:  # image mode
                # Görüntüyü çıkar
                self.extracted_image = extract_image_from_image(self.input_image)
                self.display_image(self.extracted_image, self.extracted_preview, (300, 150))
                self.controller.update_status("Görüntü başarıyla çıkarıldı!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Veri çıkarma sırasında hata oluştu: {str(e)}")
    
    def save_image(self):
        if hasattr(self, 'extracted_image') and self.extracted_image:
            file_path = filedialog.asksaveasfilename(
                title="Çıkarılan Görüntüyü Kaydet",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if file_path:
                self.extracted_image.save(file_path)
                self.controller.update_status(f"Çıkarılan görüntü kaydedildi: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Hata", "Kaydedilecek çıkarılmış görüntü bulunamadı!")