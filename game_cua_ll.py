import pygame
import random
import cv2

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Screen dimensions
width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PIRATE ADVANTURE')

# Colors
yellow = (255, 255, 102)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green =(0,255,0)
red_black = (139, 0, 0)
# Game settings
block_size = 50
snake_speed = 7

background_img = pygame.image.load("./images/background1.jpg")
background_img = pygame.transform.scale(background_img, (width, height))

start_bg_img = pygame.image.load("./images/screenStart.jpg")
start_bg_img = pygame.transform.scale(start_bg_img, (width, height))

lose_bg_img = pygame.image.load("./images/screenLose.jpg")
lose_bg_img = pygame.transform.scale(lose_bg_img, (width, height))

food_img = pygame.image.load("./images/fod.png")
food_img = pygame.transform.scale(food_img, (block_size, block_size))

boom_img = pygame.image.load("./images/boom.png")
boom_img = pygame.transform.scale(boom_img, (block_size, block_size))

poison_img = pygame.image.load("./images/poison.png")
poison_img = pygame.transform.scale(poison_img, (block_size, block_size))

# Load music
pygame.mixer.music.load("./sounds/soundGame.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

food_sound = pygame.mixer.Sound("./sounds/soundEatFood.mp3")
lose_sound = pygame.mixer.Sound("./sounds/soundLose.mp3")

# Fonts
title_font = pygame.font.SysFont("comicsansms", 75)
message_font = pygame.font.SysFont("comicsansms", 35)
chuto = pygame.font.SysFont("comicsansms", 45) 
def select_boat_screen():
    # Danh sách các thuyền
    boat_images = [
        pygame.transform.scale(pygame.image.load("./images/ship5.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship2.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship4.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship7.png"), (block_size, block_size))
    ]

    selected_boat = 0  # Vị trí thuyền được chọn ban đầu
    boat_count = len(boat_images)

    selecting = True
    while selecting:

        new_width = block_size * 2  # Tăng kích thước lên gấp đôi
        new_height = block_size * 2
        boat_image_scaled = pygame.transform.scale(boat_images[selected_boat], (new_width, new_height))
        # Vẽ background màn hình chọn thuyền
        screen.fill(black)
        draw_text("Select Your Boat", title_font, yellow, width / 2, height / 3)

        # Hiển thị thuyền hiện đang được chọn
        screen.blit(boat_image_scaled , (width // 2 - new_width // 2, height // 2 - new_height // 2))

        draw_text("Use Left/Right to Choose", message_font, white, width / 2, height / 2 + new_height // 2 + 100)
        draw_text("Press OK to Start", message_font, white, width / 2, height / 2 + new_height // 2 + 150)

        pygame.display.update()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_boat = (selected_boat - 1) % boat_count  
                elif event.key == pygame.K_RIGHT:
                    selected_boat = (selected_boat + 1) % boat_count 
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return selected_boat  


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def start_screen():
    screen.blit(start_bg_img, (0, 0))
    
    draw_text("Press SPACE to Start", chuto, black, width/1.9, height/1.3)
    draw_text("Use Arrow Keys to Move", chuto, black, width/1.9, height/1.3 + 50)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def your_score(score):
    value = message_font.render("Score: " + str(score), True, yellow)
    screen.blit(value, [10, 10])

def our_snake(snake_list, snake_img):
    for segment in snake_list:
        screen.blit(snake_img, (segment[0], segment[1]))

def gameLoop():
    selected_boat_index = select_boat_screen()
    boat_images = [
        pygame.transform.scale(pygame.image.load("./images/ship5.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship2.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship4.png"), (block_size, block_size)),
        pygame.transform.scale(pygame.image.load("./images/ship7.png"), (block_size, block_size))
    ]
    snake_img = boat_images[selected_boat_index]
    score = 0
    speed = snake_speed
    game_over = False
    game_close = False

    x1 = width // 2
    y1 = height // 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1


    # Random item generation
   
    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size
    item_die_list = []


    aprear_die = False
    clock = pygame.time.Clock()
    lose_sound_played = False 
    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            if not lose_sound_played:
                lose_sound.play()
                lose_sound_played = True
            screen.blit(lose_bg_img, (0, 0))
            draw_text("Game Over!", title_font, red, width/2, height/3)
            draw_text(f"Your Score: {score}", message_font, red, width/2, height/2)
            draw_text("Press C to Play Again", message_font, red, width/2, height/2 + 50)
            draw_text("Press Q to Quit", message_font, red, width/2, height/2 + 100)
            pygame.display.update()  
            # nhập q để quit c để tiếp tục
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(-1)
                        gameLoop()
        # di chuyển 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0
            


        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.blit(background_img, (0, 0))

        screen.blit(food_img, (foodx, foody))
        for item_die, diex, diey in item_die_list:
            if item_die == 'boom':
                screen.blit(boom_img, (diex, diey))  
            else:
                screen.blit(poison_img, (diex, diey))  

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        our_snake(snake_List, snake_img)
        your_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            food_sound.play()  # Phát âm thanh khi ăn
            score += 1  # Tăng điểm
            aprear_die = True
            if aprear_die:
                # Random vị trí của boom hoặc poison
                item_die = random.choice(['boom', 'poison'])
                diex = round(random.randrange(0, width - block_size) / block_size) * block_size
                diey = round(random.randrange(0, height - block_size) / block_size) * block_size
            item_die_list.append((item_die, diex, diey))

            # Random lại vị trí của thức ăn mới và kiểm tra trùng với các item
            while True:
                foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
                foody = round(random.randrange(0, height - block_size) / block_size) * block_size
                if not any(diex == foodx and diey == foody for _, diex, diey in item_die_list):
                    break  # Thoát vòng lặp khi vị trí food không trùng

        # Xử lý va chạm với Boom và Poison
        for item_die, diex, diey in item_die_list:
            if x1 == diex and y1 == diey:
                if item_die == 'poison':
                    score -= 1  # Trừ 1 điểm khi ăn Poison
                    item_die_list.remove((item_die, diex, diey))  # Xóa Poison khỏi danh sách
                elif item_die == 'boom':
                    game_close = True  # Thua game khi ăn Boom

        clock.tick(speed)

    pygame.quit()
    quit()

# Main game execution
start_screen()
gameLoop()
