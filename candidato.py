from skills_data import CATEGORIAS, PREGUNTAS_POR_CATEGORIA


class Candidato:
    def __init__(self, nombre: str, edad: int, telefono: str,
                 correo: str, formacion: str):
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono
        self.correo = correo
        self.formacion = formacion
        # puntaje 0-100 por categoria
        self.puntajes: dict = {cat: 0 for cat in CATEGORIAS}
        # {categoria: {texto_pregunta: bool}}
        self.checks: dict = {
            cat: {texto: False for texto, _ in preguntas}
            for cat, preguntas in PREGUNTAS_POR_CATEGORIA.items()
        }

    @property
    def puntaje_total(self) -> int:
        return sum(self.puntajes.values())

    def puntaje_en_categorias(self, categorias: list) -> int:
        return sum(self.puntajes.get(c, 0) for c in categorias)

    def aplicar_checks(self, nuevos_checks: dict) -> None:
        """Recibe {categoria: {texto: bool}}, recalcula puntajes."""
        for cat, preguntas_marcadas in nuevos_checks.items():
            total_cat = 0
            for texto, marcado in preguntas_marcadas.items():
                if marcado:
                    for preg, peso in PREGUNTAS_POR_CATEGORIA[cat]:
                        if preg == texto:
                            total_cat += peso
                            break
            self.puntajes[cat] = total_cat
            self.checks[cat] = dict(preguntas_marcadas)

    def __repr__(self) -> str:
        return f"Candidato({self.nombre}, total={self.puntaje_total})"
