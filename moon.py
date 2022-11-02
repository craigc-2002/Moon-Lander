import pygame
import math


class Moon:
    def __init__(self, game):
        self.game = game

        self.height_map = []
        self.display_points = []
        for i in range(100000):
            height = 200 + (90*math.sin(2*math.pi*0.001*i))
            self.height_map.append(height)
        self.display_offset = round((len(self.height_map) / 2)-self.game.window_width/2)
        self.init_offset = self.display_offset

    def draw(self):
        self.display_points = []
        for i in range(self.game.window_width):
            map_index = self.display_offset + i
            self.display_points.append((i, 720 - self.height_map[map_index]))

        pygame.draw.lines(self.game.screen, (255, 255, 255), False, self.display_points)

    def update(self):
        self.display_offset = self.init_offset + round(self.game.rocket.display_pos_delta)

    def check_index(self, next_step):
        index_ok = True
        if (self.display_offset + self.game.window_width + next_step) > len(self.height_map):
            index_ok = False
        print(int(self.display_offset + self.game.window_width))
        return index_ok

    def get_height(self, x):
        index = round(x+len(self.height_map)/2)
        if 0 < index < len(self.height_map)-1:
            ground_height = self.height_map[index]
        else:
            ground_height = 0
        return ground_height
