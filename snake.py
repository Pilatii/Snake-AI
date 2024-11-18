import pygame
from food import Food
import random

GREEN = (0, 255, 0)
BLUE = (0 , 0, 255)

class Snake():
    def __init__(self, screen, cell_size) -> None:
        
        # pygames attributes
        self.screen = screen
        self.cell_size = cell_size
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # snake attributes
        self.head = [screen.get_width() / 2, screen.get_height() / 2]
        self.body = [[self.head[0], self.head[1]]]
        self.size = 1
        self.food = Food(self.cell_size, screen)
        
    # Função responsavel por desenhar a cobra na tela
    def draw_snake(self):
        if len(self.body) > self.size:
            tail = self.body[0]
            pygame.draw.rect(self.screen, (255, 255, 255), [tail[0], tail[1], self.cell_size, self.cell_size])

        snake_length = len(self.body)
        
        #Desenha a cobra formando um gradiente
        for index, part in enumerate(self.body):
            ratio = index / (snake_length - 1) if snake_length > 1 else 0
            color = (
                int(GREEN[0] + (BLUE[0] - GREEN[0]) * ratio),
                int(GREEN[1] + (BLUE[1] - GREEN[1]) * ratio),
                int(GREEN[2] + (BLUE[2] - GREEN[2]) * ratio),
            )

            pygame.draw.rect(self.screen, color, [part[0], part[1], self.cell_size, self.cell_size])

        #Desenha uma borda em volta da corpo da cobra
        for index, part in enumerate(self.body):
            x, y = part
            adjacent_parts = {
                "left": [x - self.cell_size, y],
                "right": [x + self.cell_size, y],
                "up": [x, y - self.cell_size],
                "down": [x, y + self.cell_size]
            }

            if adjacent_parts["left"] not in self.body:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y + self.cell_size), 5)
            if adjacent_parts["right"] not in self.body:
                pygame.draw.line(self.screen, (0, 0, 0), (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 5)
            if adjacent_parts["up"] not in self.body:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + self.cell_size, y), 5)
            if adjacent_parts["down"] not in self.body:
                pygame.draw.line(self.screen, (0, 0, 0), (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 5)
    
    #retorna distancia euclidiana entre uma dada posição e a comida
    def get_distance_to_food(self, position):
        dist = pygame.math.Vector2(position[0], position[1]).distance_to((self.food.position[0], self.food.position[1]))
        return dist
    
    # Retorna a poxima posição da cabeça da cobra com base na posição atual
    # Os movimento da cobra são limitados de forma que garantem que ela
    # Sempre tenha um caminho ate a cauda e nunca bata em seu corpo ou em uma parede
    def get_next_position(self):
        allow = []
        
        x, y = self.head[0], self.head[1]
        
        # Use a função generate_arrows do "main" para entender melhor essa parte do codigo
        
        if x // self.cell_size % 2 == 0:
            if not y + self.cell_size == self.screen_width:
                allow.append([x, y + self.cell_size])
        else:
            if not y - self.cell_size < 0:
                allow.append([x, y - self.cell_size])
                
        if y // self.cell_size % 2 == 0:
            if not x - self.cell_size < 0:
                allow.append([x - self.cell_size, y])
        else:
            if not x + self.cell_size == self.screen_width:
                allow.append([x + self.cell_size, y])
        
        moves = []
        
        for move in allow:
            if move not in self.body:
                moves.append(move)      
        
        # Algumas vezes a distancias entres as posiveis posiçoes são iguas, fazendo com que, por conta
        # das limitaços nos movimentos da cobra, ela entre em um loop, entre quando a distancia ate a
        # comida for igual pra duas posiçoes, ela escolhera uma aleatoriamente
        if len(moves) > 1 and self.get_distance_to_food(moves[0]) == self.get_distance_to_food(moves[1]):
            next_move = moves[random.randint(0, 1)]
        else:
            next_move = min(moves, key=self.get_distance_to_food)
        
        return next_move
    
    # Fução principal da cobra, move, desenha, e pega a comida.
    def move_snake(self):
        
        self.get_food()
        self.draw_snake()
        self.food.draw_food()

        next_position = self.get_next_position()
        
        self.head[0] = next_position[0]
        self.head[1] = next_position[1]
        
        self.body.append([self.head[0], self.head[1]])
        
        if len(self.body) > self.size:
            del self.body[0]
    
    # Quando a cabeça e a comida da cobra estiverem na mesma posição aumenta o tamhno dela e gera uma nova posição pra comida       
    def get_food(self):
        if self.head[0] == self.food.position[0] and self.head[1] == self.food.position[1]:
            self.size += 1
        
            food_inside_snake = True
            
            while food_inside_snake:
                self.food.regenerate_food_positions()
                food_inside_snake = any(part == [self.food.position[0], self.food.position[1]] for part in self.body)