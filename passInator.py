import secrets
import base64
from typing import Any
import requests

class casingStyle:
    def __init__(self) -> None:
        self.single = "single"
        self.CamelCase = "CamelCase"
        self.none = "none"

class Generator:
    def __init__(self, words_url: str = 'https://api.github.com/repos/zdog16/pass-inator/contents/words.txt') -> None:
        # passprase settings
        self.number_of_words = [2, 2]
        self.numbers = [1, 2]
        self.min_word_length = 3
        self.max_word_length = 5
        self.number_of_symbols = [0, 1]
        self.use_symbol_chars = False
        self.casingStyles = casingStyle()
        self.casing_style = self.casingStyles.CamelCase

        # password settings
        self.password_length = 6
        self.useLowerLetters = True
        self.useUpperLetters = True
        self.useSymbols = True
        self.useNumbers = True

        # character pools
        self.LetterPool = 'abcdefghijklmnopqrstuvwxyz'
        self.numberPool = '1234567890'
        self.left_hand_mode = False
        self.left_hand_chars = 'asdfgqwertzxcvb'
        self.left_hand_numbers = '123456'
        self.left_hand_symbols = '!@#$%^'
        self.all_symbols = '!@#$%^&*()-_+='
        self.char_pool = ''
        self.generate_char_pool()
        
        # word pool
        response = requests.get(words_url)
        if response.status_code == requests.codes.ok:
            jsonResponse = response.json()
            content = base64.b64decode(jsonResponse['content'])
            jsonString = content.decode('utf-8')
            self.full_word_list = jsonString.split('\n')
        else:
            try:
                self.full_word_list = open("words.txt", "r").read().split("\n")
            except FileNotFoundError:
                raise Exception("The Words list was not found. Please connect to the internet or put the words.txt file in the same directory.")

        self.current_word_list = self.full_word_list
        self.filter_word_length(self.min_word_length, self.max_word_length)

    def filter_word_length(self, min_length, max_length=None):
        outList = []
        for i in self.current_word_list:
            if len(i) >= min_length:
                if max_length != None:
                    if len(i) <= max_length:
                        outList.append(i)
                else:
                    outList.append(i)
        
        self.current_word_list = outList
        if len(self.current_word_list) == 0:
            raise Exception("Filter Returned 0 Results")
        return len(self.current_word_list)
    
    def filter_word_letters(self, exclude=None, include=None):
        outList = []
        
        if exclude != None:
            for i in self.current_word_list:
                for j in exclude:
                    if not j in i:
                        outList.append(i)
        if include != None:
            for i in self.current_word_list:
                for j in include:
                    if j in i:
                        outList.append(i)
        
        if exclude == None and include == None:
            pass
        else:
            self.current_word_list = outList
        
        if len(self.current_word_list) == 0:
            raise Exception("Filter Returned 0 Results")

        return len(self.current_word_list)
        
    def filter_word_left_hand(self):
        self.left_hand_mode = True
        outList = []

        for i in self.current_word_list:
            good = True
            for j in i:
                if j not in self.left_hand_chars:
                    good = False
                    break
            if good:
                outList.append(i)

        self.current_word_list = outList
        return len(outList)

    def reset_word_list(self):
        self.current_word_list = self.full_word_list
        return len(self.current_word_list)

    def symbol_char(self, word):
        outWord = ""
        for char in word:
            if char == "i" or char == "l":
                outChar = "!"
            elif char == "a":
                outChar = "@"
            elif char == "s":
                outChar = "$"
            elif char == "x":
                outChar = "%"
            elif char == "c" and not self.left_hand_mode:
                outChar = "("
            elif char == "t" and not self.left_hand_mode:
                outChar = "+"
            else:
                outChar = char
            outWord += outChar
        
        return outWord
            
    def set_strength(self, strength):
        if strength == "high":
            self.number_of_words = [4, 5]
            self.numbers = [1, 2]
            self.min_word_length = 5
            self.max_word_length = 10
            self.number_of_symbols = [2, 3]
            self.use_symbol_chars = True
            self.casing_style = "CamelCase"
            self.left_hand_mode = False

        elif strength == "medium":
            self.number_of_words = [2, 3]
            self.numbers = [1, 2]
            self.min_word_length = 3
            self.max_word_length = 5
            self.number_of_symbols = [0, 1]
            self.use_symbol_chars = False
            self.casing_style = "single"
            self.left_hand_mode = False

        elif strength == "low":
            self.number_of_words = [2, 2]
            self.numbers = [0, 1]
            self.min_word_length = 2
            self.max_word_length = 4
            self.number_of_symbols = [0, 1]
            self.use_symbol_chars = False
            self.casing_style = "single"
            self.left_hand_mode = False

        self.reset_word_list()
        self.filter_word_length(self.min_word_length, self.max_word_length)

    def upload_settings(self, settings: dict) -> None:
        for key in settings:
            if key == "number_of_words":
                self.number_of_words = settings[key]
            elif key == "numbers":
                self.numbers = settings[key]
            elif key == "min_word_length":
                self.min_word_length = settings[key]
            elif key == "max_word_length":
                self.max_word_length = settings[key]
            elif key == "number_of_symbols":
                self.number_of_symbols = settings[key]
            elif key == "use_symbol_chars":
                self.use_symbol_chars = settings[key]
            elif key == "casing_style":
                self.casing_style = settings[key]
            elif key == "left_hand_mode":
                self.left_hand_mode = settings[key]
            elif key == "password_length":
                self.password_length = settings[key]
            elif key == "useLowerLetters":
                self.useLowerLetters = settings[key]
            elif key == "useUpperLetters":
                self.useUpperLetters = settings[key]
            elif key == "useSymbols":
                self.useSymbols = settings[key]
            elif key == "useNumbers":
                self.useNumbers = settings[key]

    def generate_char_pool(self):
        self.char_pool = ""
        if self.left_hand_mode:
            if self.useLowerLetters:
                self.char_pool = self.char_pool + self.left_hand_chars
            if self.useUpperLetters:
                self.char_pool = self.char_pool + self.left_hand_chars.upper()
            if self.useNumbers:
                self.char_pool = self.char_pool + self.left_hand_numbers
            if self.useSymbols:
                self.char_pool = self.char_pool + self.left_hand_symbols
        else:
            if self.useLowerLetters:
                self.char_pool = self.char_pool + self.LetterPool
            if self.useUpperLetters:
                self.char_pool = self.char_pool + self.LetterPool.upper()
            if self.useNumbers:
                self.char_pool = self.char_pool + self.numberPool
            if self.useSymbols:
                self.char_pool = self.char_pool + self.all_symbols

    def generate_passphrase(self, simpleOutput=False):
        if len(self.current_word_list) == 0:
            raise Exception("Word List is currently empty")
        
        words = []
        words_plain = []
        for i in range(0, secrets.choice(range(self.number_of_words[0], self.number_of_words[1]))):
            curWord = secrets.choice(self.current_word_list)
            if self.use_symbol_chars:
                words.append(self.symbol_char(curWord))
                words_plain.append(curWord)
            else:
                words.append(curWord)
        
        numbers = []
        for i in range(self.numbers[0], self.numbers[1]):
            if self.left_hand_mode:
                numbers.append(secrets.choice(range(1, 6)))
            else:
                numbers.append(secrets.choice(range(0, 9)))

        symbols = []
        for i in range(self.number_of_symbols[0], self.number_of_symbols[1]):
            if self.left_hand_mode:
                symbols.append(secrets.choice(self.left_hand_symbols))
            else:
                symbols.append(secrets.choice(self.all_symbols))
    
        if not self.left_hand_mode:
            if self.casing_style == "single":
                words[0] = words[0].capitalize()
            elif self.casing_style == "CamelCase":
                for i in words:
                    words[words.index(i)] = i.capitalize()
            elif self.casing_style == "none":
                pass

        
        password_result = ""
        for i in words:
            password_result += i
        for i in numbers:
            password_result += str(i)
        for i in symbols:
            password_result += i
        
        if simpleOutput:
            return password_result
        else:
            return {"result": password_result, "words": words, "words_plain": words_plain, "numbers": numbers}
        
    def generate_password(self) -> str:
        password = ""
        for char in range(0, self.password_length):
            password = password + secrets.choice(self.char_pool)
        return password