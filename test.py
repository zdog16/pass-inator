
from rich.traceback import install
from rich.console import Console
from generator import pswd_generator
install()
c = Console()


password = pswd_generator()
password.filter_length(15)
password.filter_left_hand()
password.filter_letters(exclude=['a', 'e', 'i', 'o', 'u', 'm', 'n', 't'])
password.generate_pswd()