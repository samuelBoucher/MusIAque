class CharacterToCsv:
    time_clock_interval = 48

    def __init__(self, text_file):
        with open(text_file) as text:
            content = text.read()

        rows = self.get_csv_content(content).split('\n')
        print(rows)
        self.write_csv(rows)

    def get_csv_content(self, content):
        rows = ""
        nb_tracks = self.get_nb_tracks(content)
        rows += self.generate_header(nb_tracks)
        rows += self.generate_settings_track()
        rows += self.generate_notes_tracks(content, nb_tracks)
        rows += self.append_end_file()
        return rows

    def append_header(self, nb_tracks, rows):
        rows += self.generate_header(nb_tracks)

    @staticmethod
    def generate_header(nb_tracks):
        return "0, 0, Header, 1, " + str(nb_tracks) + ", 96 \n"

    def append_settings_track(self, rows):
        rows += self.generate_settings_track()

    @staticmethod
    def get_nb_tracks(content):
        content_without_repetition = content.replace('~', '')
        chords = content_without_repetition.split(" ")
        # + 1 pour inclure la track des settings
        nb_tracks = len(max(chords, key=len)) + 1
        return nb_tracks

    @staticmethod
    def generate_settings_track():
        return "1, 0, Start_track \n" \
               "1, 0, Time_signature, 4, 2, 24, 8 \n" \
               "1, 0, Tempo, 500000 \n" \
               "1, 0, Program_c, 1, 6 \n" \
               "1, 0, End_track \n"

    def generate_notes_tracks(self, content, nb_tracks):
        character_tracks = self.get_character_tracks(content, nb_tracks)
        csv_note_tracks = ""
        for i in range(nb_tracks):
            channel_index = i + 2
            csv_note_tracks += self.append_note_channel(channel_index, character_tracks[i])

        return csv_note_tracks

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
                continue
            elif note == ' ':
                self.fill_tracks_blanks(time_clocks, tracks)
                channel_counter = 0
                time_clocks += 1
            else:
                if repeated_note:
                    tracks[channel_counter].append('~' + note)
                else:
                    tracks[channel_counter].append(note)

                channel_counter += 1
                repeated_note = False

        self.fill_tracks_blanks(time_clocks, tracks)
        return tracks

    @staticmethod
    def fill_tracks_blanks(time_clocks, tracks):
        for track in tracks:
            if len(track) < time_clocks:
                track.append(" ")

    def append_note_channel(self, channel_index, character_track):
        return self.convert_track_to_csv(channel_index, character_track)

    def convert_track_to_csv(self, channel_index, character_track):
        csv_track = ""

        csv_track += str(channel_index) + ", 0, Start_track \n"

        time_clock = 0
        previous_character = ""
        for character in character_track:
            if character != " ":
                if '~' in character:
                    character = character.replace('~', '')
                    csv_track += self.generate_note_off_row(channel_index, previous_character, time_clock)
                    csv_track += self.generate_note_on_row(channel_index, character, time_clock)
                if character != previous_character:
                    if previous_character != "":
                        csv_track += self.generate_note_off_row(channel_index, previous_character, time_clock)
                    csv_track += self.generate_note_on_row(channel_index, character, time_clock)

            previous_character = character
            time_clock += self.time_clock_interval

        csv_track += str(channel_index) + "," + str(time_clock) + ", End_track \n"
        print(csv_track)
        return csv_track

    @staticmethod
    def generate_note_on_row(channel_index, character, time_clock):
        note_in_decimal = str(ord(character))
        track_index = channel_index - 2
        return str(channel_index) + ", " + str(time_clock) + ", Note_on_c, " + str(track_index) + ", " + \
               str(note_in_decimal) + ", 100 \n"

    @staticmethod
    def generate_note_off_row(channel_index, character, time_clock):
        note_in_decimal = str(ord(character))
        track_index = channel_index - 2
        return str(channel_index) + ", " + str(time_clock) + ", Note_off_c, " + str(track_index) + ", " + \
               str(note_in_decimal) + ", 100 \n"

    @staticmethod
    def append_end_file():
        return "0, 0, End_of_file \n"

    @staticmethod
    def write_csv(rows):
        with open("csv_result\\csv_generated.csv", 'w') as csv_file:
            for row in rows:
                csv_file.write(row)
                csv_file.write('\n')


if __name__ == '__main__':
    CharacterToCsv("txt_result\\test2.txt")
