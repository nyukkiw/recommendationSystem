"""
GUI Interface untuk Sistem Rekomendasi Rumah
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from recommendation_engine import RecommendationEngine, House
from typing import Dict

class RecommendationGUI:
    """GUI untuk aplikasi rekomendasi rumah"""
    
    def __init__(self, root: tk.Tk, engine: RecommendationEngine):
        self.root = root
        self.engine = engine
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Setup styling untuk aplikasi"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define colors
        bg_color = '#f0f0f0'
        primary_color = '#4CAF50'
        secondary_color = '#2196F3'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background=bg_color)
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background=bg_color)
        style.configure('TButton', font=('Arial', 10))
        style.map('TButton', foreground=[('pressed', 'white')])
    
    def create_widgets(self):
        """Membuat semua widget GUI"""
        # Main container dengan notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Rekomendasi
        self.recommendation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recommendation_frame, text='Rekomendasi')
        self.create_recommendation_tab()
        
        # Tab 2: Database Rumah
        self.database_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.database_frame, text='Database Rumah')
        self.create_database_tab()
        
        # Tab 3: Import Data
        self.import_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.import_frame, text='Import Data')
        self.create_import_tab()
    
    def create_recommendation_tab(self):
        """Membuat tab untuk input preferensi dan menampilkan rekomendasi"""
        # Frame untuk input preferensi
        input_frame = ttk.LabelFrame(self.recommendation_frame, text='Preferensi Anda', padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        # Harga
        ttk.Label(input_frame, text='Harga (Juta Rupiah):').grid(row=0, column=0, sticky='w', pady=5)
        ttk.Label(input_frame, text='Min:').grid(row=0, column=1, sticky='w')
        self.min_price_var = tk.StringVar(value='500')
        ttk.Entry(input_frame, textvariable=self.min_price_var, width=10).grid(row=0, column=2, padx=5)
        
        ttk.Label(input_frame, text='Max:').grid(row=0, column=3, sticky='w')
        self.max_price_var = tk.StringVar(value='3000')
        ttk.Entry(input_frame, textvariable=self.max_price_var, width=10).grid(row=0, column=4, padx=5)
        
        # Kamar Tidur
        ttk.Label(input_frame, text='Kamar Tidur:').grid(row=1, column=0, sticky='w', pady=5)
        self.bedrooms_var = tk.StringVar(value='3')
        ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.bedrooms_var, width=10).grid(row=1, column=2)
        
        # Kamar Mandi
        ttk.Label(input_frame, text='Kamar Mandi:').grid(row=2, column=0, sticky='w', pady=5)
        self.bathrooms_var = tk.StringVar(value='2')
        ttk.Spinbox(input_frame, from_=1, to=5, textvariable=self.bathrooms_var, width=10).grid(row=2, column=2)
        
        # Luas Area
        ttk.Label(input_frame, text='Luas Area (m²):').grid(row=3, column=0, sticky='w', pady=5)
        self.area_var = tk.StringVar(value='200')
        ttk.Entry(input_frame, textvariable=self.area_var, width=10).grid(row=3, column=2, padx=5)
        
        # Lokasi
        ttk.Label(input_frame, text='Lokasi:').grid(row=4, column=0, sticky='w', pady=5)
        self.location_var = tk.StringVar(value='')
        ttk.Entry(input_frame, textvariable=self.location_var, width=30).grid(row=4, column=2, columnspan=3, padx=5)
        
        # Umur Rumah
        ttk.Label(input_frame, text='Max Umur Rumah (Tahun):').grid(row=5, column=0, sticky='w', pady=5)
        self.max_age_var = tk.StringVar(value='10')
        ttk.Spinbox(input_frame, from_=0, to=50, textvariable=self.max_age_var, width=10).grid(row=5, column=2)
        
        # Tombol untuk mencari rekomendasi
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=6, column=0, columnspan=5, pady=15)
        
        ttk.Button(button_frame, text='Cari Rekomendasi', 
                   command=self.get_recommendations).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Reset', 
                   command=self.reset_inputs).pack(side='left', padx=5)
        
        # Frame untuk hasil rekomendasi
        result_frame = ttk.LabelFrame(self.recommendation_frame, text='Hasil Rekomendasi', padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview untuk menampilkan hasil
        columns = ('No', 'Nama', 'Harga', 'Lokasi', 'Kamar', 'Area', 'Score')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, height=8)
        self.result_tree.column('#0', width=0, stretch=tk.NO)
        self.result_tree.column('No', anchor=tk.CENTER, width=30)
        self.result_tree.column('Nama', anchor=tk.W, width=150)
        self.result_tree.column('Harga', anchor=tk.CENTER, width=100)
        self.result_tree.column('Lokasi', anchor=tk.W, width=100)
        self.result_tree.column('Kamar', anchor=tk.CENTER, width=60)
        self.result_tree.column('Area', anchor=tk.CENTER, width=70)
        self.result_tree.column('Score', anchor=tk.CENTER, width=80)
        
        self.result_tree.heading('#0', text='', anchor=tk.W)
        self.result_tree.heading('No', text='No', anchor=tk.CENTER)
        self.result_tree.heading('Nama', text='Nama Rumah', anchor=tk.W)
        self.result_tree.heading('Harga', text='Harga (Juta)', anchor=tk.CENTER)
        self.result_tree.heading('Lokasi', text='Lokasi', anchor=tk.W)
        self.result_tree.heading('Kamar', text='Kamar', anchor=tk.CENTER)
        self.result_tree.heading('Area', text='Area (m²)', anchor=tk.CENTER)
        self.result_tree.heading('Score', text='Score', anchor=tk.CENTER)
        
        self.result_tree.pack(fill='both', expand=True)
        
        # Bind double-click untuk melihat detail
        self.result_tree.bind('<Double-1>', self.show_house_detail)
        
        # Detail frame
        detail_frame = ttk.LabelFrame(self.recommendation_frame, text='Detail Rumah', padding=10)
        detail_frame.pack(fill='x', padx=10, pady=10)
        
        self.detail_text = tk.Text(detail_frame, height=5, width=80, wrap='word', state='disabled')
        self.detail_text.pack(fill='both', expand=True)
    
    def create_database_tab(self):
        """Membuat tab untuk menampilkan semua rumah dalam database"""
        # Treeview untuk menampilkan semua rumah
        columns = ('No', 'Nama', 'Harga', 'Lokasi', 'Kamar', 'Kamar Mandi', 'Area', 'Umur')
        self.db_tree = ttk.Treeview(self.database_frame, columns=columns, height=20)
        self.db_tree.column('#0', width=0, stretch=tk.NO)
        self.db_tree.column('No', anchor=tk.CENTER, width=30)
        self.db_tree.column('Nama', anchor=tk.W, width=150)
        self.db_tree.column('Harga', anchor=tk.CENTER, width=100)
        self.db_tree.column('Lokasi', anchor=tk.W, width=100)
        self.db_tree.column('Kamar', anchor=tk.CENTER, width=60)
        self.db_tree.column('Kamar Mandi', anchor=tk.CENTER, width=80)
        self.db_tree.column('Area', anchor=tk.CENTER, width=70)
        self.db_tree.column('Umur', anchor=tk.CENTER, width=60)
        
        self.db_tree.heading('#0', text='', anchor=tk.W)
        self.db_tree.heading('No', text='No', anchor=tk.CENTER)
        self.db_tree.heading('Nama', text='Nama Rumah', anchor=tk.W)
        self.db_tree.heading('Harga', text='Harga (Juta)', anchor=tk.CENTER)
        self.db_tree.heading('Lokasi', text='Lokasi', anchor=tk.W)
        self.db_tree.heading('Kamar', text='Kamar', anchor=tk.CENTER)
        self.db_tree.heading('Kamar Mandi', text='K. Mandi', anchor=tk.CENTER)
        self.db_tree.heading('Area', text='Area (m²)', anchor=tk.CENTER)
        self.db_tree.heading('Umur', text='Umur (Th)', anchor=tk.CENTER)
        
        self.db_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.db_tree.bind('<Double-1>', self.show_house_detail)
        
        # Refresh database
        self.refresh_database()
    
    def create_import_tab(self):
        """Membuat tab untuk import data dari CSV"""
        frame = ttk.Frame(self.import_frame, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Judul
        ttk.Label(frame, text='Import Data Rumah dari CSV', 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Info
        info_text = """Format CSV yang diperlukan:
id,name,price,location,bedrooms,bathrooms,area,age,features

Contoh:
1,Rumah Mewah,2500,Jakarta,5,3,450,2,kolam renang;garasi
2,Rumah Modern,1200,BSD,3,2,200,1,smart home;keamanan
        """
        ttk.Label(frame, text=info_text, justify='left').pack(pady=20)
        
        # Button untuk browse file
        ttk.Button(frame, text='Pilih File CSV', 
                   command=self.browse_csv).pack(pady=10)
        
        # Label untuk menampilkan file yang dipilih
        self.csv_file_var = tk.StringVar(value='Tidak ada file yang dipilih')
        ttk.Label(frame, textvariable=self.csv_file_var, 
                  foreground='blue').pack(pady=5)
        
        # Button untuk import
        ttk.Button(frame, text='Import Data', 
                   command=self.import_csv).pack(pady=10)
    
    def get_recommendations(self):
        """Mendapatkan dan menampilkan rekomendasi"""
        try:
            # Validasi input
            min_price = int(self.min_price_var.get())
            max_price = int(self.max_price_var.get())
            bedrooms = int(self.bedrooms_var.get())
            bathrooms = int(self.bathrooms_var.get())
            area = int(self.area_var.get())
            location = self.location_var.get()
            max_age = int(self.max_age_var.get())
            
            if min_price < 0 or max_price < 0:
                messagebox.showerror('Error', 'Harga tidak boleh negatif')
                return
            
            if min_price > max_price:
                messagebox.showerror('Error', 'Harga minimum tidak boleh lebih besar dari maksimum')
                return
            
            # Buat preference dictionary
            preference = {
                'min_price': min_price,
                'max_price': max_price,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'area': area,
                'max_age': max_age
            }
            
            if location:
                preference['location'] = location
            
            # Dapatkan rekomendasi
            recommendations = self.engine.recommend(preference, top_n=5)
            
            # Tampilkan di treeview
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
            
            if not recommendations:
                messagebox.showinfo('Informasi', 'Tidak ada rekomendasi yang sesuai dengan preferensi Anda')
                return
            
            for idx, (house, score) in enumerate(recommendations, 1):
                self.result_tree.insert('', 'end', values=(
                    idx,
                    house.name,
                    f'Rp {house.price}',
                    house.location,
                    f'{house.bedrooms}/{house.bathrooms}',
                    house.area,
                    f'{score:.2%}'
                ))
            
            messagebox.showinfo('Sukses', f'Ditemukan {len(recommendations)} rekomendasi')
            
        except ValueError:
            messagebox.showerror('Error', 'Masukan harus berupa angka')
    
    def reset_inputs(self):
        """Reset semua input ke nilai default"""
        self.min_price_var.set('500')
        self.max_price_var.set('3000')
        self.bedrooms_var.set('3')
        self.bathrooms_var.set('2')
        self.area_var.set('200')
        self.location_var.set('')
        self.max_age_var.set('10')
        
        # Clear hasil
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
    
    def refresh_database(self):
        """Refresh tampilan database"""
        for item in self.db_tree.get_children():
            self.db_tree.delete(item)
        
        houses = self.engine.get_all_houses()
        for idx, house in enumerate(houses, 1):
            self.db_tree.insert('', 'end', values=(
                idx,
                house.name,
                f'Rp {house.price}',
                house.location,
                house.bedrooms,
                house.bathrooms,
                house.area,
                house.age
            ))
    
    def show_house_detail(self, event):
        """Menampilkan detail rumah saat diklik"""
        selection = self.result_tree.selection() or self.db_tree.selection()
        
        if not selection:
            return
        
        item = selection[0]
        values = self.result_tree.item(item, 'values') or self.db_tree.item(item, 'values')
        
        if not values:
            return
        
        # Cari house berdasarkan nama
        house_name = values[1]
        house = next((h for h in self.engine.get_all_houses() if h.name == house_name), None)
        
        if house:
            detail_str = f"""
DETAIL RUMAH

Nama: {house.name}
Harga: Rp {house.price} Juta
Lokasi: {house.location}
Kamar Tidur: {house.bedrooms}
Kamar Mandi: {house.bathrooms}
Luas Area: {house.area} m²
Umur Rumah: {house.age} tahun
Fitur: {', '.join(house.features) if house.features else 'Tidak ada fitur khusus'}
            """
            
            self.detail_text.config(state='normal')
            self.detail_text.delete('1.0', 'end')
            self.detail_text.insert('1.0', detail_str)
            self.detail_text.config(state='disabled')
    
    def browse_csv(self):
        """Browse file CSV"""
        filename = filedialog.askopenfilename(
            title='Pilih file CSV',
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')]
        )
        
        if filename:
            self.csv_file_var.set(filename)
    
    def import_csv(self):
        """Import data dari CSV"""
        csv_file = self.csv_file_var.get()
        
        if csv_file == 'Tidak ada file yang dipilih':
            messagebox.showerror('Error', 'Pilih file CSV terlebih dahulu')
            return
        
        success, message = self.engine.add_houses_from_csv(csv_file)
        
        if success:
            messagebox.showinfo('Sukses', message)
            self.refresh_database()
        else:
            messagebox.showerror('Error', message)
