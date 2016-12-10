#! /usr/bin/env python

import os, sys, copy, sqlite3, time
import pygame
import math
from pygame.locals import *
from helpers import *

from entity import PlayerEntity, EnemyEntity
from ui import hud, mainmenu
from level import LevelManager, Background

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

conn = sqlite3.connect('alien_takeover.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS scores(date text, score INT)''')
conn.commit()

class GameMain:
    def __init__(self, width=1280, height=720):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Alien Takeover")
        self.levelManager = LevelManager
        self.hud = hud.RenderHUD()
        self.readyForNextLevel = False
        self.pausedEnemies = []
        self.enemySpritesBackups = pygame.sprite.Group()

    def checkBulletsForEntity(self, entity):
        for bullet in entity.bullets:
            bullet.update()
            w, h = pygame.display.get_surface().get_size()
            if bullet.rect.midtop[1] < 1 or bullet.rect.midtop[1] > h or bullet.rect.midtop[0] < 1 or bullet.rect.midtop[0] > w:
                entity.bullets.remove(bullet)
                self.bulletSprites.remove(bullet)
                continue
            self.bulletSprites.add(bullet)

    def checkBulletCollisionsForEntity(self, entity):
        lstCols = []
        if entity:
            lstCols = pygame.sprite.spritecollide(entity, self.bulletSprites, True)
        if len(lstCols) > 0:
            if (entity.__class__.__name__ == "BaseEnemy" and lstCols[0].__class__.__name__ == "EnemyBullet") or \
              (entity.__class__.__name__ == "PlayerShip" and lstCols[0].__class__.__name__ == "Bullet"):
                return False
            try:
                entity.takeDamage(self.hud, lstCols[0])
            except:
                entity.takeDamage(lstCols[0])
            if entity.health <= 0:
                return True
            lstCols[0].parentEntity.bullets.remove(lstCols[0])
            self.bulletSprites.remove(lstCols[0])

    def playerLose(self):
        self.hud.displayMessage("Game Over", self.screen)
        self.hud.renderFinalScore(self.screen)
        returnToMenu = self.hud.displayCustomMessage("Return to main menu", self.screen, (640, 440), (198, 37, 37))

        if returnToMenu.collidepoint(pygame.mouse.get_pos()):
            returnToMenu = self.hud.displayCustomMessage("Return to main menu", self.screen, (640, 440), (1, 188, 73))
            if pygame.mouse.get_pressed()[0]:
                return True

        for enemy in self.levelManager.getCurrentLevel().enemies:
            self.levelManager.getCurrentLevel().enemies.remove(enemy)
            for bullet in enemy.bullets:
                self.bulletSprites.remove(bullet)
            self.enemySprites.remove(enemy)

        for powerup in self.levelManager.getCurrentLevel().powerups:
            self.bulletSprites.remove(powerup)

    def doPause(self):
        self.background = Background.Background('data/images/mainmenu.jpg', [0, 0], 0)
        self.enemySpritesBackups = pygame.sprite.Group()
        self.pausedBulletSprites = copy.copy(self.bulletSprites)
        self.pausedPowerupSprites = pygame.sprite.Group()
        self.pausedEnemies = copy.copy(self.levelManager.getCurrentLevel().enemies)
        for enemy in self.enemySprites:
            self.enemySpritesBackups.add(enemy)

        for powerup in self.powerupSprites:
            self.pausedPowerupSprites.add(powerup)
            self.powerupSprites.remove(powerup)

        #Remove player bullets when they pause (don't want to accidentally quit)
        self.player.bullets = []

        for bullet in self.bulletSprites:
            self.bulletSprites.remove(bullet)

        for enemy in self.levelManager.getCurrentLevel().enemies:
            self.levelManager.getCurrentLevel().enemies.remove(enemy)
            self.enemySprites.remove(enemy)

    def doUnpause(self):
        if self.levelManager.getCurrentLevel() is not None:
            self.background = Background.Background(self.levelManager.getCurrentLevel().backgroundLocation, [0, 0], int(self.levelManager.getCurrentLevel().levelLength))
        else:
            self.background = Background.Background('data/images/default.png', [0, 0], self.levelManager.getCurrentLevel().levelLength)

        for powerup in self.pausedPowerupSprites:
            self.powerupSprites.add(powerup)

        #Remove player bullets when they unpause (no buffering)
        for bullet in self.player.bullets:
            self.bulletSprites.remove(bullet)
        self.player.bullets = []

        for enemy in self.enemySpritesBackups:
            self.enemySprites.add(enemy)
        self.levelManager.getCurrentLevel().enemies = self.pausedEnemies
        self.bulletSprites = self.pausedBulletSprites

    def runGame(self):
        pygame.mouse.set_visible(False)
        # Load all of our sprites
        self.loadSprites()
        self.player.health = 100
        self.hud.updateHealth(self.player)
        self.levelManager.levels = []
        self.levelManager.loadLevel()

        self.levelManager.getCurrentLevel().createLevel(self.enemySprites, self.powerupSprites)
        if self.levelManager.getCurrentLevel() is not None:
            self.background = Background.Background(self.levelManager.getCurrentLevel().backgroundLocation, [0, 0], int(self.levelManager.getCurrentLevel().levelLength))
        else:
            self.background = Background.Background('data/images/default.png', [0, 0], self.levelManager.getCurrentLevel().levelLength)

        continueOnwards = None
        exitGame = None
        unpauseGame = None
        pause = False
        while 1:
            if pygame.mouse.get_pressed()[0] and self.player:
                self.player.fire()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == MOUSEMOTION and self.player:
                    self.player.move()
                elif event.type == KEYDOWN and self.player:
                    if event.key == pygame.K_SPACE:
                        self.player.fire()
                    elif event.key == pygame.K_ESCAPE:
                        pause = not pause
                        if pause:
                            self.doPause()
                        else:
                            self.doUnpause()

            # Check if the map has reached the end of it's scroll
            if self.levelManager.getCurrentLevel().levelLength - 150 < 0 and not self.readyForNextLevel:
                #Remove player bullets when they finish (no buffering)
                for bullet in self.player.bullets:
                    self.bulletSprites.remove(bullet)
                self.player.bullets = []
                self.background = Background.Background('data/images/mainmenu.jpg', [0, 0], 0)
                self.readyForNextLevel = True
                self.player.score += int(math.sqrt(self.player.health) * 5)
                self.hud.updateScore(self.player)

            if not pause:
                for powerup in self.levelManager.getCurrentLevel().powerups:
                    powerup.update()

            # Check for collision
            if self.player:
                # Powerup collision
                lstCols = pygame.sprite.spritecollide(self.player, self.powerupSprites, True)
                if len(lstCols) > 0:
                    lstCols[0].doPowerup(self.player, self.levelManager.getCurrentLevel().enemies)
                    self.hud.updateScore(self.player)
                    self.hud.updateHealth(self.player)

            if self.player:
                if self.checkBulletCollisionsForEntity(self.player):
                    for bullet in self.player.bullets:
                        self.bulletSprites.remove(bullet)
                    c.execute("INSERT INTO scores VALUES ('{}','{}')".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                             str(self.player.score)))
                    conn.commit()
                    self.player = None
            for enemy in self.levelManager.getCurrentLevel().enemies:
                if self.checkBulletCollisionsForEntity(enemy):
                    # Update player score
                    self.player.score += enemy.scoreValue
                    self.hud.updateScore(self.player)

                    self.levelManager.getCurrentLevel().enemies.remove(enemy)
                    for bullet in enemy.bullets:
                        self.bulletSprites.remove(bullet)
                    self.enemySprites.remove(enemy)

            # Check for bullets colliding with next choices
            if exitGame is not None and continueOnwards is not None:
                bulletRectList = []
                for bullet in self.player.bullets:
                    bulletRectList.append(bullet.rect)
                if exitGame.collidelist(bulletRectList) > -1:
                    pygame.mouse.set_visible(True)
                    self.levelManager.currentLevel = None
                    self.levelManager.loadLevel()
                    self.readyForNextLevel = False
                    exitGame = None
                    continueOnwards = None
                    c.execute("INSERT INTO scores VALUES ('{}','{}')".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                             str(self.player.score)))
                    conn.commit()
                    break
                elif continueOnwards.collidelist(bulletRectList) > -1:
                    #Remove player bullets when they finsh (no buffering)
                    for bullet in self.player.bullets:
                        self.bulletSprites.remove(bullet)
                    self.player.bullets = []
                    self.background = self.levelManager.nextLevel()
                    self.levelManager.getCurrentLevel().createLevel(self.enemySprites, self.powerupSprites)
                    self.readyForNextLevel = False
                    exitGame = None
                    continueOnwards = None

            if exitGame and self.readyForNextLevel and not self.levelManager.hasNextLevel:
                bulletRectList = []
                for bullet in self.player.bullets:
                    bulletRectList.append(bullet.rect)
                if exitGame.collidelist(bulletRectList) > -1:
                    pygame.mouse.set_visible(True)
                    self.levelManager.currentLevel = None
                    self.levelManager.loadLevel()
                    self.readyForNextLevel = False
                    exitGame = None
                    c.execute("INSERT INTO scores VALUES ('{}','{}')".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                             str(self.player.score)))
                    conn.commit()
                    break
            # Check for bullets colliding pause choices
            if exitGame is not None and unpauseGame is not None:
                bulletRectList = []
                for bullet in self.player.bullets:
                    bulletRectList.append(bullet.rect)
                if exitGame.collidelist(bulletRectList) > -1:
                    pygame.mouse.set_visible(True)
                    self.doUnpause()
                    self.levelManager.currentLevel = None
                    self.levelManager.loadLevel()
                    c.execute("INSERT INTO scores VALUES ('{}','{}')".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                             str(self.player.score)))
                    conn.commit()
                    break
                elif unpauseGame.collidelist(bulletRectList) > -1:
                    self.doUnpause()
                    pause = False
                    exitGame = None
                    unpauseGame = None

            # Check for bullets that need to be drawn
            if self.player:
                self.checkBulletsForEntity(self.player)
            for enemy in self.levelManager.getCurrentLevel().enemies:
                enemy.fire()
                self.checkBulletsForEntity(enemy)

            # Update enemy position
            for enemy in self.levelManager.getCurrentLevel().enemies:
                enemy.update()

            # Draw all the items on the screen
            self.screen.fill([255, 255, 255])
            if self.player and not self.readyForNextLevel and not pause:
                self.screen.blit(self.background.image, (0, self.levelManager.getCurrentLevel().incrementLevel
                                                     (self.background.initialHeight, self.player, self.hud)))
            else:
                self.screen.blit(self.background.image, (0, 0))

            if not self.player:
                self.background = Background.Background('data/images/mainmenu.jpg', [0, 0], 0)
                pygame.mouse.set_visible(True)
                if self.playerLose():
                    pygame.mouse.set_visible(True)
                    self.levelManager.currentLevel = None
                    self.levelManager.loadLevel()
                    self.readyForNextLevel = False
                    exitGame = None
                    continueOnwards = None
                    break

            if pause:
                self.hud.displayMessage("Game paused", self.screen)
                self.hud.displayCustomMessage("Shoot at one of the options below, or press ESC to continue", self.screen, (640, 400), (255, 255, 255))
                exitGame = self.hud.displayCustomMessage("Quit to main menu", self.screen, (320, 480), (255, 0, 0))
                unpauseGame = self.hud.displayCustomMessage("Continue", self.screen, (960, 480), (0, 255, 0))
                for enemy in self.levelManager.getCurrentLevel().enemies:
                    self.levelManager.getCurrentLevel().enemies.remove(enemy)
                    for bullet in enemy.bullets:
                        self.bulletSprites.remove(bullet)
                    self.enemySprites.remove(enemy)

            if self.readyForNextLevel:
                if self.levelManager.hasNextLevel:
                    self.player.health = 100
                    self.hud.updateHealth(self.player)
                    self.hud.displayMessage("You have finished level " + str(self.levelManager.getCurrentLevel().levelNumber), self.screen)
                    self.hud.displayCustomMessage("Shoot at one of the options below:", self.screen, (640, 400), (255, 255, 255))
                    exitGame = self.hud.displayCustomMessage("Quit to main menu", self.screen, (320, 440), (255, 0, 0))
                    continueOnwards = self.hud.displayCustomMessage("Go to next level", self.screen, (960, 440), (0, 255, 0))
                    for enemy in self.levelManager.getCurrentLevel().enemies:
                        self.levelManager.getCurrentLevel().enemies.remove(enemy)
                        for bullet in enemy.bullets:
                            self.bulletSprites.remove(bullet)
                        self.enemySprites.remove(enemy)
                else:
                    self.hud.displayMessage("You have completed the game", self.screen)
                    exitGame = self.hud.displayCustomMessage("Quit to main menu", self.screen, (640, 480), (255, 0, 0))
                    self.hud.renderFinalScore(self.screen)
                    for i in range(0, len(self.levelManager.getCurrentLevel().enemies)):
                        if i == len(self.levelManager.getCurrentLevel().enemies):
                            c.execute("INSERT INTO scores VALUES ('{}','{}')".format(time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                     str(self.player.score)))
                            conn.commit()
                        try:
                            self.levelManager.getCurrentLevel().enemies.remove(self.levelManager.getCurrentLevel().enemies[i])
                            for bullet in self.levelManager.getCurrentLevel().enemies[i].bullets:
                                self.bulletSprites.remove(bullet)
                            self.enemySprites.remove(self.levelManager.getCurrentLevel().enemies[i])
                        except IndexError:
                            print ''

            # Display health for the player and enemy
            if self.player:
                self.hud.renderHealth(self.player, self.screen)
                self.hud.renderScore(self.width, self.screen)
            self.levelManager.getCurrentLevel().renderHealth(self.screen)

            if self.player:
                self.playerSprite.draw(self.screen)
            self.enemySprites.draw(self.screen)
            self.bulletSprites.draw(self.screen)
            self.powerupSprites.draw(self.screen)

            pygame.display.flip()

    def loadSprites(self):
        # Load the sprites that we need
        self.player = PlayerEntity.PlayerShip()
        self.playerSprite = pygame.sprite.RenderPlain(self.player)

        self.enemySprites = pygame.sprite.Group()
        self.bulletSprites = pygame.sprite.Group()
        self.powerupSprites = pygame.sprite.Group()

    def main(self):
        global c
        pygame.mouse.set_visible(True)
        mainmenu.createMainMenu(self.screen, c)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
            status = mainmenu.updateMenu(self.screen)
            if status == "playgame":
                self.runGame()
            pygame.display.flip()

if __name__ == "__main__":
    MainWindow = GameMain()
    MainWindow.main()
