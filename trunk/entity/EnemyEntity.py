import pygame, random

import helpers

from . import BulletEntity

class BaseEnemy(pygame.sprite.Sprite):
    # This class constructs a basic enemy to oppose the player
    # This is to be treated as a "level 1" enemy and as a template for other enemies

    def __init__(self, startLocation, fireRate, health, bulletsInfo, speed, scoreValue, imageFile):
        self.currentLoc = startLocation
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image(imageFile, -1)
        # Speed to move in pixels per update
        self.speed = speed
        self.healthMax = health
        self.health = health
        self.damageFactor = 5
        self.bullets = []
        self.firecount = 0
        self.firelimit = fireRate
        self.bulletsInfo = bulletsInfo
        self.scoreValue = scoreValue

    def create(self, width):
        self.rect.midtop = self.currentLoc
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render("%s/%s" % (self.health, self.healthMax), 1, (255, 0, 0))

    def display_health(self, screen):
        if pygame.font:
            textpos = self.text.get_rect(center=(self.rect.midtop[0], self.rect.midtop[1] - 10))
            screen.blit(self.text, textpos)

    def update(self):
        self.currentLoc = (self.rect.midtop[0], self.currentLoc[1] + self.speed)
        self.rect.midtop = (self.currentLoc[0], int(self.currentLoc[1]))

    def takeDamage(self, bullet):
        self.health -= self.damageFactor
        self.text = self.font.render("%s/%s" % (self.health, self.healthMax), 1, (255, 0, 0))

    def fire(self):
        # Fire some bullets periodically
        self.firecount += 1
        if self.firecount > self.firelimit:
            self.firecount = 0
            for bulletInfo in self.bulletsInfo:
                bullet = BulletEntity.EnemyBullet(bulletInfo['damage'])
                bullet.create((self.rect.midbottom[0], self.rect.midbottom[1]), bulletInfo['positionMultiplier'], self)
                self.bullets.append(bullet)
            pygame.mixer.music.load("data/sound/gunfire.wav")
            pygame.mixer.music.play()
