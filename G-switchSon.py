# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:19:31 2024

@author: busramercan
"""

import pygame
import sys

# Ekran boyutları
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Harita tanımı
MAP = [
    'X   X   X   X   X   X   X                X   X   X            X   X   X   X   X      X                X   X   X              X   X   X   X          X   X   X   X   X                                                          X   X   X                                      X   X   X   X   X   X                  X   X   X                   X   X   X   X               X   X   X   X                  X   X   X   X                     X   X              X   X   X                      ',
    '                                                                                                                                                                          X                                                                                                                                                     X             X                  X        X                                                                                                 X           ',
    '                       X                                                                                                                                                        X   X   X   X   X   X                                                           X   X                                                              X   X   X                         X                                                                                                          X    X  X        ',
    '                           X                                                                                                                      X   X   X                                                                                                                                                                                                                                                                                                                               X    ',   
    '                                              X   X   X   X   X                                                     X                                                                                    X   X   X             X                    X   X                                                                                                                               X   X   X   X                                                                                     X      ',
    '           X   X                                                                                                         X                                                                                                                                                                    X   X   X                                                                                                                     X   X   X   X                    X   X   X                    X       ',  
    '                                                                                        X                                     X                    X   X   X                             X   X   X                                                                                                                              X   X   X                                                                                                                                            X    X           ',
    '                                    X                                              X                                                                                              X                  X                                                                          X                                            X             X                  X   X                                                                                                              X            ',  
    '                                    X                                         X                                                                                              X                                                                       X   X                      X                                        X                    X                                                                                                                              X                ',
    'X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X   X        X   X   X   X   X   X   X   X   X   X   X   X   X                X   X   X            X   X   X   X                                X   X    X   X   X            X   X   X                         X   X   X   X                     X   X   X   X                          X   X   X              X   X   X   X                     X   X   X   X                             X   X   X   X   X   X                               ',          
]

# Map'in boyutlarını hesapla
map_width = len(MAP[0])
map_height = len(MAP)

# Blok boyutlarını hesapla
block_width = SCREEN_WIDTH // map_width * 44 
block_height = SCREEN_HEIGHT // map_height 

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, control_key, blocks):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.bottom = SCREEN_HEIGHT - 50
        self.speed = 5
        self.gravity = 6
        self.control_key = control_key
        self.gravity_direction = 1
        self.gravity_changed = False
        self.blocks = blocks
        self.distance = 0  # Oyuncunun ilerlediği mesafe

    def update(self):
        keys = pygame.key.get_pressed()

        # Yerçekimini değiştirme
        if keys[self.control_key] and not self.gravity_changed:
            self.gravity_direction *= -1
            self.gravity_changed = True

        # Yerçekimini değiştirirken tuşun bırakıldığını kontrol et
        if not keys[self.control_key]:
            self.gravity_changed = False

        # Yerçekimi uygula
        self.rect.y += self.gravity * self.gravity_direction

        # Ekran sınırlarını kontrol et
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Bloklarla çarpışma kontrolü
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        if collisions:
            for block in collisions: 
                if self.rect.right == block.rect.left:
                    self.rect.right = block.rect.left
                elif self.rect.left == block.rect.right:
                    self.rect.left = block.rect.right
                
        # Blokların sağına veya soluna çarpma kontrolü
        for block in self.blocks:
            if self.rect.colliderect(block.rect):
                if self.rect.centerx < block.rect.centerx:
                    self.rect.right = block.rect.left
                elif self.rect.centerx > block.rect.centerx:
                    self.rect.left = block.rect.right

        # Mesafeyi artır
        self.distance += self.speed

        # Ekran dışına çıkma kontrolü
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            return True
        return False

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, move_speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_speed = move_speed

    def update(self):
        self.rect.x -= self.move_speed
        if self.rect.right < 0:  # Eğer blok ekranın solundan çıkarsa, ekranın sağına geri koy
            self.rect.x = SCREEN_WIDTH

def create_moving_blocks(map_data):
    blocks = pygame.sprite.Group()
    block_image = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\engel1.png").convert_alpha()
    block_image = pygame.transform.scale(block_image, (block_width, block_height))
    
    y_pos = 0
    for row in map_data:
        x_pos = 0
        for char in row:
            if (char == 'X'):
                block = Block(x_pos, y_pos, block_width, block_height, block_image, move_speed=5)
                blocks.add(block)
            x_pos += block_width
        y_pos += block_height
    
    return blocks

def draw_scores(screen, player1, player2):
    font = pygame.font.SysFont(None, 36)
    score_text1 = font.render(f"Player 1 Distance: {player1.distance}", True, WHITE)
    score_text2 = font.render(f"Player 2 Distance: {player2.distance}", True, WHITE)
    screen.blit(score_text1, (20, 20))
    screen.blit(score_text2, (20, 60))

def draw_game_over(screen, message):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render(message, True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

def create_button(screen, image, x, y, w, h):
    screen.blit(image, (x, y, w, h))
    return pygame.Rect(x, y, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bir Ters Bir Düz Oyunu")

    # Arkaplan resmi yükleniyor
    background_image = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\backgr2.png").convert()
    background_rect = background_image.get_rect()

    # İkinci arka plan resmi ve dikdörtgeni
    background_image2 = background_image.copy()
    background_rect2 = background_rect.copy()
    background_rect2.x = background_rect.width

    # Oyuncu resimleri yükleniyor
    player1_image = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\oyuncu1.png").convert_alpha()
    player2_image = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\oyuncu2.png").convert_alpha()
    playerwidth = 64
    playerheight = 64
    player1_image = pygame.transform.scale(player1_image, (playerwidth, playerheight))
    player2_image = pygame.transform.scale(player2_image, (playerwidth, playerheight))

    # Hareketli bloklar oluşturuluyor
    blocks = create_moving_blocks(MAP)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(blocks)
    
    # Oyuncular oluşturuluyor
    start_x_pos = SCREEN_WIDTH // 2  # Center of the screen
    player1 = Player(player1_image, start_x_pos - playerwidth, pygame.K_SPACE, blocks)
    player2 = Player(player2_image, start_x_pos + playerwidth, pygame.K_x, blocks)
    
    all_sprites.add(player1)
    all_sprites.add(player2)

    # "Yeniden Oyna" buton resmi yükleniyor
    tryagain_img = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\tryyy.jpeg").convert_alpha()
    tryagainwidth = 200  # Genişlik ayarı
    tryagainheight = 50  # Yükseklik ayarı
    tryagain_img = pygame.transform.scale(tryagain_img, (tryagainwidth, tryagainheight))

    # "Çıkış" buton resmi yükleniyor
    exit_img = pygame.image.load(r"C:\Users\ASUS\Desktop\oyunprog\exit.jpeg").convert_alpha()
    exitwidth = 200  # Genişlik ayarı
    exitheight = 50  # Yükseklik ayarı
    exit_img = pygame.transform.scale(exit_img, (exitwidth, exitheight))

    clock = pygame.time.Clock()
    running = True

    # Zaman geçtikçe hızlanacak değişken
    speed_increase = 0.01
    speed = 4
    camera_x = 0  # Kamera pozisyonu

    game_over = False
    game_over_message = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            all_sprites.update()
            
            # İlk arka plan resmini ekrana çiz
            screen.blit(background_image, (background_rect.x - camera_x, 0))
            # İkinci arka plan resmini ekrana çiz
            screen.blit(background_image2, (background_rect2.x - camera_x, 0))

            # İlk arka plan resmini kaydır
            background_rect.x -= speed
            # İkinci arka plan resmini kaydır
            background_rect2.x -= speed

            # Eğer birinci arka plan resmi ekranın sol tarafından tamamen çıkarsa,
            # ekranın sağ tarafına taşı
            if background_rect.right - camera_x <= 0:
                background_rect.x = background_rect2.right

            # Eğer ikinci arka plan resmi ekranın sol tarafından tamamen çıkarsa,
            # ekranın sağ tarafına taşı
            if background_rect2.right - camera_x <= 0:
                background_rect2.x = background_rect.right

            # Zaman geçtikçe hızı artır
            speed += speed_increase
            
            if speed > 14:
                speed = 14

            # Kamera konumunu güncelle
            camera_x += speed

            # Oyuncuların ekran dışına çıkma kontrolü
            player1_lost = player1.update()
            player2_lost = player2.update()

            if player1_lost and player2_lost:
                game_over = True
                game_over_message = "Berabere!"
            elif player1_lost:
                game_over = True
                game_over_message = "Player 1 lost!"
            elif player2_lost:
                game_over = True
                game_over_message = "Player 2 lost!"

            all_sprites.draw(screen)  # Tüm sprite'lar ekrana çiziliyor
            draw_scores(screen, player1, player2)  # Skorları çiz
        else:
            draw_game_over(screen, game_over_message)
            tryagain_button_rect = create_button(screen, tryagain_img, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, tryagainwidth, tryagainheight)
            exit_button_rect = create_button(screen, exit_img, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, exitwidth, exitheight)

            # Yeniden oyna ve çıkış butonlarına tıklama kontrolü
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if tryagain_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                main()  # Oyunu yeniden başlat

            if exit_button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()