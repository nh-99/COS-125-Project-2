import pygame

import helpers

class Bullet(pygame.sprite.Sprite):
    # This is the object that controls the bullets that a player or NPC can shoot

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image('bullet.png', -1)
        # Speed to move in pixels per update
        self.speed = 1
        self.parentEntity = None

    def create(self, location, parentEntity):
        self.rect.midtop = location
        self.parentEntity = parentEntity

    def update(self):
        pos = self.rect.midtop
        self.rect.midtop = (pos[0], pos[1] - self.speed)

class EnemyBullet(pygame.sprite.Sprite):
    # This is the object that controls the bullets that a player or NPC can shoot

    def __init__(self, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image('bulletenemy.png', -1)
        # Speed to move in pixels per update
        self.speed = 1
        self.moveMultiplier = 1
        self.trueXPos = 0
        self.parentEntity = None
        self.damage = damage

    def create(self, location, moveMultiplier, parentEntity):
        self.rect.midtop = location
        self.trueXPos = self.rect.midtop[0]
        self.moveMultiplier = moveMultiplier
        self.parentEntity = parentEntity

    def update(self):
        pos = self.rect.midtop
        self.trueXPos += self.moveMultiplier
        self.rect.midtop = (self.trueXPos, pos[1] + self.speed)
