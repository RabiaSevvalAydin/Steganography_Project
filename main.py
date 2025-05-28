import tkinter as tk
from tkinter import ttk
from pages.main_page import MainPage
from pages.hiding_page import HidingPage
from pages.extraction_page import ExtractionPage

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
        
        # Sayfa örneklerini oluştur
        self.main_page = None
        self.hiding_page = None
        self.extraction_page = None
        
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
        self.main_page = MainPage(self.main_container, self)
        
    def show_hiding_page(self):
        """Veri gizleme sayfasını göster"""
        self.clear_container()
        self.hiding_page = HidingPage(self.main_container, self)
        
    def show_extraction_page(self):
        """Veri çıkarma sayfasını göster"""
        self.clear_container()
        self.extraction_page = ExtractionPage(self.main_container, self)

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()