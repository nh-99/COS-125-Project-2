import pygame
from pygame.locals import *
import helpers

from level import Background

messageFont = None
optionsFont = None
background = None
soundimage = None
soundrect = None
isMuted = False
c = None

def createMainMenu(screen, cursor):
    global messageFont
    global optionsFont
    global background
    global soundimage
    global soundrect
    global c

    pygame.mixer.music.load("data/sound/mainmenu.wav")
    pygame.mixer.music.play(-1)
    messageFont = pygame.font.Font(None, 68)
    optionsFont = pygame.font.Font(None, 38)
    background = Background.Background('data/images/mainmenu.jpg', [0, 0], 0)
    soundimage, soundrect = helpers.load_image('soundon.png', -1)
    c = cursor

def drawScoreboard(screen):
    scores = []
    for row in c.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 5'):
        scores.append(row)
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        screen.blit(background.image, (0, 0))

        messageText = messageFont.render("Top 5 High Scores", 1, (255, 255, 255))
        textpos = messageText.get_rect(center=(640, 150))
        screen.blit(messageText, textpos)

        for i in range(0, len(scores)):
            credits = optionsFont.render("{} points - set on {}".format(scores[i][1], scores[i][0]), 1, (198, 37, 37))
            textpos3 = credits.get_rect(center=(640, 260 + i*40))
            screen.blit(credits, textpos3)

        exitGame = optionsFont.render("Return to Main Menu", 1, (198, 37, 37))
        textpos4 = exitGame.get_rect(center=(640, 500))
        if textpos4.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                break
            exitGame = optionsFont.render("Return to Main Menu", 1, (1, 188, 73))
            textpos4 = exitGame.get_rect(center=(640, 500))
        screen.blit(exitGame, textpos4)

        pygame.display.flip()

def drawCredits(screen):
    teamMembers = [('Lead Programmer', 'Noah Howard'), ('QA/Testing', 'Joshua Schaff'), ('Documentalist', 'Leah Dodier'),
                   ('Graphics Designer', 'Liwen Chen'), ('Team Lead', 'Raeanna Crowe')]
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        screen.blit(background.image, (0, 0))

        messageText = messageFont.render("Credits", 1, (255, 255, 255))
        textpos = messageText.get_rect(center=(640, 150))
        screen.blit(messageText, textpos)

        for i in range(0, len(teamMembers)):
            credits = optionsFont.render("{} - {}".format(teamMembers[i][1], teamMembers[i][0]), 1, (33, 111, 237))
            textpos3 = credits.get_rect(center=(640, 260 + i*40))
            screen.blit(credits, textpos3)

        exitGame = optionsFont.render("Return to Main Menu", 1, (198, 37, 37))
        textpos4 = exitGame.get_rect(center=(640, 500))
        if textpos4.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                break
            exitGame = optionsFont.render("Return to Main Menu", 1, (1, 188, 73))
            textpos4 = exitGame.get_rect(center=(640, 500))
        screen.blit(exitGame, textpos4)

        pygame.display.flip()

def updateMenu(screen):
    global soundimage
    global soundrect
    global isMuted

    screen.blit(background.image, (0, 0))
    messageText = messageFont.render("Alien Takeover", 1, (255, 255, 255))
    textpos = messageText.get_rect(center=(640, 150))
    screen.blit(messageText, textpos)

    playGame = optionsFont.render("Play Game", 1, (198, 37, 37))
    textpos1 = playGame.get_rect(center=(640, 260))
    if textpos1.collidepoint(pygame.mouse.get_pos()):
        playGame = optionsFont.render("Play Game", 1, (1, 188, 73))
        if pygame.mouse.get_pressed()[0]:
            return "playgame"
        textpos1 = playGame.get_rect(center=(640, 260))
    screen.blit(playGame, textpos1)

    scoreboard = optionsFont.render("High Scores", 1, (198, 37, 37))
    textpos2 = scoreboard.get_rect(center=(640, 320))
    if textpos2.collidepoint(pygame.mouse.get_pos()):
        scoreboard = optionsFont.render("High Scores", 1, (1, 188, 73))
        if pygame.mouse.get_pressed()[0]:
            drawScoreboard(screen)
        textpos2 = scoreboard.get_rect(center=(640, 320))
    screen.blit(scoreboard, textpos2)

    credits = optionsFont.render("Credits", 1, (198, 37, 37))
    textpos3 = credits.get_rect(center=(640, 380))
    if textpos3.collidepoint(pygame.mouse.get_pos()):
        credits = optionsFont.render("Credits", 1, (1, 188, 73))
        if pygame.mouse.get_pressed()[0]:
            drawCredits(screen)
        textpos3 = credits.get_rect(center=(640, 380))
    screen.blit(credits, textpos3)

    exitGame = optionsFont.render("Exit", 1, (198, 37, 37))
    textpos4 = exitGame.get_rect(center=(640, 440))
    if textpos4.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
        exitGame = optionsFont.render("Exit", 1, (1, 188, 73))
        textpos4 = exitGame.get_rect(center=(640, 440))
    screen.blit(exitGame, textpos4)
