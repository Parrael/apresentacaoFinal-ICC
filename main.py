# Imports das bibliotecas
import pygame
import random
import requests
from io import BytesIO

# Inicializa o Pygame
pygame.init()

# Configura a janela do jogo
win_width, win_height = 800, 600
border_width = 10
win = pygame.display.set_mode((win_width + 2 * border_width, win_height + 2 * border_width))
pygame.display.set_caption("Jogo da Cobrinha")


# Define cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Configurações do jogo
snake_block = 20
snake_speed = 10

# URL da imagem da comida online (Logo do ICMC)
food_image_url = 'https://web.icmc.usp.br/SCAPINST/identidade_visual/logomarca/NO%20ICMC%20CMYK.png'


# Função para carregar a imagem da web
def load_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = pygame.image.load(BytesIO(response.content))
        return pygame.transform.scale(image, (snake_block, snake_block))
    else:
        print("Não foi possível carregar a imagem.")
        return None


# Carrega a imagem da comida
food_image = load_image_from_url(food_image_url)


# Função para desenhar a borda ao redor da janela
def draw_window_border():
    pygame.draw.rect(win, WHITE, (0, 0, win_width + 2 * border_width, border_width))  # Topo
    pygame.draw.rect(win, WHITE, (0, 0, border_width, win_height + 2 * border_width))  # Esquerda
    pygame.draw.rect(win, WHITE, (0, win_height + border_width, win_width + 2 * border_width, border_width))  # Baixo
    pygame.draw.rect(win, WHITE, (win_width + border_width, 0, border_width, win_height + 2 * border_width))  # Direita


# Função para desenhar a cobra na tela
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, GREEN, [x[0], x[1], snake_block, snake_block])


# Função para facilitar a exibição das mensagens de alerta
def message_to_screen(msg, color, size, y_displace=0):
    font = pygame.font.Font(None, size)
    lines = msg.splitlines()
    total_height = len(lines) * font.get_linesize()  # Calcula a altura total do texto
    text_y = (win_height / 2) - (total_height / 2) + y_displace  # Posição vertical do texto

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(win_width / 2, text_y))
        win.blit(text_surface, text_rect)
        text_y += font.get_linesize()  # Move para a próxima linha


# Loop principal que faz o jogo funcionar
def game_loop():
    game_over = False
    game_close = False

    x1 = win_width / 2
    y1 = win_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, win_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, win_height - snake_block) / 20.0) * 20.0

    clock = pygame.time.Clock()

    while not game_over:
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Atualiza posição da cobra
        x1 += x1_change
        y1 += y1_change

        # Verifica se a cobra atingiu as bordas
        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            game_over = True

        # Verifica colisão da cobra com ela mesma
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        # Desenha a comida
        win.fill(BLACK)
        if food_image:
            win.blit(food_image, (foodx, foody))
        else:
            pygame.draw.rect(win, RED, [foodx, foody, snake_block, snake_block])

        # Desenha a cobra
        draw_snake(snake_list)

        # Desenha a borda após desenhar os objetos
        draw_window_border()

        # Atualiza a tela
        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, win_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, win_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1

        # Controla a velocidade do jogo
        clock.tick(snake_speed)

        # Verifica se o jogo acabou e exibe tela de game over
        if game_over:
            message_to_screen(
                "Você perdeu!\nPressione R para Reiniciar ou F para Fechar",
                RED, 35, -50)
            pygame.display.update()

            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            game_over = False
                            pygame.quit()  # Fecha o Pygame
                            quit()  # Sai do programa
                        if event.key == pygame.K_r:
                            game_loop()

    # Finaliza o Pygame e sai do programa
    pygame.quit()
    quit()


# Chama o loop principal do jogo
game_loop()
