import os
import re


class MmlToNeuralNetwork:
    path = "Data\\"
    useless_section_string = [
        "[Settings]",
        "[3MLEEXTENSION]",
        "r1r1r1r1r1r1r1r1r1r1"
    ]

    def format_mml(self):
        mml_content_list = []
        data = ""
        for filename in os.listdir(self.path):
            mml_content_list.append(open(self.path + filename).read())

        for song in mml_content_list:
            formatted_song = ""
            song = self.remove_comments(song)
            sections = self.split_content_list(song)
            for section in sections:
                section = self.trim(section)  # enlever tous les espaces et les newlines
                if not self.is_useful(section):
                    continue
                section = self.remove_header(section)
                formatted_song += section
                formatted_song += '\n'  # on met une section par ligne

            data += formatted_song
            data += "\n"  # On sépare chaque chanson par une ligne vide

        return data

    # La conversion de MIDI en MML utilisée est le logiciel 3MLE.
    # Pendant la conversion, 3MLE ajoute des commentaires pour mieux organiser le fichier.
    # Nous n'en avons pas besoin: nous avons seulement besoin des "notes de musique".
    def remove_comments(self, song):
        song = re.sub(re.compile("/\*.*?\*/"), "",
                      song)  # Enlever tous les commentaires /* ... */
        song = re.sub(re.compile("//.*?\n"), "",
                      song)  # Enlever tous les commentaires // ...
        return song

    # Chaque section est délimitée par un en-tête entre brackets (exemple: [entete].
    # Donc, on fait un split sur le symbole '['.
    def split_content_list(self, song):
        delimiter = "["
        return [delimiter + section for section in song.split(delimiter) if section]

    def is_useful(self, section):
        for string in self.useless_section_string:
            if string in section:
                return False
        return True

    def trim(self, section):
        section = section.replace("\n", "")
        section = section.replace(" ", "")
        return section

    def remove_header(self, section):
        return re.sub(re.compile(r'\[.*\]'), "", section)


if __name__ == '__main__':
    mml_format = MmlToNeuralNetwork()
    data = mml_format.format_mml()
    data
