"""
Case-Based Reasoning Engine untuk Rekomendasi Rumah
Implementasi siklus CBR 4R: Retrieve → Reuse → Revise → Retain
"""
from typing import List, Dict, Tuple, Optional
import json
import csv
import os
from pathlib import Path
from datetime import datetime


class House:
    """Kelas untuk merepresentasikan data rumah"""
    def __init__(self, id: int, name: str, price: int, location: str,
                 bedrooms: int, bathrooms: int, area: int, age: int,
                 features: List[str] = None):
        self.id = id
        self.name = name
        self.price = price       # dalam jutaan rupiah
        self.location = location
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area         # dalam m²
        self.age = age           # dalam tahun
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


# ─────────────────────────────────────────────
# BARU: Kelas untuk merepresentasikan sebuah "kasus" dalam CBR
# ─────────────────────────────────────────────
class Case:
    """
    Merepresentasikan satu kasus dalam case base CBR.
    Setiap kasus menyimpan: preferensi user, rumah yang dipilih,
    skor similarity saat itu, feedback user, dan timestamp.
    """
    def __init__(self, case_id: int, preference: Dict, chosen_house: House,similarity_score: float, feedback: Optional[str] = None):
        self.case_id = case_id
        self.preference = preference          # problem description
        self.chosen_house = chosen_house      # solution
        self.similarity_score = similarity_score
        self.feedback = feedback              # "satisfied" / "unsatisfied"
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            'case_id': self.case_id,
            'preference': self.preference,
            'chosen_house': self.chosen_house.to_dict(),
            'similarity_score': self.similarity_score,
            'feedback': self.feedback,
            'timestamp': self.timestamp
        }


class RecommendationEngine:
    """
    Engine rekomendasi rumah dengan siklus CBR lengkap:
    Retrieve → Reuse → Revise → Retain
    """

    def __init__(self, case_base_path: str = "case_base.json"):
        self.houses: List[House] = []
        # BARU: case base untuk menyimpan kasus historis (Retain)
        self.case_base: List[Case] = []
        self.case_base_path = case_base_path
        self.load_data()
        self.load_case_base()  # BARU

    # ─────────────────────────────────────────────
    # LOAD DATA 
    # ─────────────────────────────────────────────

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
                            price=int(row['price']) // 1_000_000,
                            location=row['district'],
                            bedrooms=int(row['bed_rooms']),
                            bathrooms=int(row['bath_rooms']),
                            area=int(row['building_area']),
                            age=0,  # Dataset tidak memiliki kolom umur
                            features=[]
                        )
                        houses.append(house)
                    except (ValueError, KeyError):
                        continue
                self.houses = houses
        except Exception as e:
            raise RuntimeError(
                f"Gagal membaca file CSV: {e}. "
                "Pastikan format file sudah benar dengan kolom: "
                "index, price, district, city, bed_rooms, bath_rooms, "
                "carport, land_area, building_area"
            )

    # ─────────────────────────────────────────────
    # SIMILARITY 
    # ─────────────────────────────────────────────

    def calculate_similarity(self, preference: Dict, house: House) -> float:
        """
        Menghitung similarity score antara preferensi user dan rumah.
        Weighted scoring system — bagian dari tahap RETRIEVE.

        Perbaikan dari versi lama:
        - Area score kini menggunakan formula berbasis jarak yang simetris
        - Location score kini memberi penalti lebih tegas (0.0, bukan 0.5)
          untuk lokasi yang tidak cocok sama sekali
        """
        score = 0.0
        weights = {
            'price':     0.25,
            'bedrooms':  0.15,
            'bathrooms': 0.10,
            'area':      0.20,
            'location':  0.20,
            'age':       0.10
        }

        # Price score
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

        # Bedrooms score
        if 'bedrooms' in preference:
            bedroom_diff = abs(preference['bedrooms'] - house.bedrooms)
            bedroom_score = max(0.0, 1.0 - (bedroom_diff * 0.2))
            score += bedroom_score * weights['bedrooms']

        # Bathrooms score
        if 'bathrooms' in preference:
            bathroom_diff = abs(preference['bathrooms'] - house.bathrooms)
            bathroom_score = max(0.0, 1.0 - (bathroom_diff * 0.2))
            score += bathroom_score * weights['bathrooms']

        # DIPERBAIKI: Area score — formula simetris berbasis jarak relatif
        if 'area' in preference:
            pref_area = preference['area']
            if pref_area > 0:
                relative_diff = abs(house.area - pref_area) / pref_area
                area_score = max(0.0, 1.0 - relative_diff)
            else:
                area_score = 1.0
            score += area_score * weights['area']

        # DIPERBAIKI: Location score — penalti lebih tegas jika tidak cocok
        if 'location' in preference:
            pref_loc = preference['location'].lower()
            house_loc = house.location.lower()
            if pref_loc in house_loc or house_loc in pref_loc:
                location_score = 1.0
            else:
                # Cek apakah ada kata yang overlap (partial match)
                pref_words = set(pref_loc.split())
                house_words = set(house_loc.split())
                overlap = pref_words & house_words
                location_score = 0.3 * (len(overlap) / max(len(pref_words), 1))
            score += location_score * weights['location']

        # Age score
        if 'max_age' in preference:
            if house.age <= preference['max_age']:
                age_score = 1.0 - (house.age / (preference['max_age'] + 1))
            else:
                age_score = 0.3
            score += age_score * weights['age']

        return round(score, 4)

    # ─────────────────────────────────────────────
    # TAHAP 1 — RETRIEVE
    # ─────────────────────────────────────────────

    def retrieve(self, preference: Dict, top_n: int = 5) -> List[Tuple[House, float]]:
        """
        TAHAP RETRIEVE:
        Mencari rumah-rumah dari case base dan katalog yang paling
        mirip dengan preferensi user saat ini.

        Langkah:
        1. Hitung similarity semua rumah di katalog
        2. Cek case base — jika ada kasus historis yang mirip
           dan mendapat feedback 'satisfied', naikkan skornya
        3. Kembalikan top_n hasil terurut
        """
        scores = []

        # Ambil bobot tambahan dari kasus historis yang positif
        positive_case_locations = self._get_positive_case_locations(preference)

        for house in self.houses:
            similarity = self.calculate_similarity(preference, house)

            # Reuse signal: jika lokasi rumah ini pernah dipilih
            # dan user puas, beri sedikit bonus skor (max +0.05)
            if house.location in positive_case_locations:
                similarity = min(1.0, similarity + 0.05)

            scores.append((house, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

    def _get_positive_case_locations(self, preference: Dict) -> set:
        """
        Helper untuk RETRIEVE:
        Ambil lokasi dari kasus historis yang preferensinya
        mirip dengan preferensi sekarang DAN feedback-nya 'satisfied'.
        """
        positive_locations = set()
        for case in self.case_base:
            if case.feedback != 'satisfied':
                continue
            # Cek apakah preferensi historis cukup mirip
            pref_sim = self._preference_similarity(preference, case.preference)
            if pref_sim >= 0.7:
                positive_locations.add(case.chosen_house.location)
        return positive_locations

    def _preference_similarity(self, pref_a: Dict, pref_b: Dict) -> float:
        """
        Menghitung seberapa mirip dua preferensi user.
        Digunakan secara internal untuk mencocokkan kasus historis.
        """
        sim_scores = []

        # Bandingkan rentang harga
        if all(k in pref_a and k in pref_b for k in ['min_price', 'max_price']):
            mid_a = (pref_a['min_price'] + pref_a['max_price']) / 2
            mid_b = (pref_b['min_price'] + pref_b['max_price']) / 2
            if max(mid_a, mid_b) > 0:
                sim_scores.append(1.0 - abs(mid_a - mid_b) / max(mid_a, mid_b))

        # Bandingkan bedrooms
        if 'bedrooms' in pref_a and 'bedrooms' in pref_b:
            diff = abs(pref_a['bedrooms'] - pref_b['bedrooms'])
            sim_scores.append(max(0.0, 1.0 - diff * 0.25))

        # Bandingkan area
        if 'area' in pref_a and 'area' in pref_b:
            if max(pref_a['area'], pref_b['area']) > 0:
                rel = abs(pref_a['area'] - pref_b['area']) / max(pref_a['area'], pref_b['area'])
                sim_scores.append(max(0.0, 1.0 - rel))

        if not sim_scores:
            return 0.0
        return sum(sim_scores) / len(sim_scores)

    # ─────────────────────────────────────────────
    # TAHAP 2 — REUSE
    # ─────────────────────────────────────────────

    def reuse(self, retrieved: List[Tuple[House, float]]) -> List[Tuple[House, float]]:
        """
        TAHAP REUSE:
        Dari hasil retrieve, susun daftar rekomendasi final yang
        akan ditampilkan ke user. Pada tahap ini sistem mengadaptasi
        hasil jika ada kesamaan dengan solusi kasus lama yang berhasil.

        Saat ini: pass-through dengan normalisasi skor ke persentase.
        """
        reused = []
        for house, score in retrieved:
            # Normalisasi: tampilkan sebagai persentase 0–100
            display_score = round(score * 100, 1)
            reused.append((house, display_score))
        return reused

    # ─────────────────────────────────────────────
    # TAHAP 3 — REVISE
    # ─────────────────────────────────────────────

    def revise(self, recommendations: List[Tuple[House, float]],
               preference: Dict) -> List[Tuple[House, float]]:
        """
        TAHAP REVISE:
        Evaluasi dan koreksi daftar rekomendasi berdasarkan
        aturan bisnis atau feedback historis negatif.

        Aturan revisi yang diterapkan:
        1. Jika rumah pernah dipilih dan mendapat feedback 'unsatisfied'
           dengan preferensi yang mirip → turunkan skornya
        2. Hapus duplikat (id yang sama muncul lebih dari sekali)
        """
        negative_ids = self._get_negative_case_ids(preference)

        revised = []
        seen_ids = set()

        for house, score in recommendations:
            # Hapus duplikat
            if house.id in seen_ids:
                continue
            seen_ids.add(house.id)

            # Penalti untuk rumah yang pernah mengecewakan user
            if house.id in negative_ids:
                score = max(0.0, score - 10.0)  # Kurangi 10 poin

            revised.append((house, score))

        # Urutkan ulang setelah revisi
        revised.sort(key=lambda x: x[1], reverse=True)
        return revised

    def _get_negative_case_ids(self, preference: Dict) -> set:
        """
        Helper untuk REVISE:
        Ambil ID rumah dari kasus historis yang feedback-nya 'unsatisfied'
        dan preferensinya mirip dengan sekarang.
        """
        negative_ids = set()
        for case in self.case_base:
            if case.feedback != 'unsatisfied':
                continue
            pref_sim = self._preference_similarity(preference, case.preference)
            if pref_sim >= 0.7:
                negative_ids.add(case.chosen_house.id)
        return negative_ids

    # ─────────────────────────────────────────────
    # TAHAP 4 — RETAIN
    # ─────────────────────────────────────────────

    def retain(self, preference: Dict, chosen_house: House,
               similarity_score: float, feedback: str) -> Case:
        """
        TAHAP RETAIN:
        Simpan kasus baru ke case base setelah user memberi feedback.
        Kasus disimpan di memori (self.case_base) dan
        dipersistensikan ke file JSON (case_base.json).

        Args:
            preference       : preferensi user saat itu
            chosen_house     : rumah yang dipilih user
            similarity_score : skor similarity rumah tersebut
            feedback         : 'satisfied' atau 'unsatisfied'

        Returns:
            Case yang baru disimpan
        """
        if feedback not in ('satisfied', 'unsatisfied'):
            raise ValueError("feedback harus 'satisfied' atau 'unsatisfied'")

        new_case_id = len(self.case_base) + 1
        new_case = Case(
            case_id=new_case_id,
            preference=preference,
            chosen_house=chosen_house,
            similarity_score=similarity_score,
            feedback=feedback
        )
        self.case_base.append(new_case)
        self._save_case_base()
        return new_case

    def _save_case_base(self):
        """Simpan seluruh case base ke file JSON."""
        data = [c.to_dict() for c in self.case_base]
        with open(self.case_base_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_case_base(self):
        """
        Muat case base dari file JSON saat engine diinisialisasi.
        Jika file belum ada, case base dimulai kosong.
        """
        if not os.path.exists(self.case_base_path):
            self.case_base = []
            return
        try:
            with open(self.case_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.case_base = []
            for item in data:
                h_data = item['chosen_house']
                house = House(
                    id=h_data['id'],
                    name=h_data['name'],
                    price=h_data['price'],
                    location=h_data['location'],
                    bedrooms=h_data['bedrooms'],
                    bathrooms=h_data['bathrooms'],
                    area=h_data['area'],
                    age=h_data['age'],
                    features=h_data.get('features', [])
                )
                case = Case(
                    case_id=item['case_id'],
                    preference=item['preference'],
                    chosen_house=house,
                    similarity_score=item['similarity_score'],
                    feedback=item.get('feedback')
                )
                case.timestamp = item.get('timestamp', '')
                self.case_base.append(case)
        except (json.JSONDecodeError, KeyError):
            # Jika file corrupt, mulai dari kosong
            self.case_base = []

    # ─────────────────────────────────────────────
    # ENTRY POINT UTAMA — menggabungkan semua 4R
    # ─────────────────────────────────────────────

    def recommend(self, preference: Dict, top_n: int = 5) -> List[Tuple[House, float]]:
        """
        Entry point rekomendasi lengkap dengan siklus CBR 4R.

        Alur:
          1. RETRIEVE  — cari kandidat dari katalog + sinyal case base
          2. REUSE     — adaptasi dan normalisasi skor
          3. REVISE    — terapkan koreksi berdasarkan feedback historis
          4. (RETAIN dipanggil terpisah setelah user memilih dan memberi feedback)

        Returns:
            List of (House, display_score_persen) tuples
        """
        # Tahap 1: Retrieve
        retrieved = self.retrieve(preference, top_n=top_n * 2)

        # Tahap 2: Reuse
        reused = self.reuse(retrieved)

        # Tahap 3: Revise
        revised = self.revise(reused, preference)

        return revised[:top_n]

    # ─────────────────────────────────────────────
    # UTILITY — tidak berubah dari versi lama
    # ─────────────────────────────────────────────

    def get_all_houses(self) -> List[House]:
        """Mendapatkan semua data rumah"""
        return self.houses

    def add_house(self, house: House):
        """Menambah data rumah baru ke katalog"""
        self.houses.append(house)

    def add_houses_from_csv(self, filepath: str):
        """
        Menambah data rumah dari file CSV tambahan.
        Format: id,name,price,location,bedrooms,bathrooms,area,age,features
        """
        try:
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

    def get_case_base_summary(self) -> Dict:
        """
        BARU: Ringkasan statistik case base untuk keperluan
        debugging atau tampilan di UI.
        """
        total = len(self.case_base)
        satisfied = sum(1 for c in self.case_base if c.feedback == 'satisfied')
        unsatisfied = sum(1 for c in self.case_base if c.feedback == 'unsatisfied')
        return {
            'total_cases': total,
            'satisfied': satisfied,
            'unsatisfied': unsatisfied,
            'satisfaction_rate': round(satisfied / total * 100, 1) if total > 0 else 0.0
        }