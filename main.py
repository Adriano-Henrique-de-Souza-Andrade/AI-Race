import pygame
import random
import numpy as np
from menu import draw_menu

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE, RED, GREEN, BLUE, BLACK, ORANGE = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 165, 0)

# Configurações do Agente e do Jogo
agent_size = 20
n_actions = 4  # cima, baixo, esquerda, direita
epsilon = 0.1
alpha = 0.1
gamma = 0.9
agent_points = 0
agent_points2 = 0
epochs = 0

# Estado é a posição do agente
state_size = (WIDTH // agent_size) * (HEIGHT // agent_size)
Q_table = np.zeros((state_size, n_actions))

# Fonte para texto
font = pygame.font.Font(None, 24)

# Converte posição para estado
def pos_to_state(pos):
    return (pos[1] // agent_size) * (WIDTH // agent_size) + (pos[0] // agent_size)

# Atualiza a tabela Q agente 1
def update_Q_table(state, action, reward, next_state):
    future = np.max(Q_table[next_state])
    Q_table[state, action] += alpha * (reward + gamma * future - Q_table[state, action])

# Escolhe uma ação usando a política ε-greedy
def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1)
    else:
        return np.argmax(Q_table[state])

# Configurações iniciais para o primeiro agente
agent_pos = [WIDTH // 4, HEIGHT // 4]
agent_pos2 = [WIDTH // 4, HEIGHT // 4]
goal_pos = [WIDTH * 3 // 4, HEIGHT * 3 // 4]
obstacle_pos = [WIDTH // 2, HEIGHT // 2]

# Função para calcular a distância entre duas posições
def calculate_distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Função para mover o primeiro agente
def move_agent(action):
    if action == 0 and agent_pos[1] > 0:  # cima
        agent_pos[1] -= agent_size
    if action == 1 and agent_pos[1] < HEIGHT - agent_size:  # baixo
        agent_pos[1] += agent_size
    if action == 2 and agent_pos[0] > 0:  # esquerda
        agent_pos[0] -= agent_size
    if action == 3 and agent_pos[0] < WIDTH - agent_size:  # direita
        agent_pos[0] += agent_size

# Função para mover o segundo agente
def move_agent2(action):
    global agent_pos2
    if action == 0 and agent_pos2[1] > 0:  # cima
        agent_pos2[1] -= agent_size
    if action == 1 and agent_pos2[1] < HEIGHT - agent_size:  # baixo
        agent_pos2[1] += agent_size
    if action == 2 and agent_pos2[0] > 0:  # esquerda
        agent_pos2[0] -= agent_size
    if action == 3 and agent_pos2[0] < WIDTH - agent_size:  # direita
        agent_pos2[0] += agent_size


def reset_agents():
    global agent_pos, agent_pos2, epochs
    agent_pos = [WIDTH // 4, HEIGHT // 4]  # Agente 1 volta para o início
    agent_pos2 = [WIDTH // 4, HEIGHT // 4]  # Agente 2 volta para o início
    epochs += 1
# Função para verificar se o primeiro agente atingiu o objetivo ou o obstáculo
def check_collision():
    global agent_pos, agent_pos2, reward, reward2, agent_points
    reward = -0.3  # Penalidade leve por movimento, para encorajar a eficiência
    distance_to_goal = calculate_distance(agent_pos, goal_pos)
    if agent_pos == goal_pos:
        agent_points += 1
        reward = 1  # Recompensa alta por alcançar o objetivo
        reward2 -= 1
        reset_agents()
    elif agent_pos == obstacle_pos:
        reward = -1  # Penalidade alta por colidir com o obstáculo
        reset_agents()
    elif agent_pos == agent_pos2:
        reward -= 0.5
    elif distance_to_goal < calculate_distance(agent_pos2, goal_pos):
        reward += 0.2  # Recompensa por se aproximar do objetivo
    return reward

# Função para verificar se o segundo agente atingiu o objetivo
def check_collision2():
    global agent_pos, agent_pos2, reward2, reward, agent_points2
    reward2 = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
    distance_to_goal = calculate_distance(agent_pos2, goal_pos)
    if agent_pos2 == goal_pos:
        agent_points2 += 1
        reward2 = 1  # Recompensa alta por alcançar o objetivo
        reward -= 1
        reset_agents()
    elif agent_pos2 == obstacle_pos:
        reward2 = -1  # Penalidade alta por colidir com o obstáculo
        reset_agents()
    elif agent_pos2 == agent_pos:
        reward2 -= 0.5
    elif distance_to_goal < calculate_distance(agent_pos, goal_pos):
        reward2 += 0.2
    return reward2

# Desenha os elementos do jogo
def draw_elements():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (*agent_pos, agent_size, agent_size))
    pygame.draw.rect(screen, ORANGE, (*agent_pos2, agent_size, agent_size))
    pygame.draw.rect(screen, GREEN, (*goal_pos, agent_size, agent_size))
    pygame.draw.rect(screen, RED, (*obstacle_pos, agent_size, agent_size))

    # Mostrar valores Q para o estado atual do primeiro agente
    state = pos_to_state(agent_pos)
    q_values = Q_table[state]
    q_text = font.render(f"Q-values (Azul): {q_values}", True, BLACK)
    screen.blit(q_text, (5, HEIGHT - 60))

    # Mostrar valores Q para o estado atual do segundo agente
    state2 = pos_to_state(agent_pos2)
    q_values2 = Q_table[state2]

    # Mostrar valores Q para o estado atual do primeiro agente
    epochs_text = font.render(f"Epocas: {epochs}", True, BLACK)
    screen.blit(epochs_text, (WIDTH - 100, 25))

    q_text2 = font.render(f"Q-values (Laranja): {q_values2}", True, BLACK)
    screen.blit(q_text2, (5, HEIGHT - 30))

    # Mostrar valores Q para o estado atual do primeiro agente
    q_text = font.render(f"Vitórias (Azul): {agent_points}", True, BLACK)
    screen.blit(q_text, (5, HEIGHT - 120))
    
    # Mostrar valores Q para o estado atual do segundo agente
    q_text2 = font.render(f"Vitórias (Laranja): {agent_points2}", True, BLACK)
    screen.blit(q_text2, (5, HEIGHT - 90))

    pygame.display.flip()


def game():
        # Movimento e atualização do primeiro agente
        current_state = pos_to_state(agent_pos)
        action = choose_action(current_state)
        move_agent(action)
        reward = check_collision()
        next_state = pos_to_state(agent_pos)
        update_Q_table(current_state, action, reward, next_state)

        # Movimento e atualização do segundo agente
        current_state2 = pos_to_state(agent_pos2)
        action2 = choose_action(current_state2)
        move_agent2(action2)
        reward2 = check_collision2()
        next_state2 = pos_to_state(agent_pos2)
        update_Q_table(current_state2, action2, reward2, next_state2)  # Corrigindo o nome da variável next_state2


        draw_elements()
# Loop principal do jogo
running = True
clock = pygame.time.Clock()

# Defina a fonte
title_font = pygame.font.Font(None, 52)
small_font = pygame.font.Font(None, 26)

state = "menu"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:    
            state = "game"

    if(state == "game"):
        game()
    
    if(state == "menu"):
        draw_menu(title_font, small_font,  WIDTH, HEIGHT ,screen)

    pygame.display.update()
    clock.tick(50)  # Controla a velocidade do jogo

pygame.quit()