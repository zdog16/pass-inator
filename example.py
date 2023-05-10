import argparse
import pyperclip
import passInator


customSettings = {
    "type": "passphrase",
    "number_of_words": [2, 3],
    "min_word_length": 2,
    "max_word_length": 5,
    "number_of_symbols": [0, 0],
    "numbers": [0, 0]
    }



def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--custom', action='store_true', help='Generate a password with pre-saved custom settings')
    parser.add_argument('-a', '--alphanum', action='store_true', help='Exclude Symbols')
    parser.add_argument('-p', '--passphrase', action='store_true', help='Generate a Passprase instead of a password')
    options = parser.parse_args()
    
    return options

options = get_arguments()
generator = passInator.Generator()


while True:
    if options.custom:
        generator.upload_settings(customSettings)
        if customSettings["type"] == "passphrase":
            password = generator.generate_passphrase(simpleOutput=True)
        else:
            password = generator.generate_password()
    elif options.passphrase:
        password = generator.generate_passphrase(simpleOutput=True)
    else:
        password = generator.generate_password()

    print(f"How about: {password}")
    if input(">>") != "":
        pyperclip.copy(password)
        print(f"{password} copied to clipboard")
        break
