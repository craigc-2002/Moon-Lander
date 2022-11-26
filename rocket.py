"""
This file defines a Sprite class and Rocket class for use in the Moon Lander game
Rocket is a subclass of Sprite, which allows other game objects to be made with the same basic movement physics
"""

import pygame
import vector as v
import math


class Sprite:
    """
    Class to define the general behaviour of sprites in the game
    Stores the sprite's image and has methods to handle movement and collisions
    """

    def __init__(self, game, image, scale,
                 init_pos=(0, 0), init_velocity=(0, 0), init_angular_velocity=0, init_angle=0):
        """
        Constructor method for the sprite class.

        :param game:
        :param image:
        :param scale:
        :param init_pos:
        :param init_velocity:
        :param init_angular_velocity:
        """
        self.game = game
        self.screen_dims = pygame.display.get_window_size()
        self.scale = (scale[0], scale[1])

        self.image = image

        # Initialise vectors for position, velocity and acceleration
        self.position = v.vector(init_pos[0], init_pos[1])
        self.display_pos = self.display_coord_transform(self.position)
        self.velocity = v.vector(init_velocity[0], init_velocity[1])
        self.acceleration = v.vector()
        self.accelerating = False

        self.display_pos_delta = 0
        self.display_height_delta = 0

        # Initialise the angle and direction of the sprite
        self.direction = v.vector()  # A unit vector to represent the sprite's direction
        self._angle = 0  # Angle in radians clockwise from the y-axis (0 is pointing straight up)
        self.angle = init_angle
        self.angular_velocity = init_angular_velocity  # Angular velocity in rad/s
        self.rotating = 0

    def update(self):
        """
        Method to update the sprite by calculating its position for the next frame
        Uses Euler integration to calculate the updated position, velocity and rotation
        """
        dt = self.game.dt  # Simulation timestep

        # Integrate to get the new position and velocity
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.angle = self.angle + self.angular_velocity * dt

    def check_collision(self, other):
        """
        Method to check if the sprite has collided with another passed in as other.

        :param other:
        """
        collided = False

        if other.corners()[0][0] < self.position.x < other.corners()[2][0]:
            if other.corners()[0][1] < self.position.y < other.corners()[2][1]:
                collided = True

        return collided

    def corners(self):
        """
        Method to return a tuple of each of the sprite's corners.
        Starts from the top left, going clockwise
        :return corners:
        """
        c1 = (self.position.x - self.scale[0] / 2, self.position.y - self.scale[1] / 2)
        c2 = (self.position.x + self.scale[0] / 2, self.position.y - self.scale[1] / 2)
        c3 = (self.position.x + self.scale[0] / 2, self.position.y + self.scale[1] / 2)
        c4 = (self.position.x - self.scale[0] / 2, self.position.y + self.scale[1] / 2)
        corners = (c1, c2, c3, c4)
        return corners

    def draw(self):
        """
        Method to draw the sprite onto the screen
        """
        # Rotate image (angle is stored in radians clockwise from 0, has to be converted to degrees anticlockwise)
        scale = (self.scale[0] * self.game.scale[0], self.scale[1] * self.game.scale[1])
        scaled_image = pygame.transform.scale(self.image, scale)
        rotated_image = pygame.transform.rotate(scaled_image, self.angle * (-180 / math.pi))

        # Calculate where the rocket should be on screen
        self.display_pos = self.display_coord_transform(self.position, rotated_image.get_size())
        target_pos = self.display_pos

        # If it is too close to either edge then clamp it
        if 3 * self.screen_dims[0] / 4 < self.display_pos[0]:
            self.display_pos = (3 * self.screen_dims[0] / 4, self.display_pos[1])
        elif self.display_pos[0] < self.screen_dims[0] / 4:
            self.display_pos = (self.screen_dims[0] / 4, self.display_pos[1])

        # Calculate the horizontal offset
        self.display_pos_delta = target_pos[0] - self.display_pos[0]

        # Clamp the vertical display position
        if self.display_pos[1] < 150:
            self.display_pos = (self.display_pos[0], 150)

        elif self.display_pos[1] > 600:
            self.display_pos = (self.display_pos[0], 600)

        # Calculate the vertical offset
        self.display_height_delta = target_pos[1] - self.display_pos[1]

        # Draw image to screen
        self.game.screen.blit(rotated_image, self.display_pos)

    def display_coord_transform(self, coords, img_dims=(0, 0)):
        display_pos = (coords[0] + (self.screen_dims[0] / 2) - (img_dims[0] / 2),
                       self.screen_dims[1] - coords[1])
        return display_pos

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self.direction = v.vector(math.sin(new_angle), math.cos(new_angle))


class Rocket(Sprite):
    """
    Class to represent the rocket and give it some necessary methods
    Child class of Sprite
    """

    def __init__(self, game):
        start_pos = (0, 0)

        image = game.sprite_images["lander"]

        self.height = 0

        self.throttle = 0
        self.fuel = 100
        self.max_throttle = 50
        self.m = 25
        self.twr_max = self.max_throttle/self.m

        super().__init__(game, image, (75, 75), start_pos)

    def reset(self, position, velocity):
        """
        Method to reset the rocket's position on a new game
        """
        self.position = v.vector(position[0], position[1])
        self.velocity = v.vector(velocity[0], velocity[1])
        self.acceleration = v.vector()
        self.angle = 0
        self.height = 0
        self.display_pos_delta = 0
        self.display_height_delta = 0

        self.accelerating = False
        self.rotating = 0

        self.throttle = 0
        self.fuel = 100

        self.draw()

    def update(self):
        """
        Overloaded update method for the Rocket class. Sets the acceleration and angular velocity
        of the rocket depending on keyboard inout and current speed
        """
        self.height = self.position.y - self.game.moon.get_height(self.display_pos[0])
        dt = self.game.dt  # Simulation timestep

        if self.height <= 0:
            self.land()
            self.acceleration = v.vector()
            self.velocity = v.vector()
            self.position = v.vector(self.position.x, self.game.moon.get_height(self.display_pos[0]))
        else:
            self.acceleration = v.vector(0, -self.game.g)

            # Set angular velocity depending on whether the a or d keys have been pressed
            if self.rotating == 1:
                self.angular_velocity = -0.9
            elif self.rotating == 2:
                self.angular_velocity = 0.9
            else:
                self.angular_velocity = 0

        d_throttle = 2.5
        if self.fuel > 0:
            if self.accelerating:
                self.image = self.game.sprite_images["lander_flames"]
                self.throttle += d_throttle * self.max_throttle * dt
            else:
                self.image = self.game.sprite_images["lander"]
                self.throttle -= d_throttle * self.max_throttle * dt
            if self.throttle > self.max_throttle:
                self.throttle = self.max_throttle
            elif self.throttle < 0:
                self.throttle = 0
        else:
            self.image = self.game.sprite_images["lander"]
            self.throttle = 0

        twr = self.throttle / self.m
        self.acceleration += (self.direction * twr)
        self.fuel -= self.throttle * 0.015 * dt
        self.m = 10 + (15 * self.fuel/100)
        self.twr_max = self.max_throttle / self.m if self.fuel > 0 else 0

        self.rotating = 0
        self.accelerating = False
        super().update()

    def land(self):
        """
        Method called when the rocket lands to check whether it crashes
        """
        if self.velocity.mag > 25:
            self.image = self.game.sprite_images["explosion"]
            self.game.game_over("crash")
        else:
            self.image = self.game.sprite_images["lander"]
            self.game.game_over("safe")

    def move_forward(self):
        self.accelerating = True

    def turn_left(self):
        self.rotating = 1

    def turn_right(self):
        self.rotating = 2
