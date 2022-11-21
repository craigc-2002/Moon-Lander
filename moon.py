import pygame
import perlin_noise
import random


class Moon:
    def __init__(self, game):
        self.game = game

        self.p = perlin_noise.PerlinNoise(octaves=3, seed=random.randint(0,1000))

        self.height_map = []
        self.display_points = []

        self.display_offset = -round(self.game.window_width / 2)
        self.init_offset = self.display_offset

    def load(self, n: int = 0, start_point: int = 0):
        """
        Method to generate the height map for the moon. Generates as many points as passed in by n and appends to the
        height map to enable map to be generated in stages
        :param n:
        :param start_point:
        """
        for i in range(n):
            index = (i + start_point)*0.0005
            perlin_val = 500*self.p(index)
            height = 150 + perlin_val
            self.height_map.append(height)

        self.display_offset += n//2
        self.init_offset = self.display_offset

    def draw(self):
        self.display_points = []
        for i in range(self.game.window_width):
            map_index = self.display_offset + i
            if len(self.height_map)-1 > map_index > 0:
                self.display_points.append((i, 720 - self.height_map[map_index] - self.game.rocket.display_height_delta))
            else:
                self.display_points.append((i, 720))

        pygame.draw.lines(self.game.screen, (255, 255, 255), False, self.display_points)

    def update(self):
        self.display_offset = self.init_offset + round(self.game.rocket.display_pos_delta)

    def get_height(self, x):
        index = round(x)
        # index = round(x+len(self.height_map)/2)
        if 0 < index < len(self.display_points)-1:
            ground_height = 720 - self.display_points[index][1] - self.game.rocket.display_height_delta
        else:
            ground_height = 0
        return ground_height
