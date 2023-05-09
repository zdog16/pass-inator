from rich.console import Console
from rich.traceback import install
import argparse
import pyperclip
import passInator
install()
c = Console()


customerSettings = {
    "type": "passphrase",
    "number_of_words": [2, 3],
    "min_word_length": 2,
    "max_word_length": 5,
    "number_of_symbols": [0, 0]
    }



def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--customer', action='store_true', help='Generate A customer worthy password')
    parser.add_argument('-a', '--alphanum', action='store_true', help='Exclude Symbols')
    parser.add_argument('-p', '--passphrase', action='store_true', help='Generate a Passprase instead of a password')
    options = parser.parse_args()
    
    return options

options = get_arguments()
generator = passInator.Generator()






while True:
    if options.customer:
        generator.upload_settings(customerSettings)
        if customerSettings["type"] == "passphrase":
            password = generator.generate_passphrase()
        else:
            password = generator.generate_password()
    elif options.passphrase:
        password = generator.generate_passphrase()
    else:
        password = generator.generate_password()

    c.print(f"How about: {password}")
    if input(">>") != "":
        pyperclip.copy(password)
        c.print(f"{password} copied to clipboard")
        break
