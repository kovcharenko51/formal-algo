from grammar import Grammar
from earley_parser import EarleyParser
from lr_1_parser import LRParser


class Algo:

    def __init__(self, grammar: Grammar):
        self.parser = LRParser(grammar)
        self.grammar = grammar

    def fit(self):
        self.parser.build_states("S#", self.grammar.start)
        self.parser.build_table()

    @staticmethod
    def predict(word: str, grammar: Grammar) -> bool:
        parser = EarleyParser(word, grammar)
        return parser.parse()

