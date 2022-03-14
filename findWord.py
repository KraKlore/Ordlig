from __future__ import annotations  
from typing import List  
from collections import namedtuple
import sys
import os

correct_letter = namedtuple('correct_letter',['pos', 'letter'])

def create_correct_letter(pos: int, letter: str) -> correct_letter:
    """Create the named tuple used for searching words when the posistion is correct for the letter.

    Args:
        pos (int): position in the word, 0 is the start
        letter (str): The single letter that shall be used for the search.

    Returns:
        correct_letter: Create a numed tuple used for the search.
    """
    return correct_letter(pos, ord(letter))

def openDictionary(filename:str) -> List[str]:
    # To make sure that pyinstaller can open the dictionary when the packaged to one exe file.
    if getattr(sys, 'frozen', False):
        filename = os.path.join(sys._MEIPASS, "./"+filename)
    with open(filename, mode='r', encoding='iso-8859-1') as fp:
        dict_lan = fp.read().splitlines()
    return dict_lan

def _correct_letter_pos(words : [str], correct_letters: [correct_letter]) -> List[str]:
    if len(correct_letters) == 0 :
        return words
    result = []
    for word in words:
        for correct_letter in correct_letters:
            if ord(word[correct_letter.pos]) != correct_letter.letter:
                break
        else:
            result.append(word)
    return result

def _correct_letters(words:[str], letters:[str]) -> [str]:
    if len(letters) == 0:
        return words
    result = []
    letters = set(letters)
    for word in words:
        for letter in letters:
            if letter not in word:
                break
        else:
            result.append(word)
    return result

def _not_letters(words:[str], letters:[str]) -> List[str]:
    """Find words that does not contain the letters given and return any that does not contain these.

    Args:
        words (str]): list of words to check
        letters (str]): list of letters to check

    Returns:
        [str]: A list of words that does not contain the letters given.
    """
    if len(letters) == 0:
        return words
    result = []
    letters = set(letters)
    for word in words:
        for letter in letters:
            if letter in word:
                break
        else:
            result.append(word)
    return result

def findWords(words:List[str], correct_letters : List[correct_letter], letters : List[str], not_letters:List[str]) -> List[str]:
    # Find the words that
    words = _correct_letter_pos(words, correct_letters)
    words = _correct_letters(words, letters)
    words = _not_letters(words, not_letters)
    return words

def main() -> None:
    words = openDictionary('fem_bokstav.txt')
    correct_letters = [create_correct_letter(0,'s')]
    print(findWords(words, correct_letters, ['l','s','u'], []))


if __name__ == '__main__':
    raise SystemExit( main())
