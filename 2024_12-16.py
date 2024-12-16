import pygame
import sys
import random
import time


# 初始化 Pygame
pygame.init()

# 載入並播放背景音樂
pygame.mixer.music.load("C:/Users/zhen9/OneDrive/Desktop/My Project/BGM.mp3")  # 使用正確的路徑格式
pygame.mixer.music.set_volume(0.8)  # 設定音量（0.0 到 1.0）
pygame.mixer.music.play(-1)  # -1 表示無限循環播放

# 視窗設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Breakout Game")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS 設定
clock = pygame.time.Clock()
FPS = 60

# 蛇設定
snake_speed = 10
snake_position = [300, 350]
snake_body = [[300, 350], [290, 350], [280, 350]]
snake_direction = 'RIGHT'
change_to = snake_direction

# 球的設定
ball_speed_x = 5
ball_speed_y = -5
ball_position = [random.randint(50, WINDOW_WIDTH - 50), random.randint(50, WINDOW_HEIGHT // 2)]
ball_radius = 10

# 板子設定
paddle_width = 80
paddle_height = 10
paddle_position = [WINDOW_WIDTH // 2 - paddle_width // 2, WINDOW_HEIGHT - 20]

# 磚塊設定
brick_width = 50
brick_height = 20
brick_fall_speed = 2
bricks = []
brick_timer = 0
brick_delay = 500  # 每 1000 毫秒生成一個磚塊

# 分數
score = 0
font = pygame.font.Font(None, 36)

# 控制遊戲結束顯示的視窗
def game_over(final_score):
    # 載入音效
    game_over_sound = pygame.mixer.Sound("C:/Users/zhen9/OneDrive/Desktop/My Project/New_Project.mp3")  # 確保路徑正確
    game_over_sound.play()  # 播放音效

    # 顯示遊戲結束畫面
    window.fill(BLACK)
    game_over_text = font.render(f"Game Over! Final Score: {final_score}", True, RED)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
    pygame.display.flip()

    # 等待音效播放完成
    pygame.time.wait(int(game_over_sound.get_length() * 500))  # 等待音效播放的時間（毫秒）

    # 停止所有音效並退出
    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


# 遊戲循環
run = True
while run:
    window.fill(BLACK)
    
    # 處理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # 鍵盤控制蛇
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        change_to = 'UP'
    elif keys[pygame.K_DOWN]:
        change_to = 'DOWN'
    elif keys[pygame.K_LEFT]:
        change_to = 'LEFT'
    elif keys[pygame.K_RIGHT]:
        change_to = 'RIGHT'

    # 確保蛇不會反向移動
    if change_to == 'UP' and not snake_direction == 'DOWN':
        snake_direction = 'UP'
    if change_to == 'DOWN' and not snake_direction == 'UP':
        snake_direction = 'DOWN'
    if change_to == 'LEFT' and not snake_direction == 'RIGHT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT' and not snake_direction == 'LEFT':
        snake_direction = 'RIGHT'

    # 更新蛇的位置
    if snake_direction == 'UP':
        snake_position[1] -= snake_speed
    elif snake_direction == 'DOWN':
        snake_position[1] += snake_speed
    elif snake_direction == 'LEFT':
        snake_position[0] -= snake_speed
    elif snake_direction == 'RIGHT':
        snake_position[0] += snake_speed

    # 限制蛇在視窗內，並根據碰撞邊界改變位置
    if snake_position[0] < 0:
        snake_position[0] = WINDOW_WIDTH - 10
    elif snake_position[0] >= WINDOW_WIDTH:
        snake_position[0] = 0
    if snake_position[1] < 0:
        snake_position[1] = WINDOW_HEIGHT - 10
    elif snake_position[1] >= WINDOW_HEIGHT:
        snake_position[1] = 0

    # 更新蛇的身體
    snake_body.insert(0, list(snake_position))
    if len(snake_body) > 15:
        snake_body.pop()

    # 更新球的位置
    ball_position[0] += ball_speed_x
    ball_position[1] += ball_speed_y

    # 球與視窗邊界碰撞
    if ball_position[0] <= ball_radius or ball_position[0] >= WINDOW_WIDTH - ball_radius:
        ball_speed_x *= -1
    if ball_position[1] <= ball_radius:
        ball_speed_y *= -1
    if ball_position[1] >= WINDOW_HEIGHT:
        print("Game Over! Final Score:", score)
        game_over(score)

    # 球與板子的碰撞
    paddle_rect = pygame.Rect(paddle_position[0], paddle_position[1], paddle_width, paddle_height)
    if paddle_rect.collidepoint(ball_position[0], ball_position[1] + ball_radius):
        ball_speed_y *= -1

    # 滑鼠控制板子
    mouse_x, _ = pygame.mouse.get_pos()
    paddle_position[0] = mouse_x - paddle_width // 2
    paddle_position[0] = max(0, min(WINDOW_WIDTH - paddle_width, paddle_position[0]))

    # 更新磚塊位置
    brick_timer += clock.get_time()
    if brick_timer > brick_delay:
        brick_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        new_brick = pygame.Rect(random.randint(0, WINDOW_WIDTH - brick_width), 
                                random.randint(-300, -20), 
                                brick_width, 
                                brick_height)
        bricks.append(new_brick)
        brick_timer = 0

    # 磚塊下落
    for brick in bricks[:]:
        brick.y += brick_fall_speed
        if brick.y > WINDOW_HEIGHT:
            bricks.remove(brick)  # 移除超出視窗的磚塊
            score -= 5  # 磚塊掉落扣分
            if score <= -30:
                game_over(score)

    # 檢查蛇吃磚塊
    for brick in bricks[:]:
        snake_rect = pygame.Rect(snake_position[0], snake_position[1], 10, 10)
        if snake_rect.colliderect(brick):
            bricks.remove(brick)
            score += 10

    # 磚塊與球的碰撞
    for brick in bricks[:]:
        if brick.collidepoint(ball_position):
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 10

    # 繪製磚塊
    for brick in bricks:
        pygame.draw.rect(window, RED, brick)

    # 繪製蛇
    for segment in snake_body:
        pygame.draw.rect(window, GREEN, pygame.Rect(segment[0], segment[1], 10, 10))

    # 繪製板子
    pygame.draw.rect(window, BLUE, paddle_rect)

    # 繪製球
    pygame.draw.circle(window, WHITE, ball_position, ball_radius)

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
