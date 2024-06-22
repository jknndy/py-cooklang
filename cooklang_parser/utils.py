import re
from fractions import Fraction


def parse_quantity_unit(details):
    possible_units = [
        "g",
        "gram",
        "grams",
        "kg",
        "kilogram",
        "kilograms",
        "mg",
        "milligram",
        "milligrams",
        "lb",
        "pound",
        "pounds",
        "oz",
        "ounce",
        "ounces",
        "cup",
        "cups",
        "tbsp",
        "tablespoon",
        "tablespoons",
        "tsp",
        "teaspoon",
        "teaspoons",
        "ml",
        "milliliter",
        "milliliters",
        "l",
        "liter",
        "liters",
        "litre",
        "litres",
    ]

    match = re.match(r"(\d+/\d+|\d+)?%?(\s*[a-zA-Z]+)?", details, re.IGNORECASE)
    if match:
        quantity, unit = match.groups()
        quantity = quantity.strip() if quantity else None
        unit = unit.strip() if unit else None
        if unit and unit.lower() not in possible_units:
            unit = None
        if quantity:
            try:
                quantity = str(Fraction(quantity))
            except ValueError:
                pass
        return quantity, unit
    return details, None
