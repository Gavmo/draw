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
import cv2
import os


def reverse_tuple(tup):
    return tup[1], tup[0]


def compile_video():
    """Compiles the saved pics into a video"""
    image_folder = '../images'
    video_name = 'video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 30, (height, width))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()



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
    # for countdown in range(10, 0, -1):
    #     print(countdown)
    #     time.sleep(1)
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
        base.mapcanvas.blit(human_time, date_rect)
        # ac_remaining = font.render(str(len(aclist)),
        #                            True,
        #                            (255, 0, 0)
        #                            )
        # ac_rem_rect = ac_remaining.get_rect()
        # ac_rem_rect.center = (100, 100)
        # iq_remaining = font.render('Item Queue: {}'.format(len(itemqueue)),
        #                            True,
        #                            (255, 0, 0)
        #                            )
        # iq_rem_rect = iq_remaining.get_rect()
        # iq_rem_rect.center = (100, 120)
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
        # base.mapcanvas.blit(ac_remaining, ac_rem_rect)
        # base.mapcanvas.blit(iq_remaining, iq_rem_rect)
        # base.mapcanvas.blit(*eb.draw_events(simulated_time))
        pygame.image.save(base.mapcanvas, f'../images/{simulated_time}.jpg')
        base.draw_change()
        simulated_time += 750  # Sets the Tick rate.  The amount of seconds per frame

    base.mapcanvas.fill((0, 0, 0))
    base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
    compile_video()
    time.sleep(5)
