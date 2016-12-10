import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, levelSize):
        self.image = pygame.image.load(image_file).convert_alpha()
        self.initialHeight = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image, (1280, self.image.get_rect().height + levelSize))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
