import pygame
# we will import os for that this module will help to define the path to artifacts
import os
pygame.font.init()
pygame.mixer.init()

HEIGHT, WIDTH = 750, 1050
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# sets the name of the "game" more specific the name of the window that pop up
pygame.display.set_caption("TwoPlayerGame")

WINDOW_COLOR = (255, 255, 255) # WHITE
# store how many frames per second our game window will be updated
# most games run as 60FPS
FPS = 60
PLAYER_VELOCITY = 5

#BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
BORDER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'var1.png')), (90, HEIGHT//2))
BORDER_IMG2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'var1.png')), (90, HEIGHT//2))
BORDER_COLOR = (0, 1, 70)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40, True)
WINNER_FONT = pygame.font.SysFont('comicsans', 100, True)
BULLETS_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'yellow_spaceship.png' ))
YELLOW_SPACESHIP_IMG = pygame.transform.scale(
    YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.image.load(
    os.path.join('Assets', 'red_spaceship.png' ))
RED_SPACESHIP_IMG = pygame.transform.scale(
    RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# define new events; +1  and +2 represents the number of event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

HIT_SOUND = pygame.mixer.Sound('Assets/Grenade.wav')
FIRE_SOUND = pygame.mixer.Sound('Assets/Gun.wav')
APPLAUSE_SOUND = pygame.mixer.Sound('Assets/Audience_Applause.wav')

GAME_ICON = pygame.image.load(os.path.join('Assets/cartoon-spaceship.png'))


def yellow_player_movement(keys_pressed, yellow_player, custom_border):
    if keys_pressed[pygame.K_LEFT] and yellow_player.x - PLAYER_VELOCITY > custom_border.x + custom_border.width:  # left
        yellow_player.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and yellow_player.x + PLAYER_VELOCITY + SPACESHIP_WIDTH< WIDTH:  # right
        yellow_player.x += PLAYER_VELOCITY
    if keys_pressed[pygame.K_UP] and yellow_player.y - PLAYER_VELOCITY > 0:  # up
        yellow_player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN] and yellow_player.y + PLAYER_VELOCITY < HEIGHT - SPACESHIP_HEIGHT:  # down
        yellow_player.y += PLAYER_VELOCITY


def red_player_movement(keys_pressed, red_player, custom_border):
    if keys_pressed[pygame.K_a] and red_player.x - PLAYER_VELOCITY > 0:  # left
        red_player.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_d] and red_player.x + PLAYER_VELOCITY + SPACESHIP_WIDTH < custom_border.x:  # right
        red_player.x += PLAYER_VELOCITY
    if keys_pressed[pygame.K_w] and red_player.y - PLAYER_VELOCITY > 0:  # up
        red_player.y -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_s] and red_player.y + PLAYER_VELOCITY + SPACESHIP_HEIGHT < HEIGHT:  # down
        red_player.y += PLAYER_VELOCITY


def handle_bullets_shot(bullets_red, bullets_yellow, red_player, yellow_player):
    for bullet in bullets_red:
        bullet.x += BULLETS_VEL
        if yellow_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullets_red.remove(bullet)
        elif bullet.x > WIDTH:
            bullets_red.remove(bullet)

    for bullet in bullets_yellow:
        bullet.x -= BULLETS_VEL
        if red_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            bullets_yellow.remove(bullet)
        elif bullet.x < 0:
            bullets_yellow.remove(bullet)


def add_window_elements(red_player, yellow_player, red_bullets, yellow_bullets, red_health, yellow_health, custom_border):
    # ! the order of drawing matters
    pygame.display.set_icon(GAME_ICON)
    WINDOW.blit(SPACE, (0, 0))
    WINDOW.blit(BORDER_IMG, (custom_border.x, custom_border.y))
    WINDOW.blit(BORDER_IMG2, (custom_border.x, custom_border.y + HEIGHT/2))
    #pygame.draw.rect(WINDOW, BORDER_COLOR, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WINDOW_COLOR)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WINDOW_COLOR)
    WINDOW.blit(yellow_health_text,(WIDTH - yellow_health_text.get_width() - 10, 10))
    WINDOW.blit(red_health_text, (10, 10))
    # images are seen as surfaces, so we need to blit them in order to see it on the screen
    WINDOW.blit(YELLOW_SPACESHIP_IMG, (yellow_player.x, yellow_player.y))
    WINDOW.blit(RED_SPACESHIP_IMG, (red_player.x, red_player.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED_COLOR, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW_COLOR, bullet)

    pygame.display.update()


def winner(text):
    APPLAUSE_SOUND.play()
    draw_text = WINNER_FONT.render(text, 1, WINDOW_COLOR)
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    custom_border = pygame.Rect(WIDTH/2 - 40, 0, 90, HEIGHT/2)
    # to store the player position will be used 2 rectangles which will take the coordinates
    red_player = pygame.Rect(100, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_player = pygame.Rect(895, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_health = 10
    yellow_health = 10

    bullets_red = []
    bullets_yellow = []
    clock = pygame.time.Clock()
    run = True
    while run:
        # control the speed of the while loop
        clock.tick(FPS)
        # in the next line we will get the list of the available events and handle the target ones
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullets_red) < MAX_BULLETS:
                    bullet = pygame.Rect(red_player.x + red_player.width, red_player.y + red_player.height// 2 - 2, 10, 5)
                    bullets_red.append(bullet)
                    FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(bullets_yellow) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow_player.x,
                                         yellow_player.y + yellow_player.height // 2 - 2, 10, 5)
                    bullets_yellow.append(bullet)
                    FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Player Wins"

        if yellow_health <= 0:
            winner_text = "Red Player Wins"

        if winner_text != "":
            winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_player_movement(keys_pressed, red_player, custom_border)
        yellow_player_movement(keys_pressed, yellow_player, custom_border)

        handle_bullets_shot(bullets_red, bullets_yellow, red_player, yellow_player)
        add_window_elements(red_player, yellow_player, bullets_red, bullets_yellow,
                            red_health, yellow_health, custom_border)

    main()


# if we were to import this file in another module, it will
# automatically run the game
# but we want to run the game only if we run this specific file
if __name__ == "__main__":
    main()
