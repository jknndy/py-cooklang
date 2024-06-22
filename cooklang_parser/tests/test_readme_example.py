import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()

def test_parse_recipe():
    parser = CooklangParser()

    recipe_text = """
    -- This is a hearty breakfast recipe
    >> source: https://example.com
    >> time required: 1.5 hours
    Poke holes in @potatoes{2} with a fork.
    Place @bacon strips{500%g} on a baking sheet and glaze with @maple syrup{1/2%tbsp}.
    Slowly add @milk{1%litre}, keep mixing until smooth.
    Place the potatoes into a #pot and bring to a boil.
    If @Egg{} is Cooked, skip the next step.    
    Boil @eggs{2} for ~3%minutes.
"""
    parsed_recipe = parser.parse_recipe(recipe_text)

    expected = {
        'metadata': {
            'source': 'https://example.com',
        },
        'ingredients': [
            {'name': 'Egg', 'quantity': None, 'unit': None},
            {'name': 'bacon strips', 'quantity': '500', 'unit': 'g'},
            {'name': 'eggs', 'quantity': '2', 'unit': None},
            {'name': 'maple syrup', 'quantity': '1/2', 'unit': 'tbsp'},
            {'name': 'milk', 'quantity': '1', 'unit': 'litre'},
            {'name': 'potatoes', 'quantity': '2', 'unit': None},
        ],
        'cookware': ['pot'],
        'steps': [
            {
                'type': 'text', 
                'value': 'Poke holes in',
            },
            {
                'type': 'ingredient', 
                'name': 'potatoes', 
                'quantity': '2', 
                'unit': None
            },
            {
                'type': 'text', 
                'value': 'with a fork.'
            },
            {
                'type': 'text', 
                'value': 'Place',
            },
            {
                'type': 'ingredient', 
                'name': 'bacon strips', 
                'quantity': '500', 
                'unit': 'g'
            },
            {
                'type': 'text', 
                'value': 'on a baking sheet and glaze with',
            },
            {
                'type': 'ingredient', 
                'name': 'maple syrup', 
                'quantity': '1/2', 
                'unit': 'tbsp'
            },
            {
                'type': 'text', 
                'value': '.'
            },
            {
                'type': 'text', 
                'value': 'Slowly add',
            },
            {
                'type': 'ingredient', 
                'name': 'milk', 
                'quantity': '1', 
                'unit': 'litre'
            },
            {
                'type': 'text', 
                'value': ', keep mixing until smooth.'
            },
            {
                'type': 'text', 
                'value': 'Place the potatoes into a',
            },
            {
                'type': 'cookware', 
                'name': 'pot'
            },
            {
                'type': 'text', 
                'value': 'and bring to a boil.'
            },
            {
                'type': 'text', 
                'value': 'If',
            },
            {
                'type': 'ingredient', 
                'name': 'Egg', 
                'quantity': None, 
                'unit': None
            },
            {
                'type': 'text', 
                'value': 'is Cooked, skip the next step.'
            },
            {
                'type': 'text', 
                'value': 'Boil',
            },
            {
                'type': 'ingredient', 
                'name': 'eggs', 
                'quantity': '2', 
                'unit': None
            },
            {
                'type': 'text', 
                'value': 'for ~3%minutes.'
            },
        ],
        'conditions': [
            {
                'ingredient': 'Egg',
                'condition': 'Cooked',
                'action': 'skip the next step'
            }
        ],
        'comments': [
            {
                'name': 'This is a hearty breakfast recipe',
                'type': 'comment',
            },
        ],
    }
    assert parsed_recipe == expected, f"Failed. Result: {parsed_recipe}, Expected: {expected}"
