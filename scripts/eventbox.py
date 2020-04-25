import datetime
import csv
import pygame


class EventBox(pygame.sprite.Sprite):
    def __init__(self, csvfile, position):
        self.position = position
        self.events = []
        with open(csvfile, 'r') as eventraw:
            for row in csv.reader(eventraw):
                self.events.append(row)

    def draw_events(self, timestamp):
        current_events = []
        for each in self.events:
            if datetime.datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y') == each[0]:
                current_events.append(each[1])
        eventstring = '\r\n'.join(current_events)
        font = pygame.font.Font('freesansbold.ttf', 20)
        events = []
        for each in current_events:
            events.append(font.render(each, True, (255, 0, 0)))
        # events = font.render(eventstring,
        #                      True,
        #                      (255, 0, 0)
        #                      )
        event_rect = events.get_rect()
        event_rect.center = self.position
        return events, event_rect