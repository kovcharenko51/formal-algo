import pytest

from earley_parser import EarleyParser, EarleySituation
from grammar import Grammar, GrammarRule

grammar = Grammar()
parser = EarleyParser("", Grammar())
new_start = "S#"
old_start = "S"


@pytest.fixture()
def set_grammar():
    grammar.add_rules({GrammarRule("S", []), GrammarRule("S", ["a", "S", "b", "S"])})
    grammar.set_start(old_start)
    grammar.set_alphabet({"S": False, "a": True, "b": True})


@pytest.fixture()
def prepare_parser(set_grammar):
    global parser
    parser = EarleyParser("abab", grammar)
    parser.grammar = grammar
    parser.grammar.add_rules({GrammarRule(new_start, [old_start])})
    parser.grammar.start = new_start


def test_predict(prepare_parser):
    global parser
    start_situation = EarleySituation(new_start, [old_start], 0, 0)
    parser.config[0].add(start_situation)
    parser.predict(0)
    expected_config_set = {start_situation, EarleySituation("S", ["a", "S", "b", "S"], 0, 0), EarleySituation("S", [], 0, 0)}
    assert len(expected_config_set) == len(parser.config[0])
    for actual_situation in parser.config[0]:
        assert actual_situation in expected_config_set


@pytest.mark.dependency(depends=["test_predict"])
def test_complete():
    parser.complete(0)
    complete_situation = EarleySituation(new_start, [old_start], 1, 0)
    assert len(parser.config[0]) == 4
    assert complete_situation in parser.config[0]


@pytest.mark.dependency(depends=["test_complete"])
def test_scan():
    parser.scan(1)
    scan_situation = EarleySituation("S", ["a", "S", "b", "S"], 1, 0)
    assert len(parser.config[1]) == 1
    assert scan_situation in parser.config[1]


def test_parse_if_accept():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", []), GrammarRule("S", ["a", "S", "b", "S"])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "a": True, "b": True})
    new_parser = EarleyParser("abab", new_grammar)
    assert new_parser.parse() is True


def test_another_parse_if_accept():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", ["a", "A"]), GrammarRule("A", ["+", "a", "A"]),
                           GrammarRule("A", [])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "A": False, "a": True, "+": True})
    new_parser = EarleyParser("a+a+a", new_grammar)
    assert new_parser.parse() is True


def test_parse_if_reject():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", []), GrammarRule("S", ["a", "S", "b", "S"])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "a": True, "b": True})
    new_parser = EarleyParser("ababa", new_grammar)
    assert new_parser.parse() is False


def test_another_parse_if_reject():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", ["a", "A"]), GrammarRule("A", ["+", "a", "A"]),
                           GrammarRule("A", [])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "A": False, "a": True, "+": True})
    new_parser = EarleyParser("a+a+a+a+a+", new_grammar)
    assert new_parser.parse() is False
