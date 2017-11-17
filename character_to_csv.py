import csv


class CharacterToCsv:
    time_clock_interval = 48

    def __init__(self, text_file):
        with open(text_file) as text:
            content = text.read()

        rows = self.get_csv_content(content)
        with open("csv\\memestar_generated.csv") as csv_file:
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    def get_csv_content(self, content):
        rows = []
        nb_tracks = self.get_nb_tracks(content)
        self.append_header(nb_tracks, rows)
        self.append_settings_track(rows)
        self.append_notes_tracks(content, nb_tracks, rows)

    def append_header(self, nb_tracks, rows):
        header = self.generate_header(nb_tracks)
        rows.append(header)

    def append_settings_track(self, rows):
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

    def append_notes_tracks(self, content, nb_tracks, rows):
        tracks = self.get_character_tracks(content, nb_tracks)

    def get_character_tracks(self, content, nb_tracks):
        print(content)
        tracks = []
        for i in range(nb_tracks):
            tracks.append([])
        channel_counter = 0
        repeated_note = False
        time_clocks = 1
        for note in content:
            if note == '~':
                repeated_note = True
            elif note == ' ':
                # 0 -> 123
                # 1 -> 23
                # 2 -> 3
                for track in tracks:
                    if len(track) < time_clocks:
                        track.append(" ")
                channel_counter = 0
                time_clocks += 1
            else:
                if repeated_note:
                    tracks[channel_counter].append('~' + note)
                    repeated_note = False
                else:
                    tracks[channel_counter].append(note)

                channel_counter += 1
        for track in tracks:
            print(len(track))
            print(track)
        return tracks


if __name__ == '__main__':
    CharacterToCsv("txt\\memestar.txt")
