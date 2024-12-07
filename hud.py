
import level
import bucket
import sugar_grain
import pygame as pg

class hud():
    '''Heads Up Display for Sugar Game'''
    def __init__(self):
        # Initialize font for HUD
        self.font_small = pg.font.SysFont(None, 20)  # Default font, size 36
        self.font_medium = pg.font.SysFont(None, 30)  # Default font, size 36
        self.font_large = pg.font.SysFont(None, 50)  # Default font, size 36
        self.font_sym = pg.font.Font('./images/Segoe-UI-Symbol.ttf',64)
    
    def draw(self, screen, buckets, grain_left, level, level_by, gravity = 1):
        """Draw the HUD displaying the number of grains, level, etc."""
        
        # Draw the bucket count of each bucket
        for bucket in buckets:
            text_surface = self.font_medium.render(f'{bucket.count}', True, (191, 0, 255))
            width = text_surface.get_rect().width # Get width of text to draw
            # Draw the text surface on the screen
            screen.blit(text_surface, (bucket.x-(width//2), screen.get_height() - bucket.y-8))  # Position at center
        
        # Determine Gravity indicator
        grav_char = "⇓"
        if gravity == -1:
            grav_char = "⇑"
            
        # Draw other stats in top left
        text_surface = self.font_small.render('Level  Remaining', True, (191, 0, 255))
        # Draw the text surface on the screen
        screen.blit(text_surface, (10, 10))  # Position at top-left corner
        text_surface = self.font_large.render(f'{level}   {grain_left}', True, (191, 0, 255))
        # Draw the text surface on the screen
        screen.blit(text_surface, (15, 30))  # Position at top-left corner
        
        # Draw the gravity arrow
        text_surface = self.font_sym.render(grav_char, True, (191, 0, 255))
        # Draw the text surface on the screen
        screen.blit(text_surface, (130, -10))  # Position at top-left corner

        # Draw the Level By (if available)
        if level_by and len(level_by) > 0:
            text_surface = self.font_medium.render('level by ' + level_by, True, (191, 191, 255, 50))
            # Draw the text surface on the screen
            width = text_surface.get_rect().width # Get width of text to draw
            screen.blit(text_surface, (screen.get_width() - width - 10, 10))  # Position at top-left corner
