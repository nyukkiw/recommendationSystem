import tkinter as tk
from tkinter import ttk, messagebox
from recommendation_engine import RecommendationEngine
from gui_interface import RecommendationGUI

def main():
    root = tk.Tk()
    root.title("Sistem Rekomendasi Rumah")
    root.geometry("900x700")
    
    # Initialize recommendation engine
    engine = RecommendationEngine()
    
    # Create GUI
    app = RecommendationGUI(root, engine)
    
    root.mainloop()

if __name__ == "__main__":
    main()
