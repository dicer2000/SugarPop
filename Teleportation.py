import math
import pygame as pg

class Teleportation:
    def __init__(self, entry_pos, exit_pos, entry_radius, exit_radius, scale, height):
        """
        :param entry_pos: (x, y) of the entry point in screen coordinates
        :param exit_pos: (x, y) of the exit point in screen coordinates
        :param entry_radius: radius of the entry circle in screen coordinates (pixels)
        :param exit_radius: radius of the exit circle in screen coordinates (pixels)
        :param scale: conversion scale from physics to screen (pixels per meter)
        :param height: screen height, used for coordinate conversion
        """
        self.entry_x, self.entry_y = entry_pos
#        self.entry_y -= height
        self.exit_x, self.exit_y = exit_pos
#        self.exit_y -= height
        self.entry_radius = entry_radius
        self.exit_radius = exit_radius
        self.scale = scale
        self.height = height
        self.wave_time = 0

    def update(self, dt):
        # Increase wave time for exit circle waves
        self.wave_time += dt
    
    def draw(self, screen):
        """
        Draw the teleportation entry and exit points.
        We'll represent:
          - Entry as a green spinning ring with a rotating line inside.
          - Exit as a blue circle with wave-like expanding rings.
        """
        # Draw the base entry circle

        wave_period = 2.0  # One wave cycle every 2 seconds
        wave_count = 3     # Number of waves

        # Draw the base entry and exit circles
        pg.draw.circle(screen, (0, 255, 0), (int(self.entry_x), int(self.entry_y)), self.entry_radius, 2)
        pg.draw.circle(screen, (0, 0, 255), (int(self.exit_x), int(self.exit_y)), self.exit_radius, 2)

        # Draw wave-like expanding rings at the exit
        for i in range(wave_count):
            # Offset each wave by a fraction of the period
            wave_offset = (self.wave_time + i * (wave_period / wave_count)) % wave_period
            wprog = wave_offset / wave_period
            # Radius grows from exit_radius to exit_radius*2
            wave_radius = self.exit_radius + wprog * self.exit_radius
            # Fade effect: alpha decreases as radius grows
            alpha = 255 * (1 - wprog)
            # Adjust color based on alpha
            fade_color_value = max(0, int(alpha))
            fade_color = (0, 0, fade_color_value)
            pg.draw.circle(screen, fade_color, (int(self.entry_x), int(self.entry_y)), int(wave_radius), 2)
            pg.draw.circle(screen, fade_color, (int(self.exit_x), int(self.exit_y)), int(wave_radius), 2)

    def sugarEnterTransport(self, sugar):
        """
        Check the given sugar grain to see if it has entered the entry radius.
        If so, instantly move it to the exit position, preserving its velocity.

        :param sugar: A single sugar_grain object
        """
        # Convert the sugar's physics position to screen coordinates
        pos = sugar.body.position
        sugar_screen_x = pos.x * self.scale
        sugar_screen_y = self.height - pos.y * self.scale

        dx = sugar_screen_x - self.entry_x
        dy = sugar_screen_y - self.entry_y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist <= self.entry_radius:
            # Teleport the sugar to the exit
            # Convert exit screen coords to physics coords:
            exit_phys_x = self.exit_x / self.scale
            exit_phys_y = (self.height - self.exit_y) / self.scale

            sugar.body.position = (exit_phys_x, exit_phys_y)
            # Velocity remains unchanged
