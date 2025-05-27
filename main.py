import tkinter as tk
from home_screen import HomeScreen
from embed_screen import EmbedScreen
from extract_screen import ExtractScreen

class SteganografiUygulamasi:
    def __init__(self, master):
        self.master = master
        self.master.title("Görüntü Steganografi Uygulaması")
        self.master.geometry("900x600")
        self.master.configure(bg="#f0f0f0")
        
        # Ana çerçeve
        self.main_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Durum çubuğu (önce tanımla!)
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        self.status_bar = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Ekranlar
        self.current_screen = None
        self.show_home_screen()  # ✅ şimdi güvenle çağrılabilir

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
    
    def show_home_screen(self):
        self.clear_screen()
        self.current_screen = HomeScreen(self.main_frame, self)
        self.status_var.set("Ana Ekran")
    
    def show_embed_screen(self):
        self.clear_screen()
        self.current_screen = EmbedScreen(self.main_frame, self)
        self.status_var.set("Veri Gizleme Ekranı")
    
    def show_extract_screen(self):
        self.clear_screen()
        self.current_screen = ExtractScreen(self.main_frame, self)
        self.status_var.set("Veri Çıkarma Ekranı")
    
    def update_status(self, message):
        self.status_var.set(message)


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganografiUygulamasi(root)
    root.mainloop()