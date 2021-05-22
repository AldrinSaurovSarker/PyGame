# Needs to work on
# 1. Maze/Game Area of different shape
# 2. Special Food disappearance

import pygame
import random

pygame.init()

# RGB Color codes used to color objects
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 127)
orange = (255, 69, 0)

# Setting Display Screen
display_height, display_width = 400, 600
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Anaconda')
win.fill(white)
pygame.display.update()

# High Score
try:
    f = open('high_score.txt', mode='r')
    high_score = int(f.read())
except FileNotFoundError:
    f = open('high_score.txt', mode='w')
    high_score = 0
    f.write(str(high_score))
f.close()


# Display message on the screen
def message(msg, color=black, font_style=None, font_size=30, position=(10, 10)):
    font = pygame.font.SysFont(font_style, font_size)
    m = font.render(msg, True, color)
    win.blit(m, position)


def GameLoop():
    global high_score
    upper_border_height = 30
    run = True
    game_over = False
    score = 0
    eaten = 0
    difficulty = 1

    # Snake
    snake_speed = difficulty * 3
    snake_block = 10
    snake_length = 1
    run_direction = None
    snake_list = []

    # Snake head and direction
    x, y = int(display_width / 2), int(display_height / 2)
    xm, ym = 0, 0

    # Special Food
    sfx, sfy = -100, -100
    spc = False

    # Food Coordinate
    fx = round(random.randrange(0, display_width, 10) / 10) * 10
    fy = round(random.randrange(0, display_height, 10) / 10) * 10

    clock = pygame.time.Clock()

    while run:
        while game_over:
            message('Game Over', red, position=(display_width / 2.3, display_height / 2 - 30))
            message("Your Score : " + str(score), blue, position=(display_width / 2.4, display_height / 2))
            message("Press 'Q' to exit or 'C' to play again.",
                    green, position=(display_width / 3.8, display_height / 2 + 30))
            pygame.display.update()

            # Key management
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        GameLoop()

        for event in pygame.event.get():
            # Key management
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u and difficulty < 5:
                    difficulty += 1
                    snake_speed += 3
                if event.key == pygame.K_l and difficulty > 1:
                    difficulty -= 1
                    snake_speed -= 3
                if event.key == pygame.K_UP and not run_direction == 'DOWN':
                    run_direction = 'UP'
                    ym = -snake_block
                    xm = 0
                elif event.key == pygame.K_DOWN and not run_direction == 'UP':
                    run_direction = 'DOWN'
                    ym = snake_block
                    xm = 0
                elif event.key == pygame.K_LEFT and not run_direction == 'RIGHT':
                    run_direction = 'LEFT'
                    xm = -snake_block
                    ym = 0
                elif event.key == pygame.K_RIGHT and not run_direction == 'LEFT':
                    run_direction = 'RIGHT'
                    xm = snake_block
                    ym = 0

        win.fill(white)

        # Continuous running in a direction
        x += xm
        y += ym

        # Snake collapse with it's own body
        for s in snake_list[:-1]:
            if s == (x, y):
                game_over = True
                fh = open('high_score.txt', mode='w')
                fh.write(str(high_score))
                fh.close()
                break

        # Snake length changes
        snake_list.append((x, y))
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Food Eaten and new food generate
        if (fx, fy) in snake_list:
            score += difficulty
            snake_length += 1
            eaten += 1
            fx = round(random.randrange(0, display_width, 10) / 10) * 10
            fy = round(random.randrange(upper_border_height, display_height, 10) / 10) * 10

        # Special Food Eaten
        if sfx <= x <= sfx + 2 * snake_block and sfy <= y <= sfy + 2 * snake_block:
            score += 5 * difficulty
            spc = False
            sfx = -100
            sfy = -100

        # Special Food Generate
        if eaten == 5 and not spc:
            eaten = 0
            spc = True
            sfx = round(random.randrange(0, display_width, 10) / 10) * 10
            sfy = round(random.randrange(upper_border_height, display_height, 10) / 10) * 10

        # Snake Touches Border
        if x < 0 or y < upper_border_height or x >= display_width or y >= display_height:
            game_over = True
            fh = open('high_score.txt', mode='w')
            fh.write(str(high_score))
            fh.close()
            continue

        # Draw Snake
        for s in snake_list:
            clr = blue if (s[0], s[1]) == (x, y) else black # Blue Snake Head
            pygame.draw.rect(win, clr, (s[0], s[1], snake_block, snake_block))

        # Draw Game Border
        pygame.draw.line(win, black, (0, upper_border_height), (display_width, upper_border_height))
        pygame.draw.line(win, black, (0, upper_border_height), (0, display_height))
        pygame.draw.line(win, black, (0, display_height - 1), (display_width, display_height - 1))
        pygame.draw.line(win, black, (display_width - 1, display_height - 1), (display_width - 1, upper_border_height))

        # Draw Normal and Special Food
        pygame.draw.rect(win, orange, (sfx, sfy, snake_block * 3, snake_block * 3))
        pygame.draw.rect(win, green, (fx, fy, snake_block, snake_block))

        # Update High Score
        if score > high_score:
            high_score = score

        # Display Top
        message('Score : ' + str(score) + "       High Score : " + str(high_score), color=cyan, font_size=20)
        message("Difficulty : " + str(difficulty) + "       [U] Upper Difficulty" + "       [L] Lower Difficulty",
                cyan, font_size=20, position=(display_width/2.6, 10))

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


GameLoop()
