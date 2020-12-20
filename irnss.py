import csv

SOURCE="./RNBB_L5.csv"

with open(SOURCE,'rt')as f:
    data = csv.DictReader(f)
    for row in data:
        row_list = row['Raw nav bits'].split(':')
        row_296_bit=str()
        for _ in row_list:
            if _.strip().isdecimal():
                #print(F"{int(_.strip()):08b}")
                row_296_bit+=F"{int(_.strip()):08b}"
        print(row_296_bit)
