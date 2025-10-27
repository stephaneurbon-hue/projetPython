import tkinter as tk
from Accueil import Accueil



def main():
    root = tk.Tk()
    root.title("Casse-Brique")
    root.state("zoomed")
    root.configure(bg="#001a33")

    Accueil(root)
    root.mainloop()


if __name__ == "__main__":
    main()
