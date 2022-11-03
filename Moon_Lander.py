import pygame
import rocket
import image_loader
import moon

"""
TO DO:
- Fix rocket scrolling (when it turns back it should be able to return through the middle of the screen)

- Add fuel system
- Add gauges on sides for position and velocity
- Improve procedural generation of moon (or load from file)
- Change lander art (lander and separate flames)
- Reimplement the landing site spot (hard because of scrolling terrain)
"""


class MoonLander:
    def __init__(self):
        pygame.init()
        self.window_width = 1280
        self.window_height = 720

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Moon Lander")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Helvetica", 30)

        image_index = {"rocket": ((1, 17), (10, 27))}
        self.sprite_images = image_loader.get_textures("assets/textures.png", image_index)

        self.rocket = rocket.Rocket(self)
        self.moon = moon.Moon(self)

        self.g = 2
        self.dt = 0.01
        self.scale = (1, 1)

        self.game_loop()

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            # Get a list of keys currently being pressed
            key_input = pygame.key.get_pressed()
            # Handle key presses to control the rocket
            if key_input[pygame.K_w]:
                self.rocket.move_forward()
            if key_input[pygame.K_a]:
                self.rocket.turn_left()
            if key_input[pygame.K_d]:
                self.rocket.turn_right()

            # Update sprites here
            self.moon.update()
            self.rocket.update()

            self.screen.fill("black")

            # Draw objects to display here
            self.moon.draw()
            self.rocket.draw()

            # Add current FPS to the screen
            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))

            pos_text = str(round(self.rocket.display_pos_delta))
            pos_text_img = self.font.render(pos_text, True, (255, 255, 255))
            self.screen.blit(pos_text_img, (1000, 20))

            # Update the display on screen
            pygame.display.flip()
            tick_time = self.clock.tick(60)
            self.dt = tick_time / 100


if __name__ == "__main__":
    MoonLander()
