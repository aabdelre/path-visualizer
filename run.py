import pygame, sys, math, time
from pygame.locals import *
import random

WIDTH = 600
HEIGHT = 600
SQS_PER_ROW = 20
SQ_SIZE = WIDTH // SQS_PER_ROW
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
BLACK = (0, 0, 0)

class Search():
    def __init__(self, screen, start, end, blocks):
        self.screen = screen
        self.start = start
        self.end = end
        self.blocks = blocks
        self.current = self.start
        self.path = []

    def avilable_moves(self):
        moves = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if c != 0 or r != 0:
                    if self.current[0] + r >= 0 and self.current[0] + r < SQS_PER_ROW and \
                       self.current[1] + c >= 0 and self.current[1] + c < SQS_PER_ROW and \
                       (self.current[0] + r, self.current[1] + c) not in self.blocks:
            
                       moves.append((self.current[0] + r, self.current[1] + c))
        return moves

    def distance(self, current):
        return math.dist(current, self.end)

class Dijkstra(Search):
    def __str__(self):
        return "Preforming Dijkstra's Algorithm..."

    def search(self):
        unvisited_nodes =  self.unvisited()
        shortest_path = {}
        previous_nodes = {}

        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        
        shortest_path[self.start] = 0
        while unvisited_nodes:
            current_min_node = None
            for node in unvisited_nodes: # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node

            self.current = current_min_node
            for neighbor in self.avilable_moves():
                draw_rect(self.screen, neighbor[1], neighbor[0], GREEN, 20)
                tentative_value = shortest_path[current_min_node] + self.distance(current_min_node)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node

            unvisited_nodes.remove(current_min_node)
            pygame.display.update()
            time.sleep(0.1)

        self.print_result(previous_nodes, shortest_path) 

    def print_result(self, previous_nodes, shortest_path):
        node = self.end
        while node != self.start:
            draw_rect(self.screen, node[1], node[0], BLUE, 20)
            self.path.append(node)
            node = previous_nodes[node]
        # Add the start node manually
        draw_rect(self.screen, self.start[1], self.start[0], BLUE, 20)
        self.path.append(self.start)
        pygame.display.update()

        print("We found the following best path with a value of {}.".format(shortest_path[self.end]))
        self.path.reverse()
        print("The path is:", self.path)

    def unvisited(self):
        nodes = []
        for i in range(SQS_PER_ROW):
            for j in range(SQS_PER_ROW):
                if (i, j) not in self.blocks:
                    nodes.append((i, j))
        return nodes

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
                return (col, row)

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
                if (col, row) not in blocks:
                    blocks.append((col, row))
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
                s = Dijkstra(screen, start, end, blocks)
                s.search()
                time.sleep(2)
                pygame.quit()
                sys.exit()                
                
        draw_board(screen)        
        pygame.display.update()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Number Board")
    run_window(screen)

if __name__ == "__main__":
    main()