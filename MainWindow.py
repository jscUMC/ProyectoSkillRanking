import tkinter as tk
from tkinter import ttk, messagebox
from Candidate import Candidate, SKILL_MAX
from RankingQueue import RankingQueue
from CandidateDetailWindow import CandidateDetailWindow


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Candidatos")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)
        self.ranking = RankingQueue()
        self._build()

    def _build(self) -> None:
        tk.Label(
            self.root,
            text="Sistema de Gestion de Candidatos",
            font=("Segoe UI", 15, "bold"),
            bg="#3b4cca",
            fg="white",
            pady=10,
        ).pack(fill="x")

        content = tk.Frame(self.root, bg="#f0f4f8", padx=16, pady=16)
        content.pack(fill="both", expand=True)

        self._build_form(content)
        self._build_skills_panel(content)
        self._build_ranking_panel(content)

    # ── Form ──────────────────────────────────────────────────────────────────
    def _build_form(self, parent: tk.Frame) -> None:
        form = tk.LabelFrame(
            parent, text="Crear candidato",
            font=("Segoe UI", 10, "bold"), bg="#f0f4f8", padx=12, pady=12
        )
        form.grid(row=0, column=0, sticky="n", padx=(0, 14))

        field_names = ["Nombre", "Edad", "Telefono", "Correo", "Nivel de formacion"]
        self.entries: dict = {}

        for i, name in enumerate(field_names):
            tk.Label(
                form, text=f"{name}:", font=("Segoe UI", 9),
                bg="#f0f4f8", anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=4)

            entry = tk.Entry(
                form, width=28, relief="flat",
                highlightthickness=1, highlightbackground="#aab",
                font=("Segoe UI", 9)
            )
            entry.grid(row=i, column=1, padx=(8, 0), pady=4)
            self.entries[name] = entry

        n = len(field_names)

        tk.Button(
            form, text="Añadir Hoja de Vida", command=self._clear_form,
            bg="#555555", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=10, pady=6, cursor="hand2"
        ).grid(row=n, column=0, columnspan=2, sticky="ew", pady=(12, 4))

        tk.Button(
            form, text="Insertar", command=self._insert_candidate,
            bg="#5b7fff", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=10, pady=8, cursor="hand2"
        ).grid(row=n + 1, column=0, columnspan=2, sticky="ew")

    # ── Skills panel ──────────────────────────────────────────────────────────
    def _build_skills_panel(self, parent: tk.Frame) -> None:
        panel = tk.LabelFrame(
            parent, text="Puntuacion de habilidades",
            font=("Segoe UI", 10, "bold"), bg="#f0f4f8", padx=12, pady=12
        )
        panel.grid(row=0, column=1, sticky="n", padx=(0, 14))

        for skill, max_val in SKILL_MAX.items():
            row = tk.Frame(panel, bg="#f0f4f8")
            row.pack(fill="x", pady=3)
            tk.Label(
                row, text=skill, font=("Segoe UI", 9),
                bg="#f0f4f8", width=22, anchor="w"
            ).pack(side="left")
            tk.Label(
                row, text=str(max_val), font=("Segoe UI", 9, "bold"),
                bg="#f0f4f8", fg="#3b4cca"
            ).pack(side="left")

    # ── Ranking table ─────────────────────────────────────────────────────────
    def _build_ranking_panel(self, parent: tk.Frame) -> None:
        panel = tk.LabelFrame(
            parent, text="Ranking de candidatos",
            font=("Segoe UI", 10, "bold"), bg="#f0f4f8", padx=12, pady=12
        )
        panel.grid(row=0, column=2, sticky="nsew")

        cols = ("Pos", "Nombre", "Formacion", "Puntuacion")
        self.tree = ttk.Treeview(
            panel, columns=cols, show="headings",
            height=12, selectmode="browse"
        )

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

        widths = {"Pos": 40, "Nombre": 160, "Formacion": 120, "Puntuacion": 85}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self._on_row_double_click)

        tk.Label(
            panel,
            text="Doble clic en un candidato para ver sus detalles",
            font=("Segoe UI", 8), bg="#f0f4f8", fg="#888"
        ).pack(pady=(6, 0))

    # ── Actions ───────────────────────────────────────────────────────────────
    def _clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _insert_candidate(self) -> None:
        values = {k: v.get().strip() for k, v in self.entries.items()}

        if not values["Nombre"]:
            messagebox.showwarning("Campo requerido", "El nombre es obligatorio.")
            return

        try:
            age = int(values["Edad"]) if values["Edad"] else 0
        except ValueError:
            messagebox.showerror("Error de validacion", "La edad debe ser un numero entero.")
            return

        candidate = Candidate(
            name=values["Nombre"],
            age=age,
            phone=values["Telefono"],
            email=values["Correo"],
            education=values["Nivel de formacion"],
        )

        self.ranking.insert(candidate)
        self._refresh_ranking()
        self._clear_form()

        messagebox.showinfo(
            "Candidato insertado",
            f"{candidate.name} fue agregado exitosamente.\nPuntuacion: {candidate.score}"
        )

    def _refresh_ranking(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        for pos, c in enumerate(self.ranking.get_sorted(), start=1):
            tag = "gold" if pos == 1 else ("silver" if pos == 2 else "")
            self.tree.insert(
                "", "end",
                iid=str(id(c)),
                values=(pos, c.name, c.education, c.score),
                tags=(tag,)
            )

        self.tree.tag_configure("gold", background="#fff3b0")
        self.tree.tag_configure("silver", background="#eaeaea")

    def _on_row_double_click(self, event) -> None:
        item = self.tree.focus()
        if not item:
            return
        candidate = self.ranking.find_by_id(int(item))
        if candidate:
            CandidateDetailWindow(self.root, candidate)