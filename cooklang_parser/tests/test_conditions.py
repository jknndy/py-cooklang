import pytest
from cooklang_parser.parser import CooklangParser


@pytest.fixture
def parser():
    return CooklangParser()


def test_extract_conditions(parser):
    text = "If @egg is cooked, proceed to the next step."
    expected = [
        {
            "ingredient": "egg",
            "condition": "cooked",
            "action": "proceed to the next step.",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_empty(parser):
    text = ""
    expected = []
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_multiple_conditions(parser):
    text = "If @egg is cooked, proceed to the next step. If @milk is boiled, add to the mixture."
    expected = [
        {
            "ingredient": "egg",
            "condition": "cooked",
            "action": "proceed to the next step.",
        },
        {"ingredient": "milk", "condition": "boiled", "action": "add to the mixture."},
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_no_condition_keyword(parser):
    text = "Cook the @egg."
    expected = []
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_complex_condition(parser):
    text = "If @egg is lightly cooked, gently fold into the mixture."
    expected = [
        {
            "ingredient": "egg",
            "condition": "lightly cooked",
            "action": "gently fold into the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_condition_with_hyphen(parser):
    text = "If @butter is room-temperature, spread on bread."
    expected = [
        {
            "ingredient": "butter",
            "condition": "room-temperature",
            "action": "spread on bread",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_multiple_actions(parser):
    text = "If @dough is ready, roll it out and bake at 350 degrees."
    expected = [
        {
            "ingredient": "dough",
            "condition": "ready",
            "action": "roll it out and bake at 350 degrees",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_with_spaces(parser):
    text = "If @heavy cream is whipped, fold into the mixture."
    expected = [
        {
            "ingredient": "heavy cream",
            "condition": "whipped",
            "action": "fold into the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_with_numbers(parser):
    text = "If @water is 100 degrees, add to the mixture."
    expected = [
        {
            "ingredient": "water",
            "condition": "100 degrees",
            "action": "add to the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_case_insensitive(parser):
    text = "If @Egg is Cooked, proceed to the next step."
    expected = [
        {
            "ingredient": "Egg",
            "condition": "Cooked",
            "action": "proceed to the next step",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_malformed_input(parser):
    text = "If @egg is, proceed to the next step"
    expected = []
    assert parser.extract_conditions(text) == expected


def test_extract_conditions(parser):
    text = "If @egg{} is cooked, proceed to the next step."
    expected = [
        {
            "ingredient": "egg",
            "condition": "cooked",
            "action": "proceed to the next step",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_multiple_conditions(parser):
    text = "If @egg{} is cooked, proceed to the next step. If @milk{} is boiled, add to the mixture"
    expected = [
        {
            "ingredient": "egg",
            "condition": "cooked",
            "action": "proceed to the next step",
        },
        {"ingredient": "milk", "condition": "boiled", "action": "add to the mixture"},
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_complex_condition(parser):
    text = "If @egg{} is lightly cooked, gently fold into the mixture."
    expected = [
        {
            "ingredient": "egg",
            "condition": "lightly cooked",
            "action": "gently fold into the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_condition_with_hyphen(parser):
    text = "If @butter{} is room-temperature, spread on bread."
    expected = [
        {
            "ingredient": "butter",
            "condition": "room-temperature",
            "action": "spread on bread",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_multiple_actions(parser):
    text = "If @dough{} is ready, roll it out and bake at 350 degrees."
    expected = [
        {
            "ingredient": "dough",
            "condition": "ready",
            "action": "roll it out and bake at 350 degrees",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_with_spaces(parser):
    text = "If @heavy cream{} is whipped, fold into the mixture."
    expected = [
        {
            "ingredient": "heavy cream",
            "condition": "whipped",
            "action": "fold into the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_with_numbers(parser):
    text = "If @water{} is 100 degrees, add to the mixture."
    expected = [
        {
            "ingredient": "water",
            "condition": "100 degrees",
            "action": "add to the mixture",
        }
    ]
    assert parser.extract_conditions(text) == expected


def test_extract_conditions_case_insensitive(parser):
    text = "If @Egg{} is Cooked, proceed to the next step."
    expected = [
        {
            "ingredient": "Egg",
            "condition": "Cooked",
            "action": "proceed to the next step",
        }
    ]
    assert parser.extract_conditions(text) == expected
