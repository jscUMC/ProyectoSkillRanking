import tkinter as tk
from tkinter import ttk
from candidato import Candidato
from skills_data import PREGUNTAS_POR_CATEGORIA


class VentanaDetalle(tk.Toplevel):
    def __init__(self, padre, candidato: Candidato):
        super().__init__(padre)
        self.title("Informacion del candidato")
        self.resizable(False, True)
        self.configure(bg="#f0f4f8")
        self.geometry("500x600")
        self._construir(candidato)
        self.grab_set()

    def _construir(self, c: Candidato) -> None:
        # Header fijo
        header = tk.Frame(self, bg="#3b4cca", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Informacion del candidato",
                 font=("Segoe UI", 13, "bold"),
                 fg="white", bg="#3b4cca").pack()

        # Canvas scrollable
        contenedor = tk.Frame(self, bg="#f0f4f8")
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg="#f0f4f8",
                           highlightthickness=0)
        vsb = ttk.Scrollbar(contenedor, orient="vertical",
                             command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(canvas, bg="#f0f4f8")
        canvas.create_window((0, 0), window=interior, anchor="nw")

        def _scroll_mouse(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _scroll_mouse)

        # Info personal
        card = tk.Frame(interior, bg="white", padx=20, pady=14,
                        bd=1, relief="solid")
        card.pack(padx=20, pady=(12, 6), fill="x")

        for etiqueta, valor in [
            ("Nombre:", c.nombre), ("Edad:", str(c.edad)),
            ("Telefono:", c.telefono), ("Correo:", c.correo),
            ("Nivel de formacion:", c.formacion),
        ]:
            fila = tk.Frame(card, bg="white")
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=etiqueta,
                     font=("Segoe UI", 10, "bold"),
                     bg="white", width=20, anchor="w").pack(side="left")
            tk.Label(fila, text=valor,
                     font=("Segoe UI", 10),
                     bg="white", anchor="w").pack(side="left")

        # Badge puntaje total
        badge = tk.Frame(interior, bg="#f0f4f8")
        badge.pack(pady=6)
        tk.Label(badge, text="PUNTAJE TOTAL",
                 font=("Segoe UI", 9, "bold"),
                 bg="#f0f4f8", fg="#555").pack()
        tk.Label(badge, text=str(c.puntaje_total),
                 font=("Segoe UI", 28, "bold"),
                 fg="#3b4cca", bg="#f0f4f8").pack()

        # Habilidades por categoria con checks
        tk.Label(interior, text="Detalle de habilidades",
                 font=("Segoe UI", 11, "bold"),
                 bg="#f0f4f8").pack(pady=(8, 2))

        sk_frame = tk.Frame(interior, bg="#f0f4f8")
        sk_frame.pack(fill="x", padx=16, pady=(0, 14))

        for cat, preguntas in PREGUNTAS_POR_CATEGORIA.items():
            puntaje_cat = c.puntajes.get(cat, 0)
            maximo = sum(p for _, p in preguntas)

            lf = tk.LabelFrame(
                sk_frame,
                text=f"{cat}  —  {puntaje_cat} / {maximo} pts",
                font=("Segoe UI", 9, "bold"),
                bg="#f0f4f8", padx=8, pady=4
            )
            lf.pack(fill="x", pady=4)

            # Barra de progreso
            barra_bg = tk.Frame(lf, bg="#dde3ee", height=10)
            barra_bg.pack(fill="x", pady=(0, 4))
            barra_bg.pack_propagate(False)
            ancho_rel = puntaje_cat / maximo if maximo else 0

            def _dibujar_barra(marco=barra_bg, rel=ancho_rel):
                marco.update_idletasks()
                w = marco.winfo_width()
                fill = int(w * rel)
                tk.Frame(marco, bg="#3b4cca",
                         width=fill, height=10).place(x=0, y=0)

            lf.after(50, _dibujar_barra)

            # Checks individuales
            for texto, _ in preguntas:
                marcado = c.checks.get(cat, {}).get(texto, False)
                color = "#2a7a2a" if marcado else "#aaa"
                marca = "✔" if marcado else "✘"
                tk.Label(lf,
                         text=f"  {marca}  {texto}",
                         font=("Segoe UI", 8),
                         bg="#f0f4f8", fg=color,
                         anchor="w").pack(fill="x")

        interior.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Boton cerrar fijo
        tk.Button(self, text="Cerrar", command=self.destroy,
                  bg="#3b4cca", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=24, pady=7,
                  cursor="hand2").pack(pady=10)
