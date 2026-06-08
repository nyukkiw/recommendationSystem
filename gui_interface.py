"""
GUI Interface untuk Sistem Rekomendasi Rumah - Fully Responsive & Adaptive Layout
"""
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
from recommendation_engine import RecommendationEngine, House
from typing import Dict

class RecommendationGUI:
    """GUI Modern dengan Sistem Grid Responsif Berbobot Dinamis"""
    
    def __init__(self, root: ctk.CTk, engine: RecommendationEngine):
        self.root = root
        self.engine = engine
        
        # Palet Warna Premium Modern
        self.COLORS = {
            'bg_main': '#f4f7fc',
            'bg_card': '#ffffff',
            'primary': '#1d63ed',       
            'primary_hover': '#154ec2',
            'text_dark': '#1e293b',     
            'text_muted': '#64748b',
            'border': '#e2e8f0',
            'success_bg': '#ecfdf5',    
            'success_text': '#059669'
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main Container untuk Rekomendasi Rumah
        main_container = ctk.CTkFrame(self.root, fg_color=self.COLORS['bg_main'])
        main_container.pack(fill='both', expand=True, padx=15, pady=(15, 45))
        
        # Setup konten visual
        self.setup_recommendation_tab(main_container)
        
        # Modern Footer Status Bar
        footer = ctk.CTkFrame(self.root, height=30, fg_color="#ffffff", corner_radius=0, border_width=1, border_color="#e2e8f0")
        footer.place(relx=0, rely=1, relwidth=1, anchor='sw')
        
        lbl_left = ctk.CTkLabel(footer, text=" 🏠 Sistem Rekomendasi Rumah ", font=('Segoe UI', 11), text_color=self.COLORS['text_muted'])
        lbl_left.pack(side='left', padx=15, pady=2)
        
        self.lbl_total_db = ctk.CTkLabel(footer, text=f"Total Data: {len(self.engine.get_all_houses())} Rumah 🗄️", font=('Segoe UI', 11, 'bold'), text_color=self.COLORS['text_muted'])
        self.lbl_total_db.pack(side='right', padx=15, pady=2)

    def setup_recommendation_tab(self, parent):
        """Layout Responsif: Menggunakan Pembagian Proporsi Grid Tanpa Batasan Minsize yang Kaku"""
        # FRAME UTAMA: Diubah menggunakan CTkFrame biasa (bukan scrollable luar) agar layout kanan-kiri tidak pecah ke samping
        main_grid = ctk.CTkFrame(parent, fg_color="transparent")
        main_grid.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Mengatur konfigurasi bobot kolom (35% kiri, 65% kanan) secara elastis
        main_grid.columnconfigure(0, weight=35) 
        main_grid.columnconfigure(1, weight=65) 
        main_grid.rowconfigure(0, weight=1)
        
        # ================= KOLOM KIRI: SCROLLABLE FORM INPUT =================
        # Memindahkan ScrollableFrame khusus ke bagian form input saja (Kek di YouTube, side-panelnya yang scrollable)
        left_card = ctk.CTkScrollableFrame(
            main_grid, 
            fg_color=self.COLORS['bg_card'], 
            corner_radius=12, 
            border_width=1, 
            border_color=self.COLORS['border'],
            label_text=""
        )
        left_card.grid(row=0, column=0, sticky='nsew', padx=(5, 8), pady=5)
        
        lbl_title_left = ctk.CTkLabel(left_card, text="👤 Preferensi Rumah Anda", font=('Segoe UI', 14, 'bold'), text_color=self.COLORS['text_dark'])
        lbl_title_left.pack(anchor='w', padx=10, pady=(10, 5))
        
        form_container = ctk.CTkFrame(left_card, fg_color="transparent")
        form_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        def create_input_field(parent, label_text, placeholder):
            lbl = ctk.CTkLabel(parent, text=label_text, font=('Segoe UI', 11, 'bold'), text_color=self.COLORS['text_dark'])
            lbl.pack(anchor='w', pady=(4, 2))
            entry = ctk.CTkEntry(parent, placeholder_text=placeholder, font=('Segoe UI', 12), height=34, corner_radius=8, border_color=self.COLORS['border'], fg_color="#ffffff", text_color=self.COLORS['text_dark'])
            entry.pack(fill='x', pady=(0, 4))
            return entry

        lbl_p = ctk.CTkLabel(form_container, text="💳 Rentang Harga (Juta)", font=('Segoe UI', 11, 'bold'), text_color=self.COLORS['text_dark'])
        lbl_p.pack(anchor='w', pady=(4, 2))
        
        price_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        price_frame.pack(fill='x')
        self.ent_min_price = ctk.CTkEntry(price_frame, placeholder_text="Min: 500", font=('Segoe UI', 12), height=34, corner_radius=8)
        self.ent_min_price.insert(0, "500")
        self.ent_min_price.pack(side='left', fill='x', expand=True, padx=(0, 3))
        
        self.ent_max_price = ctk.CTkEntry(price_frame, placeholder_text="Max: 3000", font=('Segoe UI', 12), height=34, corner_radius=8)
        self.ent_max_price.insert(0, "3000")
        self.ent_max_price.pack(side='right', fill='x', expand=True, padx=(3, 0))
        
        self.ent_bedrooms = create_input_field(form_container, "🛏️ Minimal Kamar Tidur", "Contoh: 3")
        self.ent_bedrooms.insert(0, "3")
        
        self.ent_bathrooms = create_input_field(form_container, "🚿 Minimal Kamar Mandi", "Contoh: 2")
        self.ent_bathrooms.insert(0, "2")
        
        self.ent_area = create_input_field(form_container, "📐 Luas Bangunan Minimal (m²)", "Contoh: 150")
        self.ent_area.insert(0, "200")
        
        self.ent_location = create_input_field(form_container, "📍 Prioritas Lokasi Sektor", "Contoh: Jakarta Selatan")
        
        self.ent_age = create_input_field(form_container, "📅 Maksimal Umur Bangunan (Tahun)", "Contoh: 10")
        self.ent_age.insert(0, "10")
        
        self.btn_search = ctk.CTkButton(
            form_container, text="🔍 Cari Rekomendasi", font=('Segoe UI', 13, 'bold'),
            fg_color=self.COLORS['primary'], hover_color=self.COLORS['primary_hover'],
            height=38, corner_radius=8, command=self.get_recommendations
        )
        self.btn_search.pack(fill='x', pady=(15, 5))
        
        btn_reset = ctk.CTkButton(
            form_container, text="🔄 Reset Filter", font=('Segoe UI', 11),
            fg_color="#f1f5f9", hover_color="#e2e8f0", text_color=self.COLORS['text_dark'],
            height=34, corner_radius=8, command=self.reset_inputs
        )
        btn_reset.pack(fill='x', pady=0)

        # ================= KOLOM KANAN: TABEL HASIL & DETAIL RESPONSIVE =================
        right_container = ctk.CTkFrame(main_grid, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky='nsew', padx=(8, 5), pady=5)
        
        right_container.columnconfigure(0, weight=1)
        right_container.rowconfigure(0, weight=70)  
        right_container.rowconfigure(1, weight=30)  
        
        # 1. Card Tabel Hasil Rekomendasi
        card_table = ctk.CTkFrame(right_container, fg_color=self.COLORS['bg_card'], corner_radius=12, border_width=1, border_color=self.COLORS['border'])
        card_table.grid(row=0, column=0, sticky='nsew', pady=(0, 8))
        
        lbl_title_right = ctk.CTkLabel(card_table, text="⭐ Rekomendasi Properti Terbaik", font=('Segoe UI', 15, 'bold'), text_color=self.COLORS['text_dark'])
        lbl_title_right.pack(anchor='w', padx=15, pady=(12, 2))
        
        # Banner Notifikasi Sukses
        self.alert_frame = ctk.CTkFrame(card_table, fg_color=self.COLORS['success_bg'], corner_radius=8)
        self.alert_label = ctk.CTkLabel(self.alert_frame, text="", text_color=self.COLORS['success_text'], font=('Segoe UI', 11, 'bold'), anchor='w')
        self.alert_label.pack(fill='x', padx=12, pady=5)
        self.alert_frame.pack_forget()
        
        table_frame = ctk.CTkFrame(card_table, fg_color="transparent")
        table_frame.pack(fill='both', expand=True, padx=15, pady=(2, 12))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview", 
            background="#ffffff", 
            fieldbackground="#ffffff", 
            rowheight=30,                   
            font=('Segoe UI', 11),          
            borderwidth=0
        )
        style.configure(
            "Custom.Treeview.Heading", 
            background=self.COLORS['primary'], 
            foreground="#ffffff", 
            font=('Segoe UI', 11, 'bold'),  
            rowheight=34, 
            borderwidth=0
        )
        style.map("Custom.Treeview.Heading", background=[('active', self.COLORS['primary_hover'])])
        
        columns = ('No', 'Nama', 'Harga', 'Lokasi', 'Fasilitas', 'Luas', 'Match Score')
        self.result_tree = ttk.Treeview(table_frame, columns=columns, show='headings', style="Custom.Treeview")
        
        self.result_tree.heading('No', text='No')
        self.result_tree.heading('Nama', text='Nama Rumah')
        self.result_tree.heading('Harga', text='Harga')
        self.result_tree.heading('Lokasi', text='Sektor Lokasi')
        self.result_tree.heading('Fasilitas', text='K. Tidur / Mandi')
        self.result_tree.heading('Luas', text='Luas m²')
        self.result_tree.heading('Match Score', text='Kecocokan')
        
        # Menggunakan bentangan proporsional (stretch=True) agar kolom tabel ikut mengecil/membesar otomatis
        self.result_tree.column('No', width=35, minwidth=30, anchor='center', stretch=False)
        self.result_tree.column('Nama', width=150, minwidth=100, anchor='w', stretch=True)
        self.result_tree.column('Harga', width=80, minwidth=70, anchor='center', stretch=True)
        self.result_tree.column('Lokasi', width=110, minwidth=80, anchor='w', stretch=True)
        self.result_tree.column('Fasilitas', width=100, minwidth=90, anchor='center', stretch=False)
        self.result_tree.column('Luas', width=70, minwidth=60, anchor='center', stretch=False)
        self.result_tree.column('Match Score', width=80, minwidth=70, anchor='center', stretch=False)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        self.result_tree.pack(side="left", fill='both', expand=True)
        self.result_tree.bind('<<TreeviewSelect>>', self.show_house_detail)
        
        # 2. Card Bawah: Panel Lembar Detail Spesifikasi (Auto-wrapping text)
        card_detail = ctk.CTkFrame(right_container, fg_color=self.COLORS['bg_card'], corner_radius=12, border_width=1, border_color=self.COLORS['border'])
        card_detail.grid(row=1, column=0, sticky='nsew', pady=(8, 0))
        
        lbl_title_detail = ctk.CTkLabel(card_detail, text="📋 Lembar Spesifikasi Unit", font=('Segoe UI', 13, 'bold'), text_color=self.COLORS['text_dark'])
        lbl_title_detail.pack(anchor='w', padx=15, pady=(8, 2))
        
        # Mengaktifkan wrap='word' agar teks spesifikasi otomatis turun ke bawah saat jendela mengecil
        self.txt_detail = tk.Text(card_detail, height=3, font=('Segoe UI', 11), bg='#f8fafc', fg=self.COLORS['text_dark'], bd=0, highlightthickness=0, padx=12, pady=8, wrap='word')
        self.txt_detail.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        self.txt_detail.insert('1.0', "Silakan pilih baris unit rumah di atas untuk memunculkan detail cetak spesifikasi fisik.")
        self.txt_detail.config(state='disabled')

    def get_recommendations(self):
        try:
            min_price = int(self.ent_min_price.get())
            max_price = int(self.ent_max_price.get())
            bedrooms = int(self.ent_bedrooms.get())
            bathrooms = int(self.ent_bathrooms.get())
            area = int(self.ent_area.get())
            location = self.ent_location.get()
            max_age = int(self.ent_age.get())
            
            if min_price > max_price:
                messagebox.showerror('Validation Error', 'Batas harga terendah dilarang melebihi harga tertinggi!')
                return
                
            preference = {
                'min_price': min_price, 'max_price': max_price,
                'bedrooms': bedrooms, 'bathrooms': bathrooms,
                'area': area, 'max_age': max_age
            }
            if location:
                preference['location'] = location
                
            recommendations = self.engine.recommend(preference, top_n=5)
            
            for row in self.result_tree.get_children():
                self.result_tree.delete(row)
                
            if not recommendations:
                self.alert_frame.pack_forget()
                messagebox.showinfo('Kosong', 'Kriteria rumah idaman Anda tidak ditemukan di database.')
                return
                
            for idx, (house, score) in enumerate(recommendations, 1):
                formatted_price = f"Rp {house.price:,}".replace(",", ".")
                self.result_tree.insert('', 'end', values=(
                    idx, house.name, formatted_price, house.location,
                    f"{house.bedrooms} / {house.bathrooms}", house.area, f"{score:.1%}"
                ))
                
            self.alert_label.configure(text=f"  ✅  Sukses! Algoritma CBR berhasil menyaring {len(recommendations)} alternatif terbaik.")
            self.alert_frame.pack(fill='x', padx=15, pady=2, before=self.result_tree)
            
        except ValueError:
            messagebox.showerror('Format Salah', 'Pastikan semua kotak isian berformat angka diisi dengan benar!')

    def show_house_detail(self, event):
        selection = self.result_tree.selection()
        if not selection: return
        
        item = selection[0]
        values = self.result_tree.item(item, 'values')
        house_name = values[1]
        
        house = next((h for h in self.engine.get_all_houses() if h.name == house_name), None)
        if house:
            formatted_price = f"Rp {house.price:,}".replace(",", ".")
            detail_str = (
                f"▪️ Nama Unit\t: {house.name}\n"
                f"▪️ Wilayah Sektor\t: {house.location}\n"
                f"▪️ Patokan Harga\t: {formatted_price} Juta Rupiah\n"
                f"▪️ Fasilitas Utama\t: {house.bedrooms} K. Tidur | {house.bathrooms} K. Mandi  |  Luas Bangunan: {house.area} m²\n"
                f"▪️ Umur Fisik & Fitur\t: {house.age} Tahun  •  ({', '.join(house.features) if house.features else '-'})"
            )
            self.txt_detail.config(state='normal')
            self.txt_detail.delete('1.0', 'end')
            self.txt_detail.insert('1.0', detail_str)
            self.txt_detail.config(state='disabled')

    def reset_inputs(self):
        self.ent_min_price.delete(0, 'end'); self.ent_min_price.insert(0, "500")
        self.ent_max_price.delete(0, 'end'); self.ent_max_price.insert(0, "3000")
        self.ent_bedrooms.delete(0, 'end'); self.ent_bedrooms.insert(0, "3")
        self.ent_bathrooms.delete(0, 'end'); self.ent_bathrooms.insert(0, "2")
        self.ent_area.delete(0, 'end'); self.ent_area.insert(0, "200")
        self.ent_location.delete(0, 'end')
        self.ent_age.delete(0, 'end'); self.ent_age.insert(0, "10")
        self.alert_frame.pack_forget()
        for row in self.result_tree.get_children(): self.result_tree.delete(row)