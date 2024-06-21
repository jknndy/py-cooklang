import pytest
from cooklang_parser.utils import parse_quantity_unit

# Test with integers
def test_parse_quantity_unit_integer_2():
    assert parse_quantity_unit('2') == ('2', None)

def test_parse_quantity_unit_integer_3cup():
    assert parse_quantity_unit('3cup') == ('3', 'cup')

def test_parse_quantity_unit_integer_4tbsp():
    assert parse_quantity_unit('4tbsp') == ('4', 'tbsp')

def test_parse_quantity_unit_integer_5kg():
    assert parse_quantity_unit('5kg') == ('5', 'kg')

def test_parse_quantity_unit_integer_6litres():
    assert parse_quantity_unit('6litres') == ('6', 'litres')

# Test with fractions
def test_parse_quantity_unit_fraction_1_2cup():
    assert parse_quantity_unit('1/2cup') == ('1/2', 'cup')

def test_parse_quantity_unit_fraction_3_4tbsp():
    assert parse_quantity_unit('3/4tbsp') == ('3/4', 'tbsp')

def test_parse_quantity_unit_fraction_2_3kg():
    assert parse_quantity_unit('2/3kg') == ('2/3', 'kg')

def test_parse_quantity_unit_fraction_1_4litres():
    assert parse_quantity_unit('1/4litres') == ('1/4', 'litres')

# Test with invalid units
def test_parse_quantity_unit_invalid_1invalid():
    assert parse_quantity_unit('1invalid') == ('1', None)

def test_parse_quantity_unit_invalid_1_2invalid():
    assert parse_quantity_unit('1/2invalid') == ('1/2', None)

def test_parse_quantity_unit_invalid_3unknown():
    assert parse_quantity_unit('3unknown') == ('3', None)

# Test with missing quantity
def test_parse_quantity_unit_missing_quantity_cup():
    assert parse_quantity_unit('cup') == (None, 'cup')

def test_parse_quantity_unit_missing_quantity_tbsp():
    assert parse_quantity_unit('tbsp') == (None, 'tbsp')

def test_parse_quantity_unit_missing_quantity_kg():
    assert parse_quantity_unit('kg') == (None, 'kg')

# Test with mixed cases
def test_parse_quantity_unit_mixed_case_1CUP():
    assert parse_quantity_unit('1CUP') == ('1', 'CUP')

def test_parse_quantity_unit_mixed_case_2Tbsp():
    assert parse_quantity_unit('2Tbsp') == ('2', 'Tbsp')

def test_parse_quantity_unit_mixed_case_3Kg():
    assert parse_quantity_unit('3Kg') == ('3', 'Kg')

# Test with space
def test_parse_quantity_unit_space_1_cup():
    assert parse_quantity_unit('1 cup') == ('1', 'cup')

def test_parse_quantity_unit_space_1_2_tbsp():
    assert parse_quantity_unit('1/2 tbsp') == ('1/2', 'tbsp')

def test_parse_quantity_unit_percent_1_cup():
        assert parse_quantity_unit('1%cup') == ('1', 'cup')

def test_parse_quantity_unit_percent_1_2_tbsp():
    assert parse_quantity_unit('1/2%tbsp') == ('1/2', 'tbsp')

def test_parse_quantity_unit_percent_3_kg():
    assert parse_quantity_unit('3%kg') == ('3', 'kg')

def test_parse_quantity_unit_percent_4_litres():
    assert parse_quantity_unit('4%litres') == ('4', 'litres')

