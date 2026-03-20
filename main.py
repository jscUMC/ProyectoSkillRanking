import tkinter as tk
from MainWindow import MainWindow


def main():
    print("Aplicacion corriendo")
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
    print("Aplicacion cerrada")

if __name__ == "__main__":
    main()