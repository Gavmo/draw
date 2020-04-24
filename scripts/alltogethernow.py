import time
import map
from aircraft import Aircraft
from acicon import AcIcon


def reverse_tuple(tup):
    return (tup[1], tup[0])


if __name__ == "__main__":
    gisdata = map.import_coords(r'..//GIS/aus10cgd_r.mif')
    bounds = ((-2, 105), (-40, 165))
    base = map.OzMap([gisdata[1][34], gisdata[1][194]], bounds)
    ac = Aircraft('BNE', 'SYD', 1587711600, 1587717300)
    ac2 = Aircraft('SYD', 'BNE', 1587711600, 1587717300)
    ac3 = Aircraft('MEL', 'SYD', 1587711600, 1587717300)
    ac4 = Aircraft('PER', 'SYD', 1587711600, 1587717300)
    simulated_time = 1587711600
    aclist = [ac, ac2, ac3, ac4]
    dot = AcIcon()

    pos = map.dms_to_pix(reverse_tuple(ac.position), map.window_size, bounds)
    dot.rect.y = pos[1]
    dot.rect.x = pos[0]
    base = map.OzMap([gisdata[1][34], gisdata[1][194]], bounds)
    while simulated_time < 1587717300:

        pos = map.dms_to_pix(reverse_tuple(ac.position), map.window_size, bounds)
        base.mapcanvas.fill((0, 0, 0))
        base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))
        for each in aclist:
            base.mapcanvas.blit(dot.image, map.dms_to_pix(reverse_tuple(each.position), map.window_size, bounds))
            each.update_position(simulated_time)
        # print(pos)
        # ac.update_position(simulated_time)
        base.draw_change()
        # print(ac.position)
        # time.sleep(1)
        simulated_time += 60
    base.mapcanvas.fill((0, 0, 0))
    base.drawoz([gisdata[1][34], gisdata[1][194]], ((-2, 105), (-40, 165)))

