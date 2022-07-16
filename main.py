import pygame
import random
import datetime


# Initialize
pygame.init()
board_dict = {"left" : 0, "right" : 0, "up" : 0, "down" : 0}
initial_time = datetime.datetime.now()
start_time = {"left": initial_time, "right": initial_time, "up" : initial_time, "down" : initial_time}
pressed_button = {"left": False, "right": False, "up" : False, "down" : False}

# Assets
icon = pygame.image.load("Assets/ufo.png")
background_img = pygame.image.load("Assets/background.png")
enemyImg = pygame.image.load("Assets/enemy.png")
PLAYER = pygame.image.load("Assets/battleship.png")
bullet = pygame.image.load("Assets/bullet.png")

bullet_reset_time_start = None
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
current_bullet = 6
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Spaceship
PLAYER_X = 420
PLAYER_Y = 380
change = 4.0

# List
bulletList = []
enemyList = [[enemyX,enemyY,"right"]]   


def speed_up(limit: int, milisecond: int, speeding: float, speed: float, pressed : bool, timeee: datetime.datetime, left_up: bool = False):
    check_time = datetime.datetime.now()
    difference = check_time - timeee
    difference_in_miliseconds = difference.microseconds

    if left_up == True:  
        if speed > 0:
            speed = 0
        if abs(speed) <= limit: 
            if pressed == True:
                if difference_in_miliseconds < milisecond:
                    return speed
                else: 
                    if abs(speed) != 4:
                        return speed + speeding
                
            if pressed == False:
                if difference_in_miliseconds < milisecond:
                    return speed
                else:
                    if speed == 0:
                        return speed 
                    return speed - speeding/4
        else:
            speed = -limit
        return speed

    if left_up == False:  
        if speed < 0: 
            speed = 0
        if speed <= limit: 
            if pressed == True:
                if difference_in_miliseconds < milisecond:
                    return speed
                else: 
                    if speed != 4:
                        return speed + speeding
                
            if pressed == False:
                if difference_in_miliseconds < milisecond:
                    return speed
                else:
                    if speed == 0:
                        return speed 
                    return speed - speeding/4
        else:
            speed = limit
        return speed

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
    

first_encounter = True
running = True
game_over = False
# Game loop
while running:
    # Black screen
    screen.fill((0,0,0))
    # Background
    screen.blit(background_img,(0,0))
    show_score(textX, textY)
    show_bullet(current_bullet, 10, 70)
    
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
                    start_time["left"] = datetime.datetime.now()
                    pressed_button["left"] = True
                if event.key == pygame.K_d:
                    start_time["right"] = datetime.datetime.now()
                    pressed_button["right"] = True
                if event.key == pygame.K_w:
                    start_time["up"] = datetime.datetime.now()
                    pressed_button["up"] = True
                if event.key == pygame.K_s:
                    start_time["down"] = datetime.datetime.now()
                    pressed_button["down"] = True
                if event.key == pygame.K_SPACE:
                    if current_bullet > 0:
                        bullet_X = PLAYER_X
                        bullet_Y = PLAYER_Y
                        bulletList.append([bullet_X + 16,bullet_Y - 10, True])
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    start_time["left"] = datetime.datetime.now()
                    pressed_button["left"] = False
                if event.key == pygame.K_d:
                    start_time["right"] = datetime.datetime.now()
                    pressed_button["right"] = False
                if event.key == pygame.K_w:
                    start_time["up"] = datetime.datetime.now()
                    pressed_button["up"] = False
                if event.key == pygame.K_s:
                    start_time["down"] = datetime.datetime.now()
                    pressed_button["down"] = False
            
        board_dict["left"] = speed_up(4,50,-0.2,board_dict["left"], pressed_button["left"], start_time["left"], True)
        board_dict["right"] = speed_up(4,50,0.2,board_dict["right"], pressed_button["right"], start_time["right"], False)
        board_dict["up"] = speed_up(4,50,-0.2,board_dict["up"], pressed_button["up"], start_time["up"], True)
        board_dict["down"] = speed_up(4,50,0.2,board_dict["down"], pressed_button["down"], start_time["down"], False)
        
        """if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    board_dict["left"] = -change
                if event.key == pygame.K_d:
                    board_dict["right"] = change
                if event.key == pygame.K_w:
                    board_dict["up"] = -change
                if event.key == pygame.K_s:
                    board_dict["down"] = change
                if event.key == pygame.K_SPACE:
                    if current_bullet > 0:
                        bullet_X = PLAYER_X
                        bullet_Y = PLAYER_Y
                        bulletList.append([bullet_X + 16,bullet_Y - 10, True])
                    
                    
            if event.type == pygame.KEYUP:
                if  event.key == pygame.K_a:
                    board_dict["left"] = 0
                if event.key == pygame.K_d:
                    board_dict["right"] = 0
                if  event.key == pygame.K_w:
                    board_dict["up"] = 0
                if event.key == pygame.K_s:
                    board_dict["down"] = 0"""
            
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
            i[1] -= 10  # BulletList is a 2 dimensional array, every member has 2 coordinates so i[1] correspondsa to Y dimension
            for j in enemyList:
                isColide = isCollision(i[0], i[1], j[0], j[1])
                if isColide is True:
                    score += 1
                    enemyList.remove(j)
                    if i[2] == True:
                        i[2] = False
                        bulletList.remove(i)
                    current_num_enemy -= 1
                    if current_bullet < bullet_limit:
                        current_bullet += 1
                    if current_num_enemy < 0:
                        enemyX = random.randint(0,736)
                        enemyY = random.randint(50,150)
                        enemyList.append([enemyX, enemyY, "right"])
                        current_num_enemy += 1


            
        for i in bulletList:
            if i[1] < -50:
                bulletList.remove(i)
                current_bullet -= 1 # Bullet Iska
        
        if current_bullet == 0 and first_encounter == True:
            first_encounter = False
            bullet_reset_time_start = datetime.datetime.now()

        # Bullet cooling
        if current_bullet <= 0:
            bullet_reset_time_end = datetime.datetime.now()
            try:
                difference = bullet_reset_time_end - bullet_reset_time_start
            except:
                pass
            # print(type(difference)) -> datetime.timedelta
            time = difference.seconds + difference.microseconds/10**6
            show_cool_down(int(round(time)), 10, 40)
            if time > 5:
                current_bullet = 6
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
            score = 0
            bullet_limit = 6
            current_bullet = 6
            
        
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