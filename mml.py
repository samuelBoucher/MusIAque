import os


class MllFormat:
    path = "Data\\"

    def format_mml(self):
        mml_content_list = []
        for filename in os.listdir(self.path):
            mml_content_list.append(open(self.path + filename).read())

        print(mml_content_list)


if __name__ == '__main__':
    mml_format = MllFormat()
    mml_format.format_mml()

