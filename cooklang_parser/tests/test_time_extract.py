import pytest
from cooklang_parser.parser import CooklangParser


@pytest.fixture
def parser():
    return CooklangParser()


def test_single_timer():
    parser = CooklangParser()
    text = "Boil @eggs{2} for ~eggs{3%minutes}"
    assert parser.extract_timers(text) == [("eggs", "3%minutes")]


def test_multiple_timers():
    parser = CooklangParser()
    text = (
        "Boil @eggs{2} for ~eggs{3%minutes}, then bake @bread{1} for ~bread{20%minutes}"
    )
    assert parser.extract_timers(text) == [
        ("eggs", "3%minutes"),
        ("bread", "20%minutes"),
    ]


def test_no_timers():
    parser = CooklangParser()
    text = "Mix @flour{2%cups} and @water{1%cup}"
    assert parser.extract_timers(text) == []


def test_timer_without_name():
    parser = CooklangParser()
    text = "Wait for ~{10%minutes}"
    assert parser.extract_timers(text) == [("", "10%minutes")]


def test_timer_with_spaces_in_name():
    parser = CooklangParser()
    text = "Bake @cake{1} for ~cake baking time{45%minutes}"
    assert parser.extract_timers(text) == [("cake baking time", "45%minutes")]


def test_timer_with_hyphen_in_name():
    parser = CooklangParser()
    text = "Simmer @sauce{1} for ~low-heat{30%minutes}"
    assert parser.extract_timers(text) == [("low-heat", "30%minutes")]


def test_timer_with_uppercase_characters():
    parser = CooklangParser()
    text = "Rest @meat{1} for ~Meat{10%Minutes}"
    assert parser.extract_timers(text) == [("Meat", "10%Minutes")]


def test_timer_with_mixed_case():
    parser = CooklangParser()
    text = "Cook @soup{1} for ~SimmerTime{15%Minutes}"
    assert parser.extract_timers(text) == [("SimmerTime", "15%Minutes")]


def test_timer_with_spaces_and_hyphens():
    parser = CooklangParser()
    text = "Boil @pasta{1} for ~pasta cooking-time{8%minutes}"
    assert parser.extract_timers(text) == [("pasta cooking-time", "8%minutes")]


def test_timer_with_leading_and_trailing_spaces():
    parser = CooklangParser()
    text = "Chill @dough{1} for ~ rest time {60%minutes}"
    assert parser.extract_timers(text) == [(" rest time ", "60%minutes")]


def test_timer_with_only_duration():
    parser = CooklangParser()
    text = "Wait for ~{15%minutes} before serving"
    assert parser.extract_timers(text) == [("", "15%minutes")]


def test_timer_with_only_letters_in_duration():
    parser = CooklangParser()
    text = "Mix for ~{ten minutes}"
    assert parser.extract_timers(text) == []


def test_timer_with_numbers_and_spaces():
    parser = CooklangParser()
    text = "Cook @rice{1} for ~rice{20 minutes}"
    assert parser.extract_timers(text) == [("rice", "20 minutes")]


def test_timer_with_special_characters_in_name():
    parser = CooklangParser()
    text = "Bake @pie{1} for ~pie-time@123{30%minutes}"
    assert parser.extract_timers(text) == [("pie-time@123", "30%minutes")]


def test_timer_with_percentage_sign_in_duration():
    parser = CooklangParser()
    text = "Ferment @dough{1} for ~fermentation{12%hours}"
    assert parser.extract_timers(text) == [("fermentation", "12%hours")]
