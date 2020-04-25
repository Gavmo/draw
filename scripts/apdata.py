import csv


class apdatatest:
    def __init__(self):
        with open('../apdata/airports.csv', 'r', encoding='utf-8') as airport_raw:
            airport_csv = csv.reader(airport_raw)
            next(airport_csv)
            thedict = {}
            for row in airport_csv:
                thedict[row[13]] = (float(row[4]), float(row[5]))


if __name__ == "__main__":
    apdatatest()
