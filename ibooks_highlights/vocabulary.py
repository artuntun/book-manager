from os import EX_CANTCREAT
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import List, Dict, Optional
import json
import pathlib

import wget
from pydantic import BaseModel
VOC_API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


class Word(BaseModel):
    value: str = ''
    definitions: List[Dict] = []
    phonetics: Optional[str]
    audio: Optional[str] 
    book_examples: Optional[List[str]]

    def download_audio(self, path_out: pathlib.Path):
        if self.audio:
            if not path_out.joinpath(self.value + '.mp3').exists():
                try:
                    new_path = str(path_out.joinpath(self.value + '.mp3'))
                    wget.download(self.audio, new_path)
                    self._update_audio_path(new_path)
                except ValueError:
                    raise Exception('Invalid path')

    def _update_audio_path(self, new_path: str):
        self.audio = new_path
            

def request_word_to_api(word: str) -> List:
    response = urlopen(VOC_API + word)
    payload = json.load(response)
    return payload


def process_raw_word_response(payload: List) -> Word:
    word = Word()
    word.value = payload[0]['word']
    try:
        # word.value = payload[0]['word']
        meanings = payload[0]['meanings']
        word.definitions = meanings[0]['definitions']
        if payload[0]['phonetics']:
            try:
                word.audio = payload[0]['phonetics'][0]['audio']
            except KeyError:
                word.audio = None
    except IndexError:
        pass
    return word


def request_word_info(word: str) -> Dict:
    try:
        response = request_word_to_api(word)
        word_info = process_raw_word_response(response)
    except HTTPError as e:
        if e.reason != 'Not Found':
            raise e
        word_info = Word()
        word_info.value = word
    except UnicodeEncodeError:
        word_info = Word()
        word_info.value = word
    return word_info
