from csv_to_character import CsvToCharacter
import os

if __name__ == '__main__':
    mml_content_list = []
    data = ""
    for filename in os.listdir("Data"):
        CsvToCharacter("Data\\" + filename)
