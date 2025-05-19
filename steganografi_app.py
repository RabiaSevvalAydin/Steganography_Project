import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os

class SteganografiUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Görüntü Steganografi Uygulaması")
        self.master.geometry("900x600")
        self.master.configure(bg="#f0f0f0")
        
        # Ana çerçeve
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Değişkenler
        self.input_image_path = ""
        self.output_image_path = ""
        self.second_image_path = ""
        self.message = ""
        self.input_image = None
        self.second_image = None
        self.embed_mode = tk.StringVar(value="text")
        
        # Arayüz elemanlarını oluştur
        self.create_widgets()
    
    def create_widgets(self):
        # Sol panel - Görüntüler
        self.left_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Görüntü önizleme alanları
        self.preview_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ana görüntü önizleme
        self.input_preview_label = tk.Label(self.preview_frame, text="Ana Görüntü", bg="#f0f0f0")
        self.input_preview_label.pack(pady=(0, 5))
        
        self.input_preview = tk.Label(self.preview_frame, bg="#e0e0e0", width=40, height=15)
        self.input_preview.pack(pady=(0, 5))
        
        # İkinci görüntü önizleme (gizlenecek görüntü)
        self.second_preview_label = tk.Label(self.preview_frame, text="Gizlenecek Görüntü", bg="#f0f0f0")
        self.second_preview_label.pack(pady=(0, 5))
        
        self.second_preview = tk.Label(self.preview_frame, bg="#e0e0e0", width=40, height=10)
        self.second_preview.pack(pady=(0, 5))
        
        # Sağ panel - Kontroller
        self.right_frame = tk.Frame(self.main_frame, bg="#f0f0f0", width=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))
        
        # Kontrol bölgesi
        self.control_frame = tk.LabelFrame(self.right_frame, text="Kontrol Paneli", bg="#f0f0f0", padx=10, pady=10)
        self.control_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dosya seçme
        self.input_button = tk.Button(self.control_frame, text="Ana Görüntü Seç", command=self.select_input_image, width=25)
        self.input_button.pack(pady=(10, 5))
        
        # Gizleme modu seçimi
        self.mode_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.mode_frame.pack(pady=10)
        
        self.text_mode = tk.Radiobutton(self.mode_frame, text="Metin Gizle", variable=self.embed_mode, 
                                        value="text", command=self.toggle_mode, bg="#f0f0f0")
        self.text_mode.pack(side=tk.LEFT, padx=5)
        
        self.image_mode = tk.Radiobutton(self.mode_frame, text="Görüntü Gizle", variable=self.embed_mode, 
                                         value="image", command=self.toggle_mode, bg="#f0f0f0")
        self.image_mode.pack(side=tk.LEFT, padx=5)
        
        # Metin giriş alanı
        self.text_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.text_frame.pack(fill=tk.X, pady=5)
        
        self.message_label = tk.Label(self.text_frame, text="Gizlenecek Metin:", bg="#f0f0f0")
        self.message_label.pack(anchor="w", pady=(0, 5))
        
        self.message_text = tk.Text(self.text_frame, height=6, width=30)
        self.message_text.pack(fill=tk.X)
        
        # İkinci görüntü seçme butonu (başlangıçta gizli)
        self.second_image_button = tk.Button(self.control_frame, text="Gizlenecek Görüntü Seç", 
                                            command=self.select_second_image, width=25)
        self.second_image_button.pack(pady=10)
        self.second_image_button.pack_forget()  # Başlangıçta gizli
        
        # İşlem butonları
        self.buttons_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        self.buttons_frame.pack(fill=tk.X, pady=20)
        
        self.embed_button = tk.Button(self.buttons_frame, text="Gizle", command=self.embed_data, width=15)
        self.embed_button.pack(side=tk.LEFT, padx=5)
        
        self.extract_button = tk.Button(self.buttons_frame, text="Çıkar", command=self.extract_data, width=15)
        self.extract_button.pack(side=tk.LEFT, padx=5)
        
        # Kaydetme butonu
        self.save_button = tk.Button(self.control_frame, text="Görüntüyü Kaydet", command=self.save_image, width=25)
        self.save_button.pack(pady=10)
        
        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        self.status_bar = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
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
            self.status_var.set(f"Ana görüntü yüklendi: {os.path.basename(file_path)}")
    
    def select_second_image(self):
        file_path = filedialog.askopenfilename(
            title="Gizlenecek Görüntüyü Seç",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        
        if file_path:
            self.second_image_path = file_path
            self.second_image = Image.open(file_path)
            self.display_image(self.second_image, self.second_preview, (300, 150))
            self.status_var.set(f"Gizlenecek görüntü yüklendi: {os.path.basename(file_path)}")
    
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
                self.output_image = self.embed_text_to_image(self.input_image, message)
                
            else:  # image mode
                if not self.second_image_path:
                    messagebox.showerror("Hata", "Lütfen gizlenecek bir görüntü seçin!")
                    return
                
                # Görüntüyü gizle
                self.output_image = self.embed_image_to_image(self.input_image, self.second_image)
            
            # Önizleme göster
            self.display_image(self.output_image, self.input_preview, (300, 200))
            self.status_var.set("Veri başarıyla gizlendi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Veri gizleme sırasında hata oluştu: {str(e)}")
    
    def embed_text_to_image(self, image, text):
        # Görüntüyü NumPy dizisine dönüştür (kopyasını al)
        img_array = np.array(image).copy()
        
        # Metni binary formatına dönüştür
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        binary_text += '0' * 8  # Metnin sonunu işaretlemek için null karakteri ekle

        # Metni gizlemek için yeterli piksel var mı kontrol et
        if len(binary_text) > img_array.size:
            raise ValueError("Metin bu görüntü için çok uzun!")
        
        # Şekillendir
        flat_img = img_array.flatten()
        
        # LSB steganografi - her pikselin en düşük değerlikli bitini değiştir
        for i in range(len(binary_text)):
            if binary_text[i] == '1':
                flat_img[i] = flat_img[i] | 1  # En düşük biti 1 yap
            else:
                flat_img[i] = flat_img[i] & 254  # En düşük biti 0 yap (254 = 0b11111110)
        
        # Diziyi orijinal şekline geri döndür
        stego_img = flat_img.reshape(img_array.shape)
        
        # NumPy dizisini PIL Image'a dönüştür
        return Image.fromarray(stego_img.astype(np.uint8))
    
    def embed_image_to_image(self, cover_image, secret_image):
        # Örtü görüntüsü ve gizli görüntüyü NumPy dizilerine dönüştür
        cover_array = np.array(cover_image).copy()
        
        # Gizli görüntüyü örtü görüntüsü boyutuna yeniden boyutlandır
        secret_resized = secret_image.resize(cover_image.size, Image.LANCZOS)
        secret_array = np.array(secret_resized)
        
        # Gizli görüntünün en yüksek 4 bitini al ve 4 bit sağa kaydır (düşük bitler için)
        secret_bits = (secret_array & 0xF0) >> 4
        
        # Örtü görüntüsünün en düşük 4 bitini temizle
        cover_cleared = cover_array & 0xF0
        
        # Gizli görüntü bitlerini örtü görüntüsüne ekle (düşük 4 bite)
        stego_array = cover_cleared | secret_bits
        
        # NumPy dizisini PIL Image'a dönüştür
        return Image.fromarray(stego_array.astype(np.uint8))
    
    def extract_data(self):
        if not self.input_image_path:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü seçin!")
            return
        
        try:
            mode = self.embed_mode.get()
            
            if mode == "text":
                # Metni çıkar
                message = self.extract_text_from_image(self.input_image)
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", message)
                self.status_var.set("Metin başarıyla çıkarıldı!")
                
            else:  # image mode
                # Görüntüyü çıkar
                extracted_image = self.extract_image_from_image(self.input_image)
                self.display_image(extracted_image, self.second_preview, (300, 150))
                self.status_var.set("Görüntü başarıyla çıkarıldı!")
                self.second_image = extracted_image
            
        except Exception as e:
            messagebox.showerror("Hata", f"Veri çıkarma sırasında hata oluştu: {str(e)}")
    
    def extract_text_from_image(self, image):
        # Görüntüyü NumPy dizisine dönüştür
        img_array = np.array(image)
        
        # Şekillendir
        flat_img = img_array.flatten()
        
        # LSB'leri çıkar
        binary_text = ''
        for i in range(flat_img.size):
            binary_text += str(flat_img[i] & 1)
            # Her 8 bit sonra kontrol et
            if i > 0 and (i+1) % 8 == 0:
                # Son 8 biti kontrol et - eğer null karakter ise dur
                if binary_text[i-7:i+1] == '00000000':
                    break
        
        # Binary'den text'e dönüştür
        text = ""
        for i in range(0, len(binary_text), 8):
            if i + 8 > len(binary_text):
                break
            
            byte = binary_text[i:i+8]
            char = chr(int(byte, 2))
            
            # Null karakteri görünce dur (metnin sonu)
            if char == '\0':
                break
                
            text += char
        
        return text
    
    def extract_image_from_image(self, stego_image):
        # Steganografi görüntüsünü NumPy dizisine dönüştür
        stego_array = np.array(stego_image)
        
        # Düşük 4 biti çıkar ve yüksek 4 bite kaydır
        extracted_array = np.left_shift((stego_array & 0x0F), 4)
        
        # NumPy dizisini PIL Image'a dönüştür
        return Image.fromarray(extracted_array.astype(np.uint8))
    
    def save_image(self):
        if hasattr(self, 'output_image'):
            file_path = filedialog.asksaveasfilename(
                title="Görüntüyü Kaydet",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            
            if file_path:
                self.output_image.save(file_path)
                self.status_var.set(f"Görüntü kaydedildi: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Hata", "Kaydedilecek işlenmiş görüntü bulunamadı!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganografiUygulamasi(root)
    root.mainloop()