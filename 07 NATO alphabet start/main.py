from pathlib import Path
import pandas

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR/"nato_phonetic_alphabet.csv"

data = pandas.read_csv(file_path)

# data = pandas.read_csv(r"D:\python code Udemy\python\NATO-alphabet-start\nato_phonetic_alphabet.csv")

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

# TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}

formated_dict = {row.letter: row.code for (index, row) in data.iterrows()}
# print(formated_dict)
#TODO 2. Create a list of the phonetic code words from a word that the user inputs.



def generate_phonetic():
    word = input("enter a word: ").upper()
    try:
        output_list = [formated_dict[letter] for letter in word]

    except KeyError:
        print("please enter a valid input !")
        generate_phonetic()
    else:
        print(output_list)

generate_phonetic()