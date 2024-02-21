import pygame
WHITE, RED, GREEN, BLUE, BLACK, ORANGE = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 165, 0)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_menu(title_font, small_font, WIDTH, HEIGHT, screen):
    screen.fill(BLACK)
    draw_text('Trabalho de IA', title_font, WHITE, screen, WIDTH//2, HEIGHT//3)
    draw_text('Clique para iniciar', small_font, WHITE, screen, WIDTH//2, HEIGHT//2)

    draw_text('Desenvolvido por:', small_font, WHITE, screen, WIDTH//2, 250)
    draw_text('Lucas Cruz - olucas', small_font, WHITE, screen, WIDTH//2, 300)
    draw_text('Adriano Henrique - AA Games', small_font, WHITE, screen, WIDTH//2, 325)
    draw_text('Júlio Cesar - mago do bolo', small_font, WHITE, screen, WIDTH//2, 350)
    # draw_text('olucas | AA Games | Mago do bolo', small_font, WHITE, screen, WIDTH//2, 450)
    
