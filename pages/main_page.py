import tkinter as tk
from tkinter import ttk

class MainPage:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.create_page()
    
    def create_page(self):
        """Ana sayfayı oluştur"""
        # Ana sayfa frame'i
        self.main_frame = tk.Frame(self.parent, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = tk.Label(self.main_frame, text="🔐 Steganography Uygulaması", 
                              font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=50)
        
        # Alt başlık
        subtitle_label = tk.Label(self.main_frame, text="Resimlerde veri gizleme ve çıkarma işlemleri", 
                                 font=('Arial', 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 50))
        
        # Buton frame'i
        button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        button_frame.pack(expand=True)
        
        # Veri Gizleme butonu
        hide_button = ttk.Button(button_frame, text="📁 Veri Gizleme", 
                                style='Big.TButton',
                                command=self.app.show_hiding_page)
        hide_button.pack(pady=20, ipadx=30, ipady=10)
        
        # Veri Çıkarma butonu
        extract_button = ttk.Button(button_frame, text="🔍 Veri Çıkarma", 
                                   style='Big.TButton',
                                   command=self.app.show_extraction_page)
        extract_button.pack(pady=20, ipadx=30, ipady=10)