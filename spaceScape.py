##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.9                      ###
##############################################################
### TELA DE VITÓRIA + TELA DE DERROTA + INSERT COIN        ###
###      + METEORO DE VIDA (EXTRA LIFE METEOR)             ###
###      + METEORO DE DANO AUMENTADO (FATAL METEOR)        ###
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
    "meteor_life": "meteoroVerde.png",  # <-- meteoro especial: +1 vida
    "meteor_fatal": "meteoroVermelho.png",  # <-- NOVO meteoro: -2 vidas
    "laser": "laser.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_shoot": "shoot.wav",
    "sound_coin": "insert_coin.wav",
    "sound_life": "somVida.mp3",  # <-- som opcional
    "music": "distorted-future-363866.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 80)
GREEN = (80, 255, 80)
GRAY = (40, 40, 40)
DARK_RED = (150, 0, 0)  # Cor para o fallback do meteoro fatal


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
meteor_fatal_img = load_image(ASSETS["meteor_fatal"], DARK_RED, (50, 50))  # NOVO meteoro fatal
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
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE / INSERT COIN", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 350))

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
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 150))

        pts = font.render(f"Pontuação final: {score}", True, WHITE)
        screen.blit(pts, (WIDTH // 2 - pts.get_width() // 2, 250))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE TO RESTART", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 400))

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
        screen.blit(win, (WIDTH // 2 - win.get_width() // 2, 150))

        pts = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(pts, (WIDTH // 2 - pts.get_width() // 2, 250))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESS SPACE TO CONTINUE", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


# ----------------------------------------------------------
# FUNÇÃO AUXILIAR PARA CRIAR NOVO METEORO (RESET/REAPARECIMENTO)
# ----------------------------------------------------------
def create_new_meteor(rect_width, rect_height):
    """Gera um dicionário para um novo meteoro, escolhendo o tipo aleatoriamente."""
    x = random.randint(0, WIDTH - rect_width)
    y = random.randint(-400, -40)
    speed = random.randint(3, 8)

    # Lógica de probabilidade para os tipos de meteoro
    chance = random.randint(1, 100)
    if chance <= 8:  # 8% de chance (1 em 12.5) para meteoro de vida
        tipo = "life"
        # Ajusta tamanho para imagem do meteoro de vida
        rect = pygame.Rect(x, y, 45, 45)
    elif chance >= 98:  # 2% de chance (1 em 50) para meteoro fatal
        tipo = "fatal"
        # Ajusta tamanho para imagem do meteoro fatal
        rect = pygame.Rect(x, y, 50, 50)
    else:  # Chance restante para meteoro normal
        tipo = "normal"
        # Ajusta tamanho para imagem do meteoro normal
        rect = pygame.Rect(x, y, 40, 40)

    return {
        "rect": rect,
        "speed": speed,
        "type": tipo
    }


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
    # Cria o número inicial de meteoros usando a nova função
    for _ in range(6):
        meteor_list.append(create_new_meteor(40, 40))  # O tamanho inicial aqui é um chute seguro

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
        for i, meteor in enumerate(meteor_list):
            rect = meteor["rect"]
            rect.y += meteor["speed"]

            # --- Reset meteoro ---
            if rect.y > HEIGHT:

                # Se for um meteoro normal que sai da tela, ganha 1 ponto
                if meteor["type"] == "normal":
                    score += 1
                    if sound_point:
                        sound_point.play()

                # Substitui o meteoro por um novo (novo tipo e nova posição)
                meteor_list[i] = create_new_meteor(40, 40)  # O tamanho aqui é um chute seguro

            # --- COLISÃO COM O PLAYER ---
            if rect.colliderect(player_rect):

                if meteor["type"] == "normal":
                    lives -= 1
                    if sound_hit:
                        sound_hit.play()

                elif meteor["type"] == "life":
                    lives += 1
                    if sound_life:
                        sound_life.play()

                elif meteor["type"] == "fatal":
                    lives -= 2  # Tira 2 vidas
                    if sound_hit:
                        sound_hit.play()

                # Substitui o meteoro colidido por um novo
                meteor_list[i] = create_new_meteor(40, 40)

                if lives <= 0:
                    running = False
                    # O loop principal cuidará da tela de Game Over/Insert Coin
                    break

            # --- COLISÃO COM TIRO ---
            for laser in lasers[:]:
                if rect.colliderect(laser):
                    lasers.remove(laser)

                    if meteor["type"] == "normal":
                        score += 5

                    elif meteor["type"] == "life":
                        lives += 1
                        if sound_life:
                            sound_life.play()

                    # O meteoro fatal também deve ser destruído pelo tiro, mas não concede bônus
                    # ou penalidade de vida/pontos.
                    # elif meteor["type"] == "fatal":
                    #    pass

                    # Substitui o meteoro destruído por um novo
                    meteor_list[i] = create_new_meteor(40, 40)
                    break  # Sai do loop de lasers, pois o meteoro foi destruído

        if not running:
            break

        # VITÓRIA
        if score >= 1000:
            tela_vitoria(score)
            tela_insert_coin()
            running = False  # Sai do loop do jogo e volta para o loop principal

        # DESENHO
        screen.blit(player_img, player_rect)

        for meteor in meteor_list:
            if meteor["type"] == "life":
                screen.blit(meteor_life_img, meteor["rect"])
            elif meteor["type"] == "fatal":
                screen.blit(meteor_fatal_img, meteor["rect"])  # Desenha o meteoro fatal
            else:
                screen.blit(meteor_img, meteor["rect"])

        for laser in lasers:
            screen.blit(laser_img, laser)

        hud = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(hud, (10, 10))

        pygame.display.flip()

    # Lógica de fim de jogo após sair do loop 'while running'
    if lives <= 0:
        tela_game_over(score)
        tela_insert_coin()
    elif score >= 100:
        # Já passou pelas telas de vitória e insert coin
        pass