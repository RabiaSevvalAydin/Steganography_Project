import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    embed_text_to_image, 
    extract_text_from_image, 
    select_input_image,
    display_image
)
import os

class TextHidingTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.input_image_path = ""
        self.input_image = None
        self.output_image = None
        self.create_tab()
    
    def create_tab(self):
        """Yazı gizleme tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="📝 Yazı Gizle")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - SCROLLABLE Görüntü önizleme
        left_outer_frame = ttk.LabelFrame(main_container, text="Görüntü Önizleme", padding="5")
        left_outer_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas ve Scrollbar oluştur
        canvas = tk.Canvas(left_outer_frame, bg="#f8f8f8")
        scrollbar = ttk.Scrollbar(left_outer_frame, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = ttk.Frame(canvas)
        
        # Canvas'ı yapılandır
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            # Canvas genişliğini scrollable_frame'e uygula
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Canvas window oluştur ve referansını sakla
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Canvas ve scrollbar'ı yerleştir
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scroll desteği
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Scrollable frame içine resim önizlemesini ekle
        self.create_image_preview(scrollable_frame)
        
        # Sağ panel - Kontroller (SABİT GENİŞLİK)
        right_frame = ttk.LabelFrame(main_container, text="Kontrol Paneli", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        right_frame.configure(width=300)
        
        self.create_widgets(right_frame)
    
    def create_image_preview(self, parent):
        """Resim önizleme alanını oluştur (tam genişlik)"""
        
        # Başlık
        preview_label = ttk.Label(parent, text="Seçilen Resim:", font=('Arial', 10, 'bold'))
        preview_label.pack(fill=tk.X, pady=(5, 5))
        
        # Resim önizleme frame'i
        image_frame = tk.Frame(parent, bg="#f0f0f0", relief="sunken", bd=1, height=400)
        image_frame.pack(fill=tk.X, pady=(0, 10))
        image_frame.pack_propagate(False)
        
        # Resim önizleme label'ı
        self.image_preview = tk.Label(image_frame, bg="#f0f0f0", 
                                    text="Resim seçilmedi\n(Yazının gizleneceği ana resim)\n\nBuraya yüklenecek resim tam ekran görünecek",
                                    font=('Arial', 10), fg='gray')
        self.image_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # İşlem durumu göstergesi
        status_frame = ttk.LabelFrame(parent, text="İşlem Durumu", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.process_status_var = tk.StringVar(value="Henüz işlem yapılmadı")
        process_status_label = ttk.Label(status_frame, textvariable=self.process_status_var, 
                                        font=('Arial', 9, 'bold'), foreground='orange')
        process_status_label.pack()
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=5, wrap=tk.WORD, font=('Arial', 9),
                           state=tk.DISABLED, bg="#f9f9f9")
        info_text.pack(fill=tk.X)
        
        # Bilgi metnini ekle
        info_content = ("• Önce bir resim seçin, sonra gizlemek istediğiniz yazıyı girin.\n\n"
                       "• 'Yazıyı Gizle' butonuna tıklayarak yazıyı resme gizleyin.\n\n"
                       "• Steganografik resmi kaydetmeyi unutmayın!")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Resim seçme bölümü
        image_section = ttk.LabelFrame(parent, text="1. Resim Seçimi", padding="10")
        image_section.pack(fill=tk.X, pady=(0, 15))
        
        select_button = ttk.Button(image_section, text="📁 Resim Seç", 
                                  command=self.select_image, width=28)
        select_button.pack(pady=(0, 10))
        
        # Dosya yolu gösterme
        self.file_path_var = tk.StringVar(value="Dosya seçilmedi")
        path_label = ttk.Label(image_section, textvariable=self.file_path_var, 
                              wraplength=270, font=('Arial', 8))
        path_label.pack()
        
        # Yazı gizleme bölümü
        text_section = ttk.LabelFrame(parent, text="2. Yazı Girişi", padding="10")
        text_section.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        text_label = ttk.Label(text_section, text="Gizlenecek Yazı:", font=('Arial', 9, 'bold'))
        text_label.pack(pady=(0, 5))
        
        # Text widget frame
        text_frame = ttk.Frame(text_section)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.text_entry = tk.Text(text_frame, height=8, width=32, wrap=tk.WORD, font=('Arial', 9))
        scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar_text.set)
        
        self.text_entry.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")
        
        # Karakter sayacı
        self.char_count_var = tk.StringVar(value="0 karakter")
        char_count_label = ttk.Label(text_section, textvariable=self.char_count_var, 
                                    font=('Arial', 8), foreground='gray')
        char_count_label.pack()
        
        # Karakter sayacını güncelleme
        def update_char_count(event=None):
            text = self.text_entry.get("1.0", tk.END).strip()
            count = len(text)
            self.char_count_var.set(f"{count} karakter")
        
        self.text_entry.bind('<KeyRelease>', update_char_count)
        
        # İşlem butonları bölümü
        action_section = ttk.LabelFrame(parent, text="3. İşlemler", padding="10")
        action_section.pack(fill=tk.X, pady=(0, 15))
        
        hide_button = ttk.Button(action_section, text="🔒 Yazıyı Gizle", 
                                command=self.hide_text, width=28)
        hide_button.pack(pady=3)
        
        extract_button = ttk.Button(action_section, text="🔓 Yazıyı Çıkar (Test)", 
                                   command=self.extract_text, width=28)
        extract_button.pack(pady=3)
        
        save_button = ttk.Button(action_section, text="💾 Steganografik Resmi Kaydet", 
                                command=self.save_image, width=28)
        save_button.pack(pady=3)
        
        # Durum göstergesi
        status_section = ttk.LabelFrame(parent, text="Durum", padding="10")
        status_section.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(status_section, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack()
    
    def select_image(self):
        """Resim seçme fonksiyonu"""
        try:
            file_path = select_input_image()
            
            if file_path:
                self.input_image_path = file_path
                self.input_image = Image.open(file_path)
                
                # Görüntüyü önizlemede göster (daha büyük boyut)
                display_image(self.input_image, self.image_preview, (600, 380))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Görüntü başarıyla yüklendi")
                self.process_status_var.set("Resim yüklendi - Yazı girişi bekleniyor")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Görüntü yüklenemedi")
    
    def hide_text(self):
        """Yazı gizleme fonksiyonu"""
        if not self.input_image:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        text_to_hide = self.text_entry.get("1.0", tk.END).strip()
        if not text_to_hide:
            messagebox.showwarning("Uyarı", "Lütfen gizlenecek yazıyı girin!")
            return
        
        try:
            # Path'i kullanarak yazıyı resme gizle (output_path olarak input_path'i kullan)
            embed_text_to_image(self.input_image_path, text_to_hide, self.input_image_path)
            
            # İşlenen resmi yeniden yükle
            self.output_image = Image.open(self.input_image_path)
            
            # Sonucu önizlemede göster
            display_image(self.output_image, self.image_preview, (600, 380))
            
            self.status_var.set("Yazı başarıyla gizlendi!")
            self.process_status_var.set("Yazı gizlendi - Kaydetmeye hazır ✅")
            
            char_count = len(text_to_hide)
            messagebox.showinfo("Başarılı", f"Yazı resme başarıyla gizlendi!\n\nGizlenen yazı: {char_count} karakter\n\nOrijinal resim üzerine kaydedildi.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı gizleme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı gizlenemedi")
            self.process_status_var.set("İşlem başarısız ❌")
    
    def extract_text(self):
        """Yazı çıkarma fonksiyonu (test amaçlı)"""
        if not self.input_image:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim seçin!")
            return
        
        try:
            # Resimden yazıyı çıkar
            extracted_text = extract_text_from_image(self.input_image)
            
            if extracted_text.strip():
                # Çıkarılan yazıyı text widget'a yaz
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert("1.0", extracted_text)
                
                self.status_var.set("Yazı başarıyla çıkarıldı!")
                self.process_status_var.set("Test: Gizli yazı çıkarıldı ✅")
                
                char_count = len(extracted_text)
                messagebox.showinfo("Başarılı", f"Gizli yazı başarıyla çıkarıldı!\n\nÇıkarılan yazı: {char_count} karakter")
            else:
                messagebox.showinfo("Bilgi", "Bu resimde gizli yazı bulunamadı.")
                self.status_var.set("Gizli yazı bulunamadı")
                self.process_status_var.set("Test: Gizli yazı bulunamadı")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı çıkarılamadı")
    
    def save_image(self):
        """İşlenmiş resmi kaydetme fonksiyonu"""
        if not hasattr(self, 'output_image') or self.output_image is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek steganografik resim bulunamadı!\nÖnce yazı gizleme işlemi yapın.")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Steganografik Resmi Kaydet",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                self.output_image.save(file_path)
                filename = os.path.basename(file_path)
                self.status_var.set(f"Resim kaydedildi: {filename}")
                self.process_status_var.set("Steganografik resim kaydedildi! 🎉")
                
                # Dosya boyutu bilgisi
                file_size = os.path.getsize(file_path) / 1024
                messagebox.showinfo("Başarılı", f"Steganografik resim başarıyla kaydedildi:\n{filename}\n\nDosya boyutu: {file_size:.1f} KB")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Resim kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Resim kaydedilemedi")
