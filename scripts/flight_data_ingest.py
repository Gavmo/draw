import re
import datetime
import pandas

from aircraft import Aircraft


class FlightData:
    def __init__(self, path, fromdate=None):
        self.flex_start = 0
        self.flex_end = 0
        date_regexp = re.compile(r'\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{1,2}')
        self.aclist = []
        import pandas as pd
        df = pd.read_csv(path, sep=',', header=0)
        df["ACTUAL_ARRIVAL_DT"] = pandas.to_datetime(df["ACTUAL_ARRIVAL_DT"], dayfirst=True)
        df["ACTUAL_DEPARTURE_DT"] = pandas.to_datetime(df["ACTUAL_DEPARTURE_DT"], dayfirst=True)
        arr = df.sort_values(by="ACTUAL_DEPARTURE_DT")
        for row in arr.values:
            if 'XXX' in row[7:8]:
                continue
            if row[3] == row[4]:
                continue
            if fromdate is not None:
                if row[3].value // 10 ** 9 < datetime.datetime.strptime(fromdate, "%d/%m/%Y").timestamp():
                    continue
            self.aclist.append(Aircraft(row[8],
                                        row[7],
                                        row[3].value // 10 ** 9,
                                        row[4].value // 10 ** 9,
                                        debug=False,
                                        flight_type_code="P")
                               )
            if self.flex_start == 0:
                self.flex_start = row[3].value // 10 ** 9
                self.flex_end = row[4].value // 10 ** 9
            else:
                if row[3].value // 10 ** 9 < self.flex_start:
                    self.flex_start = row[3].value // 10 ** 9
                if row[4].value // 10 ** 9 > self.flex_end:
                    self.flex_end = row[4].value // 10 ** 9


if __name__ == "__main__":
    a = FlightData('../flight_data/a_years_worth.csv')
    print(len(a.aclist))
    # for each in a.aclist:
    #     print(each.arr_datetime)
