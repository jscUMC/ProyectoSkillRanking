class ColaPrioridad:
    """
    Cola de prioridad tipo max-heap implementada manualmente.
    Almacena tuplas (-puntaje, contador, candidato) para ordenar
    de mayor a menor puntaje sin usar modulos externos de heap.
    """

    def __init__(self):
        self._heap = []
        self._contador = 0

    # ── Operaciones internas del heap ─────────────────────────────────────────
    def _padre(self, i: int) -> int:
        return (i - 1) // 2

    def _hijo_izq(self, i: int) -> int:
        return 2 * i + 1

    def _hijo_der(self, i: int) -> int:
        return 2 * i + 2

    def _intercambiar(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _subir(self, i: int) -> None:
        while i > 0:
            p = self._padre(i)
            if self._heap[i] < self._heap[p]:
                self._intercambiar(i, p)
                i = p
            else:
                break

    def _bajar(self, i: int) -> None:
        n = len(self._heap)
        while True:
            menor = i
            iz = self._hijo_izq(i)
            de = self._hijo_der(i)
            if iz < n and self._heap[iz] < self._heap[menor]:
                menor = iz
            if de < n and self._heap[de] < self._heap[menor]:
                menor = de
            if menor != i:
                self._intercambiar(i, menor)
                i = menor
            else:
                break

    # ── API publica ───────────────────────────────────────────────────────────
    def insertar(self, candidato, puntaje: int) -> None:
        """Inserta un candidato con su puntaje."""
        self._heap.append((-puntaje, self._contador, candidato))
        self._subir(len(self._heap) - 1)
        self._contador += 1

    def obtener_ordenados(self) -> list:
        """Devuelve lista de (candidato, puntaje) de mayor a menor."""
        copia = sorted(self._heap)
        return [(c, -s) for s, _, c in copia]

    def limpiar(self) -> None:
        self._heap.clear()
        self._contador = 0

    def __len__(self) -> int:
        return len(self._heap)
