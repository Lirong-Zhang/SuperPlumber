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
        self.screen = pygame.display.set_mode((657, 298))
        self.bird = pygame.Rect(65, 50, 26, 48) #??
        self.background = pygame.image.load("assets/background.png").convert()
        #self.background = setup.GFX["assets/background.png"]
        self.background = pygame.transform.scale(self.background,(657, 298))                
        
        self.asset_1 = pygame.image.load("assets/1.png").convert_alpha()
        self.asset_2 = pygame.image.load("assets/2.png").convert_alpha()
        self.asset_d = pygame.image.load("assets/dead.png").convert_alpha()
        
        self.asset_1 = pygame.transform.scale(self.asset_1,(26, 48))
        self.asset_2 = pygame.transform.scale(self.asset_2,(26, 48))
        self.asset_d = pygame.transform.scale(self.asset_d,(26, 48))
        
        self.birdSprites = [self.asset_1, self.asset_2, self.asset_d]
        
        # self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(), #different motions of the birds
                            # pygame.image.load("assets/2.png").convert_alpha(),
                            # pygame.image.load("assets/dead.png")]
        # self.birdSprites = pygame.transform.scale(self.birdSprites,(26, 48))
        
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha() #the walls
        self.wallUp = pygame.transform.scale(self.wallUp,(30, 150))
        
        #self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        
        self.start_img = pygame.image.load("assets/background.png").convert_alpha() #start screen
        self.start_img = pygame.transform.scale(self.background,(657, 298))
        
        self.get_ready_img = pygame.image.load("assets/get_ready.png").convert_alpha() #get ready marks
        self.gap = 200 #distance between upper wall and lower wall
        self.wallx = 657
        self.birdY = 249
        self.jump = -100
        self.jumpSpeed = 15
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-50, 50)
        self.state = "start"
        self.font = 0
        self.clock = 0


    def updateWalls(self):
        self.wallx -= 5
        if self.wallx < -80:
            self.wallx = 657
            self.counter += 1
            self.offset = random.randint(-50, 50)

    def birdUpdate(self):
        if self.jump > 0:
            self.jumpSpeed = self.jumpSpeed - 1
            self.birdY = self.birdY - self.jumpSpeed
            self.jump = self.jump - 1
            
        if -40< self.jump <= 0:
            self.jumpSpeed = 10
            self.birdY = self.birdY + self.jumpSpeed
            self.jump = self.jump - 1
            if self.birdY >= 230:
                self.birdY = 249
                self.jump == -100            
            
        else :
            self.birdY = self.birdY
        
            # self.jump = self.jump - 1
            # self.birdY += self.gravity
            # self.gravity += 0.2
        
        self.bird[1] = self.birdY #provide info for collision
        
        # upRect = pygame.Rect(self.wallx,
                             # 200 + self.offset,
                             # self.wallUp.get_width() - 10,
                             # self.wallUp.get_height()) # the area of the plump (up plump)
        upRect = pygame.Rect(self.wallx,
                             220 + self.offset,
                             30,
                             150) # the area of the plump (up plump)                             
                             
        # downRect = pygame.Rect(self.wallx,
                               # 0 - self.gap - self.offset - 10,
                               # self.wallDown.get_width() - 10,
                               # self.wallDown.get_height()) #plump (down plump)
                               
        if upRect.colliderect(self.bird): # overlap: dead
            self.dead = True
            self.bird[1] = 50
            self.birdY = 249
            self.dead = False
            self.wallx = 657
            self.offset = random.randint(-30, 30)
            self.gravity = 5
            self.state = "end" #dead
            
         #if downRect.colliderect(self.bird):
             #self.dead = True
             
        # if not 0 < self.bird[1] < 720:
            # self.bird[1] = 50
            # self.birdY = 298
            # self.dead = False
            # self.wallx = 657
            # self.offset = random.randint(-50, 50)
            # self.gravity = 5
            # self.state = "end" #dead

    def play(self):

        self.screen.fill((255, 255, 255)) #fill Surface with white color???
        self.screen.blit(self.background, (0, 0)) #draw one image onto another
        # self.screen.blit(self.wallUp,
                         # (self.wallx, 360 + self.gap - self.offset))
        self.screen.blit(self.wallUp,
                          (self.wallx, 220 + self.offset))                         
                         
                         
        # self.screen.blit(self.wallDown,
                         # (self.wallx, 0 - self.gap - self.offset)) # two pipes
                         
        self.screen.blit(self.font.render(str(self.counter), # points counter
                                     -1,
                                     (255, 255, 255)),
                                     (200, 50)) #render(text, antialias, color, background=None)
        if self.dead:
            self.sprite = 2
            pygame.mixer.Sound.play(falling_sound)
        elif self.jump >-40:
            self.sprite = 1
        else:
            self.sprite = 0
        
        #if not self.dead:
            #self.sprite = 0 #reverse counter: 2: dead
            
        self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))            
        self.updateWalls()
        self.birdUpdate()

    def start_screen (self):
        self.screen.fill((255, 0, 0)) #red
        self.screen.blit(self.start_img, (0, 0))

        get_ready_x = 241 + 20 * math.sin(pygame.time.get_ticks() / 500.0)
        get_ready_y = 125 + 10 * math.sin(pygame.time.get_ticks() / 150.0) 

        self.screen.blit(self.get_ready_img, (get_ready_x, get_ready_y))#get ready animation
        self.screen.blit(self.font.render(str(self.counter),
                     -1,
                     (255, 255, 255)),
              (180, 80))


    def run(self):
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 50) 	#create a Font object from the system fonts
        while True:
            self.clock.tick(60) #unit:ms
            readable, writable, errored  = select.select([server], [], [], 0)
            for s in readable: #with nodes
                if s is server:
                    data, addr = server.recvfrom(1024)
                    if data:
                        rpt = Theft.Theft(data=data, data_length=len(data)) #probably need to work with the nodes
                        if (rpt.get_sender() ==2 and rpt.get_stolen() == 1) and not self.dead: #player1, stolen: light sensor covered: jump
                            self.jump = 17
                            self.gravity = 5
                            self.jumpSpeed = 15
                        if (rpt.get_sender() ==3 and rpt.get_humidity() > 2000) and not self.dead: #player2, decrease the gap width
                            self.gap = 160
                        elif (rpt.get_sender() ==3 and rpt.get_humidity() < 2000): 
                            self.gap = 200
                        if (rpt.get_sender() ==2 and rpt.get_button() == 1):
                            self.state = "play" #begin game
                            self.counter = 0
            for event in pygame.event.get():# without nodes
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and not self.dead: #press, default: space key
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 15
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'end':
                        self.state = 'start'
                    else:
                        self.state = "play" #reset counter
                        self.counter = 0

            if self.state == "end":
                self.screen.fill((0, 0, 0)) #black
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
