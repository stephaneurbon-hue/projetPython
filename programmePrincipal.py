"""
Auteur : Stéphane Urbon et Rayane Zidane
Date : 06/10/2025
Objectif : Script d'un casse brique sous tkinter (version responsive)
"""

import tkinter as tk
from accueil import InterfaceAccueil


def main():
    root = tk.Tk()
    root.title("Casse-Brique")
    root.state("zoomed")  # Plein écran adaptatif
    root.configure(bg="#001a33")

    app = InterfaceAccueil(root)
    root.mainloop()


if __name__ == "__main__":
    main()

