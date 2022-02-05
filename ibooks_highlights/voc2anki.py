from typing import List
from copy import copy
import pathlib

import genanki
from ibooks_highlights.vocabulary import Word
from ibooks_highlights.models import Book

class CardTemplates:
    BASIC_MODEL = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])


def generate_flashcards(book: Book, words: List[Word], with_audio: bool) -> None:
    my_deck = genanki.Deck(
        2059400110,
        'Vocabulary: ' + book.title)
    my_package = genanki.Package(my_deck)
    if with_audio:
        my_package.media_files = [word.audio for word in words if word.audio]
    
    templates = CardTemplates()

    for word in words:
        word_flashcards = generate_flashcards_from_word(word, templates, with_audio)
        for fs in word_flashcards:
            my_deck.add_note(fs)

    genanki.Package(my_deck).write_to_file(
        './Vocabulary_' + book.title + '.apkg')


def generate_flashcards_from_word(word: Word, templates: CardTemplates, with_audio: bool = False) -> List[genanki.Note]:
    fcs = []
    definitions = [definition['definition'] for definition in word.definitions]
    fcs.append(generate_definition_fc(word.value, definitions, templates.BASIC_MODEL))
    if word.audio and with_audio:
        fcs.append(generate_audio_fc(word.value, word.audio, templates.BASIC_MODEL))
    for book_example in word.book_examples:
        fcs.append(generate_book_quote_fc(word.value, book_example, templates.BASIC_MODEL))
    for definition in word.definitions:
        if 'synonyms' in definition:
            fcs.append(generate_synonyms_fc(word.value, definition['synonyms'], definition['definition'], templates.BASIC_MODEL))
        if 'example' in definition:
            fcs.append(generate_example_fc(word.value, definition['example'], definition['definition'], templates.BASIC_MODEL))
    return fcs


def generate_definition_fc(word: str, definitions: List[str], model: genanki.Model) -> genanki.Note:
    question = '<h2>' + word + '</h2> ' + 'means..' 
    answer = '<ol>'
    for defnition in definitions:
        answer += ('<li>' + defnition + '</li>')
    answer += '</ol>'
    return genanki.Note(
        model=model,
        fields=[question, answer]
    )


def generate_audio_fc(word: str, audio: str, model: genanki.Model) -> genanki.Note:
    question = '<h2>' + word + '</h2> ' + 'sounds like...' 
    answer = '[sound:' + audio + ']'
    return genanki.Note(
        model=model,
        fields=[question, answer]
    )


def generate_synonyms_fc(word: str, synonyms: List[str], definition: str, model: genanki.Model) -> genanki.Note:
    question = '<i>'
    for synonym in synonyms:
        question += (synonym + ', ')
    question = question[: -2] 
    question += '</i>'
    question += ' are synonyms of...'
    answer = '<h3>' + word + '</h3><br>'
    answer += definition

    return genanki.Note(
        model=model,
        fields=[question, answer]
    )


def generate_example_fc(word: str, example: str, definition: str, model: genanki.Model) -> genanki.Note:
    question = '<i>' + copy(example) + '</i>'
    question = question.replace(word, '<b>' + word + '</b>')
    question += ('<br><br><b>' + word + '</b> int this context means..')
    answer = copy(definition)
    return genanki.Note(
        model=model,
        fields=[question, answer]
    )


def generate_book_quote_fc(word: str, example: str, model: genanki.Model) -> genanki.Note:
    question = '<i>' + copy(example) + '</i><br><br>' + 'book quote'
    question = question.replace(word, '_' * len(word))
    answer = copy(example)
    answer = answer.replace(word, '<b>' + word + '</b>')
    return genanki.Note(
        model=model,
        fields=[question, answer]
    )

