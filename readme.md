# Sistem Rekomendasi Rumah

Aplikasi Python sederhana untuk merekomendasikan rumah berdasarkan preferensi pengguna menggunakan Case-Based Reasoning (CBR).

## Fitur Utama

1. **Case-Based Reasoning Engine**
   - Sistem rekomendasi menggunakan similarity matching
   - Weighted scoring system untuk perhitungan similarity
   - Mendukung multiple preference criteria

2. **GUI Interface (Tkinter)**
   - User-friendly interface dengan 3 tab utama:
     - **Tab Rekomendasi**: Input preferensi dan lihat hasil rekomendasi
     - **Tab Database Rumah**: Lihat semua data rumah dalam database
     - **Tab Import Data**: Import data rumah dari file CSV

3. **Database Management**
   - Menyimpan dan mengelola data rumah
   - Support import dari CSV
   - Pre-loaded sample data

## Struktur File

```
recommendation_app/
├── main.py                      # Entry point aplikasi
├── recommendation_engine.py     # Core recommendation engine (CBR)
├── gui_interface.py            # GUI implementation (Tkinter)
├── sample_data.csv             # Sample dataset untuk testing
└── readme.md                   # Dokumentasi
```

## Requirements

- Python 3.7+
- tkinter (biasanya sudah termasuk dengan Python)

## Instalasi

1. Pastikan Python sudah terinstall di sistem Anda
2. Buka terminal/command prompt
3. Navigate ke folder project

## Cara Menjalankan

```bash
python main.py
```

## Cara Menggunakan

### 1. Tab Rekomendasi

1. Atur preferensi Anda:
   - **Harga (Juta Rupiah)**: Range harga minimum dan maksimum
   - **Kamar Tidur**: Jumlah kamar tidur yang diinginkan
   - **Kamar Mandi**: Jumlah kamar mandi yang diinginkan
   - **Luas Area**: Luas area rumah dalam m²
   - **Lokasi**: Lokasi/area yang diinginkan (optional)
   - **Max Umur Rumah**: Umur maksimal rumah dalam tahun

2. Klik tombol "Cari Rekomendasi"
3. Lihat hasil rekomendasi dengan score similarity
4. Double-click pada hasil untuk melihat detail rumah

### 2. Tab Database Rumah

- Menampilkan semua rumah dalam database
- Double-click untuk melihat detail rumah
- Menampilkan informasi: harga, lokasi, jumlah kamar, luas area, dan umur rumah

### 3. Tab Import Data

Untuk import data dari CSV:
1. Klik "Pilih File CSV"
2. Pilih file CSV dengan format yang benar
3. Klik "Import Data"

## Format CSV

```
id,name,price,location,bedrooms,bathrooms,area,age,features
1,Rumah Mewah,2500,Jakarta,5,3,450,2,kolam renang;garasi;taman
2,Rumah Modern,1200,BSD,3,2,200,1,smart home;keamanan
```

## Algoritma Recommendation

Menggunakan **Case-Based Reasoning** dengan weighted similarity scoring:

- **Price (25%)**
- **Location (20%)**
- **Area (20%)**
- **Bedrooms (15%)**
- **Age (10%)**
- **Bathrooms (10%)**

## Status

✅ Implementasi Selesai:
- ✅ Core recommendation engine dengan CBR
- ✅ GUI dengan Tkinter (3 tabs)
- ✅ Database management
- ✅ Import CSV
- ✅ Sample data

Siap untuk disambungkan dengan dataset yang lebih besar!

