from grammar import Grammar
from earley_parser import EarleyParser
from lr_1_parser import LRParser


class Algo:

    def __init__(self, grammar: Grammar):
        self.parser = None
        self.grammar = grammar

    def fit(self):
        self.parser.build_states("S#", self.grammar.start)
        self.parser.build_table()

    def predict(self, word: str, grammar: Grammar, algorithm: str) -> bool:
        if algorithm == "earley":
            self.parser = EarleyParser(word, grammar)
            return self.parser.parse()
        if algorithm == "lr":
            self.parser = LRParser(grammar)
            return self.parser.parse(word) == "accept"


