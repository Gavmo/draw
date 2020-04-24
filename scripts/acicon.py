import pygame
import time


class AcIcon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill((0, 0, 255))
        pygame.draw.circle(self.image, (255, 0, 0), (3, 3), 3)
        self.rect = self.image.get_rect()


class bop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cover = pygame.Surface((400, 300))
        self.cover.fill((255, 255, 255))
        self.rect = self.cover.get_rect()


if __name__ == "__main__":
    icon = AcIcon()
    print(icon.rect)
    mapcanvas = pygame.display.set_mode((400, 300))
    mapcanvas.fill((255, 255, 255))
    pygame.display.set_caption("icon test")
    time.sleep(3)
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(icon)
    all_sprites_list.draw(mapcanvas)
    pygame.display.update()
    safetylayer = bop()
    mapcanvas.blit(safetylayer.cover, (0,0))
    for x in range(0, 100):
        print(x)
        icon.rect.x = x
        icon.rect.y = x
        time.sleep(0.1)
        safetylayer.blit(icon.image, (x, x / 2))
        pygame.display.flip()
        print(icon.rect)
    time.sleep(5)
