import pygame
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
cyan = (0, 255, 127)
orange = (255, 69, 0)

display_height, display_width = 400, 600
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Anaconda')
win.fill(white)
pygame.display.update()


def message(msg, color=black, font_style=None, font_size=30, position=(10, 10)):
    font = pygame.font.SysFont(font_style, font_size)
    m = font.render(msg, True, color)
    win.blit(m, position)


def GameLoop():
    run = True
    game_over = False
    score = 0
    eaten = 0
    difficulty = 1
    snake_speed = difficulty * 3
    snake_block = 10
    snake_length = 1
    snake_list = []
    x, y = int(display_width / 2), int(display_height / 2)
    xm, ym = 0, 0
    sfx, sfy = -100, -100
    spc = False
    fx = round(random.randrange(0, display_width, 10) / 10) * 10
    fy = round(random.randrange(0, display_height, 10) / 10) * 10
    clock = pygame.time.Clock()

    while run:
        while game_over:
            message('Game Over', red, position=(display_width / 2.3, display_height / 2))
            message("Press 'Q' to exit or 'C' to play again.",
                    green, position=(display_width / 3.8, display_height / 2 + 30))
            pygame.display.update()

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
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u and difficulty < 5:
                    difficulty += 1
                    snake_speed += 3
                if event.key == pygame.K_l and difficulty > 1:
                    difficulty -= 1
                    snake_speed -= 3
                if event.key == pygame.K_UP:
                    ym = -snake_block
                    xm = 0
                elif event.key == pygame.K_DOWN:
                    ym = snake_block
                    xm = 0
                elif event.key == pygame.K_LEFT:
                    xm = -snake_block
                    ym = 0
                elif event.key == pygame.K_RIGHT:
                    xm = snake_block
                    ym = 0

        win.fill(white)
        x += xm
        y += ym

        for s in snake_list[:-1]:
            if s == (x, y):
                game_over = True
                break

        snake_list.append((x, y))

        if len(snake_list) > snake_length:
            del snake_list[0]

        if (fx, fy) in snake_list:
            score += difficulty
            snake_length += 1
            eaten += 1
            fx = round(random.randrange(0, display_width, 10) / 10) * 10
            fy = round(random.randrange(0, display_height, 10) / 10) * 10

        if sfx <= x <= sfx + 2 * snake_block and sfy <= y <= sfy + 2 * snake_block:
            score += 5 * difficulty
            spc = False
            sfx = -100
            sfy = -100

        if eaten == 5 and not spc:
            eaten = 0
            spc = True
            sfx = round(random.randrange(0, display_width, 10) / 10) * 10
            sfy = round(random.randrange(0, display_height, 10) / 10) * 10

        if x < 0 or y < 0 or x > display_width or y > display_height:
            game_over = True
            continue

        for s in snake_list:
            pygame.draw.rect(win, black, (s[0], s[1], snake_block, snake_block))

        pygame.draw.rect(win, orange, (sfx, sfy, snake_block * 3, snake_block * 3))
        pygame.draw.rect(win, green, (fx, fy, snake_block, snake_block))
        message('Score : ' + str(score) + "             Difficulty : " + str(difficulty) +
                "             U --> Upper Difficulty" + "             L --> Lower Difficulty", cyan, font_size=20)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


GameLoop()
