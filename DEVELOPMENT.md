# DEVELOPMENT GUIDE

## Arsitektur Aplikasi

```
┌─────────────────────────────────────────┐
│         main.py (Entry Point)           │
│  - Initialize Tkinter root window       │
│  - Create RecommendationEngine          │
│  - Create RecommendationGUI             │
└────────────────┬────────────────────────┘
                 │
     ┌───────────┴──────────┐
     │                      │
┌────▼──────────────────┐   │
│ recommendation_engine │   │
│                       │   │
│ - House (class)       │   │
│ - RecommendationEngine│   │
│   - load_sample_data()│   │
│   - calculate_similarity()
│   - recommend()       │   │
│   - add_house()       │   │
│   - add_houses_from_csv()
└──────────────────────┘    │
                            │
                    ┌───────▼──────────────┐
                    │   gui_interface      │
                    │                      │
                    │ - RecommendationGUI  │
                    │   - create_widgets() │
                    │   - get_recommendations()
                    │   - refresh_database()
                    │   - import_csv()     │
                    └──────────────────────┘
```

## File Structure & Descriptions

### 1. main.py
**Tujuan**: Entry point aplikasi

**Isi**:
- Import dependencies
- Create Tkinter root window
- Initialize RecommendationEngine
- Create GUI
- Start mainloop

**Cara Extend**:
- Tambahkan argument parsing jika ingin CLI mode
- Tambahkan config loading dari file

---

### 2. recommendation_engine.py
**Tujuan**: Core logic untuk rekomendasi berbasis Case-Based Reasoning

**Classes**:
```
House:
  - id: int
  - name: str
  - price: int (jutaan rupiah)
  - location: str
  - bedrooms: int
  - bathrooms: int
  - area: int (m²)
  - age: int (tahun)
  - features: List[str]
  
  Methods:
  - to_dict(): Dict
```

```
RecommendationEngine:
  Methods:
  - load_sample_data(): Muat data sample
  - calculate_similarity(preference, house): float
      Menghitung similarity score 0-1
      Menggunakan weighted scoring
      
  - recommend(preference, top_n): List[Tuple[House, float]]
      Return top N recommended houses with scores
      
  - get_all_houses(): List[House]
      Return semua house dalam database
      
  - add_house(house): None
      Tambah satu house ke database
      
  - add_houses_from_csv(filepath): Tuple[bool, str]
      Import houses dari CSV file
      Return (success, message)
```

**Similarity Calculation**:
```
Score = Σ(Factor_Score × Weight)

Weights:
- price: 0.25 (25%)
- location: 0.20 (20%)
- area: 0.20 (20%)
- bedrooms: 0.15 (15%)
- age: 0.10 (10%)
- bathrooms: 0.10 (10%)
Total = 1.0

Scoring Logic:
- Price: Cek range [min, max]
- Location: String matching
- Area: Tolerance ±20% dari preference
- Bedrooms: Difference-based penalty
- Age: Prefer younger houses
- Bathrooms: Difference-based penalty
```

**Cara Extend**:
1. Tambah atribut House:
   ```python
   self.condition = condition  # Baru atau Bekas
   self.parking = parking      # Tipe parkir
   ```

2. Tambah weight di calculate_similarity():
   ```python
   weights = {
       'price': 0.25,
       'condition': 0.15,  # Baru
       ...
   }
   ```

3. Implementasi scoring logic untuk atribut baru

---

### 3. gui_interface.py
**Tujuan**: GUI dengan Tkinter

**Main Class**: RecommendationGUI

**Tabs**:
1. **Recommendation Tab**
   - Input preference fields
   - "Cari Rekomendasi" button
   - Treeview untuk hasil
   - Detail panel untuk house yang dipilih

2. **Database Tab**
   - Treeview menampilkan semua houses
   - Double-click untuk detail

3. **Import Tab**
   - Browse CSV file
   - Import button dengan validation

**Cara Extend**:

1. **Tambah Input Field**:
```python
# Di create_recommendation_tab()
ttk.Label(input_frame, text='Tipe Rumah:').grid(row=7, column=0, sticky='w')
self.house_type_var = tk.StringVar(value='')
ttk.Combobox(input_frame, textvariable=self.house_type_var, 
             values=['Rumah', 'Apartemen', 'Villa']).grid(row=7, column=2)

# Di get_recommendations()
house_type = self.house_type_var.get()
preference['house_type'] = house_type
```

2. **Tambah Output Column**:
```python
# Di create_recommendation_tab()
columns = ('No', 'Nama', 'Harga', 'Lokasi', 'Kamar', 'Area', 'Tipe', 'Score')
# ... setup columns
```

3. **Ubah Styling**:
```python
# Di setup_styles()
style.configure('Custom.TButton', font=('Arial', 12))
```

4. **Tambah Tab Baru**:
```python
# Di create_widgets()
self.statistics_frame = ttk.Frame(self.notebook)
self.notebook.add(self.statistics_frame, text='Statistik')
self.create_statistics_tab()

# Definisikan method create_statistics_tab()
```

---

## How Case-Based Reasoning Works

CBR adalah pendekatan AI yang:
1. **Retrieve**: Ambil cases (rumah) yang mirip dari knowledge base
2. **Reuse**: Gunakan solusi dari cases yang mirip
3. **Revise**: Adapt solution jika diperlukan
4. **Retain**: Simpan case baru untuk penggunaan mendatang

Dalam aplikasi ini:
- **Cases**: Data rumah dalam database
- **Features**: Price, location, area, bedrooms, etc.
- **Similarity**: Weighted scoring system
- **Recommendation**: Top-N houses dengan highest similarity

---

## CSV Import Format

```csv
id,name,price,location,bedrooms,bathrooms,area,age,features
1,Rumah Mewah,2500,Jakarta,5,3,450,2,kolam renang;garasi;taman
2,Rumah Praktis,1000,Bekasi,3,2,150,5,dekat stasiun;aman;nyaman
```

**Parsing Logic** (di `add_houses_from_csv()`):
- Baca file dengan `csv.DictReader`
- Parse setiap field dengan tipe yang sesuai
- Split features dengan delimiter `;`
- Create House object dan add ke database

---

## Performance Considerations

Current bottlenecks:
1. Linear search di `calculate_similarity()` - O(n) untuk n houses
2. No indexing pada location/price range

Optimization untuk large dataset:
1. Add hash index untuk location
2. Use KD-tree atau R-tree untuk spatial queries
3. Implement caching untuk preference-house pairs
4. Use numpy array untuk vectorized similarity calculation

---

## Testing Guide

### Unit Testing (Manual)
```python
# Test similarity calculation
from recommendation_engine import RecommendationEngine, House

engine = RecommendationEngine()
pref = {
    'min_price': 500,
    'max_price': 2000,
    'bedrooms': 3,
    'area': 200
}
result = engine.recommend(pref, top_n=5)
print([(h.name, score) for h, score in result])
```

### Integration Testing
1. Load sample data ✓
2. Calculate similarities ✓
3. Rank recommendations ✓
4. Import CSV ✓
5. Display in GUI ✓

### User Testing
1. Input various preference combinations
2. Verify results match expectations
3. Test with custom data
4. Performance check with large dataset

---

## Common Modifications

### Ubah Weights
```python
# recommendation_engine.py, calculate_similarity()
weights = {
    'price': 0.30,      # Increased
    'location': 0.25,   # Increased
    'area': 0.15,       # Decreased
    'bedrooms': 0.15,
    'age': 0.10,
    'bathrooms': 0.05   # Decreased
}
```

### Ubah Similarity Logic
```python
# Untuk price, instead of range checking:
if 'price_preference' in preference:
    # Prefer cheaper houses
    price_score = preference['max_price'] / house.price
    score += price_score * weights['price']
```

### Tambah Constraint
```python
# Mandatory filter before scoring
def recommend(self, preference, top_n=3):
    candidates = []
    for house in self.houses:
        # Add hard constraint
        if 'min_price' in preference:
            if house.price < preference['min_price']:
                continue  # Skip this house
        
        similarity = self.calculate_similarity(preference, house)
        candidates.append((house, similarity))
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[:top_n]
```

---

## Future Enhancements

1. **Machine Learning**
   - Replace manual weights dengan learned weights
   - Gunakan collaborative filtering
   - Implement neural networks untuk similarity

2. **Data Persistence**
   - Save houses ke database (SQLite/PostgreSQL)
   - Load preferences dari user profile

3. **Advanced Features**
   - Real-time price tracking
   - Map visualization dengan folium/plotly
   - Photo gallery untuk setiap house
   - Comparison tool untuk 2+ houses
   - Wishlist/favorite system

4. **Deployment**
   - Web version dengan Flask/Django
   - Mobile app dengan React Native
   - Cloud deployment ke Azure/AWS

5. **Analytics**
   - Track search patterns
   - Generate house market reports
   - Predict price trends

---

## Code Style Guidelines

**Naming**:
- Classes: PascalCase (House, RecommendationEngine)
- Functions: snake_case (calculate_similarity, add_house)
- Variables: snake_case (min_price, house_name)
- Constants: UPPER_SNAKE_CASE (MAX_RECOMMENDATIONS = 5)

**Documentation**:
```python
def calculate_similarity(self, preference: Dict, house: House) -> float:
    """
    Menghitung similarity score antara preferensi dan rumah.
    
    Args:
        preference: Dict berisi user preferences
        house: House object untuk dibandingkan
        
    Returns:
        float: Similarity score antara 0 dan 1
    """
```

**Type Hints**:
Gunakan type hints untuk clarity dan IDE support

---

Good luck with development! 🚀
