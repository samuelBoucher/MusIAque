import csv

if __name__ == '__main__':
    with open('memestar.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))


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



