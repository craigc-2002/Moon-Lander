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

        # self.image = pygame.image.load(image_path)
        # self.image = self.image.convert_alpha(self.image)
        self.image = image

        # Initialise vectors for position, velocity and acceleration
        self.position = v.vector(init_pos[0], init_pos[1])
        self.display_pos = self.display_coord_transform(self.position)
        self.display_pos_delta = 0
        self.clamped_position = (0, 0)
        self.velocity = v.vector(init_velocity[0], init_velocity[1])
        self.acceleration = v.vector()
        self.accelerating = False

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

        self.check_edges()

    def check_edges(self):
        """
        Method to check whether the sprite has reached the edge of the screen and wrap it around if so
        """
        if self.screen_dims[0] < self.display_pos[0]:
            self.position = v.vector(0, self.position.y)

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
        position_fixed = False

        # If it is too close to either edge then clamp it
        if 3*self.screen_dims[0]/4 < self.display_pos[0]:
            self.display_pos = (3 * self.screen_dims[0] / 4, self.display_pos[1])

        elif self.display_pos[0] < self.screen_dims[0]/4:
            self.display_pos = (self.screen_dims[0] / 4, self.display_pos[1])

        # Calculate the difference between where the image should be and where it is
        self.display_pos_delta = target_pos[0] - self.display_pos[0]

        # Draw image to screen
        self.game.screen.blit(rotated_image, self.display_pos)

    def display_coord_transform(self, coords, img_dims=(0, 0)):
        display_pos = (coords[0] + (self.screen_dims[0] / 2) - (img_dims[0] / 2),
                       self.screen_dims[1] - coords[1] - img_dims[1])
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
        self.start_pos = (0, 100)

        image = game.sprite_images["rocket"]

        self.height = 0
        self.landing_pos = v.vector()
        self.apogee_time = 0
        self.landing_time = 0

        self.throttle = 0

        super().__init__(game, image, (75, 75), self.start_pos)

    def reset(self):
        """
        Method to reset the rocket's position on a new game
        """
        self.position = v.vector(self.start_pos[0], self.start_pos[1])
        self.velocity = v.vector()
        self.acceleration = v.vector()
        self.angle = 0

        self.accelerating = False
        self.rotating = 0

        self.draw()

    def update(self):
        """
        Overloaded update method for the Rocket class. Sets the acceleration and angular velocity
        of the rocket depending on keyboard inout and current speed
        """
        self.height = self.position.y - self.game.moon.get_height(self.position.x)
        dt = self.game.dt  # Simulation timestep

        if self.height <= 0:
            self.acceleration = v.vector()
            self.velocity = v.vector()
            self.position = v.vector(self.position.x, self.game.moon.get_height(self.position.x))
        else:
            self.acceleration = v.vector(0, -self.game.g)

            # Set angular velocity depending on whether the a or d keys have been pressed
            if self.rotating == 1:
                self.angular_velocity = -0.9
            elif self.rotating == 2:
                self.angular_velocity = 0.9
            else:
                self.angular_velocity = 0

        # Calculate the new throttle level and acceleration
        max_throttle = 5
        if self.accelerating:
            self.throttle += max_throttle * dt
        else:
            self.throttle -= max_throttle * dt
        if self.throttle > max_throttle:
            self.throttle = max_throttle
        elif self.throttle < 0:
            self.throttle = 0
        self.acceleration += (self.direction * self.throttle)
        """
        self.landing_time = 0
        if self.velocity.y > 0:
            apogee_time = self.velocity.y / self.game.g
            apogee_height = (self.height + (self.velocity.y * apogee_time) +
                             ((self.acceleration.y * apogee_time ** 2) / 2))
            self.landing_time = apogee_time + math.sqrt(abs((2 * apogee_height) / self.game.g))
        else:
            if self.height > 0:
                self.landing_time = (-self.velocity.y - math.sqrt(
                    self.velocity.y ** 2 + 2 * self.game.g * self.height)) / self.game.g

        downrange = self.position.x + (self.velocity.x * self.landing_time)
        self.landing_pos = (downrange, self.game.moon.get_height(downrange))"""

        self.rotating = 0
        self.accelerating = False
        super().update()

    def draw(self):
        """
        Method to change the image used by the rocket if it's accelerating
        """

        #if self.height > 10:
            #pygame.draw.circle(self.game.screen, (255, 0, 0), self.display_coord_transform(self.landing_pos), 5)
        super().draw()

    def move_forward(self):
        self.accelerating = True

    def turn_left(self):
        self.rotating = 1

    def turn_right(self):
        self.rotating = 2
