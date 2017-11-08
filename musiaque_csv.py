# pour transformer des nombres en ascii: chr(nombre)
# inverse: ord(caractere)

# ascii: enlever les caracteres 0 a 32 pcq impossible a ecrire dans txt

# importer csv
# separer en lignes

# trouver time signature

# prendre note_on -> tableau
# prendre note_off -> tableau

# pour chaque time clock (voir combien dans time signature):
# pour chaque note_on:
# print la note
# si note encore presente sans note off au prochain time clock:
# print _ (pour la liaison)
import csv
from operator import itemgetter

class MusiaqueCsv:
    note_labels = [
        "Note_on_c,",
        "Note_off_c,"
    ]

    def __init__(self, file):
        with open(file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            rows = self.get_rows(spamreader)
            time_separation = int(self.get_time_separation(rows))
            notes_array = self.get_notes_array(rows)
            characters = self.convert_notes_to_characters(notes_array, time_separation)
            print(characters)

    def get_rows(self, spamreader):
        rows = []
        for row in spamreader:
            rows.append(row)

        return rows

    # exemple de ligne Time_signature en csv
    # L'unité de temps est au dernier item du tableau
    # ['1,', '0,', 'Time_signature,', '4,', '2,', '24,', '8']
    def get_time_separation(self, rows):
        time_signature_row = []
        for row in rows:
            if "Time_signature," in row:
                time_signature_row = row
                break

        return time_signature_row[6]

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
                        # notes_to_be_played.remove(note)
                        notes_playing.append(note)
                    elif note[2] == "Note_off_c,":
                        for note_playing in notes_playing:
                            if self.notes_are_equal(note, note_playing):
                                notes_removed.append(note_playing)
                                notes_playing.remove(note_playing)

            for note in notes_playing:
                for note_removed in notes_removed:
                    if self.notes_are_equal(note, note_removed):
                        characters += 'é'
                characters += chr(int(note[4][:-1]))

            characters += " "
            time_clock += time_separation

        return characters

    def notes_are_equal(self, note1, note2):
        return note1[3] == note2[3] and note1[4] == note2[4]


if __name__ == '__main__':
    MusiaqueCsv('memestar.csv')


