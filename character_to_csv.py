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
        header = self.generate_header(nb_tracks)
        rows.append(header)
        settings_tracks = self.generate_settings_track()
        for setting_row in settings_tracks:
            rows.append(setting_row)

    def get_nb_tracks(self, content):
        content_without_repetition = content.replace('~', '')
        chords = content_without_repetition.split(" ")
        nb_tracks = len(max(chords, key=len))
        return nb_tracks

    def generate_header(self, nb_tracks):
        return ['0,', '0,', 'Header,', '1,', str(nb_tracks) + ',', '96']

    def generate_settings_track(self):
        return [
            ['1,', '0,', 'Start_track'],
            ['1,', '0,', 'Time_signature,', '4,', '2,', '24,', '8'],
            ['1,', '0,', 'Tempo,', '500000'],
            ['1,', '0,', 'Program_c,', '1,', '6'],
            ['1,', '0,', 'End_track']
        ]


if __name__ == '__main__':
    CharacterToCsv("txt\\memestar.txt")
