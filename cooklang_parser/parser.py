import re
from .utils import parse_quantity_unit

class CooklangParser:
    def parse_recipe(self, recipe_text):
        comments = self.extract_comments(recipe_text)
        recipe_text = self.remove_comments(recipe_text)
        return {
            "metadata": self.extract_metadata(recipe_text),
            "ingredients": self.extract_ingredients(recipe_text),
            "cookware": self.extract_cookware(recipe_text),
            "steps": self.extract_steps(recipe_text),
            "timers": self.extract_timers(recipe_text),
            "conditions": self.extract_conditions(recipe_text),
            "substitutions": self.extract_ingredient_substitutions(recipe_text),
            "comments": comments,
            "images": self.extract_images(recipe_text)
        }

    def remove_comments(self, text):
        text = re.sub(r'^\s*--.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\[-.*?-\]', '', text, flags=re.DOTALL)
        return text

    def extract_comments(self, text):
        comments = []
        lines = text.split('\n')
        for line in lines:
            match = re.match(r'^\s*--\s*(.+)', line)
            if match:
                comments.append({'type': 'comment', 'name': match.group(1).strip()})
        
        block_comments = re.findall(r'\[-(.*?)\-\]', text, re.DOTALL)
        for comment in block_comments:
            comments.append({'type': 'comment', 'name': comment.strip()})
        
        return comments

    def extract_metadata(self, text):
        metadata = {}
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('>>'):
                match = re.match(r'^>>\s*(\w+)\s*:\s*(.*)$', line)
                if match:
                    key, value = match.groups()
                    metadata[key.lower()] = value.strip()
        return metadata

    def extract_ingredients(self, text):
        ingredients = []
        seen = set()
        detailed_seen = set()

        detailed_matches = re.findall(r'@([\w\s&-]+)\{([^}]*)\}', text)
        for name, details in detailed_matches:
            quantity, unit = parse_quantity_unit(details.strip())
            ingredient = {
                'name': name.strip(),
                'quantity': quantity,
                'unit': unit
            }
            ingredient_tuple = (ingredient['name'], ingredient['quantity'], ingredient['unit'])
            if ingredient_tuple not in seen:
                seen.add(ingredient_tuple)
                detailed_seen.add(ingredient['name'])
                ingredients.append(ingredient)

        simple_matches = re.findall(r'@([\w\s&-]+)\{([^}]*)\}|\b@([\w&-]+)\b', text)
        for match in simple_matches:
            name = match[0] or match[2]
            if '{' not in name.strip() and name.strip() not in detailed_seen:
                ingredient = {
                    'name': name.strip(),
                    'quantity': None,
                    'unit': None
                }
                ingredient_tuple = (ingredient['name'], ingredient['quantity'], 'unit')
                if ingredient_tuple not in seen:
                    seen.add(ingredient_tuple)
                    ingredients.append(ingredient)

        return sorted(ingredients, key=lambda x: x['name'])

    def extract_cookware(self, text):
        multi_word_cookware = re.findall(r'#([\w\s-]+)\{\}', text)
        single_word_cookware = re.findall(r'#(\w+)(?![\w\s-]*\{\})', text)

        cookware = list(dict.fromkeys(multi_word_cookware + single_word_cookware))
        return sorted(cookware)

    def extract_steps(self, text):
        steps = []
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('>>'):
                continue
            step = []
            matches = re.finditer(r'(@[\w\s-]+\{[^}]*\}|#[\w\s-]+\{\}|#[\w]+|~[\w\s-]*\{[^}]*\}|~\{[^}]*\}|~[\w\s-]*\{[\d\s%a-zA-Z°C]+\}|~[\w\s-]*[\d\s%a-zA-Z°C]+\{[^}]*\}|\+[\w\s-]+\{\})', line)
            last_end = 0
            for match in matches:
                if match.start() > last_end:
                    step.append({
                        'type': 'text',
                        'value': line[last_end:match.start()].strip()
                    })
                step.append(self.parse_step_component(match.group()))
                last_end = match.end()
            if last_end < len(line):
                step.append({
                    'type': 'text',
                    'value': line[last_end:].strip()
                })
            steps.append(step)
        return steps

    def parse_step_component(self, component):
        if component.startswith('@'):
            name, details = re.match(r'@([\w\s-]+)\{([^}]*)\}', component).groups()
            quantity, unit = parse_quantity_unit(details.strip())
            return {'type': 'ingredient', 'name': name.strip(), 'quantity': quantity, 'unit': unit}
        elif component.startswith('#'):
            name = re.match(r'#([\w\s]+)', component).group(1)
            return {'type': 'cookware', 'name': name.strip()}
        elif component.startswith('~'):
            duration_match = re.match(r'~([\w\s°-]*)\{([^}]*)\}', component)
            if duration_match:
                timer_name = duration_match.group(1).strip()
                duration = duration_match.group(2).strip()
                return {'type': 'timer', 'name': timer_name, 'duration': duration}

            duration_match = re.match(r'~\{([^}]*)\}', component)
            if duration_match:
                duration = duration_match.group(1).strip()
                return {'type': 'timer', 'duration': duration}

            raise ValueError(f"Invalid timer format: {component}")
        elif component.startswith('+'):
            name = re.match(r'\+([\w\s]+)\{\}', component).group(1)
            return {'type': 'note', 'name': name.strip()}

    def extract_timers(self, text):
        timers = re.findall(r'~([\w\s@#-]*)\{(\d+%?[a-zA-Z\s]+)\}', text)
        return timers

    def extract_conditions(self, text):
        conditions = []
        pattern = re.compile(r'If @([\w\s-]+)\{\} is ([\w\s-]+), (.*?)(?:\.|$)')
        matches = pattern.findall(text)

        for match in matches:
            ingredient, condition, action = match
            action_components = []
            for part in re.split(r'(@[\w\s-]+\{[^}]*\}|#[\w\s-]+\{\}|#[\w]+|~[\w\s-]*\{[^}]*\}|~\{[^}]*\}|\+[\w\s-]+\{\})', action):
                part = part.strip()
                if part:
                    if part.startswith(('@', '#', '~', '+')):
                        component = self.parse_step_component(part)
                        if component['type'] == 'ingredient':
                            action_components.append(component['name'])
                        elif component['type'] == 'cookware':
                            action_components.append(component['name'])
                        elif component['type'] == 'timer':
                            duration = component['duration'].replace('%', ' ')
                            action_components.append(duration)
                        elif component['type'] == 'note':
                            action_components.append(component['name'])
                    else:
                        action_components.append(part)

            action_text = ' '.join(action_components).strip()
            conditions.append({
                'ingredient': ingredient.strip(),
                'condition': condition.strip(),
                'action': action_text
            })

        return conditions

    def extract_ingredient_substitutions(self, text):
        substitutions = []
        matches = re.findall(r'@([\w\s-]+)\{(\d+[a-zA-Z]*)\} \(or @([\w\s-]+)\{(\d+[a-zA-Z]*)\}\)', text)
        for match in matches:
            primary_name, primary_details, substitute_name, substitute_details = match
            primary_quantity, primary_unit = parse_quantity_unit(primary_details.strip())
            substitute_quantity, substitute_unit = parse_quantity_unit(substitute_details.strip())
            substitutions.append({
                'primary': {'name': primary_name.strip(), 'quantity': primary_quantity, 'unit': primary_unit},
                'substitute': {'name': substitute_name.strip(), 'quantity': substitute_quantity, 'unit': substitute_unit}
            })
        return substitutions

    def extract_images(self, text):
        images = []
        image_matches = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
        for description, path in image_matches:
            images.append({'description': description.strip(), 'path': path.strip()})
        return images
