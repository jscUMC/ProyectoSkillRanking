import tkinter as tk
from tkinter import ttk
from almacen_candidatos import AlmacenCandidatos
from ventana_admin import VentanaAdmin
from ventana_contratista import VentanaContratista


def main():
    root = tk.Tk()
    root.title("Sistema de Gestion de Candidatos")
    root.configure(bg="#f0f4f8")
    root.resizable(False, False)

    almacen = AlmacenCandidatos()

    # Titulo principal
    tk.Label(root,
             text="Sistema de Gestion de Candidatos",
             font=("Segoe UI", 15, "bold"),
             bg="#1a237e", fg="white", pady=10).pack(fill="x")

    # Notebook — dos pestanas
    estilo = ttk.Style()
    estilo.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                     padding=[16, 6])

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    pestana_admin = VentanaAdmin(notebook, almacen)
    pestana_contratista = VentanaContratista(notebook, almacen)

    notebook.add(pestana_admin, text="  Administrador  ")
    notebook.add(pestana_contratista, text="  Contratista  ")

    root.mainloop()


if __name__ == "__main__":
    main()
