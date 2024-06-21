import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()

def test_extract_cookware_simple_single_word(parser):
    text = "#pan"
    expected = ["pan"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_simple_multi_word(parser):
    text = "#deep pan{}"
    expected = ["deep pan"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_multiple_single_word(parser):
    text = "#pan #pot #skillet"
    expected = ["pan", "pot", "skillet"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_multiple_multi_word(parser):
    text = "#deep pan{} #electric blender{} #cast iron skillet{}"
    expected = ["cast iron skillet", "deep pan", "electric blender"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_mixed_single_and_multi_word(parser):
    text = "#pan #deep pan{} #pot #cast iron skillet{}"
    expected = ["cast iron skillet", "deep pan", "pan", "pot"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_with_text_between(parser):
    text = "Use a #pan for this recipe. You will also need a #deep pan{} and a #pot."
    expected = ["deep pan", "pan", "pot"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_repeated_items(parser):
    text = "#pan #pan #deep pan{} #deep pan{}"
    expected = ["deep pan", "pan"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_with_special_characters(parser):
    text = "Prepare with a #pan, then transfer to a #baking sheet{}. Avoid using a #non-stick pan{}."
    expected = ["baking sheet", "non-stick pan", "pan"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_with_numbers(parser):
    text = "Use a #pan, #2-quart pot{}, and #12-inch skillet{} for this recipe."
    expected = ["12-inch skillet", "2-quart pot", "pan"]
    assert parser.extract_cookware(text) == expected

def test_extract_cookware_edge_case_no_matches(parser):
    text = "There are no cookware items mentioned here."
    expected = []
    assert parser.extract_cookware(text) == expected
