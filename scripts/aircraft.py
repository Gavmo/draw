import time
import datetime
import csv
from acicon import AcIcon

with open('../apdata/airports.csv', 'r', encoding='utf-8') as airport_raw:
    airport_csv = csv.reader(airport_raw)
    next(airport_csv)
    thedict = {}
    for row in airport_csv:
        thedict[row[13]] = (float(row[4]), float(row[5]))


class Aircraft:
    COLOR_TABLE = {
        "J": (255, 0, 0),  # Red
        "P": (0, 255, 0)   # Green
    }

    def __init__(self, dep_port, arr_port, dep_datetime, arr_datetime, debug=False, flight_type_code=None):
        self.position = (0, 0)
        self.dep_datetime = dep_datetime
        self.arr_datetime = arr_datetime
        self.active = False
        self.dep_port = thedict[dep_port]
        self.arr_port = thedict[arr_port]
        if flight_type_code is None:
            self.icon = AcIcon(Aircraft.COLOR_TABLE["J"])
        else:
            try:
                self.icon = AcIcon(Aircraft.COLOR_TABLE[flight_type_code])
            except KeyError as e:
                print(f'Flight Type code "{e}" does not exist.')
                self.icon = AcIcon(Aircraft.COLOR_TABLE["J"])
        if debug:
            print(dep_port)
            print(arr_port)
            print(self.arr_port)
            print(self.dep_port)
            print(dep_datetime)
            print(arr_datetime)

    def human_dep_date(self):
        """Return a human date for debug"""
        return datetime.datetime.utcfromtimestamp(self.dep_datetime).strftime('%Y-%m-%d %H:%M:%S')

    def progress(self, timestamp):
        if timestamp < self.dep_datetime:
            self.active = False
        else:
            self.active = True
        if self.active:
            delta_now = self.arr_datetime - timestamp
            duration = self.arr_datetime - self.dep_datetime
            try:
                return delta_now / duration
            except ZeroDivisionError as e:
                print(self.arr_datetime)
                print(self.dep_datetime)
        else:
            return False

    def is_finished(self, timestamp):
        if timestamp > self.arr_datetime:
            return True

    def update_position(self, timestamp):
        progress_ratio = self.progress(timestamp)
        if progress_ratio is not False:
            delta_lat = self.dep_port[0] - self.arr_port[0]
            prog_lat = delta_lat * progress_ratio
            delta_lon = self.dep_port[1] - self.arr_port[1]
            prog_lon = delta_lon * progress_ratio
            self.position = (prog_lat + self.arr_port[0], prog_lon + self.arr_port[1])


if __name__ == "__main__":
    ac = Aircraft('BNE', 'SYD', 1587711600, 1587717300, flight_type_code="P")
    simulated_time = 1587711600
    while simulated_time < 1587717300:
        ac.update_position(simulated_time)
        print(ac.position)
        time.sleep(1)
        simulated_time += 60

