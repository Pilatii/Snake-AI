import pygame
from snake import Snake

# pygame config
SCREEN_SIZE  = 800
GAME_SPEED = 10
CELL_SIZE = 40

pygame.init()
pygame.display.set_caption("Snake")
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
CLOCK = pygame.time.Clock()

# Colors
BLACK = (0, 0 ,0)
GRAY = (211,211,211)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)

# A função generate_arrows tem o objeto de ajudar a visualizar quais são os posiveis movimento da cobra em cada casa
arrow_image = pygame.image.load('arrow.png').convert_alpha()
arrow_image = pygame.transform.scale(arrow_image, (20, 20))

def draw_arrow(screen, angle, position):
    
    rotated_arrow = pygame.transform.rotate(arrow_image, angle)
    rect = rotated_arrow.get_rect(center=position)
    screen.blit(rotated_arrow, rect.topleft)
    
def generate_arrows():
    for x in range(0, SCREEN_SIZE, CELL_SIZE): 
        for y in range(0, SCREEN_SIZE, CELL_SIZE):
            if x // CELL_SIZE % 2 == 0:
                if not y + CELL_SIZE == SCREEN_SIZE:
                    draw_arrow(SCREEN, 0, (x + CELL_SIZE // 2, (y + CELL_SIZE // 2) + 10))
            else:
                if not y - CELL_SIZE < 0:
                    draw_arrow(SCREEN, 180, (x + CELL_SIZE // 2, (y + CELL_SIZE // 2) - 10))
                    
            if y // CELL_SIZE % 2 == 0:
                if not x - CELL_SIZE < 0:
                    draw_arrow(SCREEN, -90, ((x + CELL_SIZE // 2) - 10, y + CELL_SIZE // 2))
            else:
                if not x + CELL_SIZE == SCREEN_SIZE:
                    draw_arrow(SCREEN, 90, ((x + CELL_SIZE // 2) + 10, y + CELL_SIZE // 2))
                    
# Gera a grid na tela ( apenas visual )
def generate_grid():
    grid_surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE))
    grid_surface.fill(WHITE)
    
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        for y in range(0, SCREEN_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(grid_surface, BLACK, rect, 1)
    
    return grid_surface

grid_surface = generate_grid()

# Game loop       
done = False
snake = Snake(SCREEN, CELL_SIZE)

while not done:
    
    pygame.event.get()
    SCREEN.fill(WHITE)
    SCREEN.blit(grid_surface, (0, 0))
    # generate_arrows()
    
    # "Pausa" o jogo quando a cobra ganha
    if len(snake.body) != 400:
        snake.move_snake()
    else:
        snake.draw_snake()
        
    pygame.display.update()
    CLOCK.tick(GAME_SPEED)