##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.5                      ###
##############################################################
### Meteoro com velocidades diferentes e tiro funcional!   ###
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
pygame.display.set_caption("🚀 Space Escape - Alpha 0.5")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ----------------------------------------------------------
# ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "laser": "laser.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_shoot": "shoot.wav",
    "music": "distorted-future-363866.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 80)
GRAY = (40, 40, 40)

# ----------------------------------------------------------
# FUNÇÕES
# ----------------------------------------------------------
def load_image(filename, fallback_color, size=None):
    """Carrega imagem com fallback seguro."""
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
    """Carrega som com fallback silencioso."""
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
laser_img = load_image(ASSETS["laser"], YELLOW, (10, 20))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
sound_shoot = load_sound(ASSETS["sound_shoot"])

# Música segura
if os.path.exists(ASSETS["music"]):
    try:
        pygame.mixer.music.load(ASSETS["music"])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

# ----------------------------------------------------------
# VARIÁVEIS DO JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

# Meteoros com velocidades diferentes
meteor_list = []
for _ in range(6):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-600, -40)
    speed = random.randint(3, 8)
    meteor_list.append({"rect": pygame.Rect(x, y, 40, 40), "speed": speed})

# Tiros
lasers = []
laser_speed = 10

score = 0
lives = 3

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# ----------------------------------------------------------
# LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_rect = laser_img.get_rect(center=(player_rect.centerx, player_rect.top))
                lasers.append(laser_rect)
                if sound_shoot:
                    sound_shoot.play()

    # MOVIMENTO DO PLAYER
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # MOVIMENTO DOS TIROS
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < -20:
            lasers.remove(laser)

    # MOVIMENTO DOS METEOROS
    for meteor in meteor_list:
        rect = meteor["rect"]
        rect.y += meteor["speed"]

        # Saiu da tela
        if rect.y > HEIGHT:
            rect.y = random.randint(-300, -40)
            rect.x = random.randint(0, WIDTH - rect.width)
            meteor["speed"] = random.randint(3, 8)
            score += 1
            if sound_point:
                sound_point.play()

        # Colisão com jogador
        if rect.colliderect(player_rect):
            lives -= 1
            rect.y = random.randint(-300, -40)
            rect.x = random.randint(0, WIDTH - rect.width)
            meteor["speed"] = random.randint(3, 8)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

        # Colisão com tiros
        for laser in lasers[:]:
            if rect.colliderect(laser):
                lasers.remove(laser)
                score += 5
                rect.y = random.randint(-300, -40)
                rect.x = random.randint(0, WIDTH - rect.width)
                meteor["speed"] = random.randint(3, 8)

    # DESENHO
    screen.blit(player_img, player_rect)

    for meteor in meteor_list:
        screen.blit(meteor_img, meteor["rect"])

    for laser in lasers:
        screen.blit(laser_img, laser)

    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

# ----------------------------------------------------------
# FIM DO JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
