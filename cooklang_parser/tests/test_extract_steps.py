import pytest
from cooklang_parser.parser import CooklangParser


@pytest.fixture
def parser():
    return CooklangParser()


def test_extract_steps_no_components(parser):
    text = "Let it cool."
    expected = [{"type": "text", "value": "Let it cool."}]
    assert parser.extract_steps(text) == expected


def test_extract_steps_empty(parser):
    text = ""
    expected = []
    assert parser.extract_steps(text) == expected


def test_extract_steps_only_metadata(parser):
    text = ">> Title: Recipe Title\n>> Servings: 4\n>> Difficulty: Easy"
    expected = []
    assert parser.extract_steps(text) == expected


def test_extract_steps_multiple_components(parser):
    text = (
        "Mix @flour{200g} and @sugar{100g} in a #bowl. ~Bake at 180°C for {30 minutes}."
    )
    expected = [
        {"type": "text", "value": "Mix"},
        {"type": "ingredient", "name": "flour", "quantity": "200", "unit": "g"},
        {"type": "text", "value": "and"},
        {"type": "ingredient", "name": "sugar", "quantity": "100", "unit": "g"},
        {"type": "text", "value": "in a"},
        {"type": "cookware", "name": "bowl"},
        {"type": "text", "value": ". ~Bake at 180°C for {30 minutes}."},
    ]
    assert parser.extract_steps(text) == expected


def test_extract_steps(parser):
    text = "Mix @flour{200g} with water and heat in a #pan for ~{10 minutes}.\nLet it cool."
    expected = [
        {"type": "text", "value": "Mix"},
        {"type": "ingredient", "name": "flour", "quantity": "200", "unit": "g"},
        {"type": "text", "value": "with water and heat in a"},
        {"type": "cookware", "name": "pan"},
        {"type": "text", "value": "for"},
        {"type": "timer", "name": "", "duration": "10 minutes"},
        {"type": "text", "value": "."},
        {"type": "text", "value": "Let it cool."},
    ]

    assert parser.extract_steps(text) == expected


def test_extract_steps_multiple_lines(parser):
    text = "Mix @flour{200g} with water and heat in a #pan for ~{10%minutes}.\nLet it cool.\n#Serve immediately."
    expected = [
        {"type": "text", "value": "Mix"},
        {"type": "ingredient", "name": "flour", "quantity": "200", "unit": "g"},
        {"type": "text", "value": "with water and heat in a"},
        {"type": "cookware", "name": "pan"},
        {"type": "text", "value": "for"},
        {"type": "timer", "name": "", "duration": "10%minutes"},
        {"type": "text", "value": "."},
        {"type": "text", "value": "Let it cool."},
        {"type": "cookware", "name": "Serve"},
        {"type": "text", "value": "immediately."},
    ]
    assert parser.extract_steps(text) == expected
