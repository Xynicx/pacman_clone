import pygame
import random
import math
from constants import *

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = RIGHT
        self.speed = PACMAN_SPEED
        self.next_direction = None

    def update(self, walls):
        # Store current position in case we need to move back
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Try to move in the next_direction if it exists
        if self.next_direction:
            temp_x = self.rect.x + self.next_direction[0] * self.speed
            temp_y = self.rect.y + self.next_direction[1] * self.speed
            temp_rect = self.rect.copy()
            temp_rect.x = temp_x
            temp_rect.y = temp_y
            
            if not any(temp_rect.colliderect(wall.rect) for wall in walls):
                self.direction = self.next_direction
                self.next_direction = None
            
        # Move in current direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Check wall collisions
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x = previous_x
                self.rect.y = previous_y
                break

        # Keep in bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def change_direction(self, new_direction):
        self.next_direction = new_direction

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, personality):
        super().__init__()
        self.personality = personality
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill(GHOST_PERSONALITIES[personality]["color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = RIGHT
        self.speed = GHOST_SPEED
        self.state = GHOST_SCATTER
        self.state_timer = 0
        self.path = []
        self.path_update_timer = 0

    def get_target_position(self, pacman, blinky=None):
        if self.state == GHOST_SCATTER:
            return GHOST_PERSONALITIES[self.personality]["scatter_corner"]
        
        # Different targeting behavior for each ghost
        if self.personality == "BLINKY":
            # Directly target Pacman
            return (pacman.rect.x, pacman.rect.y)
            
        elif self.personality == "PINKY":
            # Target 4 tiles ahead of Pacman
            offset = GHOST_PERSONALITIES[self.personality]["chase_offset"]
            target_x = pacman.rect.x + (pacman.direction[0] * offset[0])
            target_y = pacman.rect.y + (pacman.direction[1] * offset[1])
            return (target_x, target_y)
            
        elif self.personality == "INKY":
            if not blinky:
                return (pacman.rect.x, pacman.rect.y)
            # Use Blinky's position to calculate target
            # First, get position 2 tiles ahead of Pacman
            ahead_x = pacman.rect.x + (pacman.direction[0] * 2 * CELL_SIZE)
            ahead_y = pacman.rect.y + (pacman.direction[1] * 2 * CELL_SIZE)
            # Then double the vector from Blinky to that position
            target_x = ahead_x + (ahead_x - blinky.rect.x)
            target_y = ahead_y + (ahead_y - blinky.rect.y)
            return (target_x, target_y)
            
        elif self.personality == "CLYDE":
            # If far from Pacman, target him. If close, go to scatter corner
            distance = math.sqrt((pacman.rect.x - self.rect.x)**2 + 
                               (pacman.rect.y - self.rect.y)**2)
            if distance > 8 * CELL_SIZE:
                return (pacman.rect.x, pacman.rect.y)
            else:
                return GHOST_PERSONALITIES[self.personality]["scatter_corner"]

    def get_possible_directions(self, walls):
        possible = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            temp_rect = self.rect.copy()
            temp_rect.x += direction[0] * self.speed * 5
            temp_rect.y += direction[1] * self.speed * 5
            
            if not any(temp_rect.colliderect(wall.rect) for wall in walls):
                possible.append(direction)
        return possible

    def choose_direction(self, target_pos, walls):
        possible_directions = self.get_possible_directions(walls)
        if not possible_directions:
            return
        
        # Remove opposite direction unless it's the only option
        if len(possible_directions) > 1:
            opposite = (-self.direction[0], -self.direction[1])
            if opposite in possible_directions:
                possible_directions.remove(opposite)
        
        # Choose direction that gets closest to target
        best_direction = possible_directions[0]
        best_distance = float('inf')
        
        for direction in possible_directions:
            future_x = self.rect.x + direction[0] * CELL_SIZE
            future_y = self.rect.y + direction[1] * CELL_SIZE
            distance = math.sqrt((target_pos[0] - future_x)**2 + 
                               (target_pos[1] - future_y)**2)
            
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
        
        self.direction = best_direction

    def update(self, walls, pacman, blinky=None):
        # Update state timer
        self.state_timer += 1
        if self.state == GHOST_SCATTER and self.state_timer >= SCATTER_TIME:
            self.state = GHOST_CHASE
            self.state_timer = 0
        elif self.state == GHOST_CHASE and self.state_timer >= CHASE_TIME:
            self.state = GHOST_SCATTER
            self.state_timer = 0

        # Store current position
        previous_x = self.rect.x
        previous_y = self.rect.y

        # Update path every second
        self.path_update_timer += 1
        if self.path_update_timer >= FPS:
            self.path_update_timer = 0
            target_pos = self.get_target_position(pacman, blinky)
            self.choose_direction(target_pos, walls)

        # Move in current direction
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Check wall collisions
        wall_collision = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                wall_collision = True
                self.rect.x = previous_x
                self.rect.y = previous_y
                target_pos = self.get_target_position(pacman, blinky)
                self.choose_direction(target_pos, walls)
                break

        # Keep in bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + CELL_SIZE // 2
        self.rect.centery = y + CELL_SIZE // 2

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
