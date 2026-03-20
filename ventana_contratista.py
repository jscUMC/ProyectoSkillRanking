import tkinter as tk
from tkinter import ttk, messagebox
from skills_data import CATEGORIAS
from cola_prioridad import ColaPrioridad
from ventana_detalle import VentanaDetalle


class VentanaContratista(tk.Frame):
    """
    Pestana del contratista: selecciona categorias requeridas,
    ve el ranking filtrado y puede contratar (eliminar) candidatos.
    """

    def __init__(self, padre, almacen):
        super().__init__(padre, bg="#f0f4f8")
        self._almacen = almacen
        self._cat_vars = {}
        self._ranking = []
        self._construir()

    def _construir(self) -> None:
        tk.Label(self, text="Vista del Contratista",
                 font=("Segoe UI", 13, "bold"),
                 bg="#2e7d32", fg="white", pady=8).pack(fill="x")

        cuerpo = tk.Frame(self, bg="#f0f4f8", padx=14, pady=14)
        cuerpo.pack(fill="both", expand=True)

        # Panel izquierdo — categorias
        izq = tk.LabelFrame(cuerpo, text="Habilidades requeridas",
                            font=("Segoe UI", 10, "bold"),
                            bg="#f0f4f8", padx=10, pady=10)
        izq.grid(row=0, column=0, sticky="n", padx=(0, 14))

        for cat in CATEGORIAS:
            var = tk.BooleanVar(value=False)
            tk.Checkbutton(izq, text=cat, variable=var,
                           bg="#f0f4f8", font=("Segoe UI", 9),
                           anchor="w").pack(fill="x", pady=2)
            self._cat_vars[cat] = var

        tk.Button(izq, text="Buscar candidatos",
                  command=self._buscar,
                  bg="#2e7d32", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=6,
                  cursor="hand2").pack(fill="x", pady=(12, 0))

        # Panel derecho — tabla
        der = tk.LabelFrame(cuerpo, text="Ranking de hojas de vida",
                            font=("Segoe UI", 10, "bold"),
                            bg="#f0f4f8", padx=10, pady=10)
        der.grid(row=0, column=1, sticky="nsew")

        cols = ("Pos", "Nombre", "Formacion", "Puntaje relevante", "Total")
        self._tabla = ttk.Treeview(der, columns=cols, show="headings",
                                   height=14, selectmode="browse")
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

        anchos = {"Pos": 36, "Nombre": 150, "Formacion": 110,
                  "Puntaje relevante": 120, "Total": 60}
        for col in cols:
            self._tabla.heading(col, text=col)
            self._tabla.column(col, width=anchos[col], anchor="center")

        vsb = ttk.Scrollbar(der, orient="vertical", command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=vsb.set)
        self._tabla.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self._tabla.bind("<Double-1>", self._doble_click)

        # Botones inferiores
        fila_btn = tk.Frame(cuerpo, bg="#f0f4f8")
        fila_btn.grid(row=1, column=0, columnspan=2,
                      pady=(10, 0), sticky="e")
        tk.Label(fila_btn,
                 text="Doble clic para ver detalle",
                 font=("Segoe UI", 8), bg="#f0f4f8", fg="#888").pack(side="left", padx=6)
        tk.Button(fila_btn, text="Contratar seleccionado",
                  command=self._contratar,
                  bg="#c62828", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=12, pady=5,
                  cursor="hand2").pack(side="right")

    def _buscar(self) -> None:
        cats = [c for c, v in self._cat_vars.items() if v.get()]
        if not cats:
            messagebox.showwarning("Seleccion vacia",
                                   "Selecciona al menos una categoria.")
            return
        cola = ColaPrioridad()
        for candidato in self._almacen.todos():
            puntaje = candidato.puntaje_en_categorias(cats)
            cola.insertar(candidato, puntaje)
        self._ranking = cola.obtener_ordenados()
        self._actualizar_tabla(cats)

    def _actualizar_tabla(self, cats: list) -> None:
        for fila in self._tabla.get_children():
            self._tabla.delete(fila)
        for pos, (c, rel) in enumerate(self._ranking, 1):
            tag = "oro" if pos == 1 else ("plata" if pos == 2 else "")
            self._tabla.insert("", "end", iid=str(id(c)),
                               values=(pos, c.nombre, c.formacion,
                                       rel, c.puntaje_total),
                               tags=(tag,))
        self._tabla.tag_configure("oro", background="#fff3b0")
        self._tabla.tag_configure("plata", background="#eaeaea")

    def _doble_click(self, event) -> None:
        item = self._tabla.focus()
        if not item:
            return
        candidato = next((c for c, _ in self._ranking
                          if str(id(c)) == item), None)
        if candidato:
            VentanaDetalle(self, candidato)

    def _contratar(self) -> None:
        item = self._tabla.focus()
        if not item:
            messagebox.showwarning("Sin seleccion",
                                   "Selecciona un candidato primero.")
            return
        candidato = next((c for c, _ in self._ranking
                          if str(id(c)) == item), None)
        if not candidato:
            return
        confirmar = messagebox.askyesno(
            "Confirmar contratacion",
            f"Contratar a {candidato.nombre}?\n"
            "Se eliminara su hoja de vida del sistema."
        )
        if confirmar:
            self._almacen.eliminar_por_id(int(item))
            self._ranking = [(c, s) for c, s in self._ranking
                             if str(id(c)) != item]
            self._tabla.delete(item)
            for i, fila_id in enumerate(self._tabla.get_children(), 1):
                vals = list(self._tabla.item(fila_id, "values"))
                vals[0] = i
                self._tabla.item(fila_id, values=vals)
            messagebox.showinfo("Contratado",
                                f"{candidato.nombre} fue contratado exitosamente.")
