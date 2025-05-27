import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
from utils import embed_text_to_image, embed_image_to_image

class EmbedScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Değişkenler
        self.input_image_path = ""
        self.second_image_path = ""
        self.input_image = None
        self.second_image = None
        self.output_image = None
        self.embed_mode = tk.StringVar(value="text")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Ana başlık ve geri butonu
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        home_button = tk.Button(header_frame, text="Ana Sayfa", command=self.controller.show_home_screen)
        home_button.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text="Veri Gizleme", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
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
        self.input_preview_label = tk.Label(preview_frame, text="Ana Görüntü", bg="#f0f0f0")
        self.input_preview_label.pack(pady=(0, 5))
        
        self.input_preview = tk.Label(preview_frame, bg="#e0e0e0", width=40, height=15)
        self.input_preview.pack(pady=(0, 5))
        
        # İkinci görüntü önizleme (gizlenecek görüntü)
        self.second_preview_label = tk.Label(preview_frame, text="Gizlenecek Görüntü", bg="#f0f0f0")
        self.second_preview_label.pack(pady=(0, 5))
        
        self.second_preview = tk.Label(preview_frame, bg="#e0e0e0", width=40, height=10)
        self.second_preview.pack(pady=(0, 5))
        
        # Sağ panel - Kontroller
        right_frame = tk.Frame(content_frame, bg="#f0f0f0", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Kontrol bölgesi
        control_frame = tk.LabelFrame(right_frame, text="Kontrol Paneli", bg="#f0f0f0", padx=10, pady=10)
        control_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dosya seçme
        self.input_button = tk.Button(control_frame, text="Ana Görüntü Seç", 
                                     command=self.select_input_image, width=25)
        self.input_button.pack(pady=(10, 5))
        
        # Gizleme modu seçimi
        mode_frame = tk.Frame(control_frame, bg="#f0f0f0")
        mode_frame.pack(pady=10)
        
        self.text_mode = tk.Radiobutton(mode_frame, text="Metin Gizle", variable=self.embed_mode, 
                                        value="text", command=self.toggle_mode, bg="#f0f0f0")
        self.text_mode.pack(side=tk.LEFT, padx=5)
        
        self.image_mode = tk.Radiobutton(mode_frame, text="Görüntü Gizle", variable=self.embed_mode, 
                                         value="image", command=self.toggle_mode, bg="#f0f0f0")
        self.image_mode.pack(side=tk.LEFT, padx=5)
        
        # Metin giriş alanı
        self.text_frame = tk.Frame(control_frame, bg="#f0f0f0")
        self.text_frame.pack(fill=tk.X, pady=5)
        
        self.message_label = tk.Label(self.text_frame, text="Gizlenecek Metin:", bg="#f0f0f0")
        self.message_label.pack(anchor="w", pady=(0, 5))
        
        self.message_text = tk.Text(self.text_frame, height=6, width=30)
        self.message_text.pack(fill=tk.X)
        
        # İkinci görüntü seçme butonu (başlangıçta gizli)
        self.second_image_button = tk.Button(control_frame, text="Gizlenecek Görüntü Seç", 
                                            command=self.select_second_image, width=25)
        self.second_image_button.pack(pady=10)
        self.second_image_button.pack_forget()  # Başlangıçta gizli
        
        # İşlem butonları
        buttons_frame = tk.Frame(control_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=20)
        
        self.embed_button = tk.Button(buttons_frame, text="Gizle", command=self.embed_data, width=25)
        self.embed_button.pack(pady=5)
        
        # Kaydetme butonu
        self.save_button = tk.Button(control_frame, text="Görüntüyü Kaydet", 
                                    command=self.save_image, width=25)
        self.save_button.pack(pady=10)
    
    def toggle_mode(self):
        if self.embed_mode.get() == "text":
            self.text_frame.pack(fill=tk.X, pady=5)
            self.second_image_button.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.second_image_button.pack(pady=10)
    
    def select_input_image(self):
        file_path = filedialog.askopenfilename(
            title="Ana Görüntüyü Seç",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        
        if file_path:
            self.input_image_path = file_path
            self.input_image = Image.open(file_path)
            self.display_image(self.input_image, self.input_preview, (300, 200))
            self.controller.update_status(f"Ana görüntü yüklendi: {os.path.basename(file_path)}")
    
    def select_second_image(self):
        file_path = filedialog.askopenfilename(
            title="Gizlenecek Görüntüyü Seç",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        
        if file_path:
            self.second_image_path = file_path
            self.second_image = Image.open(file_path)
            self.display_image(self.second_image, self.second_preview, (300, 150))
            self.controller.update_status(f"Gizlenecek görüntü yüklendi: {os.path.basename(file_path)}")
    
    def display_image(self, img, label, size):
        # Görüntüyü yeniden boyutlandır
        img = img.resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # Referansı koru
    
    def embed_data(self):
        if not self.input_image_path:
            messagebox.showerror("Hata", "Lütfen önce bir ana görüntü seçin!")
            return
        
        try:
            mode = self.embed_mode.get()
            
            if mode == "text":
                message = self.message_text.get("1.0", tk.END).strip()
                if not message:
                    messagebox.showerror("Hata", "Gizlenecek metin boş olamaz!")
                    return
                
                # Metni gizle
                self.output_image = embed_text_to_image(self.input_image, message)
                
            else:  # image mode
                if not self.second_image_path:
                    messagebox.showerror("Hata", "Lütfen gizlenecek bir görüntü seçin!")
                    return
                
                # Görüntüyü gizle
                self.output_image = embed_image_to_image(self.input_image, self.second_image)
            
            # Önizleme göster
            self.display_image(self.output_image, self.input_preview, (300, 200))
            self.controller.update_status("Veri başarıyla gizlendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Veri gizleme sırasında hata oluştu: {str(e)}")
    
    def save_image(self):
        if hasattr(self, 'output_image') and self.output_image:
            file_path = filedialog.asksaveasfilename(
                title="Görüntüyü Kaydet",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if file_path:
                self.output_image.save(file_path)
                self.controller.update_status(f"Görüntü kaydedildi: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Hata", "Kaydedilecek işlenmiş görüntü bulunamadı!")