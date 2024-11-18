import random
import pygame

class Food():
    def __init__(self, food_size, screen) -> None:
        self.food_size = food_size
        self.food_color = (255, 0 , 0)
        self.screen = screen
        self.position =  self.generate_food_positions()

    def generate_food_positions(self):
        food_position_x = round(random.randrange(0, self.screen.get_width() - self.food_size) / 40.0) * 40.0
        food_position_y = round(random.randrange(0, self.screen.get_height() - self.food_size) / 40.0) * 40.0
    
        return food_position_x, food_position_y
    
    def regenerate_food_positions(self):
        self.position = self.generate_food_positions()

    def draw_food(self):
        pygame.draw.rect(self.screen, self.food_color, [self.position[0], self.position[1], self.food_size, self.food_size])