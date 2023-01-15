import pygame, sys
from pygame.locals import *
import random

WIDTH = 600
HEIGHT = 600
SQS_PER_ROW = 20
SQ_SIZE = WIDTH // SQS_PER_ROW
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

def draw_board(screen):
    for i in range(SQS_PER_ROW):
        for j in range(SQS_PER_ROW):
            draw_rect(screen, i, j, WHITE, 1)

def draw_rect(screen, row, col, color, border_width):
    tile_size = WIDTH // SQS_PER_ROW
    rect = pygame.Rect(
                row * tile_size,
                col * tile_size,
                tile_size, tile_size
            )
    pygame.draw.rect(screen, color, rect, border_width)

def get_point(screen, color):
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                row, col = event.pos
                row //= SQ_SIZE
                col //= SQ_SIZE
                draw_rect(screen, row, col, color, 20)
                return (row, col)

def run_window(screen):
    screen.fill(BLACK)
    wr = False
    start, end = None, None
    blocks = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION and wr and not start:
                row, col = event.pos
                row //= SQ_SIZE
                col //= SQ_SIZE
                blocks.append((row, col))
                draw_rect(screen, row, col, WHITE, 20)

            if event.type == pygame.MOUSEBUTTONDOWN:
                wr = True

            if event.type == pygame.MOUSEBUTTONUP:
                wr = False
            
            if event.type == KEYDOWN and not start:
                if event.unicode == "s":
                    start = get_point(screen, GREEN)

            if event.type == KEYDOWN and not end:
                if event.unicode == "e":
                    end = get_point(screen, RED)

            if start and end:
                #pass start and end to search method
                pass
                
        draw_board(screen)        
        pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Board")
    run_window(screen)

if __name__ == "__main__":
    main()