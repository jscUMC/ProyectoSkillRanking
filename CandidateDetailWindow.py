import tkinter as tk
from Candidate import Candidate, SKILL_MAX


class CandidateDetailWindow(tk.Toplevel):
    def __init__(self, parent, candidate: Candidate):
        super().__init__(parent)
        self.title("Informacion de candidato")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")
        self._build(candidate)
        self.grab_set()

    def _build(self, c: Candidate) -> None:
        # Header
        header = tk.Frame(self, bg="#3b4cca", pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Informacion de candidato",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#3b4cca",
        ).pack()

        # Info card
        card = tk.Frame(self, bg="white", padx=20, pady=16, bd=1, relief="solid")
        card.pack(padx=20, pady=(12, 6), fill="x")

        fields = [
            ("Nombre:", c.name),
            ("Edad:", str(c.age)),
            ("Telefono:", c.phone),
            ("Correo:", c.email),
            ("Nivel de formacion:", c.education),
        ]
        for label, value in fields:
            row = tk.Frame(card, bg="white")
            row.pack(fill="x", pady=3)
            tk.Label(
                row, text=label, font=("Segoe UI", 10, "bold"),
                bg="white", width=20, anchor="w"
            ).pack(side="left")
            tk.Label(
                row, text=value, font=("Segoe UI", 10),
                bg="white", anchor="w"
            ).pack(side="left")

        # Score badge
        badge = tk.Frame(self, bg="#f0f4f8")
        badge.pack(pady=6)
        tk.Label(
            badge, text="PUNTUACION TOTAL",
            font=("Segoe UI", 9, "bold"), bg="#f0f4f8", fg="#555"
        ).pack()
        tk.Label(
            badge, text=str(c.score),
            font=("Segoe UI", 30, "bold"), fg="#3b4cca", bg="#f0f4f8"
        ).pack()

        # Skills section
        tk.Label(
            self, text="Puntuacion de habilidades",
            font=("Segoe UI", 11, "bold"), bg="#f0f4f8"
        ).pack(pady=(8, 2))

        sk_frame = tk.Frame(self, bg="#f0f4f8")
        sk_frame.pack(fill="x", padx=24, pady=(0, 14))

        for skill, val in c.skills.items():
            max_val = SKILL_MAX[skill]
            row = tk.Frame(sk_frame, bg="#f0f4f8")
            row.pack(fill="x", pady=3)

            tk.Label(
                row, text=skill, font=("Segoe UI", 9),
                bg="#f0f4f8", width=22, anchor="w"
            ).pack(side="left")

            bar_bg = tk.Frame(row, bg="#dde3ee", width=150, height=13)
            bar_bg.pack(side="left", padx=(4, 8))
            bar_bg.pack_propagate(False)
            fill_w = int(150 * val / max_val) if max_val else 0
            tk.Frame(bar_bg, bg="#3b4cca", width=fill_w, height=13).place(x=0, y=0)

            tk.Label(
                row, text=f"{val} / {max_val}", font=("Segoe UI", 9),
                bg="#f0f4f8", fg="#333"
            ).pack(side="left")

        tk.Button(
            self, text="Cerrar", command=self.destroy,
            bg="#3b4cca", fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", padx=24, pady=7, cursor="hand2"
        ).pack(pady=(0, 16))