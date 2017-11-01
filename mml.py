import os
import re


class MllFormat:
    path = "Data\\"

    def format_mml(self):
        mml_content_list = []
        for filename in os.listdir(self.path):
            mml_content_list.append(open(self.path + filename).read())

        self.remove_comments(mml_content_list)

    # La conversion de MIDI en MML utilisée est le logiciel 3MLE.
    # Pendant la conversion, 3MLE ajoute des commentaires pour mieux organiser le fichier.
    # Nous n'en avons pas besoin: nous avons seulement besoin des "notes de musique".
    def remove_comments(self, mml_content_list):
        for content in mml_content_list:
            content = re.sub(re.compile("/\*.*?\*/"), "",
                             content)  # Enlever tous les commentaires /* ... */
            content = re.sub(re.compile("//.*?\n"), "",
                             content)  # Enlever tous les commentaires //
            print(content)
            return content


if __name__ == '__main__':
    mml_format = MllFormat()
    mml_format.format_mml()

