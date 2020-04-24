import time
import map
import csv
import datetime
from aircraft import Aircraft
from acicon import AcIcon
import pygame


def reverse_tuple(tup):
    return (tup[1], tup[0])


if __name__ == "__main__":
    gisdata = map.import_coords(r'..//GIS/aus10cgd_r.mif')
    bounds = ((-2, 105), (-40, 165))
    # ac = Aircraft('BNE', 'SYD', 1587711600, 1587717300)
    # ac2 = Aircraft('SYD', 'BNE', 1587711600, 1587717300)
    # ac3 = Aircraft('MEL', 'SYD', 1587711600, 1587717300)
    # ac4 = Aircraft('PER', 'SYD', 1587711600, 1587717300)
    simulated_time = 1555934400
        # aclist = [ac, ac2, ac3, ac4]
    dot = AcIcon()
    aclist = []
    with open('../flight_data/last_year.csv', 'r') as flight_raw:
        flightcsv = csv.reader(flight_raw)
        header = next(flightcsv)
        for row in flightcsv:

            if header is not None:
                aclist.append(Aircraft(row[8],
                              row[7],
                              time.mktime(datetime.datetime.strptime(row[3], "%d/%m/%Y %I:%M:%S %p").timetuple()),
                              time.mktime(datetime.datetime.strptime(row[4], "%d/%m/%Y %I:%M:%S %p").timetuple()),
                                       debug=False
                                       )
                              )

    # pos = map.dms_to_pix(reverse_tuple(ac.position), map.window_size, bounds)
    # dot.rect.y = pos[1]
    # dot.rect.x = pos[0]
    base = map.OzMap([gisdata[1][34], gisdata[1][194]], bounds)
    while simulated_time < 1587769324:
        base.mapcanvas.fill((0, 0, 0))
        base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
        cleanup = []
        font = pygame.font.Font('freesansbold.ttf', 20)
        human_time = font.render(datetime.datetime.utcfromtimestamp(simulated_time).strftime('%Y-%m-%d %H:%M:%S'),
                                 True,
                                 (255, 0, 0)
                                 )
        date_rect = human_time.get_rect()
        ac_remaining = font.render(str(len(aclist)),
                                   True,
                                   (255, 0, 0)
                                   )
        ac_rem_rect = ac_remaining.get_rect()
        ac_rem_rect.center = (100, 100)
        for each in aclist:
            if each.active:
                base.mapcanvas.blit(dot.image, map.dms_to_pix(reverse_tuple(each.position), map.window_size, bounds))
            each.update_position(simulated_time)
            if each.is_finished(simulated_time):
                cleanup.append(aclist.pop(aclist.index(each)))
        # print(pos)
        # ac.update_position(simulated_time)
        base.mapcanvas.blit(human_time, date_rect)
        base.mapcanvas.blit(ac_remaining, ac_rem_rect)
        base.draw_change()
        # print(ac.position)
        # time.sleep(1)
        simulated_time += 60
    base.mapcanvas.fill((0, 0, 0))
    base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))

