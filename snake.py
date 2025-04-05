
import pygame
import random
pygame.init()
#экран
WIDTH, HEIGHT = 600,400
YELLOW=(243, 242, 17)
WHITE=(255,255,255)
GREEN=(37, 212, 28)
RED=(236, 45, 25)
BLUE=(56,122,164)
CELL_SIZE=20
score=0
level=1
last_level_score=0
snake_speed=10
screen=pygame.display.set_mode((WIDTH,HEIGHT))
score_font=pygame.font.Font(None,50)
font=pygame.font.Font(None,50)
level_font=pygame.font.Font(None,50)
game_over_flag=False
snake=[(100,100), (90,100),(80,100)]
snake_d=(CELL_SIZE,0)
food=pygame.Rect(random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE), CELL_SIZE, CELL_SIZE)
coin=pygame.Rect(random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0,HEIGHT, CELL_SIZE), CELL_SIZE,CELL_SIZE)
coin_timer=pygame.time.get_ticks()
clock=pygame.time.Clock()
running=True
while running:
    #управление
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP and snake_d != (0, CELL_SIZE):
                snake_d=(0,-CELL_SIZE)
            elif event.key==pygame.K_DOWN and snake_d !=(0, -CELL_SIZE):
                snake_d=(0, CELL_SIZE)
            elif event.key==pygame.K_RIGHT and snake_d !=(CELL_SIZE, 0):
                snake_d=(CELL_SIZE,0)
            elif event.key==pygame.K_LEFT and snake_d !=(-CELL_SIZE,0):
                snake_d=(-CELL_SIZE,0)
    new_head=(snake[0][0]+ snake_d[0], snake[0][1] + snake_d[1])
    snake.insert(0,new_head)
    if not game_over_flag:
     #столкновение с едой 
     if food.colliderect(pygame.Rect(*new_head, CELL_SIZE, CELL_SIZE)):
        food=pygame.Rect(random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE), CELL_SIZE, CELL_SIZE)
        score+=1
     else:
        snake.pop()
     #столкновение с монетой
     if coin and coin.colliderect(pygame.Rect(*new_head, CELL_SIZE, CELL_SIZE)):
         score+=2
         coin=None
     if coin and pygame.time.get_ticks()-coin_timer>7000:
         coin=None
     if not coin :
         coin=pygame.Rect(random.randrange(0,WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE), CELL_SIZE, CELL_SIZE)
         coin_timer=pygame.time.get_ticks()
    #переход на следующий уровень
     if score%3==0 and score !=last_level_score:
         level+=1
         snake_speed+=2
         last_level_score=score
     #условие если вышли за экран
     if (new_head in snake[1:] or
       new_head[0]<0 or new_head[0]>= WIDTH or
       new_head[1]<0 or new_head[1]>=HEIGHT):
        snake.pop()
        running=False
        game_over_flag=True
    screen.fill(GREEN if not game_over_flag else RED)
    score_text = score_font.render(str(score), True, (255,255,255))
    level_text = level_font.render(str(level), True, (0, 0, 1))
    screen.blit(score_text, (500, 10))
    screen.blit(level_text, (30,10))
    #прориссовка
    if not game_over_flag:
      for segment in snake:
        pygame.draw.rect(screen, YELLOW, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen,RED, food )
    if coin:
     pygame.draw.rect(screen, BLUE, coin)
    if game_over_flag:
        game_over_text=font.render("Game over", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2-100, HEIGHT//2))
    clock.tick(snake_speed)
    pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
