import pytest
from cooklang_parser.parser import CooklangParser


@pytest.fixture
def parser():
    return CooklangParser()


def test_extract_ingredients_basic(parser):
    text = "@chicken breast{2}\n@flour{200g}"
    expected = [
        {"name": "chicken breast", "quantity": "2", "unit": None},
        {"name": "flour", "quantity": "200", "unit": "g"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_empty_text(parser):
    text = ""
    expected = []
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_no_detailed_matches(parser):
    text = "@chicken{}\n@flour{}"
    expected = [
        {"name": "chicken", "quantity": None, "unit": None},
        {"name": "flour", "quantity": None, "unit": None},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_no_simple_matches(parser):
    text = "@chicken{2}\n@flour{200g}"
    expected = [
        {"name": "chicken", "quantity": "2", "unit": None},
        {"name": "flour", "quantity": "200", "unit": "g"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_both_matches(parser):
    text = "@chicken{2}\n@flour\n@tomato sauce{300ml}"
    expected = [
        {"name": "chicken", "quantity": "2", "unit": None},
        {"name": "tomato sauce", "quantity": "300", "unit": "ml"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_duplicate_detailed(parser):
    text = "@chicken{2}\n@chicken{300g}"
    expected = [
        {"name": "chicken", "quantity": "2", "unit": None},
        {"name": "chicken", "quantity": "300", "unit": "g"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_duplicate_simple(parser):
    text = "@chicken{2}\n@chicken"
    expected = [{"name": "chicken", "quantity": "2", "unit": None}]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_whitespace(parser):
    text = "@chicken  {  2  }\n@flour  {200g}"
    expected = [
        {"name": "chicken", "quantity": "2", "unit": None},
        {"name": "flour", "quantity": "200", "unit": "g"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_special_characters(parser):
    text = "@chicken{2}\n@flour{200g}\n@egg{1}\n@sugar & salt{to taste}"
    expected = [
        {"name": "chicken", "quantity": "2", "unit": None},
        {"name": "egg", "quantity": "1", "unit": None},
        {"name": "flour", "quantity": "200", "unit": "g"},
        {"name": "sugar & salt", "quantity": None, "unit": None},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_no_quantity_unit(parser):
    text = "@chicken{}\n@flour{}\n@egg{}\n@sugar{}"
    expected = [
        {"name": "chicken", "quantity": None, "unit": None},
        {"name": "egg", "quantity": None, "unit": None},
        {"name": "flour", "quantity": None, "unit": None},
        {"name": "sugar", "quantity": None, "unit": None},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients(parser):
    text = "@chicken breast{2}\n@flour{200g}"
    expected = [
        {"name": "chicken breast", "quantity": "2", "unit": None},
        {"name": "flour", "quantity": "200", "unit": "g"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_with_units(parser):
    text = "@milk{500ml}\n@butter{100g}"
    expected = [
        {"name": "butter", "quantity": "100", "unit": "g"},
        {"name": "milk", "quantity": "500", "unit": "ml"},
    ]
    assert parser.extract_ingredients(text) == expected


def test_extract_ingredients_empty(parser):
    text = ""
    expected = []
    assert parser.extract_ingredients(text) == expected
