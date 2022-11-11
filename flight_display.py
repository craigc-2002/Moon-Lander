import pygame
import vector as v


class ScaleDisplay:
    """
    Class to implement a scale display object that will be used to show the spacecraft's height, position, speed and throttle
    """
    def __init__(self, game, low_end, high_end, scale_range: tuple, middle_tick: bool = False):
        self.game = game

        self.low_end = low_end
        self.high_end = high_end
        self.middle_tick = middle_tick

        self.scale_range = scale_range
        self.display_value = scale_range[0]

    def update(self, new_value):
        if new_value > self.scale_range[1]:
            self.display_value = 1
        elif new_value < self.scale_range[0]:
            self.display_value = 0
        else:
            self.display_value = new_value / (self.scale_range[1]-self.scale_range[0])

    def draw(self):
        pygame.draw.line(self.game.screen, (255, 255, 255), self.low_end, self.high_end, 5)

        # Draw line ends
        pygame.draw.line(self.game.screen, (255, 255, 255), (self.low_end[0] - 10, self.low_end[1]),
                         (self.low_end[0] + 10, self.low_end[1]), 5)
        pygame.draw.line(self.game.screen, (255, 255, 255), (self.high_end[0] - 10, self.high_end[1]),
                         (self.high_end[0] + 10, self.high_end[1]), 5)
        if self.middle_tick:
            pygame.draw.line(self.game.screen, (255, 255, 255), (self.high_end[0] - 10, self.high_end[1]),
                             (self.high_end[0] + 10, self.high_end[1]), 5)

        # Draw value on scale
        display_pos = (self.low_end[0]-self.display_value*(self.low_end[0]-self.high_end[0]),
                       self.low_end[1]-self.display_value*(self.low_end[1]-self.high_end[1]))
        pygame.draw.circle(self.game.screen, (255, 0, 0), display_pos, 5)
