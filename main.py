# -*- coding: utf-8 -*-
"""
Created on Thu May 16 23:38:56 2024

@author: busramercan
"""

import pygame
import button
import os  # Importing os module to execute external scripts

# create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bir Ters Bir Düz Oyunu')

# load background image
background_img = pygame.image.load('backgr.png').convert()

# load button images
start_img = pygame.image.load('start.png').convert_alpha()
exit_img = pygame.image.load('exit.png').convert_alpha()

# Scale button images to the same size
button_width = 200
button_height = 234
start_img = pygame.transform.scale(start_img, (button_width, button_height))
exit_img = pygame.transform.scale(exit_img, (button_width, button_height))

# calculate positions for buttons to be side by side
start_button_x = (SCREEN_WIDTH - (button_width * 2)) // 3
exit_button_x = start_button_x + button_width + (SCREEN_WIDTH - (button_width * 2)) // 3
button_y = (SCREEN_HEIGHT - button_height) // 2

# create button instances
start_button = button.Button(start_button_x, button_y, start_img, 0.8)
exit_button = button.Button(exit_button_x, button_y, exit_img, 0.8)

# load player images
player1_img = pygame.image.load('oyuncu1.png').convert_alpha()
player2_img = pygame.image.load('oyuncu2.png').convert_alpha()

# calculate positions for player images
player_width = 100
player_height = 100
player1_x = 20
player2_x = 20
player_y = SCREEN_HEIGHT - player_height - 20

# Scale player images
player1_img = pygame.transform.scale(player1_img, (player_width, player_height))
player2_img = pygame.transform.scale(player2_img, (player_width, player_height))

# game loop
run = True
while run:
    # blit background image
    screen.blit(background_img, (0, 0))
    
    # draw buttons
    if start_button.draw(screen):
        # Execute aylinzip.py script
        os.execvp('python', ['python', 'G-switchSon.py'])
        #os.system('python aylinzip.py')
        
    if exit_button.draw(screen):
        run = False  # Set run to False to exit the game loop

    # blit player images
    screen.blit(player1_img, (player1_x, player_y))
    screen.blit(player2_img, (SCREEN_WIDTH - player_width - player2_x, player_y))

    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()