from grammar import Grammar, GrammarRule
from situation import EarleySituation


class EarleyParser:
    def __init__(self, word: str, grammar: Grammar):
        self.config = {i: set() for i in range(0, len(word) + 1)}
        self.word = word
        self.grammar = grammar

    def scan(self, position: int):
        for situation in self.config[position - 1]:
            if situation.dot_pos == len(situation.right_part):
                continue
            if situation.right_part[situation.dot_pos] == self.word[position - 1]:
                new_situation = EarleySituation(situation.left_non_terminal, situation.right_part,
                                                situation.dot_pos + 1, situation.parent_pos)
                if new_situation in self.config[position]:
                    continue
                self.config[position].add(new_situation)

    def predict(self, position: int):
        for situation in self.config[position]:
            for rule in self.grammar.rules:
                if situation.dot_pos == len(situation.right_part):
                    continue
                if rule.left_non_terminal != situation.right_part[situation.dot_pos]:
                    continue
                new_situation = EarleySituation(rule.left_non_terminal, rule.right_part, 0, position)
                if new_situation in self.config[position]:
                    continue
                self.config[position].add(new_situation)
            break

    def complete(self, position: int):
        for situation in self.config[position]:
            if situation.dot_pos != len(situation.right_part):
                continue
            for prev_situation in self.config[situation.parent_pos]:
                if prev_situation.dot_pos == len(prev_situation.right_part):
                    continue
                if prev_situation.right_part[prev_situation.dot_pos] != situation.left_non_terminal:
                    continue
                new_situation = EarleySituation(prev_situation.left_non_terminal, prev_situation.right_part,
                                                prev_situation.dot_pos + 1, prev_situation.parent_pos)
                if new_situation in self.config[position]:
                    continue
                self.config[position].add(new_situation)
                return

    def parse(self) -> bool:
        new_start = "S#"
        old_start = self.grammar.start
        self.grammar.add_rules({GrammarRule(new_start, [old_start])})
        self.grammar.start = new_start
        self.config[0].add(EarleySituation(new_start, [old_start], 0, 0))
        for i in range(len(self.word) + 1):
            if i != 0:
                self.scan(i)
            has_changed = True
            while has_changed:
                has_changed = False
                current_size = len(self.config[i])
                self.complete(i)
                self.predict(i)
                if len(self.config[i]) != current_size:
                    has_changed = True
        final = EarleySituation(new_start, [old_start], 1, 0)
        return final in self.config[len(self.word)]
