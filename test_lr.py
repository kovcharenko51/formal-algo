import pytest

from grammar import Grammar, GrammarRule
from lr_1_parser import LRParser
from situation import LRSituation
from lr_machine_state import LRMachineState, LRTableState

grammar = Grammar()
parser = LRParser(Grammar())
new_start = "S#"
old_start = "S"
END = "$"
start_state = LRMachineState(set())


@pytest.fixture()
def set_grammar():
    grammar.add_rules({GrammarRule(new_start, [old_start]), GrammarRule("S", []),
                       GrammarRule("S", ["S", "a", "S", "b"])})
    grammar.set_start(old_start)
    grammar.set_new_start(new_start)
    grammar.set_alphabet({"S": False, "a": True, "b": True})


def test_first_terminal(set_grammar):
    parser.grammar = grammar
    assert parser.first(["a", "S", "b", "b"]) == {"a"}


def test_first_non_terminal(set_grammar):
    parser.grammar = grammar
    assert parser.first(["S", "a", "S"]) == {"a"}


def test_closure(set_grammar):
    global start_state
    parser.grammar = grammar
    start_state = parser.closure({LRSituation(new_start, [old_start], 0, END)})
    expected_start = {LRSituation(new_start, [old_start], 0, END), LRSituation("S", ["S", "a", "S", "b"], 0, END),
                      LRSituation("S", [], 0, END), LRSituation("S", ["S", "a", "S", "b"], 0, "a"),
                      LRSituation("S", [], 0, "a")}
    assert len(start_state.situations) == len(expected_start)
    for situation in expected_start:
        assert situation in start_state.situations


@pytest.mark.dependency(depends=["test_closure"])
def test_goto():
    expected_goto = {LRSituation(new_start, [old_start], 1, END), LRSituation("S", ["S", "a", "S", "b"], 1, END),
                     LRSituation("S", ["S", "a", "S", "b"], 1, "a")}
    goto_state = parser.goto(start_state, "S")
    assert len(goto_state.situations) == len(expected_goto)
    for situation in expected_goto:
        assert situation in goto_state.situations


def test_build_states():
    parser.build_states(new_start, old_start)

    assert len(parser.states) == 8

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 2, END),
                            LRSituation("S", ["S", "a", "S", "b"], 2, "a"),
                            LRSituation("S", ["S", "a", "S", "b"], 0, "b"),
                            LRSituation("S", [], 0, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 0, "a"),
                            LRSituation("S", [], 0, "a")})
    assert parser.states[state] == "q2"

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 3, END),
                            LRSituation("S", ["S", "a", "S", "b"], 3, "a"),
                            LRSituation("S", ["S", "a", "S", "b"], 1, "a"),
                            LRSituation("S", ["S", "a", "S", "b"], 1, "b")})
    assert parser.states[state] == "q3"

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 2, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 2, "a"),
                            LRSituation("S", ["S", "a", "S", "b"], 0, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 0, "a"),
                            LRSituation("S", [], 0, "b"),
                            LRSituation("S", [], 0, "a")})
    assert parser.states[state] == "q4"

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 4, END),
                            LRSituation("S", ["S", "a", "S", "b"], 4, "a")})
    assert parser.states[state] == "q5"

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 3, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 3, "a"),
                            LRSituation("S", ["S", "a", "S", "b"], 1, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 1, "a")})
    assert parser.states[state] == "q6"

    state = LRMachineState({LRSituation("S", ["S", "a", "S", "b"], 4, "b"),
                            LRSituation("S", ["S", "a", "S", "b"], 4, "a")})
    assert parser.states[state] == "q7"

    transitions = {"q0": {"S": "q1"}, "q1": {"a": "q2"}, "q2": {"S": "q3"}, "q3": {"a": "q4", "b": "q5"},
                   "q4": {"S": "q6"}, "q6": {"a": "q4", "b": "q7"}}

    assert transitions == parser.transitions


@pytest.mark.dependency(depends=["test_build_states"])
def test_build_table():
    parser.build_table()
    second_rule = GrammarRule("S", ['S', "a", "S", "b"])
    first_rule = GrammarRule(new_start, [old_start])
    expected_table = {
     "q0": {"S": LRTableState.get_shift_state("q1"),
            "a": LRTableState.get_reduce_state(second_rule),
            "$": LRTableState.get_reduce_state(second_rule)},
     "q1": {"a": LRTableState.get_shift_state("q2"),
            "$": LRTableState.get_accept_state()},
     "q2": {"S": LRTableState.get_shift_state("q3"),
            "b": LRTableState.get_reduce_state(second_rule),
            "a": LRTableState.get_reduce_state(second_rule)},
     "q3": {"a": LRTableState.get_shift_state("q4"),
            "b": LRTableState.get_shift_state("q5")},
     "q4": {"S": LRTableState.get_shift_state("q6"),
            "b": LRTableState.get_reduce_state(second_rule),
            "a": LRTableState.get_reduce_state(second_rule)},
     "q5": {"$": LRTableState.get_reduce_state(first_rule),
            "a": LRTableState.get_reduce_state(first_rule)},
     "q6": {"a": LRTableState.get_shift_state("q4"),
            "b": LRTableState.get_shift_state("q7")},
     "q7": {"b": LRTableState.get_reduce_state(first_rule),
            "a": LRTableState.get_reduce_state(first_rule)}}

    for state, transitions in parser.table.items():
        for symbol, transition in transitions.items():
            assert expected_table[state][symbol].state_type == transition.state_type


@pytest.mark.dependency(depends=["test_build_table"])
def test_parse_if_accept():
    assert parser.parse("aabbab") == "accept"


@pytest.mark.dependency(depends=["test_build_table"])
def test_parse_if_reject():
    assert parser.parse("aa") == "reject"


def test_another_parse_if_accept():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", []), GrammarRule("S", ["a", "S", "b", "S"])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "a": True, "b": True})
    new_parser = LRParser(new_grammar)
    new_parser.build_states(new_start, old_start)
    new_parser.build_table()
    assert new_parser.parse("abab") == "accept"


def test_another_parse_if_reject():
    new_grammar = Grammar()
    new_grammar.add_rules({GrammarRule("S", []), GrammarRule("S", ["a", "S", "b", "S"])})
    new_grammar.set_start(old_start)
    new_grammar.set_alphabet({"S": False, "a": True, "b": True})
    new_parser = LRParser(new_grammar)
    new_parser.build_states(new_start, old_start)
    new_parser.build_table()
    assert new_parser.parse("aabb") == "accept"
