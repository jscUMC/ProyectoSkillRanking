import tkinter as tk
from tkinter import ttk, messagebox
from candidato import Candidato
from almacen_candidatos import AlmacenCandidatos
from dialogo_habilidades import DialogoHabilidades
from ventana_detalle import VentanaDetalle


class VentanaAdmin(tk.Frame):
    def __init__(self, padre, almacen: AlmacenCandidatos):
        super().__init__(padre, bg="#f0f4f8")
        self._almacen = almacen
        self._checks_pendientes = {}
        self._construir()

    # ── Construccion UI ───────────────────────────────────────────────────────
    def _construir(self) -> None:
        tk.Label(self, text="Panel del Administrador",
                 font=("Segoe UI", 13, "bold"),
                 bg="#3b4cca", fg="white", pady=8).pack(fill="x")

        cuerpo = tk.Frame(self, bg="#f0f4f8", padx=14, pady=14)
        cuerpo.pack(fill="both", expand=True)

        self._construir_formulario(cuerpo)
        self._construir_ranking(cuerpo)

    def _construir_formulario(self, padre: tk.Frame) -> None:
        form = tk.LabelFrame(padre, text="Registrar candidato",
                             font=("Segoe UI", 10, "bold"),
                             bg="#f0f4f8", padx=12, pady=12)
        form.grid(row=0, column=0, sticky="n", padx=(0, 16))

        campos = ["Nombre", "Edad", "Telefono", "Correo", "Nivel de formacion"]
        self._entradas = {}
        for i, nombre in enumerate(campos):
            tk.Label(form, text=f"{nombre}:", font=("Segoe UI", 9),
                     bg="#f0f4f8", anchor="w").grid(
                row=i, column=0, sticky="w", pady=4)
            entrada = tk.Entry(form, width=28, relief="flat",
                               highlightthickness=1,
                               highlightbackground="#aab",
                               font=("Segoe UI", 9))
            entrada.grid(row=i, column=1, padx=(8, 0), pady=4)
            self._entradas[nombre] = entrada

        n = len(campos)

        self._var_puntaje = tk.StringVar(value="Puntaje total: 0 pts")
        tk.Label(form, textvariable=self._var_puntaje,
                 font=("Segoe UI", 9, "italic"),
                 fg="#3b4cca", bg="#f0f4f8").grid(
            row=n, column=0, columnspan=2, pady=(6, 2))

        tk.Button(form, text="Evaluar habilidades",
                  command=self._abrir_dialogo_habilidades,
                  bg="#555", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=10, pady=6,
                  cursor="hand2").grid(
            row=n+1, column=0, columnspan=2, sticky="ew", pady=(4, 4))

        tk.Button(form, text="Insertar candidato",
                  command=self._insertar,
                  bg="#5b7fff", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=8,
                  cursor="hand2").grid(
            row=n+2, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Separador
        ttk.Separator(form, orient="horizontal").grid(
            row=n+3, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Label(form, text="Candidato seleccionado:",
                 font=("Segoe UI", 9, "bold"),
                 bg="#f0f4f8").grid(
            row=n+4, column=0, columnspan=2, sticky="w")

        tk.Button(form, text="Editar seleccionado",
                  command=self._editar,
                  bg="#e65100", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=10, pady=6,
                  cursor="hand2").grid(
            row=n+5, column=0, columnspan=2, sticky="ew", pady=(4, 2))

        tk.Button(form, text="Eliminar seleccionado",
                  command=self._eliminar,
                  bg="#b71c1c", fg="white",
                  font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=10, pady=6,
                  cursor="hand2").grid(
            row=n+6, column=0, columnspan=2, sticky="ew")

    def _construir_ranking(self, padre: tk.Frame) -> None:
        panel = tk.LabelFrame(padre, text="Ranking de candidatos (puntaje total)",
                              font=("Segoe UI", 10, "bold"),
                              bg="#f0f4f8", padx=12, pady=12)
        panel.grid(row=0, column=1, sticky="nsew")

        cols = ("Pos", "Nombre", "Formacion", "Puntaje Total")
        self._tabla = ttk.Treeview(panel, columns=cols,
                                   show="headings",
                                   height=14, selectmode="browse")

        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

        anchos = {"Pos": 40, "Nombre": 160,
                  "Formacion": 130, "Puntaje Total": 110}
        for col in cols:
            self._tabla.heading(col, text=col)
            self._tabla.column(col, width=anchos[col], anchor="center")

        vsb = ttk.Scrollbar(panel, orient="vertical",
                            command=self._tabla.yview)
        self._tabla.configure(yscrollcommand=vsb.set)
        self._tabla.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._tabla.bind("<Double-1>", self._doble_click)
        tk.Label(panel,
                 text="Doble clic para ver detalle del candidato",
                 font=("Segoe UI", 8), bg="#f0f4f8", fg="#888").pack(pady=(6, 0))

    # ── Acciones ──────────────────────────────────────────────────────────────
    def _abrir_dialogo_habilidades(self) -> None:
        dlg = DialogoHabilidades(self, self._checks_pendientes)
        self.wait_window(dlg)
        if dlg.resultado is not None:
            self._checks_pendientes = dlg.resultado
            from skills_data import PREGUNTAS_POR_CATEGORIA
            total = 0
            for cat, qs in dlg.resultado.items():
                for texto, marcado in qs.items():
                    if marcado:
                        for preg, peso in PREGUNTAS_POR_CATEGORIA[cat]:
                            if preg == texto:
                                total += peso
                                break
            self._var_puntaje.set(f"Puntaje total: {total} pts")

    def _limpiar_form(self) -> None:
        for e in self._entradas.values():
            e.delete(0, tk.END)
        self._checks_pendientes = {}
        self._var_puntaje.set("Puntaje total: 0 pts")

    def _insertar(self) -> None:
        valores = {k: v.get().strip() for k, v in self._entradas.items()}
        if not valores["Nombre"]:
            messagebox.showwarning("Campo requerido",
                                   "El nombre es obligatorio.")
            return
        try:
            edad = int(valores["Edad"]) if valores["Edad"] else 0
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un numero entero.")
            return

        c = Candidato(
            nombre=valores["Nombre"],
            edad=edad,
            telefono=valores["Telefono"],
            correo=valores["Correo"],
            formacion=valores["Nivel de formacion"],
        )
        if self._checks_pendientes:
            c.aplicar_checks(self._checks_pendientes)

        self._almacen.agregar(c)
        self._limpiar_form()
        self._refrescar_tabla()
        messagebox.showinfo("Candidato insertado",
                            f"{c.nombre} registrado con puntaje total: {c.puntaje_total}")

    def _refrescar_tabla(self) -> None:
        import heapq
        candidatos = self._almacen.todos()
        heap = [(-c.puntaje_total, i, c)
                for i, c in enumerate(candidatos)]
        heapq.heapify(heap)
        ordenados = []
        while heap:
            _, _, c = heapq.heappop(heap)
            ordenados.append(c)

        for fila in self._tabla.get_children():
            self._tabla.delete(fila)
        for pos, c in enumerate(ordenados, 1):
            tag = "oro" if pos == 1 else ("plata" if pos == 2 else "")
            self._tabla.insert("", "end", iid=str(id(c)),
                               values=(pos, c.nombre,
                                       c.formacion, c.puntaje_total),
                               tags=(tag,))
        self._tabla.tag_configure("oro", background="#fff3b0")
        self._tabla.tag_configure("plata", background="#eaeaea")

    def _doble_click(self, event) -> None:
        item = self._tabla.focus()
        if not item:
            return
        nodo = self._almacen.buscar_nodo_por_id(int(item))
        if nodo:
            VentanaDetalle(self, nodo.dato)

    def _candidato_seleccionado(self):
        item = self._tabla.focus()
        if not item:
            messagebox.showwarning("Sin seleccion",
                                   "Selecciona un candidato en la tabla.")
            return None
        nodo = self._almacen.buscar_nodo_por_id(int(item))
        return nodo.dato if nodo else None

    def _editar(self) -> None:
        c = self._candidato_seleccionado()
        if not c:
            return

        ventana = tk.Toplevel(self)
        ventana.title(f"Editar — {c.nombre}")
        ventana.configure(bg="#f0f4f8")
        ventana.resizable(False, False)
        ventana.grab_set()

        campos = [
            ("Nombre", c.nombre), ("Edad", str(c.edad)),
            ("Telefono", c.telefono), ("Correo", c.correo),
            ("Nivel de formacion", c.formacion),
        ]
        entradas_edit = {}
        for i, (nombre, valor) in enumerate(campos):
            tk.Label(ventana, text=f"{nombre}:", font=("Segoe UI", 9),
                     bg="#f0f4f8").grid(row=i, column=0, sticky="w",
                                        padx=12, pady=4)
            e = tk.Entry(ventana, width=28, font=("Segoe UI", 9),
                         relief="flat", highlightthickness=1,
                         highlightbackground="#aab")
            e.insert(0, valor)
            e.grid(row=i, column=1, padx=(4, 12), pady=4)
            entradas_edit[nombre] = e

        puntajes_edit = [dict({cat: dict(qs) for cat, qs in c.checks.items()})]

        def _editar_habilidades():
            dlg = DialogoHabilidades(ventana, puntajes_edit[0])
            ventana.wait_window(dlg)
            if dlg.resultado:
                puntajes_edit[0] = dlg.resultado

        tk.Button(ventana, text="Editar habilidades",
                  command=_editar_habilidades,
                  bg="#555", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=10, pady=5, cursor="hand2").grid(
            row=len(campos), column=0, columnspan=2,
            sticky="ew", padx=12, pady=(8, 4))

        def _guardar():
            try:
                edad_val = int(entradas_edit["Edad"].get().strip() or 0)
            except ValueError:
                messagebox.showerror("Error", "La edad debe ser numerica.",
                                     parent=ventana)
                return
            c.nombre = entradas_edit["Nombre"].get().strip()
            c.edad = edad_val
            c.telefono = entradas_edit["Telefono"].get().strip()
            c.correo = entradas_edit["Correo"].get().strip()
            c.formacion = entradas_edit["Nivel de formacion"].get().strip()
            c.aplicar_checks(puntajes_edit[0])
            ventana.destroy()
            self._refrescar_tabla()
            messagebox.showinfo("Actualizado",
                                f"{c.nombre} fue actualizado correctamente.")

        tk.Button(ventana, text="Guardar cambios",
                  command=_guardar,
                  bg="#3b4cca", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=7, cursor="hand2").grid(
            row=len(campos)+1, column=0, columnspan=2,
            sticky="ew", padx=12, pady=(0, 12))

    def _eliminar(self) -> None:
        item = self._tabla.focus()
        if not item:
            messagebox.showwarning("Sin seleccion",
                                   "Selecciona un candidato en la tabla.")
            return
        nodo = self._almacen.buscar_nodo_por_id(int(item))
        if not nodo:
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Eliminar a {nodo.dato.nombre} del sistema?"
        )
        if confirmar:
            nombre = nodo.dato.nombre
            self._almacen.eliminar_por_id(int(item))
            self._refrescar_tabla()
            messagebox.showinfo("Eliminado",
                                f"{nombre} fue eliminado del sistema.")
