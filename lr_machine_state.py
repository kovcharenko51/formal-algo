from situation import LRSituation


class LRMachineState:

    def __init__(self, situations: set[LRSituation]):
        self.situations = situations

    def __eq__(self, other):
        return tuple(sorted(self.situations)) == tuple(sorted(other.situations))

    def __hash__(self):
        situation_hash = 0
        mod = int(10000000007 ** len(self.situations))
        for situation in sorted(self.situations):
            situation_hash ^= int(hash(situation) * mod)
            mod /= 1000000007
        return situation_hash
