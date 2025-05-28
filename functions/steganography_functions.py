import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import os
import cv2


def select_input_image():
    """Ana görüntüyü seçme fonksiyonu"""
    file_path = filedialog.askopenfilename(
        title="Ana Görüntüyü Seç",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    return file_path

def select_second_image():
    """Gizlenecek görüntüyü seçme fonksiyonu"""
    file_path = filedialog.askopenfilename(
        title="Gizlenecek Görüntüyü Seç",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    return file_path

def select_steganographic_image():
    """Steganografik görüntüyü seçme fonksiyonu (yazı çıkarma için)"""
    file_path = filedialog.askopenfilename(
        title="Steganografik Görüntüyü Seç (İçinde Gizli Yazı Olan)",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    return file_path

def select_steganographic_image_for_extraction():
    """Steganografik görüntüyü seçme fonksiyonu (resim çıkarma için)"""
    file_path = filedialog.askopenfilename(
        title="Steganografik Görüntüyü Seç (İçinde Gizli Resim Olan)",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    return file_path

def save_text_to_file(text_content):
    """Metni dosyaya kaydetme fonksiyonu"""
    file_path = filedialog.asksaveasfilename(
        title="Metni Kaydet",
        defaultextension=".txt",
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        return file_path
    return None

def save_image_to_file(image):
    """Görüntüyü dosyaya kaydetme fonksiyonu"""
    file_path = filedialog.asksaveasfilename(
        title="Resmi Kaydet",
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
    )
    
    if file_path:
        image.save(file_path)
        return file_path
    return None

def embed_text_to_image(image, text):
    """Metni görüntüye gizleme fonksiyonu (LSB Steganografi)"""
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

def extract_text_from_image(image):
    """Görüntüden metni çıkarma fonksiyonu"""
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


def embed_image_to_image(cover_image, secret_image, quality_level=2):
    """
    Adaptif bit seçimi
    quality_level: 1=düşük bozulma, 2=orta, 3=yüksek kalite gizli resim
    """
    cover_array = np.array(cover_image).copy()
    secret_resized = secret_image.resize(cover_image.size, Image.LANCZOS)
    secret_array = np.array(secret_resized)
    
    if quality_level == 1:  # Minimum bozulma
        bits = 2
        secret_mask = 0xC0  # 11000000
        cover_mask = 0xFC   # 11111100
        shift = 6
    elif quality_level == 2:  # Dengeli
        bits = 3
        secret_mask = 0xE0  # 11100000
        cover_mask = 0xF8   # 11111000
        shift = 5
    else:  # quality_level == 3, Maksimum gizli resim kalitesi
        bits = 4
        secret_mask = 0xF0  # 11110000
        cover_mask = 0xF0   # 11110000
        shift = 4
    
    # Bit işlemleri
    secret_bits = (secret_array & secret_mask) >> shift
    cover_cleared = cover_array & cover_mask
    stego_array = cover_cleared | secret_bits
    
    return Image.fromarray(stego_array.astype(np.uint8))

def extract_image_from_image(stego_image, quality_level=2):
    """Adaptif çıkarma"""
    stego_array = np.array(stego_image)
    
    if quality_level == 1:
        bits = 2
        extract_mask = 0x03  # 00000011
        shift = 6
    elif quality_level == 2:
        bits = 3
        extract_mask = 0x07  # 00000111
        shift = 5
    else:  # quality_level == 3
        bits = 4
        extract_mask = 0x0F  # 00001111
        shift = 4
    
    # Çıkarma ve genişletme
    extracted_bits = (stego_array & extract_mask) << shift
    
    # Bit genişletme (kalite artırma)
    for i in range(1, 8 // bits):
        extracted_bits = extracted_bits | (extracted_bits >> (bits * i))
    
    return Image.fromarray(extracted_bits.astype(np.uint8))



def display_image(image, label, max_size=None):
    """
    Resmi label'da dinamik olarak göster
    max_size: (width, height) - maksimum boyut, None ise label boyutuna göre ayarla
    """
    if image is None:
        return
    
    try:
        # Label'ın gerçek boyutunu al
        label.update_idletasks()
        label_width = label.winfo_width()
        label_height = label.winfo_height()
        
        # Eğer label henüz render olmamışsa, varsayılan büyük boyut kullan
        if label_width <= 1 or label_height <= 1:
            if max_size:
                target_width, target_height = max_size
            else:
                target_width, target_height = 500, 300  # Varsayılan büyük boyut
        else:
            # Label boyutundan biraz küçük hedef boyut
            target_width = max(label_width - 10, 400)  # En az 400px
            target_height = max(label_height - 10, 250)  # En az 250px
            
            # Max size sınırı varsa uygula
            if max_size:
                target_width = min(target_width, max_size[0])
                target_height = min(target_height, max_size[1])
        
        # Orijinal resim boyutları
        original_width, original_height = image.size
        
        # Aspect ratio'yu koruyarak yeniden boyutlandır
        ratio = min(target_width / original_width, target_height / original_height)
        
        # Yeni boyutları hesapla (en az belirli bir boyut olsun)
        new_width = max(int(original_width * ratio), 300)
        new_height = max(int(original_height * ratio), 200)
        
        # Resmi yeniden boyutlandır (yüksek kalite)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # PhotoImage'e çevir
        photo = ImageTk.PhotoImage(resized_image)
        
        # Label'ı güncelle
        label.configure(image=photo, text="")
        label.image = photo  # Referansı sakla
        
    except Exception as e:
        print(f"Resim gösterme hatası: {e}")
        label.configure(text=f"Resim gösterilemiyor\n{str(e)}")
