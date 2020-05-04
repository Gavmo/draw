import pygame
import time


class AcIcon(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        # self.image.fill((0, 0, 255))
        pygame.draw.circle(self.image, color, (3, 3), 3)
        self.rect = self.image.get_rect()


if __name__ == "__main__":
    icon = AcIcon((0, 255, 0))
    print(icon.rect)
    mapcanvas = pygame.display.set_mode((400, 300))
    mapcanvas.fill((255, 255, 255))
    pygame.display.set_caption("icon test")
    time.sleep(1)
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(icon)
    all_sprites_list.draw(mapcanvas)
    pygame.display.update()

    for x in range(0, 100):

        # print(x)
        icon.rect.x = x
        icon.rect.y = x

        mapcanvas.blit(icon.image, (x, int(x / 2)))
        pygame.display.flip()
        time.sleep(0.1)
        # print(icon.rect)
    time.sleep(5)
