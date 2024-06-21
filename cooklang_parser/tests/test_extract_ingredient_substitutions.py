import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()


def test_extract_ingredient_substitutions(parser):
    text = "Use @butter{100g} (or @margarine{100g}) for frying."
    expected = [
        {
            "primary": {"name": "butter", "quantity": "100", "unit": "g"},
            "substitute": {"name": "margarine", "quantity": "100", "unit": "g"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_empty(parser):
    text = ""
    expected = []
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_multiple(parser):
    text = "Use @butter{100g} (or @margarine{100g}) for frying. Use @sugar{50g} (or @honey{50ml}) for sweetness."
    expected = [
        {
            "primary": {"name": "butter", "quantity": "100", "unit": "g"},
            "substitute": {"name": "margarine", "quantity": "100", "unit": "g"}
        },
        {
            "primary": {"name": "sugar", "quantity": "50", "unit": "g"},
            "substitute": {"name": "honey", "quantity": "50", "unit": "ml"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_no_unit(parser):
    text = "Use @butter{100} (or @margarine{100}) for frying."
    expected = [
        {
            "primary": {"name": "butter", "quantity": "100", "unit": None},
            "substitute": {"name": "margarine", "quantity": "100", "unit": None}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_different_units(parser):
    text = "Use @butter{100g} (or @oil{100ml}) for frying."
    expected = [
        {
            "primary": {"name": "butter", "quantity": "100", "unit": "g"},
            "substitute": {"name": "oil", "quantity": "100", "unit": "ml"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_with_spaces(parser):
    text = "Use @heavy cream{100ml} (or @light cream{100ml}) for the sauce."
    expected = [
        {
            "primary": {"name": "heavy cream", "quantity": "100", "unit": "ml"},
            "substitute": {"name": "light cream", "quantity": "100", "unit": "ml"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_with_hyphen(parser):
    text = "Use @self-raising flour{200g} (or @plain flour{200g}) for baking."
    expected = [
        {
            "primary": {"name": "self-raising flour", "quantity": "200", "unit": "g"},
            "substitute": {"name": "plain flour", "quantity": "200", "unit": "g"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_with_numbers(parser):
    text = "Use @flour{100g} (or @cornstarch{50g}) for thickening."
    expected = [
        {
            "primary": {"name": "flour", "quantity": "100", "unit": "g"},
            "substitute": {"name": "cornstarch", "quantity": "50", "unit": "g"}
        }
    ]
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_malformed(parser):
    text = "Use @butter{100g} (or margarine{100g}) for frying."
    expected = []
    assert parser.extract_ingredient_substitutions(text) == expected

def test_extract_ingredient_substitutions_partial_match(parser):
    text = "Use @butter{100g} (or @margarine{}) for frying."
    expected = []
    assert parser.extract_ingredient_substitutions(text) == expected
