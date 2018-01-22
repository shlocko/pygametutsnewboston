import pygame
import random

pygame.init()

# Defining colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Setting the "Surface" (IE game window)
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

# Defining some game constants
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()
fps = 15


def snake(player_size, snake_list):  # Snake rendering
    for x_y in snake_list:
        pygame.draw.rect(gameDisplay, green, [x_y[0], x_y[1], player_size, player_size])


def message_to_screen(msg, color, msg_x, msg_y):  # Display text in center of screen
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [msg_x, msg_y])


def game_loop():  # Actual main loop
    
    # Defining some game variables
    game_exit = False
    game_over = False
    player_size = 10
    snake_direction = "right"
    score = 0
    apple_size = 10
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 10
    lead_y_change = 0
    rand_apple_x = round(random.randrange(0, display_width - apple_size) / 10.0) * 10.0
    rand_apple_y = round(random.randrange(0, display_height - apple_size) / 10.0) * 10.0
    snake_list = []
    snake_length = 1
    
    while not game_exit:  # Main Game loop
        
        while game_over:  # Game Over menu
            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red, 100, 250)
            pygame.display.update()
            for event in pygame.event.get():  # Event checking for game over
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()
                    elif event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
        
        for event in pygame.event.get():  # Checking for events
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "right":
                    snake_direction = "left"
                    lead_x_change = -player_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and snake_direction != "left":
                    snake_direction = "right"
                    lead_x_change = player_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP and snake_direction != "down":
                    snake_direction = "up"
                    lead_y_change = -player_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and snake_direction != "up":
                    snake_direction = "down"
                    lead_y_change = player_size
                    lead_x_change = 0
        
        if lead_x > display_width - player_size or lead_x < 0 or lead_y > display_height - player_size or lead_y < 0:  # Check if player is within bounds
            game_over = True
        
        # Moving Player
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        # Drawing Game - - - -
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [rand_apple_x, rand_apple_y, apple_size, apple_size])
        
        # Managing snake length
        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        for each_segment in snake_list[:-1]:  # Detect collisions with tail
            if each_segment == snake_head:
                game_over = True
        
        snake(player_size, snake_list)
        
        message_to_screen("Score: {}".format(score), black, 10, 10)
        
        pygame.display.update()  # Render all changes to graphics since last frame
        
        if lead_x == rand_apple_x and lead_y == rand_apple_y:  # Snake Apple collision detection
            snake_length += 1
            print("om nom nom")
            score += 1
            rand_apple_x = round(random.randrange(0, display_width - apple_size) / 10.0) * 10.0
            rand_apple_y = round(random.randrange(0, display_height - apple_size) / 10.0) * 10.0
            for x_y in snake_list:
                if [rand_apple_x, rand_apple_y] == x_y:  # Ensuring the apple doesnt spawn within the snake's tail
                    print("Spawned in body!")
                    rand_apple_x = round(random.randrange(0, display_width - apple_size) / 10.0) * 10.0
                    rand_apple_y = round(random.randrange(0, display_height - apple_size) / 10.0) * 10.0
        
        clock.tick(fps)
    
    pygame.quit()
    quit()


game_loop()
