import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Uygulaması")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Ana pencere için stil ayarları
        self.setup_styles()
        
        # Ana notebook (tab container) oluştur
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab sayfalarını oluştur
        self.create_data_hiding_tab()
        self.create_data_extraction_tab()
        
    def setup_styles(self):
        """GUI stil ayarlarını yapılandır"""
        style = ttk.Style()
        style.theme_use('clam')  # Modern görünüm için
        
    def create_data_hiding_tab(self):
        """Veri Gizleme tabını oluştur"""
        # Veri Gizleme frame'i
        self.hiding_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hiding_frame, text="Veri Gizleme")
        
        # Başlık
        title_label = ttk.Label(self.hiding_frame, text="Veri Gizleme", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Placeholder içerik
        info_label = ttk.Label(self.hiding_frame, 
                              text="Bu bölümde resim içine veri gizleme işlemleri yapılacak.",
                              font=('Arial', 10))
        info_label.pack(pady=10)
        
        # Geçici buton (fonksiyonlar eklendikten sonra kaldırılacak)
        temp_button = ttk.Button(self.hiding_frame, text="Test Butonu", 
                                command=self.test_hiding_function)
        temp_button.pack(pady=20)
        
    def create_data_extraction_tab(self):
        """Veri Çıkarma tabını oluştur"""
        # Veri Çıkarma frame'i
        self.extraction_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extraction_frame, text="Veri Çıkarma")
        
        # Başlık
        title_label = ttk.Label(self.extraction_frame, text="Veri Çıkarma", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Placeholder içerik
        info_label = ttk.Label(self.extraction_frame, 
                              text="Bu bölümde resimden gizli veri çıkarma işlemleri yapılacak.",
                              font=('Arial', 10))
        info_label.pack(pady=10)
        
        # Geçici buton (fonksiyonlar eklendikten sonra kaldırılacak)
        temp_button = ttk.Button(self.extraction_frame, text="Test Butonu", 
                                command=self.test_extraction_function)
        temp_button.pack(pady=20)
    
    def test_hiding_function(self):
        """Test fonksiyonu - veri gizleme"""
        messagebox.showinfo("Test", "Veri Gizleme tabında test butonuna tıklandı!")
    
    def test_extraction_function(self):
        """Test fonksiyonu - veri çıkarma"""
        messagebox.showinfo("Test", "Veri Çıkarma tabında test butonuna tıklandı!")

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()