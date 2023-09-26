import csv


columns =['Pair','Price','High','Low']

with open('datos_limpios.csv') as file:
    csv_reader = csv.DictReader(file, delimiter=',')

    for row in csv_reader:
        print(row)
