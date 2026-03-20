import heapq
from Candidate import Candidate


class RankingQueue:
    """Max-heap priority queue — candidate with highest score is first."""

    def __init__(self):
        self._heap = []
        self._counter = 0

    def insert(self, candidate: Candidate) -> None:
        heapq.heappush(self._heap, (-candidate.score, self._counter, candidate))
        self._counter += 1

    def get_sorted(self) -> list:
        """Return candidates sorted from highest to lowest score."""
        return [c for _, _, c in sorted(self._heap)]

    def find_by_id(self, obj_id: int):
        for _, _, c in self._heap:
            if id(c) == obj_id:
                return c
        return None

    def __len__(self) -> int:
        return len(self._heap)