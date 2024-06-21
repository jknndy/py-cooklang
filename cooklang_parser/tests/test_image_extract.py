import pytest
from cooklang_parser.parser import CooklangParser

@pytest.fixture
def parser():
    return CooklangParser()

def test_extract_images_single():
    parser = CooklangParser()
    text = "This is a test recipe with an image ![A delicious dish](images/dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'A delicious dish', 'path': 'images/dish.jpg'}]

def test_extract_images_multiple():
    parser = CooklangParser()
    text = ("This is a test recipe with multiple images "
            "![First dish](images/first.jpg) and ![Second dish](images/second.jpg)")
    result = parser.extract_images(text)
    assert result == [{'description': 'First dish', 'path': 'images/first.jpg'},
                      {'description': 'Second dish', 'path': 'images/second.jpg'}]

def test_extract_images_no_images():
    parser = CooklangParser()
    text = "This is a test recipe with no images."
    result = parser.extract_images(text)
    assert result == []

def test_extract_images_empty_description():
    parser = CooklangParser()
    text = "Image with empty description ![](images/dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': '', 'path': 'images/dish.jpg'}]

def test_extract_images_spaces_in_path():
    parser = CooklangParser()
    text = "Image with spaces in path ![Dish](images/my dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish', 'path': 'images/my dish.jpg'}]

def test_extract_images_special_characters_in_path():
    parser = CooklangParser()
    text = "Image with special characters ![Dish](images/dish@home.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish', 'path': 'images/dish@home.jpg'}]

def test_extract_images_relative_path():
    parser = CooklangParser()
    text = "Relative path image ![Dish](../images/dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish', 'path': '../images/dish.jpg'}]

def test_extract_images_url():
    parser = CooklangParser()
    text = "Image from URL ![Dish](http://example.com/images/dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish', 'path': 'http://example.com/images/dish.jpg'}]

def test_extract_images_with_metadata():
    parser = CooklangParser()
    text = "Recipe with metadata and image\n>> title: Test Recipe\n![Dish](images/dish.jpg)"
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish', 'path': 'images/dish.jpg'}]

def test_extract_images_mixed_content():
    parser = CooklangParser()
    text = ("Recipe with mixed content\n"
            "![Dish1](images/dish1.jpg) some text\n"
            "![Dish2](images/dish2.jpg)\n"
            "More text\n![Dish3](images/dish3.jpg)")
    result = parser.extract_images(text)
    assert result == [{'description': 'Dish1', 'path': 'images/dish1.jpg'},
                      {'description': 'Dish2', 'path': 'images/dish2.jpg'},
                      {'description': 'Dish3', 'path': 'images/dish3.jpg'}]
