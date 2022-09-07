from ctypes.wintypes import WORD
from rich.console import Console
from rich.traceback import install
import random
c = Console()
install()

class pswd:
    def __init__(self) -> None:
        self.number_of_words = [2, 2]
        self.numbers = [1, 2]
        self.min_word_length = 3
        self.max_word_length = 5
        self.number_of_symbols = [0, 1]
        self.use_symbol_chars = False
        self.casing_style = "single" # Options: 'single', 'CamelCase', 'none'
        self.left_hand_mode = False

        self.left_hand_chars = ["a", "s", "d", "f", "g", "q", "w", "e", "r", "t", "z", "x", "c", "v", "b"]
        self.left_hand_numbers = [1, 2, 3, 4, 5, 6]
        self.left_hand_symbols = ["!", "@", "#", "$", "%", "^"]
        self.all_symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "="]
        
        self.full_word_list = open("words.txt", "r").read().split("\n")
        self.current_word_list = self.full_word_list
        self.filter_length(self.min_word_length, self.max_word_length)

    def filter_length(self, min_length, max_length=None):
        outList = []
        for i in self.current_word_list:
            if len(i) >= min_length:
                if max_length != None:
                    if len(i) <= max_length:
                        outList.append(i)
                else:
                    outList.append(i)
        
        self.current_word_list = outList
        return len(self.current_word_list)
    
    def filter_letters(self, exclude=None, include=None):
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
            c.print("Filter Return No Results...", style="red")
        return len(self.current_word_list)
        
    def filter_left_hand(self):
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
            self.number_of_words = [2, 2]
            self.numbers = [1, 2]
            self.min_word_length = 3
            self.max_word_length = 5
            self.number_of_symbols = [0, 1]
            self.use_symbol_chars = False
            self.casing_style = "single"
            self.left_hand_mode = False

        elif strength == "low":
            self.number_of_words = 2
            self.numbers = [0, 1]
            self.min_word_length = 2
            self.max_word_length = 4
            self.number_of_symbols = [0, 1]
            self.use_symbol_chars = False
            self.casing_style = "single"
            self.left_hand_mode = False

    def generate_pswd(self):
        words = []
        words_plain = []
        for i in range(0, random.choice(self.number_of_words)):
            curWord = random.choice(self.current_word_list)
            if self.use_symbol_chars:
                words.append(self.symbol_char(curWord))
                words_plain.append(curWord)
            else:
                words.append(curWord)
        
        numbers = []
        for i in range(0, random.choice(self.numbers)):
            if self.left_hand_mode:
                numbers.append(random.randint(1, 6))
            else:
                numbers.append(random.randint(0, 9))

        symbols = []
        for i in range(0, random.choice(self.number_of_symbols)):
            if self.left_hand_mode:
                symbols.append(random.choice(self.left_hand_symbols))
            else:
                symbols.append(random.choice(self.all_symbols))
    
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
        
        return {"result": password_result, "words": words, "words_plain": words_plain, "numbers": numbers}



#####################################
########### Program Start ###########
#####################################

password = pswd()
password.casing_style = "CamelCase"
password.use_symbol_chars = True
for i in range(0, 5):
    result = password.generate_pswd()
    if result["words_plain"] != None:
        c.print(result["words_plain"])
    c.print(result["words"])
    c.print(result["result"])