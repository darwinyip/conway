from random import randint
from typing import List
import sys

import pygame

class Cell:
    DEAD = 0
    ALIVE = 1

    def __init__(self, state: int = DEAD):
        self.state = state
        self.next_state = state

    def __repr__(self) -> str:
        return str(self.state)

class Game:
    BLOCK_SIZE = 10
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    REFRESH_RATE = 250 # ms

    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def setup(self):
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.window = pygame.display.set_mode((self.width * self.BLOCK_SIZE, self.height * self.BLOCK_SIZE))
        self.clock = pygame.time.Clock()
        self.time_elapsed_since_last_action = 0

    def render(self):
        self.window.fill(self.BLACK)
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE)
                if self.grid[y][x].state == Cell.ALIVE:
                    pygame.draw.rect(self.window, self.WHITE, rect)
                elif self.grid[y][x].state == Cell.DEAD:
                    pygame.draw.rect(self.window, self.WHITE, rect, 1)
        pygame.display.flip()

        while self.time_elapsed_since_last_action < self.REFRESH_RATE:
            dt = self.clock.tick()
            self.time_elapsed_since_last_action += dt
        self.time_elapsed_since_last_action = 0

    def seed(self, cells: List):
        for x, y in set(cells):
            self.grid[y][x].state = Cell.ALIVE

    def gen(self):
        self.seed([(randint(0, self.width - 1), randint(0, self.height - 1))
                    for _ in range(self.width) for _ in range(self.height)])

    def step(self):
        self._calculate_next_state()
        self._update_state()

    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].state = Cell.DEAD

    def _calculate_next_state(self):
        for y in range(self.height):
            for x in range(self.width):
                neighbor_count = 0

                if y - 1 >= 0 and x - 1 >= 0 and self.grid[y-1][x-1].state == Cell.ALIVE:
                    neighbor_count += 1
                if y - 1 >= 0 and self.grid[y-1][x].state == Cell.ALIVE:
                    neighbor_count += 1
                if y - 1 >= 0 and x + 1 < self.width and self.grid[y-1][x+1].state == Cell.ALIVE:
                    neighbor_count += 1
                if x - 1 >= 0 and self.grid[y][x-1].state == Cell.ALIVE:
                    neighbor_count += 1
                if x + 1 < self.width and self.grid[y][x+1].state == Cell.ALIVE:
                    neighbor_count += 1
                if y + 1 < self.height and x - 1 >= 0 and self.grid[y+1][x-1].state == Cell.ALIVE:
                    neighbor_count += 1
                if y + 1 < self.height and self.grid[y+1][x].state == Cell.ALIVE:
                    neighbor_count += 1
                if y + 1 < self.height and x + 1 < self.width and self.grid[y+1][x+1].state == Cell.ALIVE:
                    neighbor_count += 1

                if self.grid[y][x].state == Cell.ALIVE and neighbor_count < 2 or neighbor_count > 3:
                    self.grid[y][x].next_state = Cell.DEAD

                if self.grid[y][x].state == Cell.ALIVE and neighbor_count in (2, 3):
                    self.grid[y][x].next_state = Cell.ALIVE

                if self.grid[y][x].state == Cell.DEAD and neighbor_count == 3:
                    self.grid[y][x].next_state = Cell.ALIVE

    def _update_state(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].state = self.grid[y][x].next_state

    def print(self):
        for row in self.grid:
            print(row)

if __name__ == '__main__':
    game = Game(50, 50)
    game.setup()
    game.gen()

    while True:
        game.render()
        game.step()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    game.gen()