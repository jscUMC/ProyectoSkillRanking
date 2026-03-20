from nodo import Nodo


class ListaDoble:
    """Lista doblemente enlazada — almacen principal de candidatos."""

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def agregar(self, dato) -> Nodo:
        nodo = Nodo(dato)
        if self.cola is None:
            self.cabeza = self.cola = nodo
        else:
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = nodo
        self._tamano += 1
        return nodo

    def eliminar(self, nodo: Nodo) -> None:
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.cabeza = nodo.siguiente
        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior
        else:
            self.cola = nodo.anterior
        nodo.anterior = nodo.siguiente = None
        self._tamano -= 1

    def buscar_por_id(self, obj_id: int):
        actual = self.cabeza
        while actual:
            if id(actual.dato) == obj_id:
                return actual
            actual = actual.siguiente
        return None

    def a_lista(self) -> list:
        resultado, actual = [], self.cabeza
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
