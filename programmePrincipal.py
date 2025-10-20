"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter (version responsive)
"""

import tkinter as tk
from accueil import InterfaceAccueil

if __name__ == "__main__":
    fenetre = tk.Tk()
    app = InterfaceAccueil(fenetre)
    fenetre.mainloop()
