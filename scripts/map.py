import pygame
from time import sleep
import re
from random import randint

window_size = (800, 600)


def import_coords(gisfile):
    """Import the coordinates file"""
    bound_regexp = re.compile(r'\((?P<left>\d{,3}\.\d{2}),(?P<bottom>-?\d{,2}\.\d{,2})\)\s\((?P<right>\d{,3}\.\d{2}),'
                              r'(?P<top>-?\d{,2}\.\d{,2})\)')
    point_regexp = re.compile(r'(?P<lat>-?\d{,3}(?:\.\d{,3})?)*?\s(?P<lon>-?\d{,3}(?:\.\d{,3})?)', re.M)
    with open(gisfile, 'r') as points:
        capture = False
        gissectors = []
        gispoints = []
        regionlist = []
        for line in points.readlines():
            linedata = re.search(bound_regexp, line)
            if linedata:
                bounds = ((linedata.group('top'),
                           linedata.group('left')
                           ),
                          (linedata.group('bottom'),
                           linedata.group('right')
                           )
                          )
            pointdata = re.match(point_regexp, line)
            # print(pointdata)
            if line.startswith('REGION'):
                regionlist.append(line[line.index(' '):])
                if f' 74' in line or ' 3' in line:
                    capture = True
                else:
                    capture = False
            if pointdata and capture:
                specpoint = re.search(point_regexp, line)
                if (specpoint.group('lat')) != '' and (specpoint.group('lon')) != '':
                    gispoints.append((specpoint.group('lat'), specpoint.group('lon')))
                else:
                    gissectors.append(gispoints)
                    gispoints = []
    return bounds, gissectors


def dms_to_pix(coord, window, bounding):
    """Convert coordinates to pygame coordinate within the spatial boundary"""
    # print(coord)
    delta_lat = float(bounding[0][0]) - float(bounding[1][0])
    delta_lon = float(bounding[0][1]) - float(bounding[1][1])
    lat_ratio = 1 / (delta_lat / window[1])
    lon_ratio = 1 / (delta_lon / window[0])
    out_lat = float(coord[0]) * lat_ratio - 1700
    out_lon = float(coord[1]) * lon_ratio
    return int(out_lat), int(out_lon)


class OzMap:

    def __init__(self, outline, boundings):
        pygame.init()
        self.mapcanvas = pygame.display.set_mode((800, 600))
        self.mapcanvas.fill((255, 255, 255))
        pygame.display.update()
        pygame.display.set_caption("BORK BORK BORK")
        # sleep(1)
        self.mapcanvas.fill((0, 0, 0))
        self.mapsurface = pygame.surface.Surface((800, 600))
        pygame.display.update()
        # sleep(1)
        self.drawoz(outline, boundings)

    def drawoz(self, oz, bounds):
        for ranges in oz:
            pen = (255, 255, 255)
            for point in range(0, len(ranges)):
                from_point = dms_to_pix(ranges[point], window_size, bounds)
                to_point = dms_to_pix(ranges[point - 1], window_size, bounds)
                pygame.draw.line(self.mapsurface, pen, from_point, to_point, 1)

    def blitoz(self):
        self.mapcanvas.blit(self.mapsurface, (0, 0))
        self.draw_change()
        # sleep(3)

    def draw_change(self):
        pygame.display.update()


if __name__ == "__main__":
    # draw()
    gisdata = import_coords(r'..//GIS/aus10cgd_r.mif')
    # print(gisdata[0])
    # print(gisdata[1][1])
    #
    # print(randint(0, 255))
    # print(len(gisdata[1]))
    # print(dms_to_pix((-27, 153), window_size, ((-2, 105), (-40, 165))))
    print(len(gisdata[1][34]) + len(gisdata[1][194]))
    a = OzMap([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
    while True:
        a.blitoz()


    # draw(gisdata[1], ((-2, 105), (-40, 165)))
