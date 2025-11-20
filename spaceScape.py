##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Beta 1.0                       ###
##############################################################
###       3 FASES DISTINTAS (DIFICULDADE PROGRESSIVA)      ###
###       + METEORO FATAL VERDE (DANO -2)                  ###
##############################################################

import pygame
import random
import os
import time  # Adicionar para controle de tempo na transição

pygame.init()

# ----------------------------------------------------------
# CONFIGURAÇÕES GLOBAIS
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape - Fases")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ----------------------------------------------------------
# CONFIGURAÇÕES POR FASE
# ----------------------------------------------------------
# Define os parâmetros de cada fase para controle de dificuldade
GAME_SETTINGS = {
    1: {
        "score_to_next": 50,
        "player_speed": 7,
        "meteor_count": 5,
        "meteor_min_speed": 3,
        "meteor_max_speed": 7,
        "bg_music": "distorted-future-363866.mp3",
        "background_img": "fundo_espacial.png"
    },
    2: {
        "score_to_next": 200,  # 50 + 70
        "player_speed": 6,  # Player mais lento
        "meteor_count": 8,  # Mais meteoros
        "meteor_min_speed": 5,
        "meteor_max_speed": 9,  # Meteoros mais rápidos
        "bg_music": "somFase2.mp3",
        "background_img": "fundo_fase2.jpg"
    },
    3: {
        "score_to_next": 400,  # 120 + 130 (Fase final)
        "player_speed": 5,  # Player mais lento ainda
        "meteor_count": 10,  # Máximo de meteoros
        "meteor_min_speed": 7,
        "meteor_max_speed": 11,  # Meteoros muito rápidos
        "bg_music": "somfase3.mp3",
        "background_img": "fundo_fase3.jpg"
    }
}

# ----------------------------------------------------------
# ASSETS
# ----------------------------------------------------------
ASSETS = {
    # Arquivos de imagem serão carregados dinamicamente para o background
    "background_default": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "meteor_life": "meteoroVerde.png",  # Meteoro +1 vida (mantido)
    "meteor_fatal_asset": "meteoroVermelho.png",  # NOVO: Usa a imagem verde do usuário para o Fatal
    "laser": "laser.png",

    # Sons
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_shoot": "shoot.mp3",
    "sound_coin": "insert_coin.wav",
    "sound_life": "life_up.wav",
    "sound_phase_up": "phase_up.wav",  # Troque por um arquivo real (som de transição)

    # Músicas (A música de fundo será definida pelo GAME_SETTINGS)
    "music_default": "distorted-future-363866.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 80)
GREEN = (80, 255, 80)
PURPLE = (150, 0, 150)  # Cor para o meteoro fatal
GRAY = (40, 40, 40)


# ----------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO E MÚSICA
# ----------------------------------------------------------
def load_image(filename, fallback_color, size=None):
    # Tenta carregar a imagem. Se falhar, cria uma superfície colorida.
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
    print(f"Aviso: Não foi possível carregar {filename}. Usando cor de fallback.")
    return surf


def load_sound(filename):
    if os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except:
            return None
    return None


def play_phase_music(filename):
    """Carrega e toca a música de fundo da fase."""
    if os.path.exists(filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except:
            print(f"Aviso: Não foi possível tocar a música {filename}.")
            pass
    elif os.path.exists(ASSETS["music_default"]):
        try:
            pygame.mixer.music.load(ASSETS["music_default"])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass


# ----------------------------------------------------------
# CARREGAMENTO DE ASSETS FIXOS
# ----------------------------------------------------------
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))
meteor_life_img = load_image(ASSETS["meteor_life"], GREEN, (45, 45))
# Carrega a imagem fornecida pelo usuário para o meteoro fatal
meteor_fatal_img = load_image(ASSETS["meteor_fatal_asset"], PURPLE, (50, 50))
laser_img = load_image(ASSETS["laser"], YELLOW, (10, 20))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
sound_shoot = load_sound(ASSETS["sound_shoot"])
sound_coin = load_sound(ASSETS["sound_coin"])
sound_life = load_sound(ASSETS["sound_life"])
sound_phase_up = load_sound(ASSETS["sound_phase_up"])

font_big = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 60)

clock = pygame.time.Clock()


# ----------------------------------------------------------
# TELAS DO JOGO
# ----------------------------------------------------------
def tela_insert_coin():
    blink = 0
    pygame.mixer.music.stop()  # Garante que a música pare

    # Carrega o background inicial
    background = load_image(ASSETS["background_default"], GRAY, (WIDTH, HEIGHT))

    while True:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        title = font_big.render("SPACE ESCAPE", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESSIONE ESPAÇO / INSERT COIN", True, WHITE)
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


def tela_game_over(score, max_phase):
    blink = 0
    pygame.mixer.music.stop()

    while True:
        clock.tick(FPS)
        screen.fill((20, 0, 0))

        over = font_big.render("GAME OVER", True, RED)
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 150))

        pts = font.render(f"Pontuação final: {score}", True, WHITE)
        screen.blit(pts, (WIDTH // 2 - pts.get_width() // 2, 250))

        phase_msg = font.render(f"Fase Alcançada: {max_phase}", True, YELLOW)
        screen.blit(phase_msg, (WIDTH // 2 - phase_msg.get_width() // 2, 300))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESSIONE ESPAÇO PARA REINICIAR", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def tela_vitoria(score):
    blink = 0
    pygame.mixer.music.stop()

    while True:
        clock.tick(FPS)
        screen.fill((0, 30, 0))

        win = font_big.render("VITÓRIA TOTAL!", True, YELLOW)
        screen.blit(win, (WIDTH // 2 - win.get_width() // 2, 150))

        pts = font.render(f"Pontuação: {score}", True, WHITE)
        screen.blit(pts, (WIDTH // 2 - pts.get_width() // 2, 250))

        win_msg = font_medium.render("VOCÊ SALVOU A GALÁXIA!", True, GREEN)
        screen.blit(win_msg, (WIDTH // 2 - win_msg.get_width() // 2, 320))

        blink += 1
        if (blink // 30) % 2 == 0:
            msg = font.render("PRESSIONE ESPAÇO PARA REINICIAR", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def tela_transicao(phase_number):
    """Efeito de tela para mudança de fase."""
    if sound_phase_up:
        sound_phase_up.play()

    # Efeito de flash
    for alpha in range(0, 255, 10):
        screen.fill((0, 0, 0))  # Desenha preto antes do flash

        flash_surf = pygame.Surface((WIDTH, HEIGHT))
        flash_surf.fill(WHITE)
        flash_surf.set_alpha(alpha)
        screen.blit(flash_surf, (0, 0))

        msg = font_big.render(f"FASE {phase_number}", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    # Tempo de pausa com a mensagem
    time.sleep(1.5)

    # Efeito de fade out
    for alpha in range(255, 0, -10):
        # Redesenha a tela preta com o texto
        screen.fill((0, 0, 0))

        msg = font_big.render(f"FASE {phase_number}", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))

        # Adiciona a camada escura
        fade_surf = pygame.Surface((WIDTH, HEIGHT))
        fade_surf.fill((0, 0, 0))
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------------
# FUNÇÃO AUXILIAR PARA CRIAR NOVO METEORO (RESET/REAPARECIMENTO)
# ----------------------------------------------------------
def create_new_meteor(phase_settings):
    """Gera um dicionário para um novo meteoro, escolhendo o tipo e velocidade da fase."""

    # Velocidade baseada na fase
    min_speed = phase_settings["meteor_min_speed"]
    max_speed = phase_settings["meteor_max_speed"]

    speed = random.randint(min_speed, max_speed)

    # Lógica de probabilidade para os tipos de meteoro
    chance = random.randint(1, 100)

    if chance <= 8:  # 8% de chance (1 em 12.5) para meteoro de vida
        tipo = "life"
        # Ajusta o tamanho da rect para a imagem de vida
        rect = pygame.Rect(0, 0, 45, 45)
    elif chance >= 95:  # 5% de chance (1 em 20) para meteoro fatal
        tipo = "fatal"
        # Ajusta o tamanho da rect para a imagem fatal
        rect = pygame.Rect(0, 0, 50, 50)
    else:  # Chance restante (87%) para meteoro normal
        tipo = "normal"
        # Ajusta o tamanho da rect para a imagem normal
        rect = pygame.Rect(0, 0, 40, 40)

    # Define a posição inicial acima da tela
    rect.x = random.randint(0, WIDTH - rect.width)
    rect.y = random.randint(-400, -40)

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
# INICIA O LOOP PRINCIPAL DO JOGO
# ----------------------------------------------------------
while True:

    # VARIÁVEIS DE ESTADO GLOBAL
    score = 0
    lives = 3
    max_phase_reached = 1
    current_phase = 1
    running = True

    # Inicializa a primeira fase
    phase_settings = GAME_SETTINGS[current_phase]

    # Carrega assets de fase (background e música)
    background = load_image(phase_settings["background_img"], GRAY, (WIDTH, HEIGHT))
    play_phase_music(phase_settings["bg_music"])

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    lasers = []
    laser_speed = 10

    # Inicializa os meteoros da primeira fase
    meteor_list = []
    for _ in range(phase_settings["meteor_count"]):
        meteor_list.append(create_new_meteor(phase_settings))

    # ------------------------------------------------------
    # LOOP DO JOGO
    # ------------------------------------------------------
    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # --------------------------------------------------
        # TRANSIÇÃO DE FASE
        # --------------------------------------------------
        if score >= phase_settings["score_to_next"] and current_phase < len(GAME_SETTINGS):

            # Pausa o jogo e exibe a transição
            tela_transicao(current_phase + 1)

            # Atualiza para a próxima fase
            current_phase += 1
            max_phase_reached = current_phase
            phase_settings = GAME_SETTINGS[current_phase]

            # Aplica novas configurações
            player_rect = player_img.get_rect(
                center=(player_rect.centerx, player_rect.centery))  # Reseta a nave na mesma posição
            player_speed = phase_settings["player_speed"]

            # Carrega novos assets de fase
            background = load_image(phase_settings["background_img"], GRAY, (WIDTH, HEIGHT))
            play_phase_music(phase_settings["bg_music"])

            # Reinicia a lista de meteoros com a nova contagem e dificuldade
            meteor_list.clear()
            for _ in range(phase_settings["meteor_count"]):
                meteor_list.append(create_new_meteor(phase_settings))

        elif score >= phase_settings["score_to_next"] and current_phase == len(GAME_SETTINGS):
            # Condição de vitória final
            tela_vitoria(score)
            tela_insert_coin()
            running = False  # Sai do loop do jogo
            break

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
        player_speed = phase_settings["player_speed"]  # Obtém a velocidade da fase atual

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

            # --- Reset meteoro (Saiu da tela) ---
            if rect.y > HEIGHT:

                # Se for um meteoro normal que sai da tela, ganha 1 ponto
                if meteor["type"] == "normal":
                    score += 1
                    if sound_point:
                        sound_point.play()

                # Substitui o meteoro por um novo (novo tipo e nova posição)
                meteor_list[i] = create_new_meteor(phase_settings)

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
                    lives -= 2  # Tira 2 vidas!
                    if sound_hit:
                        sound_hit.play()

                # Substitui o meteoro colidido por um novo
                meteor_list[i] = create_new_meteor(phase_settings)

                if lives <= 0:
                    running = False
                    break  # Sai do loop do jogo para ir para a tela de Game Over

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

                    # Meteoro Fatal (verde) e Meteoro Normal dão 5 pontos ao serem destruídos.
                    elif meteor["type"] == "fatal":
                        score += 5

                        # Substitui o meteoro destruído por um novo
                    meteor_list[i] = create_new_meteor(phase_settings)
                    break  # Sai do loop de lasers, pois o meteoro foi destruído

        if not running:
            break

        # DESENHO
        screen.blit(player_img, player_rect)

        for meteor in meteor_list:
            if meteor["type"] == "life":
                screen.blit(meteor_life_img, meteor["rect"])
            elif meteor["type"] == "fatal":
                screen.blit(meteor_fatal_img, meteor["rect"])  # Desenha o meteoro fatal (verde do usuário)
            else:
                screen.blit(meteor_img, meteor["rect"])

        for laser in lasers:
            screen.blit(laser_img, laser)

        # HUD
        hud = font.render(f"PONTOS: {score}   VIDAS: {lives}   FASE: {current_phase}", True, WHITE)
        screen.blit(hud, (10, 10))

        # Exibir meta da fase atual (opcional, para visualização do jogador)
        goal_msg = font.render(f"Meta: {phase_settings['score_to_next']}", True, YELLOW)
        screen.blit(goal_msg, (WIDTH - goal_msg.get_width() - 10, 10))

        pygame.display.flip()

    # --- FIM DO LOOP DO JOGO ---

    # Gerencia Game Over (após sair do loop)
    if lives <= 0:
        tela_game_over(score, max_phase_reached)
        tela_insert_coin()
    # Se saiu por outro motivo (Vitória Final), já cuidou das telas.