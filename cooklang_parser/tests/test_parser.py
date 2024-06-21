import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()

# Test case to check the full parsing of a recipe including metadata, ingredients, cookware, steps, timers, conditions, and substitutions
def test_parse_recipe_full(parser):
    text = """
    >> title: Spaghetti Bolognese
    >> servings: 4
    @spaghetti{200g}
    @ground beef{300g}
    #pan
    ~{10%minutes}
    This is a test recipe with an image ![A delicious dish](images/dish.jpg)
    Cook @spaghetti{200g} in boiling water for ~{10%minutes}.
    If @spaghetti{} is cooked, drain the water.
    Use @butter{50g} (or @margarine{50g}) for frying.
    """
    expected = {
        "comments": [],
        "metadata": {"title": "Spaghetti Bolognese", "servings": "4"},
        "ingredients": [
            {"name": "butter", "quantity": "50", "unit": "g"},
            {"name": "ground beef", "quantity": "300", "unit": "g"},
            {"name": "margarine", "quantity": "50", "unit": "g"},
            {"name": "spaghetti", "quantity": "200", "unit": "g"},
            {"name": "spaghetti", "quantity": None, "unit": None},
        ],
        "cookware": ["pan"],
        "images": [{'description': 'A delicious dish', 'path': 'images/dish.jpg'}],
        "steps": [
            [
                {"type": "ingredient", "name": "spaghetti", "quantity": "200", "unit": "g"}
            ],
            [
                {"type": "ingredient", "name": "ground beef", "quantity": "300", "unit": "g"}
            ],
            [
                {"type": "cookware", "name": "pan"}
            ],
            [
                {"type": "timer", "name": "", "duration": "10%minutes"}
            ],
            [
                {"type": "text", "value": "This is a test recipe with an image ![A delicious dish](images/dish.jpg)"},
            ],
            [
                {"type": "text", "value": "Cook"},
                {"type": "ingredient", "name": "spaghetti", "quantity": "200", "unit": "g"},
                {"type": "text", "value": "in boiling water for"},
                {"type": "timer", "name": "", "duration": "10%minutes"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "spaghetti", "quantity": None, "unit": None},
                {"type": "text", "value": "is cooked, drain the water."}
            ],
            [
                {"type": "text", "value": "Use"},
                {"type": "ingredient", "name": "butter", "quantity": "50", "unit": "g"},
                {"type": "text", "value": "(or"},
                {"type": "ingredient", "name": "margarine", "quantity": "50", "unit": "g"},
                {"type": "text", "value": ") for frying."}
            ]
        ],
        "timers": [("", "10%minutes"), ("", "10%minutes")],
        "conditions": [
            {"ingredient": "spaghetti", "condition": "cooked", "action": "drain the water"}
        ],
        "substitutions": [
            {
                "primary": {"name": "butter", "quantity": "50", "unit": "g"},
                "substitute": {"name": "margarine", "quantity": "50", "unit": "g"}
            }
        ]
    }
    assert parser.parse_recipe(text) == expected

def test_complex_recipe(parser):
    text = """
    >>title: Spaghetti Carbonara
    >>servings: 4
    >>author: John Doe

    Cook @spaghetti{400g} in boiling water until al dente. 
    In a #large bowl{}, beat @eggs{4} and mix with @parmesan cheese{100g}.
    Fry @bacon{150g} in a #pan until crispy. 
    Mix @spaghetti{} with @bacon{} and pour over the @egg mixture{}.
    Season with @salt{} and @black pepper{} to taste.
    Garnish with @parsley{}.
    Serve immediately.
    """

    expected = {
        "comments": [],
        "metadata": {
            "title": "Spaghetti Carbonara",
            "servings": "4",
            "author": "John Doe"
        },
        "ingredients": [
            {"name": "bacon", "quantity": "150", "unit": "g"},
            {"name": "bacon", "quantity": None, "unit": None},
            {"name": "black pepper", "quantity": None, "unit": None},
            {"name": "egg mixture", "quantity": None, "unit": None},
            {"name": "eggs", "quantity": "4", "unit": None},
            {"name": "parmesan cheese", "quantity": "100", "unit": "g"},
            {"name": "parsley", "quantity": None, "unit": None},
            {"name": "salt", "quantity": None, "unit": None},
            {"name": "spaghetti", "quantity": "400", "unit": "g"},
            {"name": "spaghetti", "quantity": None, "unit": None}
        ],
        "cookware": ["large bowl", "pan"],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Cook"},
                {"type": "ingredient", "name": "spaghetti", "quantity": "400", "unit": "g"},
                {"type": "text", "value": "in boiling water until al dente."}
            ],
            [
                {"type": "text", "value": "In a"},
                {"type": "cookware", "name": "large bowl"},
                {"type": "text", "value": ", beat"},
                {"type": "ingredient", "name": "eggs", "quantity": "4", "unit": None},
                {"type": "text", "value": "and mix with"},
                {"type": "ingredient", "name": "parmesan cheese", "quantity": "100", "unit": "g"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "Fry"},
                {"type": "ingredient", "name": "bacon", "quantity": "150", "unit": "g"},
                {"type": "text", "value": "in a"},
                {"type": "cookware", "name": "pan"},
                {"type": "text", "value": "until crispy."}
            ],
            [
                {"type": "text", "value": "Mix"},
                {"type": "ingredient", "name": "spaghetti", "quantity": None, "unit": None},
                {"type": "text", "value": "with"},
                {"type": "ingredient", "name": "bacon", "quantity": None, "unit": None},
                {"type": "text", "value": "and pour over the"},
                {"type": "ingredient", "name": "egg mixture", "quantity": None, "unit": None},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "Season with"},
                {"type": "ingredient", "name": "salt", "quantity": None, "unit": None},
                {"type": "text", "value": "and"},
                {"type": "ingredient", "name": "black pepper", "quantity": None, "unit": None},
                {"type": "text", "value": "to taste."}
            ],
            [
                {"type": "text", "value": "Garnish with"},
                {"type": "ingredient", "name": "parsley", "quantity": None, "unit": None},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "Serve immediately."}
            ]
        ],
        "timers": [],
        "conditions": [],
        "substitutions": []
    }
    assert parser.parse_recipe(text) == expected

def test_empty_recipe(parser):
    text = ""
    expected = {
        "comments": [],
        "metadata": {},
        "ingredients": [],
        "cookware": [],
        "images": [],
        "steps": [],
        "timers": [],
        "conditions": [],
        "substitutions": []
    }
    assert parser.parse_recipe(text) == expected


def test_metadata_and_steps(parser):
    text = """
    >>title: Simple Recipe
    >>author: Anonymous

    Boil water.
    Let it cool.
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Simple Recipe",
            "author": "Anonymous"
        },
        "ingredients": [],
        "cookware": [],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Boil water."}
            ],
            [
                {"type": "text", "value": "Let it cool."}
            ]
        ],
        "timers": [],
        "conditions": [],
        "substitutions": []
    }
    assert parser.parse_recipe(text) == expected
def test_complex_recipe_with_conditions_and_substitutions(parser):
    text = """
    >>title: Fancy Omelette
    >>servings: 2

    Whisk @eggs{3} in a #bowl. 
    Cook @eggs{} in a #pan until set. 
    If @eggs{} is cooked, add @cheese{50g} (or @vegan cheese{50g}) on top. 
    If @cheese{} is melted, serve immediately.
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Fancy Omelette",
            "servings": "2"
        },
        "ingredients": [
            {"name": "cheese", "quantity": "50", "unit": "g"},
            {"name": "cheese", "quantity": None, "unit": None},
            {"name": "eggs", "quantity": "3", "unit": None},
            {"name": "eggs", "quantity": None, "unit": None},
            {"name": "vegan cheese", "quantity": "50", "unit": "g"}
        ],
        "cookware": ["bowl", "pan"],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Whisk"},
                {"type": "ingredient", "name": "eggs", "quantity": "3", "unit": None},
                {"type": "text", "value": "in a"},
                {"type": "cookware", "name": "bowl"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "Cook"},
                {"type": "ingredient", "name": "eggs", "quantity": None, "unit": None},
                {"type": "text", "value": "in a"},
                {"type": "cookware", "name": "pan"},
                {"type": "text", "value": "until set."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "eggs", "quantity": None, "unit": None},
                {"type": "text", "value": "is cooked, add"},
                {"type": "ingredient", "name": "cheese", "quantity": "50", "unit": "g"},
                {"type": "text", "value": "(or"},
                {"type": "ingredient", "name": "vegan cheese", "quantity": "50", "unit": "g"},
                {"type": "text", "value": ") on top."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "cheese", "quantity": None, "unit": None},
                {"type": "text", "value": "is melted, serve immediately."}
            ]
        ],
        "timers": [],
        "conditions": [
            {"ingredient": "eggs", "condition": "cooked", "action": "add cheese (or vegan cheese ) on top"},
            {"ingredient": "cheese", "condition": "melted", "action": "serve immediately"}
        ],
        "substitutions": [
            {
                "primary": {"name": "cheese", "quantity": "50", "unit": "g"},
                "substitute": {"name": "vegan cheese", "quantity": "50", "unit": "g"}
            }
        ]
    }
    assert parser.parse_recipe(text) == expected

def test_recipe_with_timer_and_cookware(parser):
    text = """
    >>title: Simple Tea
    >>servings: 1

    Boil @water{200ml} in a #kettle for ~{5%minutes}. 
    If @water{} is boiled, steep @tea bag{1} in it for ~{3%minutes}.
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Simple Tea",
            "servings": "1"
        },
        "ingredients": [
            {"name": "tea bag", "quantity": "1", "unit": None},
            {"name": "water", "quantity": "200", "unit": "ml"},
            {"name": "water", "quantity": None, "unit": None}
        ],
        "cookware": ["kettle"],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Boil"},
                {"type": "ingredient", "name": "water", "quantity": "200", "unit": "ml"},
                {"type": "text", "value": "in a"},
                {"type": "cookware", "name": "kettle"},
                {"type": "text", "value": "for"},
                {"type": "timer", "name": "", "duration": "5%minutes"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "water", "quantity": None, "unit": None},
                {"type": "text", "value": "is boiled, steep"},
                {"type": "ingredient", "name": "tea bag", "quantity": "1", "unit": None},
                {"type": "text", "value": "in it for"},
                {"type": "timer", "name": "", "duration": "3%minutes"},
                {"type": "text", "value": "."}
            ]
        ],
        "timers": [("", "5%minutes"), ("", "3%minutes")],
        "conditions": [
            {"ingredient": "water", "condition": "boiled", "action": "steep tea bag in it for 3 minutes"}
        ],
        "substitutions": []
    }
    assert parser.parse_recipe(text) == expected

def test_recipe_with_multiple_substitutions(parser):
    text = """
    >>title: Versatile Salad
    >>servings: 2

    Mix @lettuce{100g} with @olive oil{2tbsp} (or @canola oil{2tbsp}) and @lemon juice{1tbsp} (or @lime juice{1tbsp}).
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Versatile Salad",
            "servings": "2"
        },
        "ingredients": [
            {"name": "canola oil", "quantity": "2", "unit": "tbsp"},
            {"name": "lemon juice", "quantity": "1", "unit": "tbsp"},
            {"name": "lettuce", "quantity": "100", "unit": "g"},
            {"name": "lime juice", "quantity": "1", "unit": "tbsp"},
            {"name": "olive oil", "quantity": "2", "unit": "tbsp"}
        ],
        "cookware": [],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Mix"},
                {"type": "ingredient", "name": "lettuce", "quantity": "100", "unit": "g"},
                {"type": "text", "value": "with"},
                {"type": "ingredient", "name": "olive oil", "quantity": "2", "unit": "tbsp"},
                {"type": "text", "value": "(or"},
                {"type": "ingredient", "name": "canola oil", "quantity": "2", "unit": "tbsp"},
                {"type": "text", "value": ") and"},
                {"type": "ingredient", "name": "lemon juice", "quantity": "1", "unit": "tbsp"},
                {"type": "text", "value": "(or"},
                {"type": "ingredient", "name": "lime juice", "quantity": "1", "unit": "tbsp"},
                {"type": "text", "value": ")."}
            ]
        ],
        "timers": [],
        "conditions": [],
        "substitutions": [
            {
                "primary": {"name": "olive oil", "quantity": "2", "unit": "tbsp"},
                "substitute": {"name": "canola oil", "quantity": "2", "unit": "tbsp"}
            },
            {
                "primary": {"name": "lemon juice", "quantity": "1", "unit": "tbsp"},
                "substitute": {"name": "lime juice", "quantity": "1", "unit": "tbsp"}
            }
        ]
    }
    assert parser.parse_recipe(text) == expected

def test_recipe_with_multiple_conditions(parser):
    text = """
    >>title: Complicated Recipe
    >>servings: 4

    If @ingredient1{} is ready, do something. 
    If @ingredient2{} is done, do something else.
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Complicated Recipe",
            "servings": "4"
        },
        "ingredients": [
            {"name": "ingredient1", "quantity": None, "unit": None},
            {"name": "ingredient2", "quantity": None, "unit": None}
        ],
        "cookware": [],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "ingredient1", "quantity": None, "unit": None},
                {"type": "text", "value": "is ready, do something."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "ingredient2", "quantity": None, "unit": None},
                {"type": "text", "value": "is done, do something else."}
            ]
        ],
        "timers": [],
        "conditions": [
            {"ingredient": "ingredient1", "condition": "ready", "action": "do something"},
            {"ingredient": "ingredient2", "condition": "done", "action": "do something else"}
        ],
        "substitutions": []
    }
    assert parser.parse_recipe(text) == expected

def test_recipe_with_conditions_substitutions_and_timers(parser):
    text = """
    >>title: Full-Featured Recipe
    >>servings: 2

    Cook @rice{200g} in water for ~{15%minutes}. 
    If @rice{} is cooked, let it rest for ~{5%minutes}. 
    Use @butter{20g} (or @oil{20g}) for flavor.
    """
    expected = {
        "comments": [],
        "metadata": {
            "title": "Full-Featured Recipe",
            "servings": "2"
        },
        "ingredients": [
            {"name": "butter", "quantity": "20", "unit": "g"},
            {"name": "oil", "quantity": "20", "unit": "g"},
            {"name": "rice", "quantity": "200", "unit": "g"},
            {"name": "rice", "quantity": None, "unit": None}
        ],
        "cookware": [],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "Cook"},
                {"type": "ingredient", "name": "rice", "quantity": "200", "unit": "g"},
                {"type": "text", "value": "in water for"},
                {"type": "timer", "name": "", "duration": "15%minutes"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "rice", "quantity": None, "unit": None},
                {"type": "text", "value": "is cooked, let it rest for"},
                {"type": "timer", "name": "", "duration": "5%minutes"},
                {"type": "text", "value": "."}
            ],
            [
                {"type": "text", "value": "Use"},
                {"type": "ingredient", "name": "butter", "quantity": "20", "unit": "g"},
                {"type": "text", "value": "(or"},
                {"type": "ingredient", "name": "oil", "quantity": "20", "unit": "g"},
                {"type": "text", "value": ") for flavor."}
            ]
        ],
        "timers": [("", "15%minutes"), ("", "5%minutes")],
        "conditions": [
            {"ingredient": "rice", "condition": "cooked", "action": "let it rest for 5 minutes"}
        ],
        "substitutions": [
            {
                "primary": {"name": "butter", "quantity": "20", "unit": "g"},
                "substitute": {"name": "oil", "quantity": "20", "unit": "g"}
            }
        ]
    }
    assert parser.parse_recipe(text) == expected

def test_recipe_with_nested_conditions(parser):
    text = """
    >>title: Nested Conditions Recipe
    >>servings: 3
    -- consider it
    If @chicken{} is marinated, cook it. 
    If @chicken{} is cooked, shred it.
    If @shredded chicken{} is ready, use it in tacos.
    """
    expected = {
        "metadata": {
            "title": "Nested Conditions Recipe",
            "servings": "3"
        },
        "comments": [
            {'type': 'comment', 'name': 'consider it'}
        ],
        "ingredients": [
            {"name": "chicken", "quantity": None, "unit": None},
            {"name": "shredded chicken", "quantity": None, "unit": None}
        ],
        "cookware": [],
        "images": [],
        "steps": [
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "chicken", "quantity": None, "unit": None},
                {"type": "text", "value": "is marinated, cook it."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "chicken", "quantity": None, "unit": None},
                {"type": "text", "value": "is cooked, shred it."}
            ],
            [
                {"type": "text", "value": "If"},
                {"type": "ingredient", "name": "shredded chicken", "quantity": None, "unit": None},
                {"type": "text", "value": "is ready, use it in tacos."}
            ]
        ],
        "timers": [],
        "conditions": [
            {"ingredient": "chicken", "condition": "marinated", "action": "cook it"},
            {"ingredient": "chicken", "condition": "cooked", "action": "shred it"},
            {"ingredient": "shredded chicken", "condition": "ready", "action": "use it in tacos"}
        ],
        "substitutions": []
    }
    result = parser.parse_recipe(text)
    assert result == expected, f"Failed. Result: {result['comments']}, Expected: {expected['comments']}"

def test_custom(parser):
    text = """
    -- This is a comment
    >> source: https://example.com
    >> time required: 1.5 hours
    Poke holes in @potato{2}.
    Place @bacon strips{1%kg} on a baking sheet and glaze with @syrup{1/2%tbsp}.
    Slowly add @milk{4%cup} [- TODO change units to litres -], keep mixing
    Place the potatoes into a #pot.
    Boil @eggs{2} for ~eggs{3%minutes}.
    """
    expected = {
        'metadata': {
            'source': 'https://example.com',
        },
        'ingredients': [
            {'name': 'bacon strips', 'quantity': '1', 'unit': 'kg'},
            {'name': 'eggs', 'quantity': '2', 'unit': None},
            {'name': 'milk', 'quantity': '4', 'unit': 'cup'},
            {'name': 'potato', 'quantity': '2', 'unit': None},
            {'name': 'syrup', 'quantity': '1/2', 'unit': 'tbsp'},
        ],
        'cookware': ['pot'],
        'steps': [
            [
                {'type': 'text', 'value': 'Poke holes in'},
                {'type': 'ingredient', 'name': 'potato', 'quantity': '2', 'unit': None},
                {'type': 'text', 'value': '.'}
            ],
            [
                {'type': 'text', 'value': 'Place'},
                {'type': 'ingredient', 'name': 'bacon strips', 'quantity': '1', 'unit': 'kg'},
                {'type': 'text', 'value': 'on a baking sheet and glaze with'},
                {'type': 'ingredient', 'name': 'syrup', 'quantity': '1/2', 'unit': 'tbsp'},
                {'type': 'text', 'value': '.'}
            ],
            [
                {'type': 'text', 'value': 'Slowly add'},
                {'type': 'ingredient', 'name': 'milk', 'quantity': '4', 'unit': 'cup'},
                {'type': 'text', 'value': ', keep mixing'}
            ],
            [
                {'type': 'text', 'value': 'Place the potatoes into a'},
                {'type': 'cookware', 'name': 'pot'},
                {'type': 'text', 'value': '.'}
            ],
            [
                {'type': 'text', 'value': 'Boil'},
                {'type': 'ingredient', 'name': 'eggs', 'quantity': '2', 'unit': None},
                {'type': 'text', 'value': 'for'},
                {'type': 'timer', 'name': 'eggs', 'duration': '3%minutes'},
                {'type': 'text', 'value': '.'}
            ]
        ],
        'timers': [('eggs', '3%minutes')],
        'conditions': [],
        'substitutions': [],
        'comments': [{'type': 'comment', 'name': 'This is a comment'}],
        'images': []
    }
    result = parser.parse_recipe(text)
    assert result == expected, f"Failed. Result: {result['comments']}, Expected: {expected['comments']}"
