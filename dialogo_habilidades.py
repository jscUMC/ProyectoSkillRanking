import tkinter as tk
from tkinter import ttk
from skills_data import PREGUNTAS_POR_CATEGORIA


class DialogoHabilidades(tk.Toplevel):
    """
    Dialogo con checkboxes por categoria.
    Cada check suma su peso; la categoria tiene maximo 100 puntos.
    """

    def __init__(self, padre, checks_iniciales: dict = None):
        super().__init__(padre)
        self.title("Evaluacion de habilidades del candidato")
        self.resizable(False, True)
        self.configure(bg="#f0f4f8")
        self.geometry("520x560")
        self.resultado = None
        self._vars = {}
        self._construir(checks_iniciales or {})
        self.grab_set()

    def _construir(self, iniciales: dict) -> None:
        tk.Label(self,
                 text="Selecciona las habilidades del candidato",
                 font=("Segoe UI", 12, "bold"),
                 bg="#f0f4f8").pack(pady=(12, 4))

        # Canvas con scroll
        contenedor = tk.Frame(self, bg="#f0f4f8")
        contenedor.pack(fill="both", expand=True, padx=12)

        canvas = tk.Canvas(contenedor, bg="#f0f4f8",
                           highlightthickness=0, width=490)
        vsb = ttk.Scrollbar(contenedor, orient="vertical",
                             command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(canvas, bg="#f0f4f8")
        canvas.create_window((0, 0), window=interior, anchor="nw")

        for cat, preguntas in PREGUNTAS_POR_CATEGORIA.items():
            maximo = sum(p for _, p in preguntas)
            lf = tk.LabelFrame(
                interior,
                text=f"{cat}  (max {maximo} pts)",
                font=("Segoe UI", 9, "bold"),
                bg="#f0f4f8", padx=10, pady=6
            )
            lf.pack(fill="x", pady=5, padx=6)

            self._vars[cat] = {}

            # Label que muestra puntaje acumulado de la categoria
            var_pts = tk.StringVar(value="0 / 100 pts")
            lbl_pts = tk.Label(lf, textvariable=var_pts,
                               font=("Segoe UI", 8, "italic"),
                               fg="#3b4cca", bg="#f0f4f8", anchor="e")
            lbl_pts.pack(fill="x")

            def _hacer_callback(c=cat, vp=var_pts):
                def _cb(*_):
                    total = 0
                    for texto, (var_bool, peso) in self._vars[c].items():
                        if var_bool.get():
                            total += peso
                    vp.set(f"{total} / 100 pts")
                return _cb

            cb_fn = _hacer_callback()

            for texto, peso in preguntas:
                init_val = iniciales.get(cat, {}).get(texto, False)
                var_bool = tk.BooleanVar(value=init_val)
                var_bool.trace_add("write", cb_fn)
                tk.Checkbutton(
                    lf,
                    text=f"{texto}  (+{peso} pts)",
                    variable=var_bool,
                    bg="#f0f4f8",
                    font=("Segoe UI", 9),
                    anchor="w"
                ).pack(fill="x")
                self._vars[cat][texto] = (var_bool, peso)

            # Actualizar label inicial
            cb_fn()

        interior.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        def _scroll_mouse(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _scroll_mouse)

        # Botones
        btn_frame = tk.Frame(self, bg="#f0f4f8")
        btn_frame.pack(fill="x", pady=10, padx=16)

        tk.Button(btn_frame, text="Confirmar",
                  command=self._confirmar,
                  bg="#3b4cca", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=16, pady=6,
                  cursor="hand2").pack(side="right", padx=4)
        tk.Button(btn_frame, text="Cancelar",
                  command=self.destroy,
                  bg="#aaa", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=16, pady=6,
                  cursor="hand2").pack(side="right")

    def _confirmar(self) -> None:
        self.resultado = {
            cat: {texto: var_bool.get()
                  for texto, (var_bool, _) in qs.items()}
            for cat, qs in self._vars.items()
        }
        self.destroy()
