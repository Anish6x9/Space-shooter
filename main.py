import pygame
import random
import math
import time  # Importing time to pause after game over

# intantiate a pygame object
pygame.init()  # Added parentheses to initialize pygame

# main game screen banauna(width(x-value), height(y-value))
screen = pygame.display.set_mode((900, 600))

# game ko name halna 
pygame.display.set_caption("Space shooter")

# load background image
background_img = pygame.image.load("./assets/background.jpg")

# load the window icon
win_icon = pygame.image.load("./assets/startup.png")
# set the window icon
pygame.display.set_icon(win_icon)

# audio halna mixer import garna parcha
from pygame import mixer

mixer.init()

# BGM haleko
mixer.music.load("./assets/backgroundTrack.mp3")
# play music in a loop by passing in -1
mixer.music.play(-1)

# shot sound
shot_sound = mixer.Sound("./assets/teleport.mp3")

# crash sound
crash_sound = mixer.Sound("./assets/shot.mp3")

# spaceship load garna as a player
player_img = pygame.image.load("./assets/spaceship.png")
# game maths nahujekai ramro tauko khancha
playerX = 410
playerY = 480
change_in_playerX = 0

# alian ko numbers 
enemy_img = []
enemyX = []
enemyY = []
change_in_enemyX = []
number_of_enemies = 4

for i in range(number_of_enemies):
    # aliean load gareko
    enemy_img.append(pygame.image.load("./assets/ufo.png"))
    enemyX.append(random.randint(64, 836))
    enemyY.append(random.randint(64, 160))
    change_in_enemyX.append(0.4)

# bullet laod gareko
bullet_img = pygame.image.load("./assets/bullet.png")
bulletY = 480
bulletX = 0
bullet_state = "loaded"
change_in_bulletY = 4

# score values
player_score = 0
high_score = 69  # High score initialized to 69

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)  # Decreased the font size of score
high_score_font = pygame.font.Font("freesansbold.ttf", 24)  # Same font for high score

# font coordinates
fontX = 15
fontY = 15

game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    # player image screen screen ma load gareko
    screen.blit(player_img, (x, y))
    
def enemy(x, y, i):
    # draw player image onto screen
    screen.blit(enemy_img[i], (x, y))

def shot(x, y):
    global bullet_state
    bullet_state = "fired"
    # draw bullet on the screen
    screen.blit(bullet_img, (x, y))

def isCollided(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

def display_score(x, y):
    # create an image to blit to the screen (score in white)
    score_img = font.render(f"Total Score: {str(player_score)}", True, (255, 255, 255))
    screen.blit(score_img, (x, y))
    
    # display high score in red at the top-right corner
    high_score_img = high_score_font.render(f"High Score: {str(high_score)}", True, (255, 0, 0))
    screen.blit(high_score_img, (700, 15))  # Adjusted position to top-right corner

def game_over():
    global high_score
    if player_score > high_score:  # Update high score if player score is greater
        high_score = player_score
    # Display the 'Game Over' message
    game_over_img = game_over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_img, (250, 250))  # Adjusted position for better centering
    restart_img = font.render("Press ENTER to Restart", True, (255, 255, 255))  # Added restart instruction
    screen.blit(restart_img, (270, 350))  # Display restart message
    pygame.display.update()  # Update the screen to show the Game Over message

    # Wait for the player to press Enter to restart
    wait_for_restart()

def wait_for_restart():
    global running
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Restart on Enter key press
                restart_game()
                return

def restart_game():
    global playerX, playerY, change_in_playerX, bulletY, bulletX, bullet_state, player_score
    playerX = 410
    playerY = 480
    change_in_playerX = 0
    bulletY = 480
    bulletX = 0
    bullet_state = "loaded"
    player_score = 0  # Reset player score after restart

    for i in range(number_of_enemies):
        enemyX[i] = random.randint(64, 836)
        enemyY[i] = random.randint(64, 160)

running = True

while running:
    # gettin' list of all game events happening
    for game_event in pygame.event.get():
        # checkin' if close btn pressed
        if game_event.type == pygame.QUIT:
            running = False

        # checkn' if key has been pressed
        if game_event.type == pygame.KEYDOWN:
            # checkn' out for the ESC key press 
            if game_event.key == pygame.K_ESCAPE:
                running = False
                
            # left arrow press garyo vane left jancha
            if game_event.key == pygame.K_LEFT:
                change_in_playerX = -0.55
            #right arrow press garyo vane right jancha  
            if game_event.key == pygame.K_RIGHT:
                change_in_playerX = 0.55
                
            # this here is not going to display the bullet continuously
            # to do this, we need to put it inside of the infinite while loop
            if game_event.key == pygame.K_SPACE:
                # we can only fire a loaded bullet
                if bullet_state == "loaded":
                    shot_sound.play()
                    bulletX = playerX
                    shot(bulletX, bulletY)
            
        # check if keystroke has been released
        if game_event.type == pygame.KEYUP:
            if game_event.key == pygame.K_LEFT or game_event.key == pygame.K_RIGHT:
                change_in_playerX = 0
                
    #BG color add garera matra load nahuda pass ni garna parcha
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))
    
    #yo chei screen.fill() vanda aagadi call garna parcha natra sapceship dekhaudaina
    #ani pygame.display.update() vandai aagadi call hannu parcha

    playerX += change_in_playerX
    
    # game boundaries haleko game maths sucksssssssssss!!!!!!!!!!!!!
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        # 900 - 64(size of img) = 836
        playerX = 836
        
    for i in range(number_of_enemies):
        
        # game over
        if enemyY[i] > 400:
            for j in range(number_of_enemies):
                enemyY[j] = -3000  # Move enemies off screen
            game_over()  # This ensures that the game stops after the game-over message
            break
        
        # enemy movement
        enemyX[i] += change_in_enemyX[i]
        # randint==random integer
        if enemyX[i] <= 0:
            change_in_enemyX[i] = 0.4
            enemyY[i] += random.randint(0, 60)
        elif enemyX[i] >= 836:
            change_in_enemyX[i] = -0.4
            enemyY[i] += random.randint(0, 60)
            
        # Collision detection
        if isCollided(bulletX, bulletY, enemyX[i], enemyY[i]):
            crash_sound.play()
            bulletY = 480
            # reset the bullet for the next round of shot
            bullet_state = "loaded"
            
            player_score += 1
            print(player_score)
            # respawn enemy to a random position, reduce the y-value from
            # 836 to 835
            enemyX[i] = random.randint(64, 835)
            enemyY[i] = random.randint(64, 160)
            
        enemy(enemyX[i], enemyY[i], i) 
               
    # bullets haru niskine tarika milako    
    if bulletY <= 0:
        # move bullet back to spacecraft y-position
        bulletY = 480
        # reset the bullet for the next round of shot
        bullet_state = "loaded"
        
    if bullet_state == "fired":
        shot(bulletX, bulletY)
        # move bullet in upward direction
        bulletY -= change_in_bulletY
    
    player(playerX, playerY)
    # display the score and high score here
    display_score(fontX, fontY)
    
    #game ma vako sapai kura haru update garna pygame.display.update() garna parcha
    # this is important for also player movements and the changes in the screen
    pygame.display.update()
    
pygame.quit()
