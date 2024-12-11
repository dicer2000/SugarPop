#############################################################
# Module Name: Sugar Pop Settings Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The settings implementation of the sugar pop game
#############################################################

import pygame as pg

# Window settings
RES = WIDTH, HEIGHT = 1024, 800
FPS = 60

# Scaling factor (Pixels per meter)
SCALE = 30  # Scale Factor: 30 pixels per meter
MAX_TIME_STEP = 1.0 / FPS  # Simulation step

# Define collision types
FLOOR_COLLISION_TYPE = 1
BOX_COLLISION_TYPE = 2


# Level Info
LEVEL_START_NO = 0
LEVEL_FILE_NAME = './levels/levelX.json'

# User Defined Events
START_FLOW = pg.USEREVENT + 1
FLOW_DELAY = pg.USEREVENT + 2
LOAD_NEW_LEVEL = pg.USEREVENT + 3
EXIT_APP = pg.USEREVENT + 4
TORNADOR = pg.USEREVENT + 5
TORNADOL = pg.USEREVENT+ 6

# Sounds Contants
SOUNDS = {
    'level': './sounds/Level.mp3',
    'bonus': './sounds/bucket_explode.wav',
    'bucket': './sounds/ball_tap.wav',
    'level_complete': './sounds/complete2.wav'
}

# Sugar Attributes
SUGAR_SIZE = 4