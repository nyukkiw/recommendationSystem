"""
Case-Based Reasoning Engine untuk Rekomendasi Rumah
"""
from typing import List, Dict, Tuple
import json
import csv
from pathlib import Path

class House:
    """Kelas untuk merepresentasikan data rumah"""
    def __init__(self, id: int, name: str, price: int, location: str, 
                 bedrooms: int, bathrooms: int, area: int, age: int, 
                 features: List[str] = None):
        self.id = id
        self.name = name
        self.price = price  # dalam jutaan rupiah
        self.location = location
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area  # dalam m²
        self.age = age  # dalam tahun
        self.features = features or []
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'location': self.location,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': self.area,
            'age': self.age,
            'features': self.features
        }

class RecommendationEngine:
    """Engine untuk memberikan rekomendasi rumah menggunakan Case-Based Reasoning"""
    
    def __init__(self):
        self.houses = []
        self.load_data()
    
    def load_data(self):
        """Memuat data dari file CSV (jakarta_house.csv)"""
        csv_path = Path(__file__).parent / "jakarta_house.csv"
        if not csv_path.exists():
            raise FileNotFoundError(
                f"File 'jakarta_house.csv' tidak ditemukan di {csv_path}. "
                "Pastikan file CSV sudah ada di folder yang sama dengan script ini."
            )
        self.load_csv_data(str(csv_path))
    
    def load_csv_data(self, csv_file: str):
        """Memuat data rumah dari file CSV"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                houses = []
                for row in reader:
                    try:
                        house = House(
                            id=int(row['index']),
                            name=f"Rumah {row['district']}",
                            price=int(row['price']) // 1_000_000,  # Convert to millions
                            location=row['district'],
                            bedrooms=int(row['bed_rooms']),
                            bathrooms=int(row['bath_rooms']),
                            area=int(row['building_area']),
                            age=0,  # Data tidak memiliki informasi umur
                            features=[]
                        )
                        houses.append(house)
                    except (ValueError, KeyError) as e:
                        continue
                self.houses = houses
        except Exception as e:
            raise RuntimeError(
                f"Gagal membaca file CSV: {e}. "
                "Pastikan format file sudah benar dengan kolom: "
                "index, price, district, city, bed_rooms, bath_rooms, carport, land_area, building_area"
            )
    

    
    def calculate_similarity(self, preference: Dict, house: House) -> float:
        """
        Menghitung similarity score antara preferensi user dan karakteristik rumah
        Menggunakan weighted scoring system
        """
        score = 0
        weights = {
            'price': 0.25,
            'bedrooms': 0.15,
            'bathrooms': 0.10,
            'area': 0.20,
            'location': 0.20,
            'age': 0.10
        }
        
        # Score untuk price (harga)
        if 'max_price' in preference and 'min_price' in preference:
            min_p = preference['min_price']
            max_p = preference['max_price']
            if min_p <= house.price <= max_p:
                price_score = 1.0
            elif house.price < min_p:
                price_score = house.price / min_p
            else:
                price_score = max_p / house.price
            score += price_score * weights['price']
        
        # Score untuk bedrooms
        if 'bedrooms' in preference:
            bedroom_diff = abs(preference['bedrooms'] - house.bedrooms)
            bedroom_score = max(0, 1 - (bedroom_diff * 0.2))
            score += bedroom_score * weights['bedrooms']
        
        # Score untuk bathrooms
        if 'bathrooms' in preference:
            bathroom_diff = abs(preference['bathrooms'] - house.bathrooms)
            bathroom_score = max(0, 1 - (bathroom_diff * 0.2))
            score += bathroom_score * weights['bathrooms']
        
        # Score untuk area
        if 'area' in preference:
            area_min = preference['area'] * 0.8
            area_max = preference['area'] * 1.2
            if area_min <= house.area <= area_max:
                area_score = 1.0
            else:
                area_score = min(house.area, area_max) / max(house.area, area_max)
            score += area_score * weights['area']
        
        # Score untuk location
        if 'location' in preference:
            if preference['location'].lower() in house.location.lower():
                location_score = 1.0
            else:
                location_score = 0.5
            score += location_score * weights['location']
        
        # Score untuk age (umur rumah)
        if 'max_age' in preference:
            if house.age <= preference['max_age']:
                age_score = 1.0 - (house.age / (preference['max_age'] + 1))
            else:
                age_score = 0.3
            score += age_score * weights['age']
        
        return score
    
    def recommend(self, preference: Dict, top_n: int = 3) -> List[Tuple[House, float]]:
        """
        Memberikan rekomendasi rumah berdasarkan preferensi user
        
        Args:
            preference: Dictionary berisi preferensi user
            top_n: Jumlah rekomendasi yang dikembalikan
            
        Returns:
            List of (House, similarity_score) tuples, sorted by score descending
        """
        scores = []
        for house in self.houses:
            similarity = self.calculate_similarity(preference, house)
            scores.append((house, similarity))
        
        # Sort berdasarkan similarity score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_n]
    
    def get_all_houses(self) -> List[House]:
        """Mendapatkan semua data rumah"""
        return self.houses
    
    def add_house(self, house: House):
        """Menambah data rumah baru"""
        self.houses.append(house)
    
    def add_houses_from_csv(self, filepath: str):
        """
        Menambah data rumah dari file CSV
        Format: id,name,price,location,bedrooms,bathrooms,area,age,features
        """
        try:
            import csv
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    house = House(
                        id=int(row['id']),
                        name=row['name'],
                        price=int(row['price']),
                        location=row['location'],
                        bedrooms=int(row['bedrooms']),
                        bathrooms=int(row['bathrooms']),
                        area=int(row['area']),
                        age=int(row['age']),
                        features=row['features'].split(';') if row['features'] else []
                    )
                    self.add_house(house)
            return True, "Data berhasil dimuat dari CSV"
        except Exception as e:
            return False, f"Error membaca CSV: {str(e)}"
