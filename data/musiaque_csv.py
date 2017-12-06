from csv_to_character import CsvToCharacter
import os

if __name__ == '__main__':
    mml_content_list = []
    data = ""
    for filename in os.listdir("csv_data"):
        csv_to_character = CsvToCharacter()
        data += csv_to_character.convert("csv_data\\" + filename)

        with open("ascii_data\\ascii_data.txt", 'w') as txt_data:
            txt_data.write(data)

