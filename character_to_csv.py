import csv


class CharacterToCsv:
    time_clock_interval = 48

    def __init__(self, text_file):
        content = ""
        with open(text_file) as text:
            content = text.read()

        rows = self.get_csv_content(content)
        with open("csv\\memestar_generated.csv") as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    def get_csv_content(self, content):
        rows = []
        nb_tracks = self.get_nb_tracks(content)
        rows.append(self.generate_header(nb_tracks))

    def get_nb_tracks(self, content):
        content_without_repetition = content.replace('~', '')
        chords = content_without_repetition.split(" ")
        nb_tracks = len(max(chords, key=len))
        print(nb_tracks)
        return nb_tracks

    def generate_header(self, nb_tracks):
        pass
        # 0, 0, Header, 1, [nb tracks], 96


if __name__ == '__main__':
    CharacterToCsv("txt\\memestar.txt")
