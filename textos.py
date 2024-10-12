import pygame.sprite

class Damagetext(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image=font.render(damage, True, color)
        self.rect=self.image.get._rect()
        self.rect.center=(x, y)