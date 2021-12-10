import csv
import random
print("hello")

def readcsv(file):
    f = open(file, 'r')
    f_csv = csv.reader(f)
    headers = next(f_csv)
    rows = list(f_csv)
    f.close()
    return headers, rows

def writecsv(file, headers, rows):
    f = open(file, 'w', newline='')
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    f.close()

def main():
    headers, rows = readcsv('hiv.csv')
    rows = random.sample(rows, 11000)
    writecsv('hiv_train.csv', headers, rows[:10000])
    writecsv('hiv_test.csv', headers, rows[-1000:])

main()