import random # random movement 
import pygame
import os # For the path.
pygame.font.init() 
pygame.mixer.init()

# Main surface
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Help protect the world against the COVID-19 virus! Arrow keys to move, Right-Ctrl to shoot")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT) # // = integer division, as rect cannot work on floats.

SPLASH_FONT = pygame.font.SysFont('comicsans', 30)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60) 

FPS = 60 # Frames per second for when we want to update/redraw the game.
VEL = 5 # Velosity of spaceships - px to move if arrow key pressed. 
BULLET_VEL = 7
MAX_BULLETS = 3
VIRUS_VEL = 3

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 50

SYRINGE_WIDTH = 90
SYRINGE_HEIGHT = 90

single_player = True

# Creating custom user events to change things in the main funtion, from an outside function, when a bullet hits.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load assets.
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'virus.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'bg.jpg'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
VIRUS_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'virus.mp3'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'bg-music.mp3'))

VIRUS_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'virus.png'))
VIRUS_BULLET = pygame.transform.scale(VIRUS_BULLET_IMAGE, (SPACESHIP_WIDTH//3,SPACESHIP_HEIGHT//3))

SYRINGE_IMAGE = pygame.image.load(os.path.join('Assets', 'syringe.png'))
SYRINGE = pygame.transform.scale(SYRINGE_IMAGE, (SYRINGE_WIDTH,SYRINGE_HEIGHT))


def wait_for_key():
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(30) # Controls the speed of the infinate loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit game (click on [X])
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def show_start_screen():
    # Start splash screen.
    global single_player

    WIN.blit(SPACE, (0, 0)) # Insert background image.

    line1 = SPLASH_FONT.render("Player 1: Arrows to move. R-CTRL to shoot", 1, WHITE)
    WIN.blit(line1, (WIDTH/2 - line1.get_width()/2, HEIGHT/2 - line1.get_height()/2 - 40))

    if single_player:
        line2 = SPLASH_FONT.render("Player 2 (Optional): W,A,S,D to move. L-CTRL to shoot", 1, WHITE)
    else:
        line2 = SPLASH_FONT.render("Player 2: W,A,S,D to move. L-CTRL to shoot", 1, WHITE)
    WIN.blit(line2, (WIDTH/2 - line2.get_width()/2, HEIGHT/2 - line2.get_height()/2))

    line3 = SPLASH_FONT.render("Tip: The vaccine protects you against the virus", 1, WHITE)
    WIN.blit(line3, (WIDTH/2 - line3.get_width()/2, HEIGHT/2 - line3.get_height()/2 + 40))

    line4 = HEALTH_FONT.render("Press a key to play...", 1, RED)
    WIN.blit(line4, (WIDTH/2 - line4.get_width()/2, HEIGHT/2 - line4.get_height()/2 + 100))

    pygame.display.update() 
    wait_for_key()


# Movement of yellow spaceship.
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left - A key. Check if goes of screen before adding 1.
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # Right - D key. Check if goes over the mittle border before adding 1.
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up - W key. Check if goes of screen before adding 1.
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -17: # Down - S key. Check if goes of screen height before adding 1.
        yellow.y += VEL

# Movement of red spaceship.
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left arrow key. Check if goes of screen before adding 1.
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right arrow key. Check if goes over the mittle border before adding 1.
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up arrow key. Check if goes of screen before adding 1.
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 17: # Down arrow key. Check if goes of screen height before adding 1.
        red.y += VEL

# Movement of virus - Automatically and ramdomly!!
def yellow_handle_movement_auto(yellow):
    global VIRUS_VEL
    rand_direction = random.randrange(1, 5, 1)
    if rand_direction == 1 and yellow.x - VEL > 0:
        yellow.x -= VEL*VIRUS_VEL
    if rand_direction == 2 and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL*VIRUS_VEL
    if rand_direction == 3 and yellow.y - VEL > 0:
        yellow.y -= VEL*VIRUS_VEL
    if rand_direction == 4 and yellow.y + VEL + yellow.height < HEIGHT -17:
        yellow.y += VEL*VIRUS_VEL


# Handles movement and see if bullets fired collides with the other spaceship.
# As both bullet and spaceship are rects, "colliderect" can be used to detect collision.
def handle_bullets(syringe, yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(RED_HIT)) # Set event to catch in main.
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) # Remove bullet if position is of screen.
        elif syringe.colliderect(bullet):
            yellow_bullets.remove(bullet)

    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # Set event to catch in main.
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet) # Remove bullet if position is of screen.


# Draw/redraw window.
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) # Insert background image.
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Render text for health scores.
    red_health_text = HEALTH_FONT.render("Starfighter Health: " + str(red_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    yellow_health_text = HEALTH_FONT.render("Virus Strength: " + str(yellow_health), 1, RED)
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # Set current position of yellow spaceship.
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) # Set current position of red spaceship.

    # Draw syringe.
    WIN.blit(SYRINGE, (WIDTH-500, HEIGHT-100)) # Set current position of red spaceship.
    
    # Draw all bullets.
    for bullet in red_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) # It is a red bullet, with yellow color. ;-)
        
    for bullet in yellow_bullets:
        # pygame.draw.rect(WIN, YELLOW, bullet)
        WIN.blit(VIRUS_BULLET, bullet)

    pygame.display.update()


def draw_winner(text1, text2):
    draw_text1 = WINNER_FONT.render(text1, 1, WHITE)
    WIN.blit(draw_text1, (WIDTH/2 - draw_text1.get_width()/2, HEIGHT/2 - 2*draw_text1.get_height()))
    draw_text2 = WINNER_FONT.render(text2, 1, WHITE)
    WIN.blit(draw_text2, (WIDTH/2 - draw_text2.get_width()/2, HEIGHT/2 - draw_text2.get_height()))
    pygame.display.update() 
    pygame.time.delay(7000) # Wait 5 sec before restarting the game.


def main():
    BACKGROUND_MUSIC.play(-1)
    show_start_screen()

    global single_player
    global MAX_BULLETS
    global VIRUS_VEL

    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Current position of red spaceship.
    yellow = pygame.Rect(200, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # Current position of yellow spaceship.
    syringe = pygame.Rect(WIDTH-500, HEIGHT-100, SYRINGE_WIDTH, SYRINGE_HEIGHT) # Permenant position of protecting syringe.

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS) # Controls the speed of the infinate loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_LCTRL:
                    # Player 2 touched controls. Switch to 2 player mode.
                    single_player = False
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # Fire bullet om left ctrl key if not more than MAX_BULLETS in frame.
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    VIRUS_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # Fire bullet om right ctrl key if not more than MAX_BULLETS in frame.
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # Let virus fire randomly.
        rand_fire = random.randrange(1, 50, 1)
        if rand_fire == 1 and single_player:
            bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
            yellow_bullets.append(bullet)
            VIRUS_FIRE_SOUND.play()


        winner_text1 =""
        winner_text2 =""
        if red_health <= 0:
            winner_text1 ="We are all dead!"
            winner_text2 ="Good job, buddy."
            MAX_BULLETS = 4
            VIRUS_VEL = 3
            single_player = True

        if yellow_health <= 0:
            if MAX_BULLETS == 3:
                if single_player:
                    winner_text1 ="Yes! You won the fight."
                else:
                    winner_text1 ="Yes! The Starfighter won."
                winner_text2 ="Prepare for the second wave!"
                VIRUS_VEL += 1
            if MAX_BULLETS == 2:
                winner_text1 ="Get ready for the third and final wave."
                if single_player:
                    winner_text2 ="Remember, the vaccine protects you!"
                else:
                    winner_text2 ="Tip: the vaccine protects the Starfighter!"
                VIRUS_VEL += 2
            if MAX_BULLETS == 1:
                winner_text1 ="Virus has finally been eliminated."
                if single_player:
                    winner_text2 ="You are a hero!"
                else:
                    winner_text2 ="The Starfighter pilot is a hero!"
                MAX_BULLETS = 4
                VIRUS_VEL = 3
                single_player = True

        if winner_text1 != "": # Someone won! 
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text1, winner_text2)
            break

        keys_pressed = pygame.key.get_pressed()
        if (single_player): 
            yellow_handle_movement_auto(yellow)
        else:
            yellow_handle_movement(keys_pressed, yellow)

        red_handle_movement(keys_pressed, red)

        handle_bullets(syringe, yellow_bullets,red_bullets,yellow,red) 

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit() # Quits the game and closes the window.
    BACKGROUND_MUSIC.stop() # Stop bg music before running main.
    MAX_BULLETS -= 1
    main() # When someone wins, you can just restart the game after 5 sec, instead of quitting and closing the window.


# Only run "main" if this file i run directly. 
# Don't run if it is imported into another file.
if __name__ == "__main__":
    main()
