from rich.console import Console
from rich.traceback import install
import random
c = Console()
install()

class pswd:
    def __init__(self) -> None:
        self.number_of_words = 2
        self.numbers = 1
        self.min_word_length = 3
        self.max_word_length = 8
        self.include_symbol = True
        self.casing_style = "single"
        self.left_hand_only = False
        
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
        

    def reset_word_list(self):
        self.current_word_list = self.full_word_list
        return len(self.current_word_list)

    def generate_pswd(self):
        words = []
        for i in range(0, self.number_of_words):
            words.append(random.choice(self.current_word_list))
        
        numbers = []
        for i in range(0, self.numbers):
            numbers.append(random.randint(0, 9))
        
        c.print(words)
        c.print(numbers)


password = pswd()
#c.print(password.filter_letters(include=["a"]))
password.filter_letters(include=["a"])
password.generate_pswd()