import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Uygulaması")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Ana pencere için stil ayarları
        self.setup_styles()
        
        # Ana container frame
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Ana sayfayı göster
        self.show_main_page()
        
    def setup_styles(self):
        """GUI stil ayarlarını yapılandır"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Büyük buton stili
        style.configure('Big.TButton', font=('Arial', 14, 'bold'), padding=20)
        style.configure('Home.TButton', font=('Arial', 10), padding=10)
        
    def clear_container(self):
        """Ana container'ı temizle"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_main_page(self):
        """Ana sayfayı göster"""
        self.clear_container()
        
        # Ana sayfa frame'i
        main_frame = tk.Frame(self.main_container, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = tk.Label(main_frame, text="🔐 Steganography Uygulaması", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=50)
        
        # Alt başlık
        subtitle_label = tk.Label(main_frame, text="Resimlerde veri gizleme ve çıkarma işlemleri", 
                                 font=('Arial', 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 50))
        
        # Buton frame'i
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Veri Gizleme butonu
        hide_button = ttk.Button(button_frame, text="📁 Veri Gizleme", 
                                style='Big.TButton',
                                command=self.show_hiding_page)
        hide_button.pack(pady=20, ipadx=30, ipady=10)
        
        # Veri Çıkarma butonu
        extract_button = ttk.Button(button_frame, text="🔍 Veri Çıkarma", 
                                   style='Big.TButton',
                                   command=self.show_extraction_page)
        extract_button.pack(pady=20, ipadx=30, ipady=10)
    
    def show_hiding_page(self):
        """Veri gizleme sayfasını göster"""
        self.clear_container()
        
        # Ana frame
        page_frame = tk.Frame(self.main_container)
        page_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Üst kısım - başlık ve ana sayfa butonu
        header_frame = tk.Frame(page_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Ana sayfa butonu
        home_button = ttk.Button(header_frame, text="🏠 Ana Sayfa", 
                                style='Home.TButton',
                                command=self.show_main_page)
        home_button.pack(side=tk.LEFT)
        
        # Sayfa başlığı
        title_label = tk.Label(header_frame, text="📁 Veri Gizleme", 
                              font=('Arial', 18, 'bold'), fg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Tab notebook
        self.hiding_notebook = ttk.Notebook(page_frame)
        self.hiding_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab'ları oluştur
        self.create_text_hiding_tab()
        self.create_image_hiding_tab()
        
        # Tab genişliklerini ayarla
        self.root.after(100, lambda: self.configure_tab_widths(self.hiding_notebook))
    
    def show_extraction_page(self):
        """Veri çıkarma sayfasını göster"""
        self.clear_container()
        
        # Ana frame
        page_frame = tk.Frame(self.main_container)
        page_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Üst kısım - başlık ve ana sayfa butonu
        header_frame = tk.Frame(page_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Ana sayfa butonu
        home_button = ttk.Button(header_frame, text="🏠 Ana Sayfa", 
                                style='Home.TButton',
                                command=self.show_main_page)
        home_button.pack(side=tk.LEFT)
        
        # Sayfa başlığı
        title_label = tk.Label(header_frame, text="🔍 Veri Çıkarma", 
                              font=('Arial', 18, 'bold'), fg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Tab notebook
        self.extraction_notebook = ttk.Notebook(page_frame)
        self.extraction_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab'ları oluştur
        self.create_text_extraction_tab()
        self.create_image_extraction_tab()
        
        # Tab genişliklerini ayarla
        self.root.after(100, lambda: self.configure_tab_widths(self.extraction_notebook))
    
    def configure_tab_widths(self, notebook):
        """Tab genişliklerini eşit olarak ayarla"""
        self.root.update_idletasks()
        
        tab_count = len(notebook.tabs())
        if tab_count > 0:
            window_width = self.root.winfo_width() - 40
            tab_width = max(150, window_width // tab_count)
            
            style = ttk.Style()
            style.configure('TNotebook.Tab', width=tab_width, anchor='center')
    
    def create_text_hiding_tab(self):
        """Yazı gizleme tabını oluştur"""
        text_frame = ttk.Frame(self.hiding_notebook)
        self.hiding_notebook.add(text_frame, text="📝 Yazı Gizle")
        
        # İçerik
        content_frame = ttk.LabelFrame(text_frame, text="Resime Yazı Gizleme", padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = ttk.Label(content_frame, 
                              text="Bu bölümde resim içine yazı gizleme işlemleri yapılacak.",
                              font=('Arial', 11))
        info_label.pack(pady=20)
        
        test_button = ttk.Button(content_frame, text="Yazı Gizle Test", 
                                command=lambda: messagebox.showinfo("Test", "Yazı gizleme seçildi!"))
        test_button.pack(pady=10)
    
    def create_image_hiding_tab(self):
        """Resim gizleme tabını oluştur"""
        image_frame = ttk.Frame(self.hiding_notebook)
        self.hiding_notebook.add(image_frame, text="🖼️ Resim Gizle")
        
        # İçerik
        content_frame = ttk.LabelFrame(image_frame, text="Resime Resim Gizleme", padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = ttk.Label(content_frame, 
                              text="Bu bölümde resim içine başka bir resim gizleme işlemleri yapılacak.",
                              font=('Arial', 11))
        info_label.pack(pady=20)
        
        test_button = ttk.Button(content_frame, text="Resim Gizle Test", 
                                command=lambda: messagebox.showinfo("Test", "Resim gizleme seçildi!"))
        test_button.pack(pady=10)
    
    def create_text_extraction_tab(self):
        """Yazı çıkarma tabını oluştur"""
        text_frame = ttk.Frame(self.extraction_notebook)
        self.extraction_notebook.add(text_frame, text="📝 Yazı Çıkar")
        
        # İçerik
        content_frame = ttk.LabelFrame(text_frame, text="Resimden Yazı Çıkarma", padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = ttk.Label(content_frame, 
                              text="Bu bölümde resimden gizli yazı çıkarma işlemleri yapılacak.",
                              font=('Arial', 11))
        info_label.pack(pady=20)
        
        test_button = ttk.Button(content_frame, text="Yazı Çıkar Test", 
                                command=lambda: messagebox.showinfo("Test", "Yazı çıkarma seçildi!"))
        test_button.pack(pady=10)
    
    def create_image_extraction_tab(self):
        """Resim çıkarma tabını oluştur"""
        image_frame = ttk.Frame(self.extraction_notebook)
        self.extraction_notebook.add(image_frame, text="🖼️ Resim Çıkar")
        
        # İçerik
        content_frame = ttk.LabelFrame(image_frame, text="Resimden Resim Çıkarma", padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = ttk.Label(content_frame, 
                              text="Bu bölümde resimden gizli resim çıkarma işlemleri yapılacak.",
                              font=('Arial', 11))
        info_label.pack(pady=20)
        
        test_button = ttk.Button(content_frame, text="Resim Çıkar Test", 
                                command=lambda: messagebox.showinfo("Test", "Resim çıkarma seçildi!"))
        test_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()