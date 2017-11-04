import os
import re


class MllFormat:
    path = "Data\\"
    useless_section_header = [
        "[Settings]",
        "[3MLE EXTENSION]"
    ]

    def format_mml(self):
        mml_content_list = []
        for filename in os.listdir(self.path):
            mml_content_list.append(open(self.path + filename).read())

        for content in mml_content_list:
            content = self.remove_comments(content)
            sections = self.split_content_list(content)
            sections = self.remove_useless_sections(sections)
            sections

    # La conversion de MIDI en MML utilisée est le logiciel 3MLE.
    # Pendant la conversion, 3MLE ajoute des commentaires pour mieux organiser le fichier.
    # Nous n'en avons pas besoin: nous avons seulement besoin des "notes de musique".
    def remove_comments(self, content):
        content = re.sub(re.compile("/\*.*?\*/"), "",
                         content)  # Enlever tous les commentaires /* ... */
        content = re.sub(re.compile("//.*?\n"), "",
                         content)  # Enlever tous les commentaires // ...
        return content

    # Chaque section est délimitée par un en-tête entre brackets (exemple: [entete].
    # Donc, on fait un split sur le symbole '['.
    def split_content_list(self, content):
        delimiter = "["
        return [delimiter+section for section in content.split(delimiter) if section]

    def remove_useless_sections(self, sections):
        valid_sections = []
        for section in sections:
            useless_header = False

            for header in self.useless_section_header:
                if section.startswith(header):
                    useless_header = True

            if useless_header:
                continue

            valid_sections.append(section)

        return valid_sections


if __name__ == '__main__':
    mml_format = MllFormat()
    mml_format.format_mml()
