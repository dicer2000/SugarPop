#############################################################
# Module Name: Sugar Pop Level Designer
# Project: Sugar Pop Level Designer
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: Level designer for the Sugar Pop game without Pymunk
#############################################################

import pygame as pg
import sys
import json

# Settings
WIDTH, HEIGHT = 800, 600
RES = (WIDTH, HEIGHT)
FPS = 60

class StaticItem:
    """Class representing a static wall as a line segment."""
    def __init__(self, x1, y1, x2, y2, color='black', line_width=5):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.line_width = line_width

    def draw(self, screen):
        pg.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.line_width)

class Bucket:
    """Class representing a bucket as a rectangle."""
    def __init__(self, x, y, width=50, height=50, needed_sugar=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.needed_sugar = needed_sugar
        self.color = (0, 0, 255)  # Blue color for bucket

    def draw(self, screen):
        rect = pg.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        pg.draw.rect(screen, self.color, rect, 2)  # Draw rectangle outline

class MessageDisplay:
    """Class for displaying temporary messages on the screen."""
    def __init__(self, font_size=24):
        self.font = pg.font.SysFont(None, font_size)
        self.message = ''
        self.duration = 0
        self.start_time = 0

    def show_message(self, message, duration):
        self.message = message
        self.duration = duration
        self.start_time = pg.time.get_ticks()

    def update(self):
        if self.message:
            current_time = pg.time.get_ticks()
            if (current_time - self.start_time) / 1000.0 > self.duration:
                self.message = ''

    def draw(self, screen):
        if self.message:
            text_surface = self.font.render(self.message, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(text_surface, text_rect)

class LevelDesigner:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        # Initialize font for messages
        self.font = pg.font.SysFont(None, 36)  # Default font, size 36

        self.statics = []
        self.buckets = []
        self.level_spout_position = None
        self.mouse_down = False
        self.current_line = None
        self.message_display = MessageDisplay(font_size=24)

        # Load the background image (optional)
        self.background_image = pg.Surface(self.screen.get_size())
        self.background_image = self.background_image.convert()
        self.background_image.fill((255, 255, 255))  # Fill with white color

    def update(self):
        """Update the program."""
        # Calculate time since last frame
        self.clock.tick(FPS)

        # Update messages
        self.message_display.update()

    def draw(self):
        """Draw the level designer elements."""
        # Clear the screen
        self.screen.blit(self.background_image, (0, 0))

        # Draw the static items (walls)
        for static in self.statics:
            static.draw(self.screen)

        # Draw the buckets
        for bucket_obj in self.buckets:
            bucket_obj.draw(self.screen)

        # Draw the current line (while drawing)
        if self.current_line is not None:
            self.current_line.draw(self.screen)

        # Draw the spout position
        if self.level_spout_position:
            pg.draw.circle(
                self.screen,
                (255, 0, 0),
                (int(self.level_spout_position[0]), int(self.level_spout_position[1])),
                10
            )

        # Show any messages needed
        self.message_display.draw(self.screen)

        # Update the display
        pg.display.flip()

    def check_events(self):
        """Check for keyboard and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                # Place a bucket at the mouse position
                if event.key == pg.K_b:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    # Create a bucket object
                    new_bucket = Bucket(mouse_x, mouse_y)
                    self.buckets.append(new_bucket)
                    self.message_display.show_message("Bucket placed", 1)

                # Set the spout position
                elif event.key == pg.K_s:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    self.level_spout_position = (mouse_x, mouse_y)
                    self.message_display.show_message("Spout set", 1)

                # Save the level data
                elif event.key == pg.K_RETURN:
                    self.save_level()
                    self.message_display.show_message("Level saved", 2)

                # Clear the level data
                elif event.key == pg.K_c:
                    self.clear_level()
                    self.message_display.show_message("Level cleared", 2)

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.mouse_down = True
                    # Get mouse position and start a new static line
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    self.current_line = StaticItem(mouse_x, mouse_y, mouse_x, mouse_y)

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_down = False
                    if self.current_line:
                        # Add the completed line to statics
                        self.statics.append(self.current_line)
                        self.current_line = None

            elif event.type == pg.MOUSEMOTION and self.mouse_down:
                # Get mouse position
                mouse_x, mouse_y = pg.mouse.get_pos()
                if self.current_line:
                    # Update the end point of the current line
                    self.current_line.x2 = mouse_x
                    self.current_line.y2 = mouse_y

    def save_level(self):
        """Save the current level data to a file."""
        level_data = {
            'level_by': 'Level Designer',
            'spout_x': self.level_spout_position[0] if self.level_spout_position else 0,
            'spout_y': self.level_spout_position[1] if self.level_spout_position else 0,
            'buckets': [],
            'statics': [],
            'number_sugar_grains': 100  # Default value
        }

        # Add buckets to level data
        for bucket_obj in self.buckets:
            bucket_data = {
                'x': bucket_obj.x,
                'y': bucket_obj.y,
                'width': bucket_obj.width,
                'height': bucket_obj.height,
                'needed_sugar': bucket_obj.needed_sugar
            }
            level_data['buckets'].append(bucket_data)

        # Add static items to level data
        for static in self.statics:
            static_data = {
                'x1': static.x1,
                'y1': static.y1,
                'x2': static.x2,
                'y2': static.y2,
                'color': static.color,
                'line_width': static.line_width,
                'friction': 0.5,     # Default values
                'restitution': 0.5   # Default values
            }
            level_data['statics'].append(static_data)

        # Save to a JSON file
        with open('custom_level.json', 'w') as f:
            json.dump(level_data, f, indent=4)

    def clear_level(self):
        """Clear all level elements."""
        self.statics.clear()
        self.buckets.clear()
        self.level_spout_position = None

    def run(self):
        """Run the main loop of the level designer."""
        while True:
            self.check_events()
            self.update()
            self.draw()

def main():
    designer = LevelDesigner()
    designer.run()

if __name__ == '__main__':
    main()
