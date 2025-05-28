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





def text_to_binary(msg):
    """
    msg = "Hi"
    'H' = 72 = '01001000'
    'i' = 105 = '01101001'
    result = '0100100001101001'
    """
    return ''.join(format(ord(c), '08b') for c in msg)  # ord() returns binary version

def embed_text_to_image(image_path, msg, output_path, grey_flag:bool=False):
    if grey_flag:
        img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)    
    else:
        img = cv2.imread(image_path)

    if img is None:
        raise Exception("Image path is wrong")
    
    msg += chr(0)   # sonuna \0 eklenir
    binary_msg = text_to_binary(msg)
    binary_index = 0
    print("len of message in bits: ", len(binary_msg))
    print("binary_msg: ", binary_msg)

    if(len(img.shape) == 3): # rgb
        print("\nImage is in RGB")
        size_x, size_y, _ = img.shape

        max_bits = img.shape[0] * img.shape[1] * 3
        if len(binary_msg) > max_bits:
            raise ValueError("Mesaj çok uzun, resme sığmıyor.")
        
        for x in range(size_x):
            for y in range(size_y):
                for channel in range(3):
                    if binary_index < len(binary_msg):
                        img[x, y, channel] =  (img[x, y, channel] & ~1) | int(binary_msg[binary_index])
                        binary_index += 1
                    else:
                        break

    else: # grey scale
        print("\nImage is in grey scale")
        size_x, size_y = img.shape

        max_bits = img.shape[0] * img.shape[1]
        if len(binary_msg) > max_bits:
            raise ValueError("Mesaj çok uzun, resme sığmıyor.")
        
        for x in range(size_x):
            for y in range(size_y):
                    if binary_index < len(binary_msg):
                        img[x, y] =  (img[x, y] & ~1) | int(binary_msg[binary_index])
                        binary_index += 1
                    else:
                        break

    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  
    print("kaydetme öncesi shape: " , img.shape)     
    cv2.imwrite(output_path, img)
    test = cv2.imread(output_path , cv2.IMREAD_UNCHANGED)
    print("Kaydedilen görüntü yeniden okunduğunda shape:", test.shape)

    print("Hidden char count: ",binary_index)
    print("Message is hidden succesfully")

def extract_text_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise Exception("Image path is wrong")
    
    bitler = ""
    hidden_msg = ""
    
    if len(img.shape)==3:   # rgb
        print("\nImage is in RGB")
        size_x, size_y, _ = img.shape
        for x in range(size_x):
            for y in range(size_y):
                for channel in range(3):
                    bitler += str(img[x, y, channel] & 1)   # son biti al ve stringe çevir

                    if len(bitler) == 8:
                        print("bitler: ", bitler)
                        karakter = chr(int(bitler,2))    # toplanan 8 biti karaktere çevirir
                        print("karakter: ", karakter)
                        if karakter == "\0":  # eğer karakter \0 ise metin çıkarma işlemi sonlandırılır
                            print("hidden_msg length: ", len(hidden_msg))
                            return hidden_msg
                        hidden_msg += karakter
                        bitler = "" # yeni 8lik bit dizisi için sıfırlanır
    else:   # gray scale image
        img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
        print("\nImage is in grey scale")
        size_x, size_y = img.shape
        for x in range(size_x):
            for y in range(size_y):
                    bitler += str(img[x, y] & 1)   # son biti al ve stringe çevir

                    if len(bitler) == 8:
                        print("bitler: ", bitler)
                        karakter = chr(int(bitler,2))    # toplanan 8 biti karaktere çevirir
                        print("karakter: ", karakter)
                        if karakter == "\0":  # eğer karakter \0 ise metin çıkarma işlemi sonlandırılır
                            print("hidden_msg length: ", len(hidden_msg))
                            return hidden_msg
                        hidden_msg += karakter
                        bitler = "" # yeni 8lik bit dizisi için sıfırlanır
    
    # Eğer \0 karakteri bulunamazsa, toplanan mesajı döndür
    print("hidden_msg length (final): ", len(hidden_msg))
    return hidden_msg if hidden_msg else ""










def pixel_to_binary(flatten_img):
    """
    flatten_img = [72, 105, 0, 255, 87, 98, ...]
    72 = '01001000'
    105 = '01101001'
    result = '0100100001101001.....'
    """
    return ''.join(format(byte, '08b') for byte in flatten_img)   

def embed_image_to_image(image_path, secret_img_path, output_path, gray_flag:bool=False):
    if gray_flag:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img_secret = cv2.imread(secret_img_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        img_secret = cv2.imread(secret_img_path, cv2.IMREAD_UNCHANGED)

    if img is None or img_secret is None:
        raise Exception("Image path is wrong")
    
    if len(img.shape) == 3: # rgb
        size_x_1, size_y_1, _ = img.shape
        size_x_2, size_y_2, _ = img_secret.shape
        print("Size of original image: ", size_x_1, size_y_1)
        print("Size of image to hide: ", size_x_2, size_y_2)

        # boyut kontrolü
        if size_x_1 * size_y_1 * 3 < size_x_2 * size_y_2 * 24:
            print(img.shape)
            print(img_secret.shape)
            raise ValueError(f"Seçilen resim, saklanacak resmi gömmek için yeterli büyüklükte değil, {size_x_1 * size_y_1 * 3} > {size_x_2 * size_y_2 * 24} olmalı\n Ana resim boyutu {size_x_1}x{size_y_1}, Gömülecek resim boyutu {size_x_2}x{size_y_2}")
        
        print("img_secret.shape", img_secret.shape) # (512, 512, 3)
        img_secret_flat = img_secret.flatten()
        print("img_secret_flat.shape", img_secret_flat.shape) # (786432,) # her bir piksel değerine ulaşmayı kolaylaştırır, görüntüyü piksel piksel ve kanal kanal gezmek terine tek bir sıra haline getiriyoruz

        binary_secret = pixel_to_binary(img_secret_flat)
        print("binary_img_size", len(binary_secret))

        # resmin ilk 32 bitlik kısmı saklanacak görüntünün boyut bilgisinin saklanması için ayrılır
        # burada 32 seçilerek 2^32 boyutunda resimlerin saklanabilmesi için yeterli alan ayrılabilir
        # alternatif olarak 16 seçilebilir fakat bu sefer 2^16=65535 pikselden fazla genişlik ya da yükseklikteki görüntüler saklanamaz
        x_info = format(size_x_2, '032b')
        y_info = format(size_y_2, '032b')
        boyut_bits = x_info + y_info    # 64 bit=64 lsb lazım -> 22 pixel gerekiyor (22x3 = 66)

        # öncelikle boyut bilgisi gömülür
        boyut_bit_index = 0
        for x in range(size_x_1):
            for y in range(size_y_1):
                for channel in range(3):
                    if boyut_bit_index < len(boyut_bits):
                        img[x, y, channel] =  (img[x, y, channel] & ~1) | int(boyut_bits[boyut_bit_index])
                        boyut_bit_index += 1
                    else: 
                        break

        # ardından görüntü gömülür
        binary_index = 0
        first_22_pixel_count = 0
        for x in range(size_x_1):
            for y in range(size_y_1):
                if first_22_pixel_count < 22:
                    first_22_pixel_count += 1   # ilk 22 piksel boyut bilgisini tuttuğu için atlanır
                    continue
                for channel in range(3):
                    if binary_index < len(binary_secret):
                        img[x, y, channel] =  (img[x, y, channel] & ~1) | int(binary_secret[binary_index])
                        binary_index += 1
                    else: 
                        break
                if binary_index >= len(binary_secret):
                    break
            if binary_index >= len(binary_secret):
                break
    else: # greyscale images
        size_x_1, size_y_1 = img.shape
        size_x_2, size_y_2 = img_secret.shape
        print("Size of original image: ", size_x_1, size_y_1)
        print("Size of image to hide: ", size_x_2, size_y_2)

        # boyut kontrolü
        if size_x_1 * size_y_1 < size_x_2 * size_y_2 * 8:
            print(img.shape)
            print(img_secret.shape)
            raise ValueError(f"Seçilen resim, saklanacak resmi gömmek için yeterli büyüklükte değil, {size_x_1 * size_y_1 } > {size_x_2 * size_y_2 * 8} olmalı")
        
        print("img_secret.shape", img_secret.shape) # (512, 512)
        img_secret_flat = img_secret.flatten()
        print("img_secret_flat.shape", img_secret_flat.shape) # (262144,) # her bir piksel değerine ulaşmayı kolaylaştırır, görüntüyü piksel piksel ve kanal kanal gezmek terine tek bir sıra haline getiriyoruz

        binary_secret = pixel_to_binary(img_secret_flat)
        print("binary_img_size", len(binary_secret))

        # resmin ilk 32 bitlik kısmı saklanacak görüntünün boyut bilgisinin saklanması için ayrılır
        # burada 32 seçilerek 2^32 boyutunda resimlerin saklanabilmesi için yeterli alan ayrılabilir
        # alternatif olarak 16 seçilebilir fakat bu sefer 2^16=65535 pikselden fazla genişlik ya da yükseklikteki görüntüler saklanamaz
        x_info = format(size_x_2, '032b')
        y_info = format(size_y_2, '032b')
        boyut_bits = x_info + y_info    # 64 bit=64 lsb lazım -> 22 pixel gerekiyor (22x3 = 66)

        # öncelikle boyut bilgisi gömülür
        boyut_bit_index = 0
        for x in range(size_x_1):
            for y in range(size_y_1):
                    if boyut_bit_index < len(boyut_bits):
                        img[x, y] =  (img[x, y] & ~1) | int(boyut_bits[boyut_bit_index])
                        boyut_bit_index += 1
                    else: 
                        break

        # ardından görüntü gömülür
        binary_index = 0
        first_64_pixel_count = 0
        for x in range(size_x_1):
            for y in range(size_y_1):
                if first_64_pixel_count < 64:
                    first_64_pixel_count += 1   # ilk 64 piksel boyut bilgisini tuttuğu için atlanır
                    continue
                if binary_index < len(binary_secret):
                    img[x, y] =  (img[x, y] & ~1) | int(binary_secret[binary_index])
                    binary_index += 1
                else: 
                    break
            if binary_index >= len(binary_secret):
                break
  
    print("Hidden bit count: ",binary_index)
    cv2.imwrite(output_path, img)
    print("Image is hidden succesfully")













def extract_image_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise Exception("Image path is wrong") 

    if len(img.shape)==3: # rgb
        size_x, size_y, _ = img.shape
        # Önce boyut bilgisi çıkartılır
        bitler = ""
        bit_index = 0
        for x in range(size_x):
            for y in range(size_y):
                for channel in range(3):
                    if bit_index > 63:
                        break
                    else:   # ilk 64 bit alınır boyut bilgisi için
                        bitler += str(img[x, y, channel] & 1)
                        bit_index += 1

        x_info = int(bitler[:32], 2)
        y_info = int(bitler[32:], 2)
        print(f"Hidden image size is {x_info}x{y_info}")

        # Boyut bilgisine göre gizli görsel çıkartılır
        toplam_bit = x_info*y_info*3*8
        hidden_bits = ""
        pixel_count = 0  # Toplam piksel sayacı

        for x in range(size_x):
            for y in range(size_y):
                pixel_count += 1
                
                # İlk 22 pikseli atla (66 kanal = 22 piksel * 3 kanal)
                if pixel_count <= 22:
                    continue
                    
                for channel in range(3):
                    if len(hidden_bits) < toplam_bit:
                        hidden_bits += str(img[x, y, channel] & 1)
                    else:
                        # Yeterli bit toplandı, çık
                        break
                
                # Yeterli bit toplandıysa döngüden çık
                if len(hidden_bits) >= toplam_bit:
                    break
            
            # Yeterli bit toplandıysa döngüden çık
            if len(hidden_bits) >= toplam_bit:
                break

        print("Number of hidden image bits revealed is ", len(hidden_bits))
        print("It should be equal to:", x_info*y_info*3*8)
        
        hidden_byte_list = [int(hidden_bits[i:i+8], 2) for i in range(0, len(hidden_bits), 8)]
        hidden_img = np.array(hidden_byte_list, dtype=np.uint8).reshape((x_info, y_info, 3))
    else: #grayscale
        size_x, size_y = img.shape
        # Önce boyut bilgisi çıkartılır
        bitler = ""
        bit_index = 0
        for x in range(size_x):
            for y in range(size_y):
                if bit_index > 63:
                    break
                else:   # ilk 64 bit alınır boyut bilgisi için
                    bitler += str(img[x, y] & 1)
                    bit_index += 1

        x_info = int(bitler[:32], 2)
        y_info = int(bitler[32:], 2)
        print(f"Hidden image size is {x_info}x{y_info}")

        # Boyut bilgisine göre gizli görsel çıkartılır
        toplam_bit = x_info*y_info*8
        hidden_bits = ""
        first_64_pixel_count = 0
        for x in range(size_x):
            for y in range(size_y):
                if first_64_pixel_count < 64:
                    first_64_pixel_count += 1   # ilk 22 piksel boyut bilgisini tuttuğu için atlanır
                    continue
                if len(hidden_bits) < toplam_bit:
                    hidden_bits += str(img[x, y] & 1)
                else:
                    print("Number of hidden image bits revealed is ", len(hidden_bits))
                    print("It should be equal to:", x_info*y_info*8)
                    break
            if len(hidden_bits) >= toplam_bit:
                break

        hidden_byte_list = [int(hidden_bits[i:i+8], 2) for i in range(0, len(hidden_bits), 8)]
        hidden_img = np.array(hidden_byte_list, dtype=np.uint8).reshape((x_info, y_info))
    
    return hidden_img


    #return Image.fromarray(extracted_bits.astype(np.uint8))





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
