from spellchecker import SpellChecker
import re
from pathlib import Path


context = Path("./data/eng-simple_wikipedia_2021_300K-sentences.txt").read_text("utf-8")
context = re.sub('[^A-Za-z]', " ", context)
context = " ".join(context.split())
context = context.lower()

list_of_word = context.split(" ")
spell = SpellChecker()
spell.word_frequency.load_words(list_of_word)


def spell_checking(query):
    misspelled = spell.unknown(query.split(" "))
    if len(misspelled) != 0:
        return [spell.correction(x) for x in misspelled]
    return []
