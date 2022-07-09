import pygame
import random
import datetime


# Initialize
pygame.init()
board_dict = {"left" : 0, "right" : 0, "up" : 0, "down" : 0}

# Assets
icon = pygame.image.load("Assets/ufo.png")
background_img = pygame.image.load("Assets/background.png")
enemyImg = pygame.image.load("Assets/enemy.png")
PLAYER = pygame.image.load("Assets/battleship.png")
bullet = pygame.image.load("Assets/bullet.png")


# Screen
screen = pygame.display.set_mode((800,600))


# Title Icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# Enemy (First)
enemyChangeX, enemyChangeY = 2.5, 25
enemyX = random.randint(0,736)
enemyY = random.randint(50,150)
current_num_enemy = 1
max_enemy_limit = 10
enemy_creation_time = datetime.datetime.now()

# interface
score = 0
time = 5
bullet_limit = 6
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Spaceship
PLAYER_X = 420
PLAYER_Y = 380
change = 4

# List
bulletList = []
enemyList = [[enemyX,enemyY,"right"]]   #  

def show_score(x, y):
    score_disp = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_disp, (x, y))

def show_cool_down(passed, x, y):
    cool_disp = font.render("CD: "+ str(5-passed), True, (255, 255, 255))
    screen.blit(cool_disp, (x, y))

def show_bullet(bullet, x, y):
    bullet_disp = font.render("Bullet: " + str(bullet), True, (255, 255, 255))
    screen.blit(bullet_disp, (x, y))

def show_game_over(x, y):
    game_disp = font.render("""Game Over, press R for Replay Q for quit""", True, (255, 255, 255))
    screen.blit(game_disp, (x, y))

def imageBlit(image: pygame.image, X: int, Y: int):
    screen.blit(image,(X,Y))

def isCollision(x_1 : int, y_1 : int, enemyX : int, enemyY : int):
    """
    x_1 and y_1 are player or bullet
    """
    distance = ((x_1-enemyX)**2 + (y_1-enemyY)**2)**(1/2)
    if distance < 27: 
        return True
    else:
        return False

def enemyCreation(last_enemy_creation_time):
    enemy_creation_time = last_enemy_creation_time
    if current_num_enemy < max_enemy_limit:
        timee = datetime.datetime.now()
        difference = timee - enemy_creation_time
        if difference.seconds > 0.5:
            enemy_creation_time = timee
            return [True, enemy_creation_time]
        else:
            return [False, enemy_creation_time] 
    return [False, enemy_creation_time]
    

first_encounter =   True
running = True
game_over = False
# Game loop
while running:
    # Black screen
    screen.fill((0,0,0))
    # Background
    screen.blit(background_img,(0,0))
    show_score(textX, textY)
    show_bullet(bullet_limit, 10, 70)
    
    if game_over == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False
                    enemy_creation_time = datetime.datetime.now()

                if event.key == pygame.K_q:
                    running = False
                
            if event.type == pygame.QUIT:
                running = False
            

    elif game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    board_dict["left"] = -change
                if event.key == pygame.K_d:
                    board_dict["right"] = change
                if event.key == pygame.K_w:
                    board_dict["up"] = -change
                if event.key == pygame.K_s:
                    board_dict["down"] = change
                if event.key == pygame.K_SPACE:
                    if bullet_limit > 0:
                        bullet_X = PLAYER_X
                        bullet_Y = PLAYER_Y
                        bulletList.append([bullet_X + 16,bullet_Y - 10])
                        bullet_limit -= 1
                    if bullet_limit == 0 and first_encounter == True:
                        first_encounter = False
                        bullet_reset_time_start = datetime.datetime.now()
            
            if event.type == pygame.KEYUP:
                if  event.key == pygame.K_a:
                    board_dict["left"] = 0
                if event.key == pygame.K_d:
                    board_dict["right"] = 0
                if  event.key == pygame.K_w:
                    board_dict["up"] = 0
                if event.key == pygame.K_s:
                    board_dict["down"] = 0
            
        # Player

        PLAYER_X += board_dict["left"] + board_dict["right"]
        PLAYER_Y += board_dict["up"] + board_dict["down"]

        if PLAYER_X < 0:
            temp = pygame.image.load("Assets/battleship.png")
            temp_x = 800 + PLAYER_X
            temp_y = PLAYER_Y

            imageBlit(image = temp, X = temp_x, Y = temp_y)
            if temp_x < 736:
                PLAYER = temp
                PLAYER_X = temp_x
                PLAYER_Y = temp_y
                temp = None
            
        elif PLAYER_X > 736: 
            temp = pygame.image.load("Assets/battleship.png")
            temp_x = (PLAYER_X - 736) - 64
            temp_y = PLAYER_Y
            
            imageBlit(image = temp, X = temp_x, Y = temp_y)
            if temp_x > 0: 
                PLAYER = temp
                PLAYER_X = temp_x
                PLAYER_Y = temp_y
                temp = None



        # Bullets
        for i in bulletList:
            i[1] -= 10  # BulletList is a 2 dimensional array, every member has 2 coordinates so i[1] corresponds to Y dimension
            for j in enemyList:
                isColide = isCollision(i[0], i[1], j[0], j[1])
                if isColide is True:
                    score += 1
                    enemyList.remove(j)
                    bulletList.remove(i)
                    current_num_enemy -= 1
                    bullet_limit += 1
                    if current_num_enemy == 0:
                        enemyX = random.randint(0,736)
                        enemyY = random.randint(50,150)
                        enemyList.append([enemyX, enemyY, "right"])
                        current_num_enemy += 1


            
        for i in bulletList:
            if i[1] < 0:
                bulletList.remove(i)

        # Bullet cooling
        if bullet_limit <= 0:
            bullet_reset_time_end = datetime.datetime.now()
            difference = bullet_reset_time_end - bullet_reset_time_start
            # print(type(difference)) -> datetime.timedelta
            time = difference.seconds + difference.microseconds/10**6
            show_cool_down(int(round(time)), 10, 40)
            if time > 5:
                bullet_limit = 6
                first_encounter = True

        else: show_cool_down(0,10,40)
                
        # player Y boundary
        if PLAYER_Y > 536:
            PLAYER_Y = 536
        elif PLAYER_Y < 0:
            PLAYER_Y = 0
        
        # enemy
        status, timeee = enemyCreation(enemy_creation_time)
        if status == True:
            enemyX = random.randint(0,736)
            enemyY = random.randint(50,150)
            enemyList.append([enemyX, enemyY, "right"])
            current_num_enemy += 1
            enemy_creation_time = timeee

        for enemy in enemyList:
            if enemy[2] == "right":
                enemy[0] += enemyChangeX    
                if enemy[0] > 736:
                    enemy[1] += enemyChangeY
                    enemy[0] = 736
                    enemy[0] -= enemyChangeX
                    enemy[2] = "left"

            elif enemy[2] == "left":
                enemy[0] -= enemyChangeX    
                if enemy[0] < 0:
                    enemy[1] += enemyChangeY
                    enemy[0] = 0
                    enemy[0] += enemyChangeX
                    enemy[2] = "right"

        if enemy[1] > 600:
            enemyList.remove(enemy)

        # Game Over
        for enemy in enemyList:
            isColide = isCollision(PLAYER_X, PLAYER_Y, enemy[0], enemy[1])
            if isColide is True:
                show_game_over(100,250)
                game_over = True
                PLAYER_X = 420
                PLAYER_Y = 380
                board_dict = {"left" : 0, "right" : 0, "up" : 0, "down" : 0}
                break
        if game_over == True:
            print(len(enemyList))
            enemyList = []
            current_num_enemy = 0
            
        
        # Blitting
        # bullets
        for i in bulletList:
            bulletX, bulletY = i[0], i[1]
            imageBlit(image = bullet, X = bulletX, Y = bulletY)
        # enemies
        for enemy in enemyList:
            imageBlit(image = enemyImg, X = enemy[0], Y=enemy[1])
        # player
        imageBlit(image = PLAYER, X = PLAYER_X, Y = PLAYER_Y)

        pygame.display.update()