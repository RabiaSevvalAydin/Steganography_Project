import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from functions.steganography_functions import (
    extract_text_from_image, 
    select_steganographic_image,
    save_text_to_file,
    display_image
)
import os

class TextExtractionTab:
    def __init__(self, notebook):
        self.notebook = notebook
        self.image_path = ""
        self.image = None
        self.extracted_text = ""
        self.create_tab()
    
    def create_tab(self):
        """Yazı çıkarma tabını oluştur"""
        self.frame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame, text="🔍 Yazı Çıkar")
        
        # Ana container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sol panel - SCROLLABLE Görüntü önizleme
        left_outer_frame = ttk.LabelFrame(main_container, text="Steganografik Görüntü", padding="5")
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
        right_frame.configure(width=280)
        
        self.create_widgets(right_frame)
    
    def create_image_preview(self, parent):
        """Resim önizleme alanını oluştur (tam genişlik)"""
        
        # Başlık
        preview_label = ttk.Label(parent, text="Steganografik Görüntü:", font=('Arial', 10, 'bold'))
        preview_label.pack(fill=tk.X, pady=(5, 5))
        
        # Resim önizleme frame'i
        image_frame = tk.Frame(parent, bg="#f0f0f0", relief="sunken", bd=1, height=400)
        image_frame.pack(fill=tk.X, pady=(0, 10))
        image_frame.pack_propagate(False)
        
        # Resim önizleme label'ı
        self.image_preview = tk.Label(image_frame, bg="#f0f0f0", 
                                    text="Steganografik görüntü seçilmedi\n(İçinde gizli yazı olan resim)\n\nBuraya yüklenecek resim tam ekran görünecek",
                                    font=('Arial', 10), fg='gray')
        self.image_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bilgi kutusu
        info_frame = ttk.LabelFrame(parent, text="Bilgi", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, font=('Arial', 9),
                           state=tk.DISABLED, bg="#f9f9f9")
        info_text.pack(fill=tk.X)
        
        # Bilgi metnini ekle
        info_content = ("• Steganografik resim, içinde gizli yazı bulunan resimdir.\n\n"
                       "• Bu resim genellikle 'Yazı Gizle' sekmesinde oluşturulmuş olmalıdır.\n\n"
                       "• Çıkarılan yazı otomatik olarak sağ panelde gösterilecektir.\n\n"
                       "• Resim yüklendikten sonra 'Gizli Yazıyı Çıkar' butonuna tıklayın.")
        
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", info_content)
        info_text.config(state=tk.DISABLED)
    
    def create_widgets(self, parent):
        """Kontrol widget'larını oluştur"""
        
        # Resim seçme butonu
        select_button = ttk.Button(parent, text="📁 Steganografik Resim Seç", 
                                  command=self.select_image, width=30)
        select_button.pack(pady=(0, 15))
        
        # Dosya yolu gösterme
        self.file_path_var = tk.StringVar(value="Dosya seçilmedi")
        path_label = ttk.Label(parent, textvariable=self.file_path_var, 
                              wraplength=250, font=('Arial', 8))
        path_label.pack(pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Çıkar butonu
        extract_button = ttk.Button(parent, text="🔓 Gizli Yazıyı Çıkar", 
                                   command=self.extract_text, width=30)
        extract_button.pack(pady=(0, 20))
        
        # Çıkarılan yazı bölümü
        text_label = ttk.Label(parent, text="Çıkarılan Gizli Yazı:", font=('Arial', 10, 'bold'))
        text_label.pack(pady=(0, 5))
        
        # Text widget frame
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.result_text = tk.Text(text_frame, height=12, width=35, wrap=tk.WORD, 
                                  state=tk.DISABLED, bg="#f5f5f5")
        scrollbar_text = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar_text.set)
        
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")
        
        # Kaydet butonu
        save_button = ttk.Button(parent, text="💾 Yazıyı Dosyaya Kaydet", 
                                command=self.save_text, width=30)
        save_button.pack(pady=10)
        
        # Separator
        ttk.Separator(parent, orient='horizontal').pack(fill='x', pady=10)
        
        # Durum göstergesi
        self.status_var = tk.StringVar(value="Hazır")
        status_label = ttk.Label(parent, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.pack(pady=10)
    
    def select_image(self):
        """Steganografik resim seçme fonksiyonu"""
        try:
            file_path = select_steganographic_image()
            
            if file_path:
                self.image_path = file_path
                self.image = Image.open(file_path)
                
                # Görüntüyü önizlemede göster (daha büyük boyut)
                display_image(self.image, self.image_preview, (600, 380))
                
                # Dosya yolunu güncelle
                filename = os.path.basename(file_path)
                self.file_path_var.set(f"Seçilen: {filename}")
                self.status_var.set("Steganografik görüntü yüklendi")
                
                # Önceki çıkarılan yazıyı temizle
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete("1.0", tk.END)
                self.result_text.config(state=tk.DISABLED)
                self.extracted_text = ""
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {str(e)}")
            self.status_var.set("Hata: Görüntü yüklenemedi")
    
    def extract_text(self):
        """Gizli yazıyı çıkarma fonksiyonu"""
        if not hasattr(self, 'image_path') or not self.image_path:
            messagebox.showwarning("Uyarı", "Lütfen önce steganografik bir resim seçin!")
            return
        
        try:
            # Resimden gizli yazıyı çıkar (path gönder)
            extracted_result = extract_text_from_image(self.image_path)
            
            # None kontrolü ekle
            self.extracted_text = extracted_result if extracted_result is not None else ""
            
            # Sonucu göster
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            
            if self.extracted_text and self.extracted_text.strip():
                self.result_text.insert("1.0", self.extracted_text)
                self.status_var.set("Gizli yazı başarıyla çıkarıldı!")
                messagebox.showinfo("Başarılı", f"Gizli yazı başarıyla çıkarıldı!\n\nÇıkarılan yazı {len(self.extracted_text)} karakter uzunluğunda.")
            else:
                self.result_text.insert("1.0", "Bu resimde gizli yazı bulunamadı.")
                self.status_var.set("Gizli yazı bulunamadı")
                messagebox.showinfo("Bilgi", "Bu resimde gizli yazı bulunamadı.\n\nLütfen steganografik bir resim seçtiğinizden emin olun.")
            
            self.result_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı çıkarma sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı çıkarılamadı")
            # Hata durumunda result_text'i temizle
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.config(state=tk.DISABLED)
    
    def save_text(self):
        """Çıkarılan yazıyı dosyaya kaydetme fonksiyonu"""
        if not self.extracted_text.strip():
            messagebox.showwarning("Uyarı", "Kaydedilecek yazı bulunamadı!\nÖnce yazı çıkarma işlemi yapın.")
            return
        
        try:
            file_path = save_text_to_file(self.extracted_text)
            
            if file_path:
                filename = os.path.basename(file_path)
                self.status_var.set(f"Yazı kaydedildi: {filename}")
                messagebox.showinfo("Başarılı", f"Çıkarılan yazı başarıyla kaydedildi:\n{filename}\n\nKarakter sayısı: {len(self.extracted_text)}")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Yazı kaydetme sırasında hata oluştu: {str(e)}")
            self.status_var.set("Hata: Yazı kaydedilemedi")
