"""
Sistem Rekomendasi Rumah - Main Entry Point
"""
import customtkinter as ctk
from recommendation_engine import RecommendationEngine
from gui_interface import RecommendationGUI

def main():
    # Mengatur tema global CustomTkinter agar otomatis mengikuti tema sistem/light mode
    ctk.set_appearance_mode("light") 
    ctk.set_default_color_theme("blue")

    # KUNCI UTAMA: Wajib menggunakan ctk.CTk() bukan tk.Tk() standar
    root = ctk.CTk()
    root.title("Sistem Rekomendasi Rumah")
    root.geometry("1000x700") # Ukuran window untuk single page rekomendasi
    
    # Inisialisasi CBR engine
    engine = RecommendationEngine()
    
    # Membuat GUI Modern
    app = RecommendationGUI(root, engine)
    
    root.mainloop()

if __name__ == "__main__":
    main()
