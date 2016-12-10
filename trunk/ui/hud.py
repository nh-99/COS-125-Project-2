import pygame

class RenderHUD():
    def __init__(self):
        if pygame.font:
            self.font = pygame.font.Font(None, 24)
            self.messageFont = pygame.font.Font(None, 48)
            self.healthText = self.font.render("%s/100" % '100', 1, (255, 0, 0))
            self.scoreText = self.font.render("Score: %s" % '0', 1, (255, 255, 255))
            self.messageText = self.messageFont.render("", 1, (0, 0, 0))

    def renderHealth(self, player, screen):
        textpos = self.healthText.get_rect(center=(player.rect.midbottom[0], player.rect.midbottom[1] + 10))
        screen.blit(self.healthText, textpos)

    def updateHealth(self, player):
        self.healthText = self.font.render("%s/100" % player.health, 1, (255, 0, 0))

    def renderScore(self, width, screen):
        textpos = self.scoreText.get_rect(center=(width - 50, 10))
        screen.blit(self.scoreText, textpos)

    def renderFinalScore(self, screen):
        textpos = self.messageText.get_rect(center=(640, 408))
        screen.blit(self.scoreText, textpos)

    def updateScore(self, player):
        self.scoreText = self.font.render("Score: %s" % player.score, 1, (255, 255, 255))

    def displayMessage(self, message, screen):
        self.messageText = self.messageFont.render(message, 1, (255, 255, 255))
        textpos = self.messageText.get_rect(center=(640, 360))
        screen.blit(self.messageText, textpos)

    def displayCustomMessage(self, message, screen, centercoords, color):
        self.messageText = self.messageFont.render(message, 1, color)
        textpos = self.messageText.get_rect(center=centercoords)
        screen.blit(self.messageText, textpos)
        return textpos
