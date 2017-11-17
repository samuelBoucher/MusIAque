import csv

import sys


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
        character_tracks = self.get_character_tracks(content, nb_tracks)
        for i in range(nb_tracks):
            channel_index = i + 2
            self.append_note_channel(channel_index, character_tracks[i], rows)

        # for character_track in character_tracks:
        #    self.append_note_channel(character_track, rows)
        
    def get_character_tracks(self, content, nb_tracks):
        print(content)
        tracks = []
        for i in range(nb_tracks):
            tracks.append([])
        channel_counter = 0

        repeated_note = False
        # note repetee pendant la duree du time_clock
        repeated_note_in_time_clock = False

        time_clocks = 1
        for note in content:
            if note == '~':
                repeated_note = True
                repeated_note_in_time_clock = True
            elif note == ' ':
                self.fill_tracks_blanks(time_clocks, tracks)
                channel_counter = 0
                time_clocks += 1
                repeated_note_in_time_clock = False
            else:
                if repeated_note:
                    i = channel_counter
                    while i < nb_tracks:
                        channel_without_spaces = [x for x in tracks[i] if x != " "]
                        channel_note = channel_without_spaces[-1]
                        if channel_note == note:
                            tracks[i].append('~' + note)
                            i = sys.maxsize
                        else:
                            i += 1
                    repeated_note = False
                else:
                    if repeated_note_in_time_clock:
                        for track in tracks:
                            if len(track) < time_clocks:
                                track.append(note)
                                break
                    else:
                        tracks[channel_counter].append(note)

                channel_counter += 1

        self.fill_tracks_blanks(time_clocks, tracks)
        return tracks

    def fill_tracks_blanks(self, time_clocks, tracks):
        for track in tracks:
            if len(track) < time_clocks:
                track.append(" ")

    def append_note_channel(self, channel_index, character_track, rows):
        csv_track = self.convert_track_to_csv(channel_index, character_track)

    def convert_track_to_csv(self, channel_index, character_track):
        csv_track = []

        csv_track.append([str(channel_index) + ',', '0,', 'Start_track'])

        time_clock = 0
        previous_character = ""
        for character in character_track:
            if character == " ":
                continue
            if '~' in character:
                csv_track.append(self.generate_note_off_row(channel_index, previous_character, time_clock))
                csv_track.append(self.generate_note_on_row(channel_index, character, time_clock))
            if character != previous_character:
                if previous_character != "":
                    csv_track.append(self.generate_note_off_row(channel_index, previous_character, time_clock))

                csv_track.append(self.generate_note_on_row(channel_index, character, time_clock))

            previous_character = character
            time_clock += self.time_clock_interval

        csv_track.append([str(channel_index) + ',', '0,', 'End_track'])
        print(csv_track)
        

    def generate_note_on_row(self, channel_index, character, time_clock):
        note_in_decimal = str(ord(character))
        track_index = channel_index - 2
        return [str(channel_index) + ',', str(time_clock) + ',', 'Note_on_c,', str(track_index) + ',',
                str(note_in_decimal) + ',', '100']

    def generate_note_off_row(self, channel_index, character, time_clock):
        note_in_decimal = str(ord(character))
        track_index = channel_index - 2
        return [str(channel_index) + ',', str(time_clock) + ',', 'Note_off_c,', str(track_index) + ',',
                str(note_in_decimal) + ',', '100']


if __name__ == '__main__':
    CharacterToCsv("txt\\test.txt")
