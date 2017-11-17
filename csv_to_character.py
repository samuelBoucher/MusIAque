import csv
import sys
from operator import itemgetter


class CsvToCharacter:
    note_labels = [
        "Note_on_c,",
        "Note_off_c,"
    ]

    def __init__(self, file):
        with open(file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rows = self.get_rows(spamreader)
            notes_array = self.get_notes_array(rows)
            time_separation = int(self.get_time_separation(notes_array))
            characters = self.convert_notes_to_characters(notes_array, time_separation)
            # characters = self.convert_notes_to_characters(notes_array, 12)
            print(characters)

    def get_rows(self, spamreader):
        rows = []
        for row in spamreader:
            rows.append(row)

        return rows

    def get_time_separation(self, notes_array):
        # plus petite difference entre les time clocks
        smaller_time_separation = sys.maxsize
        for i in range(len(notes_array)):
            current_time_clock = notes_array[i][1]

            try:
                next_time_clock = notes_array[i+1][1]
            except IndexError:
                break

            time_separation = next_time_clock - current_time_clock
            if time_separation == 0:
                continue
            if time_separation < smaller_time_separation:
                smaller_time_separation = time_separation

        return smaller_time_separation

    def get_notes_array(self, rows):
        notes_array = []
        for row in rows:
            for label in self.note_labels:
                if label in row:
                    notes_array.append(row)

        return self.sort_notes_array(notes_array)

    def sort_notes_array(self, notes_array):
        for note in notes_array:
            note[1] = int(note[1][:-1])

        return sorted(notes_array, key=itemgetter(1))

    def convert_notes_to_characters(self, notes_array, time_separation):
        notes_to_be_played = notes_array
        first_clock = notes_to_be_played[0][1]
        last_clock = notes_to_be_played[-1][1]
        characters = ""
        time_clock = first_clock
        notes_playing = []
        while time_clock <= last_clock:
            notes_removed = []
            for note in notes_to_be_played:
                if note[1] > time_clock:
                    break
                if note[1] == time_clock:
                    if note[2] == "Note_on_c,":
                        notes_playing.append(note)
                    elif note[2] == "Note_off_c,":
                        for note_playing in notes_playing:
                            if self.notes_are_equal(note, note_playing):
                                notes_removed.append(note_playing)
                                notes_playing.remove(note_playing)

            for note in notes_playing:
                for note_removed in notes_removed:
                    if self.notes_are_equal(note, note_removed):
                        characters += '~'
                characters += chr(int(note[4][:-1]))

            characters += " "
            time_clock += time_separation

        return characters

    def notes_are_equal(self, note1, note2):
        return note1[3] == note2[3] and note1[4] == note2[4]


if __name__ == '__main__':
    CsvToCharacter('memestar.csv')


