import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()

def test_extract_metadata_basic(parser):
    text = ">> servings: 4\n>> title: Spaghetti Bolognese"
    expected = {"servings": "4", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_empty_text(parser):
    text = ""
    expected = {}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_no_metadata_lines(parser):
    text = "This is a recipe without metadata."
    expected = {}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_whitespace_lines(parser):
    text = "\n\n>> servings: 4\n\n>> title: Spaghetti Bolognese\n\n"
    expected = {"servings": "4", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_duplicate_keys(parser):
    text = ">> servings: 4\n>> servings: 6"
    expected = {"servings": "6"}  # Last occurrence should overwrite previous
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_different_cases(parser):
    text = ">> Servings: 4\n>> Title: Spaghetti Bolognese"
    expected = {"servings": "4", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_extra_whitespace(parser):
    text = ">> servings  :  4\n>> title: Spaghetti Bolognese"
    expected = {"servings": "4", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_colon_in_value(parser):
    text = ">> servings: 4\n>> title: Spaghetti: Bolognese"
    expected = {"servings": "4", "title": "Spaghetti: Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_empty_value(parser):
    text = ">> servings: \n>> title: Spaghetti Bolognese"
    expected = {"servings": "", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_special_characters(parser):
    text = ">> servings: 4\n>> title: Spaghetti Bolognese!\n>> author: Mr. & Mrs. Chef"
    expected = {"servings": "4", "title": "Spaghetti Bolognese!", "author": "Mr. & Mrs. Chef"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_no_value(parser):
    text = ">> servings:\n>> title: Spaghetti Bolognese"
    expected = {"servings": "", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata(parser):
    text = ">> servings: 4\n>> title: Spaghetti Bolognese"
    expected = {"servings": "4", "title": "Spaghetti Bolognese"}
    assert parser.extract_metadata(text) == expected

def test_extract_metadata_empty(parser):
    text = ""
    expected = {}
    assert parser.extract_metadata(text) == expected
