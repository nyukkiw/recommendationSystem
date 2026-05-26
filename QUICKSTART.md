# QUICK START GUIDE

## Instalasi & Menjalankan (Windows)

### Step 1: Buka Command Prompt
1. Tekan `Win + R`
2. Ketik `cmd` dan tekan Enter

### Step 2: Navigate ke Folder Project
```bash
cd "c:\Users\User\OneDrive\Documents\sms 6\SISTEM REKOMENDASI A CLASS\recommendation_app"
```

### Step 3: Jalankan Aplikasi
```bash
python main.py
```

Aplikasi akan terbuka dalam 2-3 detik.

---

## Cara Cepat Testing

### 1. Test Rekomendasi dengan Data Sample
1. Buka tab "Rekomendasi"
2. Biarkan semua input dengan nilai default
3. Klik "Cari Rekomendasi"
4. Lihat 5 hasil rekomendasi terbaik
5. Double-click untuk melihat detail

### 2. Lihat Semua Data
1. Buka tab "Database Rumah"
2. Lihat semua 6 rumah sample data
3. Double-click untuk detail lengkap

### 3. Import Data Baru (Optional)
1. Buka tab "Import Data"
2. Baca format CSV yang diperlukan
3. Siapkan file CSV dengan data rumah Anda
4. Klik "Pilih File CSV" dan pilih file
5. Klik "Import Data"

---

## Contoh Preferensi Testing

### Test Case 1: Budget Terbatas
- Harga Min: 500
- Harga Max: 1000
- Kamar Tidur: 2
- Kamar Mandi: 1
- Luas Area: 150
- Max Umur: 5

### Test Case 2: Rumah Mewah
- Harga Min: 1500
- Harga Max: 3000
- Kamar Tidur: 4
- Kamar Mandi: 3
- Luas Area: 300
- Max Umur: 3

### Test Case 3: Dekat Stasiun (Cibubur)
- Harga Min: 500
- Harga Max: 1500
- Lokasi: Cibubur
- Kamar Tidur: 3
- Klik "Cari Rekomendasi"

---

## Troubleshooting

### Error: "No module named 'tkinter'"
**Solusi:**
- Windows: Reinstall Python dan centang "tcl/tk and IDLE"
- Linux: `sudo apt-get install python3-tk`
- macOS: `brew install python-tk`

### Aplikasi lambat/lag
- Ini normal untuk aplikasi Python GUI
- Bisa di-optimize dengan menggunakan PyQt5 atau PySide2 (untuk development lanjutan)

### CSV tidak bisa di-import
- Cek format kolom: id, name, price, location, bedrooms, bathrooms, area, age, features
- Pastikan menggunakan UTF-8 encoding
- Jangan ada spasi di awal/akhir cell

---

## Next Steps

Setelah testing selesai, Anda bisa:

1. **Tambah Data Real**
   - Buat file CSV dengan data rumah sebenarnya
   - Import melalui tab "Import Data"

2. **Customize Preferensi**
   - Edit `gui_interface.py` untuk menambah field baru
   - Edit `recommendation_engine.py` untuk menambah logic baru

3. **Improve UI**
   - Ganti tkinter dengan PyQt5 untuk tampilan lebih modern
   - Tambahkan gambar/foto rumah
   - Tambahkan map integration

4. **Tambah Fitur**
   - Sorting & filtering hasil
   - Comparison mode (bandingkan 2 rumah)
   - Favorite/bookmark rumah
   - Export hasil ke PDF

---

## Support

File yang penting:
- `main.py` - Entry point
- `recommendation_engine.py` - Logic rekomendasi (Case-Based Reasoning)
- `gui_interface.py` - Interface GUI
- `sample_data.csv` - Data sample untuk testing
- `readme.md` - Dokumentasi lengkap

Untuk pertanyaan lebih detail, baca `readme.md`

Good luck! 🚀
