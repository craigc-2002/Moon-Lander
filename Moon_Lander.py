import pygame
import math

import rocket
import image_loader
import moon
import flight_display as fd
import datalogger
import pygraph

"""
TO DO:
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
        self.title_font = pygame.font.SysFont("Helvetica", 100)

        image_index = {"lander": ((0, 1), (15, 15)),
                       "lander_flames": ((15, 1), (30, 15)),
                       "explosion": ((30, 0), (45, 15))}
        self.sprite_images = image_loader.get_textures("assets/sprites.png", image_index)
        self.data_storage = datalogger.DataLogger()

        self.rocket = rocket.Rocket(self)
        self.moon = moon.Moon(self)

        self.throttle_indicator = fd.ScaleDisplay(self, (50, 485), (50, 235), (0, 50))
        self.height_indicator = fd.ScaleDisplay(self, (1230, 485), (1230, 235), (0, 10000))

        self.g = 1.5
        self.time = 0
        self.dt = 0.01
        self.scale = (1, 1)

        self.loading_screen()

    def loading_screen(self):
        """
        Method to load in the moon and display the loading screen
        """
        load_time = 0
        load_rect = pygame.Rect(540, 360, 200, 200)
        end_angle = math.pi/2
        num_points = 100000
        num_per_loop = 100
        num_loops = num_points//num_per_loop

        for i in range(num_loops):
            # Generate the moon height map for a small number of points
            self.moon.load(num_per_loop, i*num_per_loop)

            # Clear the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.screen.fill("black")

            # Add text for the game title and loading
            title_text_img = self.title_font.render("MOON LANDER", True, (255, 255, 255))
            self.screen.blit(title_text_img, ((self.window_width/2)-(title_text_img.get_width()/2), 100))

            loading_text_img = self.font.render("LOADING", True, (255, 255, 255))
            self.screen.blit(loading_text_img, ((self.window_width/2) - (loading_text_img.get_width()/2),
                                                460-(loading_text_img.get_height()/2)))

            # Draw the loading indicator
            end_angle += math.pi/(num_loops/2)
            pygame.draw.arc(self.screen, (255, 255, 255), load_rect, math.pi/2, end_angle, 20)

            pygame.display.flip()
            load_time += self.clock.tick()

        print("Loading Time: {} ms".format(load_time))
        self.title_screen()

    def title_screen(self):
        scaled_image = pygame.transform.scale(self.sprite_images["lander_flames"], (200, 200))
        i = 0

        while True:
            # Clear the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_loop()

            self.screen.fill("black")

            # Add text for the game title and loading
            title_text_img = self.title_font.render("MOON LANDER", True, (255, 255, 255))
            self.screen.blit(title_text_img, ((self.window_width / 2) - (title_text_img.get_width() / 2), 100))

            subtitle_text_img = self.font.render("CLICK TO START GAME", True, (255, 255, 255))
            self.screen.blit(subtitle_text_img, ((self.window_width / 2) - (subtitle_text_img.get_width() / 2), 575))

            """# Add current FPS to the screen
            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))"""

            display_pos = [(self.window_width/2)-(scaled_image.get_size()[0]/2), 300]
            display_pos[0] += 30*math.sin(math.pi*0.001*i)
            display_pos[1] += 30*math.sin(math.pi*0.0005*i)
            display_angle = 8*math.sin(math.pi*0.0008*i)
            rotated_image = pygame.transform.rotate(scaled_image, display_angle)
            i += 1
            self.screen.blit(rotated_image, display_pos)

            pygame.display.flip()
            self.clock.tick()

    def game_loop(self):
        #self.rocket.reset((-10000, 10000), (100, -10))
        self.rocket.reset((0, 5000), (25, 0))
        self.data_storage.clear()
        self.time = 0
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

            # Update sprites
            self.rocket.update()
            self.moon.update()
            self.throttle_indicator.update(self.rocket.throttle)
            self.height_indicator.update(self.rocket.height)

            self.data_storage.log(self.time, round(self.rocket.height, 2))

            self.screen.fill("black")

            # Draw objects to display
            self.moon.draw()
            self.rocket.draw()
            self.throttle_indicator.draw()
            self.height_indicator.draw()

            # Add current FPS to the screen
            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))

            # Add current x and y velocity components to the screen
            x_vel_text = "X VELOCITY:   "+str(round(self.rocket.velocity.x, 1))
            x_vel_img = self.font.render(x_vel_text, True, (255, 255, 255))
            self.screen.blit(x_vel_img, (50, 30))
            y_vel_text = "Y VELOCITY:   "+str(round(self.rocket.velocity.y, 1))
            y_vel_img = self.font.render(y_vel_text, True, (255, 255, 255))
            self.screen.blit(y_vel_img, (50, 80))

            # Add current x and y velocity components to the screen
            x_pos_text = "X POS:   " + str(round(self.rocket.position.x, 1))
            x_pos_img = self.font.render(x_pos_text, True, (255, 255, 255))
            self.screen.blit(x_pos_img, (325, 30))
            height_text = "HEIGHT:   " + str(round(self.rocket.height, 1))
            height_img = self.font.render(height_text, True, (255, 255, 255))
            self.screen.blit(height_img, (325, 80))

            # Display fuel level on the screen
            fuel_text = "FUEL:  "+str(round(self.rocket.fuel))
            fuel_colour = (255, 255, 255) if self.rocket.fuel > 15 else (255, 0, 0)
            fuel_text_img = self.font.render(fuel_text, True, fuel_colour)
            self.screen.blit(fuel_text_img, (575, 30))

            # Display TWR on the screen
            twr_text = "TWR:  " + str(round(self.rocket.twr_max, 1))
            twr_text_img = self.font.render(twr_text, True, (255, 255, 255))
            self.screen.blit(twr_text_img, (575, 80))

            # Update the display on screen
            pygame.display.flip()
            tick_time = self.clock.tick(60)
            self.time += tick_time
            self.dt = tick_time / 100

    def game_over(self, ending):
        """
        Method to display the game over screen
        """
        if ending == "crash":
            message = "CRASH"
        else:
            message = "SAFE LANDING"
        game_over_text_img = self.title_font.render(message, True, (255, 255, 255))
        replay_text_img = self.font.render("CLICK TO REPLAY", True, (255, 255, 255))

        graph = pygraph.line_graph(self.data_storage.get_log(), (640, 360), ("Time", "Height"))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_loop()

            self.screen.fill("black")
            self.moon.draw()
            self.rocket.draw()
            self.screen.blit(game_over_text_img, ((self.window_width/2)-(game_over_text_img.get_width()/2), 75))
            self.screen.blit(replay_text_img, ((self.window_width/2)-(replay_text_img.get_width()/2), 200))
            self.screen.blit(graph, ((self.window_width/2)-(graph.get_width()/2), 300))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    MoonLander()
