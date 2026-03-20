import random

SKILLS = [
    "Habilidades tecnicas",
    "Certificados",
    "Experiencia",
    "Gestion de proyectos",
    "Comunicacion",
    "Pensamiento critico",
]

SKILL_MAX = {
    "Habilidades tecnicas": 30,
    "Certificados": 25,
    "Experiencia": 20,
    "Gestion de proyectos": 10,
    "Comunicacion": 10,
    "Pensamiento critico": 5,
}


class Candidate:
    def __init__(self, name: str, age: int, phone: str, email: str, education: str):
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.education = education
        self.skills: dict[str, int] = self._generate_random_skills()
        self.score: int = self._calculate_score()

    def _generate_random_skills(self) -> dict[str, int]:
        return {skill: random.randint(0, max_val) for skill, max_val in SKILL_MAX.items()}

    def _calculate_score(self) -> int:
        return sum(self.skills.values())

    def __lt__(self, other: "Candidate") -> bool:
        return self.score < other.score

    def __repr__(self) -> str:
        return f"Candidate({self.name}, score={self.score})"