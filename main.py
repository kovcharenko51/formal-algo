from algo import Algo
from grammar import Grammar, GrammarRule


def main():
    alphabet = {}
    print("Enter non-terminals count:")
    non_terminal_count = int(input())
    print("Enter non-terminals:")
    for i in range(non_terminal_count):
        alphabet[input()] = False
    print("Enter terminals count:")
    terminal_count = int(input())
    print("Enter terminals:")
    for i in range(terminal_count):
        alphabet[input()] = True
    grammar = Grammar()
    print("Enter rules count:")
    rule_count = int(input())
    print("Enter rules:")
    for i in range(rule_count):
        rule = input().split()
        right_part = []
        if len(rule) != 1:
            right_part = rule[1:]
        grammar.add_rules({GrammarRule(rule[0], right_part)})
    grammar.set_alphabet(alphabet)
    print("Enter old start non-terminal:")
    grammar.set_start(input())
    print("Enter new start non-terminal:")
    grammar.set_new_start(input())
    print("Enter word:")
    word = input()
    algo = Algo(grammar)
    print("Enter preferable algorithm:")
    algorithm = input()
    print(algo.predict(word, algorithm))


if __name__ == "__main__":
    main()
