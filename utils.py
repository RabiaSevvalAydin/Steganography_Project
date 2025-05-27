import numpy as np
from PIL import Image

def embed_text_to_image(image, text):
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


def embed_image_to_image(cover_image, secret_image):
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


def extract_text_from_image(image):
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

def extract_image_from_image(stego_image):
    # Steganografi görüntüsünü NumPy dizisine dönüştür
    stego_array = np.array(stego_image)
    
    # Düşük 4 biti çıkar ve yüksek 4 bite kaydır
    extracted_array = np.left_shift((stego_array & 0x0F), 4)
    
    # NumPy dizisini PIL Image'a dönüştür
    return Image.fromarray(extracted_array.astype(np.uint8))