import pygame
import numpy as np
import random

pygame.init()

SCREEN_SIZE = 400
GRID_SIZE = 4
TILE_MARGIN = 5

BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
}
TEXT_COLOR = (119, 110, 101)

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048')

FONT = pygame.font.SysFont("arial", 40)

def add_new_tile(board):
    empty_positions = list(zip(*np.where(board == 0)))
    if empty_positions:
        y, x = random.choice(empty_positions)
        board[y, x] = 2 if random.random() < 0.9 else 4

def init_board():
    board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board

def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            tile_value = board[y, x]
            tile_color = TILE_COLORS.get(tile_value, (255, 255, 255))
            pygame.draw.rect(
                screen,
                tile_color,
                (
                    x * SCREEN_SIZE // GRID_SIZE + TILE_MARGIN,
                    y * SCREEN_SIZE // GRID_SIZE + TILE_MARGIN,
                    SCREEN_SIZE // GRID_SIZE - 2 * TILE_MARGIN,
                    SCREEN_SIZE // GRID_SIZE - 2 * TILE_MARGIN,
                ),
            )
            if tile_value:
                text_surface = FONT.render(str(tile_value), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(
                    x * SCREEN_SIZE // GRID_SIZE + SCREEN_SIZE // (2 * GRID_SIZE),
                    y * SCREEN_SIZE // GRID_SIZE + SCREEN_SIZE // (2 * GRID_SIZE)
                ))
                screen.blit(text_surface, text_rect)

def slide_left_and_merge(row):
    new_row = [i for i in row if i != 0]
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            del new_row[i + 1]
        i += 1
    return new_row + [0] * (GRID_SIZE - len(new_row))

def move_tiles(board, direction):
    rotation_count = {
        0: 1,
        1: 0,
        2: 3, 
        3: 2, 
    }

    rotated_board = np.rot90(board, rotation_count[direction])
    for i in range(GRID_SIZE):
        rotated_board[i, :] = slide_left_and_merge(rotated_board[i, :])
    board = np.rot90(rotated_board, -rotation_count[direction] % 4)
    return board



def game_loop():
    board = init_board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board = move_tiles(board, 0)
                elif event.key == pygame.K_DOWN:
                    board = move_tiles(board, 2)
                elif event.key == pygame.K_LEFT:
                    board = move_tiles(board, 1)
                elif event.key == pygame.K_RIGHT:
                    board = move_tiles(board, 3)
                add_new_tile(board)

        draw_board(board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game_loop()
