import pygame
import time
import threading

from . import BulletEntity

import helpers

class PlayerShip(pygame.sprite.Sprite):
    # This is the object that controls the player's ship.

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = helpers.load_image('player.png', -1)
        self.bullets = []
        self.health = 100
        self.damageFactor = 5
        self.score = 0
        self.canShoot = True
        self.powerup = False

    def move(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        self.rect.move_ip(0, -24)

    def cooldown(self):
        # A fire cooldown
        self.cooldownTimer = 0
        self.canShoot = False
        time.sleep(0.25)
        self.canShoot = True

    def fire(self):
        if self.canShoot:
            # Create a bullet and add it to our bullet list, for rendering
            bullet = BulletEntity.Bullet()
            bullet.create((self.rect.midtop[0], self.rect.midtop[1] - self.rect.height), self)
            self.bullets.append(bullet)
            t = threading.Thread(target=self.cooldown)
            t.start()
            pygame.mixer.music.load("data/sound/gunfire.wav")
            pygame.mixer.music.play()

    def takeDamage(self, hud, bullet):
        if bullet.damage and not self.powerup:
            self.health -= bullet.damage
        elif bullet.damage and self.powerup:
            self.health -= bullet.damage / self.damageFactor
        else:
            self.health -= self.damageFactor
        hud.updateHealth(self)
