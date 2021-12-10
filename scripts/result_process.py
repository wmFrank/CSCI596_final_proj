import csv

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

def process(rows):
    ls0 = []
    ls1 = []
    for row in rows:
        num = float(row[1])
        if num >= 0.5:
            ls1.append(row)
        else:
            ls0.append(row)
    return ls0, ls1

def main():
    headers, rows = readcsv('hiv_best_pred.csv')
    ls0, ls1 = process(rows)
    writecsv('hiv_active_0.csv', headers, ls0)
    writecsv('hiv_active_1.csv', headers, ls1)

main()