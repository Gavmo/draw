import time
import re
import map
import csv
import datetime
from aircraft import Aircraft
from flight_data_ingest import FlightData
from acicon import AcIcon
from eventbox import EventBox
import pygame


def reverse_tuple(tup):
    return (tup[1], tup[0])


if __name__ == "__main__":
    print("Importing map")
    gisdata = map.import_coords(r'..//GIS/aus10cgd_r.mif')
    bounds = ((-2, 105), (-40, 165))
    # print("Spawning aircraft")
    # dot = AcIcon()
    # eb = EventBox('../event_data/events.csv', (10000, 80))
    print("Importing Flight Data")
    # flight_data = FlightData('../flight_data/this_year.csv')
    # flight_data = FlightData('../flight_data/last_year.csv')
    flight_data = FlightData('../flight_data/may-flight-data.csv')
    aclist = flight_data.aclist
    print("Drawing Map")
    base = map.OzMap([gisdata[1][34], gisdata[1][194]], bounds)
    simulated_time = flight_data.flex_start
    # print(datetime.datetime.utcfromtimestamp(simulated_time).strftime('%Y-%m-%d %H:%M:%S'))
    finish = flight_data.flex_end
    itemqueue = []
    for countdown in range(10):
        print(countdown)
        time.sleep(1)
    while simulated_time < finish:
        if len(aclist) < 500:
            itemqueue.extend(aclist)
            aclist = []
        else:
            while len(itemqueue) < 500:
                itemqueue.append(aclist.pop(0))
        pygame.event.get()
        base.mapcanvas.fill((0, 0, 0))
        base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
        cleanup = []
        font = pygame.font.Font('freesansbold.ttf', 20)
        human_time = font.render(datetime.datetime.utcfromtimestamp(simulated_time).strftime('%Y-%m-%d %H:%M:%S'),
                                 True,
                                 (255, 0, 0)
                                 )
        date_rect = human_time.get_rect()
        date_rect.center = (400, 20)
        ac_remaining = font.render(str(len(aclist)),
                                   True,
                                   (255, 0, 0)
                                   )
        ac_rem_rect = ac_remaining.get_rect()
        ac_rem_rect.center = (100, 100)
        iq_remaining = font.render('Item Queue: {}'.format(len(itemqueue)),
                                   True,
                                   (255, 0, 0)
                                   )
        iq_rem_rect = iq_remaining.get_rect()
        iq_rem_rect.center = (100, 120)
        for each in itemqueue:
            if each.active:
                base.mapcanvas.blit(each.icon.image,
                                    map.dms_to_pix(reverse_tuple(each.position),
                                                   map.window_size,
                                                   bounds
                                                   )
                                    )
            each.update_position(simulated_time)
            if each.is_finished(simulated_time):
                cleanup.append(itemqueue.pop(itemqueue.index(each)))
        base.mapcanvas.blit(human_time, date_rect)
        base.mapcanvas.blit(ac_remaining, ac_rem_rect)
        base.mapcanvas.blit(iq_remaining, iq_rem_rect)
        # base.mapcanvas.blit(*eb.draw_events(simulated_time))
        base.draw_change()
        simulated_time += 1500

    base.mapcanvas.fill((0, 0, 0))
    base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
    time.sleep(5)
