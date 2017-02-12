#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import socket
#import Theft
import re
import select
import math

pygame.mixer.init(44100, -16,2,2048)
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)
falling_sound = pygame.mixer.Sound("falling.wav")
port = 7000
server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server.bind(('', port))
server.setblocking(0)
class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.start_img = pygame.image.load("assets/start.png").convert_alpha()
        self.get_ready_img = pygame.image.load("assets/get_ready.png").convert_alpha()
        self.gap = 200
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.state = "start"
        self.font = 0
        self.clock = 0


    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5
            self.state = "end"

    def play(self):

        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.wallUp,
                         (self.wallx, 360 + self.gap - self.offset))
        self.screen.blit(self.wallDown,
                         (self.wallx, 0 - self.gap - self.offset))
        self.screen.blit(self.font.render(str(self.counter),
                                     -1,
                                     (255, 255, 255)),
                                     (200, 50))
        if self.dead:
            self.sprite = 2
            pygame.mixer.Sound.play(falling_sound)
        elif self.jump:
            self.sprite = 1
        self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
        if not self.dead:
            self.sprite = 0
        self.updateWalls()
        self.birdUpdate()

    def start_screen (self):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.start_img, (0, 0))

        get_ready_x = 30 + 20 * math.sin(pygame.time.get_ticks() / 500.0)
        get_ready_y = 170 + 10 * math.sin(pygame.time.get_ticks() / 150.0)

        self.screen.blit(self.get_ready_img, (get_ready_x, get_ready_y))
        self.screen.blit(self.font.render(str(self.counter),
                     -1,
                     (255, 255, 255)),
              (180, 80))


    def run(self):
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 50)
        while True:
            self.clock.tick(60)
            readable, writable, errored  = select.select([server], [], [], 0)
            for s in readable:
                if s is server:
                    data, addr = server.recvfrom(1024)
                    if data:
                        rpt = Theft.Theft(data=data, data_length=len(data))
                        if (rpt.get_sender() ==2 and rpt.get_stolen() == 1) and not self.dead:
                            self.jump = 17
                            self.gravity = 5
                            self.jumpSpeed = 10
                        if (rpt.get_sender() ==3 and rpt.get_humidity() > 2000) and not self.dead:
                            self.gap = 160
                        elif (rpt.get_sender() ==3 and rpt.get_humidity() < 2000): 
                            self.gap = 200
                        if (rpt.get_sender() ==2 and rpt.get_button() == 1):
                            self.state = "play"
                            self.counter = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'end':
                        self.state = 'start'
                    else:
                        self.state = "play"
                        self.counter = 0

            if self.state == "end":
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.font.render("You Died: " + str(self.counter),
                             -1,
                             (255, 255, 255)),
                      (50, 50))
            if self.state == "play":
                self.play()
            if self.state == "start":
                self.start_screen();

            pygame.display.update()


if __name__ == "__main__":
    FlappyBird().run()
