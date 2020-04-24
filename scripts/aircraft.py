import json
import time
import csv


class Aircraft:
    def __init__(self, dep_port, arr_port, dep_datetime, arr_datetime):
        self.position = (0, 0)
        self.dep_datetime = dep_datetime
        self.arr_datetime = arr_datetime
        # with open('../apdata/airports.json', 'r') as rawjson:
        #     ap = json.load(rawjson)
        #     self.dep_port = (ap[dep_port]['lat'], ap[dep_port]['lon'])
        #     self.arr_port = (ap[arr_port]['lat'], ap[arr_port]['lon'])
        #     self.position = self.dep_port
        with open('../apdata/airports.csv', 'r', encoding='utf-8') as airport_raw:
            airport_csv = csv.reader(airport_raw)
            potential_dep = []
            potential_arr = []
            for row in airport_csv:
                # print(row)
                if row[13] == dep_port:
                    potential_dep.append(row)
                    print(row)
                if row[13] == arr_port:
                    potential_arr.append(row)
            if len(potential_arr) > 0:
                for each in potential_arr:
                    if each[8] == 'AU':
                        self.arr_port = (float(each[4]), float(each[5]))
                        break
            if len(potential_dep) > 0:
                for each in potential_dep:
                    if each[8] == 'AU':
                        self.dep_port = (float(each[4]), float(each[5]))
                        break

    def progress(self, timestamp):
        delta_now = self.arr_datetime - timestamp
        duration = self.arr_datetime - self.dep_datetime
        return delta_now / duration

    def update_position(self, timestamp):
        progress_ratio = self.progress(timestamp)
        delta_lat = self.dep_port[0] - self.arr_port[0]
        prog_lat = delta_lat * progress_ratio
        delta_lon = self.dep_port[1] - self.arr_port[1]
        prog_lon = delta_lon * progress_ratio
        self.position = (prog_lat + self.arr_port[0], prog_lon + self.arr_port[1])


if __name__ == "__main__":
    ac = Aircraft('YBBN', 'YSSY', 1587711600, 1587717300)
    simulated_time = 1587711600
    while simulated_time < 1587717300:
        ac.update_position(simulated_time)
        print(ac.position)
        time.sleep(1)
        simulated_time += 60

