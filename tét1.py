from ast import Return
from asyncore import loop
from msilib import datasizemask
from socket import SO_RCVBUF
import pygame
import random
import math
from pygame import mixer


pygame.init()

# the screen
screen = pygame.display.set_mode((800,600))

# title and icon of the game
pygame.display.set_caption("tét1")
icon = pygame.image.load('arcade-game.png')
pygame.display.set_icon(icon)
# player 
playerImg = pygame.image.load('player.png')

playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    print(playerImg)
    screen.blit(playerImg,(x,y))

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies) :
    enemyImg.append(pygame.image.load('enimies.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.175)
    enemyY_change.append(39)
    
print(enemyX, enemyY)

def enemy(x, y, i) :
    screen.blit(enemyImg[i], (x, y))

#background
background = pygame.image.load('5509862.jpg')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

def fire_bullet (x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision (enemyX, enemyY, bulletX, bulletY) :
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27 :
        return True
    else :
        return False    
    
#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score (x,y ):
    score = font.render("SCORE : " +str(score_value),True,(0,204,204))
    screen.blit(score,(x,y))

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text (x,y):
    over_text = over_font.render("GAME OVER",True,0,204,204)
    screen.blit(over_text,200,250)

#loop
running = True
while running:
    
    screen.fill((0,0,0))
    #background
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerX_change = -1           
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready" :
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
               
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                 
    playerX += playerX_change
    
    for i in range (num_of_enemies) :   
        if enemyY[i] > 200 :
            for j in range (num_of_enemies) :
                enemyY[j] = 2000
            game_over_text(200,250)
            break   

    enemyX[i] += enemyX_change[i]  
    
    if enemyX[i] <= 0 :
        enemyX_change[i] = 0.175
        enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
        enemyX_change[i] = - 0.175
        enemyY[i] += enemyY_change[i] 

    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

    if collision :
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        enemyX[i] = random.randint(0,736)
        enemyY[i] = random.randint(50,150)
        
    enemy(enemyX[i],enemyY[i],i)
    
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    if bullet_state is "fire" :
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change 
    if bulletY <=0 :
        bulletY = 480
        bullet_state = "ready"
    
   
    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update() 

# bin map dit thui  