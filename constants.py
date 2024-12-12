# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game settings
FPS = 60
PACMAN_SPEED = 2
GHOST_SPEED = 1.5

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Score points
DOT_POINTS = 10
POWER_PELLET_POINTS = 50

# Game states
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"

# Ghost personalities
GHOST_PERSONALITIES = {
    "BLINKY": {  # Red ghost - Direct chaser
        "color": RED,
        "scatter_corner": (SCREEN_WIDTH - CELL_SIZE, 0),
        "chase_offset": (0, 0)  # Targets Pacman directly
    },
    "PINKY": {   # Pink ghost - Ambusher
        "color": PINK,
        "scatter_corner": (0, 0),
        "chase_offset": (4 * CELL_SIZE, -4 * CELL_SIZE)  # Targets 4 tiles ahead of Pacman
    },
    "INKY": {    # Cyan ghost - Unpredictable
        "color": CYAN,
        "scatter_corner": (SCREEN_WIDTH - CELL_SIZE, SCREEN_HEIGHT - CELL_SIZE),
        "chase_offset": (2 * CELL_SIZE, 2 * CELL_SIZE)  # Uses Blinky's position to calculate target
    },
    "CLYDE": {   # Orange ghost - Shy
        "color": ORANGE,
        "scatter_corner": (0, SCREEN_HEIGHT - CELL_SIZE),
        "chase_offset": (8 * CELL_SIZE, 8 * CELL_SIZE)  # Stays away when close
    }
}

# Ghost states
GHOST_SCATTER = "scatter"
GHOST_CHASE = "chase"

# Ghost mode timings (in frames)
SCATTER_TIME = 420  # 7 seconds
CHASE_TIME = 1200   # 20 seconds
