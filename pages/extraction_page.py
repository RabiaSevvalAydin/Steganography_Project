import tkinter as tk
from tkinter import ttk, messagebox
from tabs.text_extraction_tab import TextExtractionTab
from tabs.image_extraction_tab import ImageExtractionTab

class ExtractionPage:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.create_page()
    
    def create_page(self):
        """Veri çıkarma sayfasını oluştur"""
        # Ana frame
        self.page_frame = tk.Frame(self.parent)
        self.page_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Üst kısım - başlık ve ana sayfa butonu
        header_frame = tk.Frame(self.page_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Ana sayfa butonu
        home_button = ttk.Button(header_frame, text="🏠 Ana Sayfa", 
                                style='Home.TButton',
                                command=self.app.show_main_page)
        home_button.pack(side=tk.LEFT)
        
        # Sayfa başlığı
        title_label = tk.Label(header_frame, text="🔍 Veri Çıkarma", 
                              font=('Arial', 18, 'bold'), fg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Tab notebook
        self.notebook = ttk.Notebook(self.page_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab'ları oluştur
        self.text_extraction_tab = TextExtractionTab(self.notebook)
        self.image_extraction_tab = ImageExtractionTab(self.notebook)
        
        # Tab genişliklerini ayarla
        self.app.root.after(100, self.configure_tab_widths)
    
    def configure_tab_widths(self):
        """Tab genişliklerini eşit olarak ayarla"""
        self.app.root.update_idletasks()
        
        tab_count = len(self.notebook.tabs())
        if tab_count > 0:
            window_width = self.app.root.winfo_width() - 40
            tab_width = max(150, window_width // tab_count)
            
            style = ttk.Style()
            style.configure('TNotebook.Tab', width=tab_width, anchor='center')