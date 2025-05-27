import tkinter as tk
from tkinter import ttk

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Başlık
        title_label = tk.Label(self, text="Görüntü Steganografi Uygulaması", 
                              font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(50, 30))
        
        # Açıklama
        desc_label = tk.Label(self, text="Görüntülerde veri gizleme ve çıkarma işlemleri yapabilirsiniz.", 
                             font=("Helvetica", 12), bg="#f0f0f0")
        desc_label.pack(pady=(0, 50))
        
        # Butonlar için çerçeve
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        # Gizleme butonu
        embed_button = tk.Button(button_frame, text="Veri Gizleme", 
                                command=self.controller.show_embed_screen,
                                width=20, height=3, font=("Helvetica", 12))
        embed_button.pack(side=tk.LEFT, padx=20)
        
        # Çıkarma butonu
        extract_button = tk.Button(button_frame, text="Veri Çıkarma", 
                                  command=self.controller.show_extract_screen,
                                  width=20, height=3, font=("Helvetica", 12))
        extract_button.pack(side=tk.LEFT, padx=20)