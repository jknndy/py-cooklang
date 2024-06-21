# Py-Cooklang

Py-Cooklang is a Python project focused on working with the Cooklang markup language. The current main feature is the CooklangParser, a library for parsing recipes written in Cooklang. It extracts metadata, ingredients, cookware, steps, timers, **conditions**, ingredient substitutions, comments, and images from recipe text files.

While the parser is the main feature at the moment, the project is designed with expansion in mind. Future functionality could include a web application, command-line interface, and more.

[Join our Discord](https://discord.gg/6PfWhrbY6x)

## CooklangParser

### Features

- **Ingredients**: Extracts single-word and multi-word ingredients, including quantities and units.
- **Comments**: Supports both inline (`--`) and block (`[- -]`) comments.
- **Metadata**: Parses metadata tags such as source, meal, total prep time, and number of people served.
- **Cookware**: Identifies necessary cookware, handling both single-word and multi-word names.
- **Timers**: Extracts timers with or without names.
- **Steps**: Breaks down the recipe into individual steps, including ingredients, cookware, timers, and notes.
- **Conditions**: Supports conditional instructions (beta).
- **Ingredient Substitutions**: Identifies alternative ingredients.
- **Images**: Associates images with the recipe or specific steps.

### Installation

To install the CooklangParser, clone the repository and install the dependencies:


```bash
git clone https://github.com/yourusername/CooklangParser.git
cd CooklangParser
pip install -r requirements.txt
```
Usage
Here's an example of how to use CooklangParser to parse a recipe:

```python
from cooklang_parser import CooklangParser

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

print(parsed_recipe)
```

Methods
```
parse_recipe(recipe_text)
Parses the entire recipe text and returns a dictionary containing metadata, ingredients, cookware, steps, timers, conditions, substitutions, comments, and images.

remove_comments(text)
Removes comments from the recipe text.

extract_comments(text)
Extracts inline and block comments from the recipe text.

extract_metadata(text)
Extracts metadata tags from the recipe text.

extract_ingredients(text)
Extracts ingredients from the recipe text, including quantities and units.

extract_cookware(text)
Extracts necessary cookware from the recipe text.

extract_steps(text)
Extracts steps from the recipe text, including ingredients, cookware, timers, and notes.

parse_step_component(component)
Parses a component of a step, such as an ingredient, cookware, timer, or note.

extract_timers(text)
Extracts timers from the recipe text.

extract_conditions(text)
Extracts conditional instructions from the recipe text (beta).

extract_ingredient_substitutions(text)
Extracts ingredient substitutions from the recipe text.

extract_images(text)
Extracts images associated with the recipe.
```
# Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

# License
This project is licensed under the MIT License.
