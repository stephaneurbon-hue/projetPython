"""
Fichier principal du jeu Casse-Brique
-------------------------------------
Auteur : Stéphane Urbon & Rayane Zidane
Date   : 27/10/2025
Rôle   : Lance le menu principal.
"""

import tkinter as tk
from menu import MenuApp  # nom du module en minuscules

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
