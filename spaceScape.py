##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.8                      ###
##############################################################
### TELA DE VITÓRIA + TELA DE DERROTA + INSERT COIN        ###
###      + METEORO DE VIDA (EXTRA LIFE METEOR)             ###
##############################################################

import pygame
import random
import os

pygame.init()

# ----------------------------------------------------------
# CONFIGURAÇÕES
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape - Victory & Game Over")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ----------------------------------------------------------
# ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "meteor_life": "meteoroVerde.png",  # <-- meteoro especial
    "laser": "laser.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_shoot": "shoot.wav",
    "sound_coin": "insert_coin.wav",
    "sound_life": "life_up.wav",  # <-- som opcional
    "music": "distorted-future-363866.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 80)
GREEN = (80, 255, 80)
GRAY = (40, 40, 40)

# ----------------------------------------------------------
# FUNÇÕES
# ----------------------------------------------------------
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except:
            pass
    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    if os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except:
            return None
    return None

# ----------------------------------------------------------
# CARREGAMENTO
# ----------------------------------------------------------
background = load_image(ASSETS["background"], GRAY, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))
meteor_life_img = load_image(ASSETS["meteor_life"], GREEN, (45, 45))  # meteoro especial
laser_img = load_image(ASSETS["laser"], YELLOW, (10, 20))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
sound_shoot = load_sound(ASSETS["sound_shoot"])
sound_coin = load_sound(ASSETS["sound_coin"])
sound_life = load_sound(ASSETS["sound_life"])

# Música de fundo
if os.path.exists(ASSETS["music"]):
    try:
        pygame.mixer.music.load(ASSETS["music"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

font_big = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# ----------------------------------------------------------
# TELA DE INTRODUÇÃO (INSERT COIN)
# ----------------------------------------------------------
def tela_insert_coin():
    blink = 0

    while True:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        title = font_big.render("SPACE ESCAPE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE / INSERT COIN", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if sound_coin:
                    sound_coin.play()
                return

        pygame.display.flip()

# ----------------------------------------------------------
# TELA DE DERROTA
# ----------------------------------------------------------
def tela_game_over(score):
    blink = 0

    while True:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        over = font_big.render("GAME OVER", True, RED)
        screen.blit(over, (WIDTH//2 - over.get_width()//2, 150))

        pts = font.render(f"Pontuação final: {score}", True, WHITE)
        screen.blit(pts, (WIDTH//2 - pts.get_width()//2, 250))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE TO RESTART", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# ----------------------------------------------------------
# TELA DE VITÓRIA
# ----------------------------------------------------------
def tela_vitoria(score):
    blink = 0

    while True:
        clock.tick(FPS)
        screen.fill((0, 30, 0))

        win = font_big.render("YOU WIN!", True, YELLOW)
        screen.blit(win, (WIDTH//2 - win.get_width()//2, 150))

        pts = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(pts, (WIDTH//2 - pts.get_width()//2, 250))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE TO CONTINUE", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# ----------------------------------------------------------
# INICIA NO INSERT COIN
# ----------------------------------------------------------
tela_insert_coin()

# ----------------------------------------------------------
# INICIA O JOGO
# ----------------------------------------------------------
while True:
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 7

    meteor_list = []
    for _ in range(6):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-600, -40)
        speed = random.randint(3, 8)

        # 1 em 8 meteoro é um meteoro de vida
        tipo = "life" if random.randint(1, 8) == 1 else "normal"

        meteor_list.append({
            "rect": pygame.Rect(x, y, 40, 40),
            "speed": speed,
            "type": tipo
        })

    lasers = []
    laser_speed = 10

    score = 0
    lives = 3
    running = True

    # ------------------------------------------------------
    # LOOP DO JOGO
    # ------------------------------------------------------
    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                laser_rect = laser_img.get_rect(center=(player_rect.centerx, player_rect.top))
                lasers.append(laser_rect)
                if sound_shoot:
                    sound_shoot.play()

        # MOVIMENTO PLAYER
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

        # TIROS
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.y < -20:
                lasers.remove(laser)

        # METEOROS
        for meteor in meteor_list:
            rect = meteor["rect"]
            rect.y += meteor["speed"]

            # Reset meteoro
            if rect.y > HEIGHT:
                rect.x = random.randint(0, WIDTH - rect.width)
                rect.y = random.randint(-300, -40)
                meteor["speed"] = random.randint(3, 8)
                meteor["type"] = "life" if random.randint(1, 8) == 1 else "normal"

                # pontos apenas meteoro normal
                if meteor["type"] == "normal":
                    score += 1
                    if sound_point:
                        sound_point.play()

            # COLISÃO COM O PLAYER
            if rect.colliderect(player_rect):
                if meteor["type"] == "normal":
                    lives -= 1
                    if sound_hit:
                        sound_hit.play()
                else:
                    lives += 1
                    if sound_life:
                        sound_life.play()

                rect.x = random.randint(0, WIDTH - rect.width)
                rect.y = random.randint(-300, -40)
                meteor["speed"] = random.randint(3, 8)

                if lives <= 0:
                    running = False
                    tela_game_over(score)
                    tela_insert_coin()

            # COLISÃO COM TIRO
            for laser in lasers[:]:
                if rect.colliderect(laser):
                    lasers.remove(laser)

                    if meteor["type"] == "normal":
                        score += 5
                    else:
                        lives += 1
                        if sound_life:
                            sound_life.play()

                    rect.x = random.randint(0, WIDTH - rect.width)
                    rect.y = random.randint(-300, -40)
                    meteor["speed"] = random.randint(3, 8)
                    meteor["type"] = "life" if random.randint(1, 8) == 1 else "normal"

        # VITÓRIA
        if score >= 1000:
            tela_vitoria(score)
            tela_insert_coin()

        # DESENHO
        screen.blit(player_img, player_rect)

        for meteor in meteor_list:
            if meteor["type"] == "life":
                screen.blit(meteor_life_img, meteor["rect"])
            else:
                screen.blit(meteor_img, meteor["rect"])

        for laser in lasers:
            screen.blit(laser_img, laser)

        hud = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(hud, (10, 10))

        pygame.display.flip()
