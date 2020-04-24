import json
import time


class Aircraft:
    def __init__(self, dep_port, arr_port, dep_datetime, arr_datetime):
        self.position = (0, 0)
        self.dep_datetime = dep_datetime
        self.arr_datetime = arr_datetime
        with open('../apdata/airports.json', 'r') as rawjson:
            ap = json.load(rawjson)
            self.dep_port = (ap[dep_port]['lat'], ap[dep_port]['lon'])
            self.arr_port = (ap[arr_port]['lat'], ap[arr_port]['lon'])
            self.position = self.dep_port

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
        time.sleep(3)
        simulated_time += 3
