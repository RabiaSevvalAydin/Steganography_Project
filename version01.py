import numpy as np
import matplotlib.pyplot as plt
import cv2
import os


# --------------TEXT TO IMAGE-------------------

def text_to_binary(msg):
    """
    msg = "Hi"
    'H' = 72 = '01001000'
    'i' = 105 = '01101001'
    result = '0100100001101001'
    """
    return ''.join(format(ord(c), '08b') for c in msg)  # ord() returns binary version

def binary_to_text(binary): # -----kullanmıyoruz, kendi kontrollerin için kullanabilirsin
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def hide_text(image_path, msg, output_path, grey_flag:bool=False):
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

def reveal_text(image_path):
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


# --------------IMAGE TO IMAGE------------------
def pixel_to_binary(flatten_img):
    """
    flatten_img = [72, 105, 0, 255, 87, 98, ...]
    72 = '01001000'
    105 = '01101001'
    result = '0100100001101001.....'
    """
    return ''.join(format(byte, '08b') for byte in flatten_img)   

def hide_img(image_path, secret_img_path, output_path, gray_flag:bool=False):
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
            raise ValueError(f"Seçilen resim, saklanacak resmi gömmek için yeterli büyüklükte değil, {size_x_1 * size_y_1 * 3} > {size_x_2 * size_y_2 * 24} olmalı")
        
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

def reveal_img(image_path):
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
        first_22_pixel_count = 0
        for x in range(size_x):
            for y in range(size_y):
                if first_22_pixel_count < 66:
                    first_22_pixel_count += 3   # ilk 22 piksel boyut bilgisini tuttuğu için atlanır
                    continue
                for channel in range(3):
                    if len(hidden_bits) < toplam_bit:
                        hidden_bits += str(img[x, y, channel] & 1)
                    else:
                        print("Number of hidden image bits revealed is ", len(hidden_bits))
                        print("It should be equal to:", x_info*y_info*3*8)
                        break
                if len(hidden_bits) >= toplam_bit:
                    break
            if len(hidden_bits) >= toplam_bit:
                break
        
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



os.chdir("c:\\Users\\rabia\\Desktop\\vs_workspace\\goruntu_isleme\\Steganography_Project")
# Resmin tam yolu
# img_path = os.path.join(base_dir, "images", "lenna.png")

# img = cv2.imread(img_path)
# hidden_img = hide_img("input_data/lenna.png", "input_data/random_gray_128_128.png", "result_data/result_img_to_img_gray.png", gray_flag=True)
hidden_img = reveal_img("result_data/result_img_to_img_gray.png")
plt.imshow(hidden_img)