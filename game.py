import pygame
from sprites import *
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.state = PLAYING
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.setup_game()

    def setup_game(self):
        # Create basic maze layout
        layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W............WW............W....W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W.WW.W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W.WW.W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W.WW.W",
            "W.............................. W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.WW.W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.WW.W",
            "W......WW....WW....WW......WW.W",
            "WWWWWW.WWWWW WW WWWWW.WWWWWWW.W",
            "     W.WWWWW WW WWWWW.W        ",
            "     W.WW          WW.W        ",
            "     W.WW WWW--WWW WW.W        ",
            "WWWWWW.WW W      W WW.WWWWWW  ",
            "      .   W      W   .        ",
            "WWWWWW.WW W      W WW.WWWWWW  ",
            "     W.WW WWWWWWWW WW.W        ",
            "     W.WW          WW.W        ",
            "     W.WW WWWWWWWW WW.W        ",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW  ",
            "W............WW............W...W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W.W.W",
            "W.WWWW.WWWW.WW.WWWW.WWWW.W.W.W",
            "W...WW................WW.....W.W",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW.W",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW.W",
            "W......WW....WW....WW......W..W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W.W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W.W",
            "W..........................W...W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        ]

        # Create game objects based on layout
        for row, line in enumerate(layout):
            for col, char in enumerate(line):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if char == "W":
                    wall = Wall(x, y)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif char == ".":
                    dot = Dot(x, y)
                    self.dots.add(dot)
                    self.all_sprites.add(dot)

        # Create Pacman
        self.pacman = Pacman(CELL_SIZE * 14, CELL_SIZE * 23)
        self.all_sprites.add(self.pacman)

        # Create Ghosts with personalities
        ghost_data = [
            (CELL_SIZE * 12, CELL_SIZE * 14, "BLINKY"),
            (CELL_SIZE * 14, CELL_SIZE * 14, "PINKY"),
            (CELL_SIZE * 16, CELL_SIZE * 14, "INKY"),
            (CELL_SIZE * 18, CELL_SIZE * 14, "CLYDE")
        ]
        
        self.blinky = None  # Reference to Blinky for Inky's behavior
        for x, y, personality in ghost_data:
            ghost = Ghost(x, y, personality)
            if personality == "BLINKY":
                self.blinky = ghost
            self.ghosts.add(ghost)
            self.all_sprites.add(ghost)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == PLAYING:
                    if event.key == pygame.K_UP:
                        self.pacman.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.change_direction(RIGHT)
                    elif event.key == pygame.K_p:
                        self.state = PAUSED
                elif self.state == PAUSED:
                    if event.key == pygame.K_p:
                        self.state = PLAYING
                elif self.state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.__init__()
                
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        if self.state != PLAYING:
            return

        # Update Pacman
        self.pacman.update(self.walls)
        
        # Update Ghosts
        for ghost in self.ghosts:
            ghost.update(self.walls, self.pacman, self.blinky)
        
        # Check collision with dots
        dots_collected = pygame.sprite.spritecollide(self.pacman, self.dots, True)
        self.score += len(dots_collected) * DOT_POINTS

        # Check collision with ghosts
        if pygame.sprite.spritecollideany(self.pacman, self.ghosts):
            self.state = GAME_OVER

        # Check win condition
        if len(self.dots) == 0:
            self.state = GAME_OVER

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game state messages
        if self.state == PAUSED:
            pause_text = self.font.render('PAUSED - Press P to continue', True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        elif self.state == GAME_OVER:
            if len(self.dots) == 0:
                game_over_text = self.font.render('YOU WIN! Press R to restart', True, WHITE)
            else:
                game_over_text = self.font.render('GAME OVER - Press R to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
