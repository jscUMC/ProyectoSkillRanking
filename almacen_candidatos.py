from lista_doble import ListaDoble
from candidato import Candidato


class AlmacenCandidatos:
    """Wrapper de la lista doble — CRUD de candidatos."""

    def __init__(self):
        self._lista = ListaDoble()

    def agregar(self, candidato: Candidato):
        return self._lista.agregar(candidato)

    def eliminar_por_id(self, obj_id: int) -> bool:
        nodo = self._lista.buscar_por_id(obj_id)
        if nodo:
            self._lista.eliminar(nodo)
            return True
        return False

    def buscar_nodo_por_id(self, obj_id: int):
        return self._lista.buscar_por_id(obj_id)

    def todos(self) -> list:
        return self._lista.a_lista()

    def __len__(self) -> int:
        return len(self._lista)
