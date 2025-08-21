import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Fighter Test")

# Player setup
player_x, player_y = WIDTH//2, HEIGHT-120  # start near bottom
player_speed = 5
ground_y = HEIGHT-120
direction = 1
leaning = 0
action = None
jumping = False
jump_vel = 10
gravity = 1

def draw_player(x, y, step, leaning, action):
    win.fill((0,0,0))
    
    # Head
    pygame.draw.circle(win, (255,255,255), (x+15, y+10), 10)
    
    # Torso
    pygame.draw.line(win, (255,255,255), (x+15, y+20), (x+15+leaning, y+50), 3)
    
    # Arms
    if action == 'punch':
        pygame.draw.line(win, (255,255,255), (x-5, y+25), (x+50, y+25), 3)
        pygame.draw.line(win, (255,255,255), (x-5, y+35), (x+15, y+20), 3)
    else:
        pygame.draw.line(win, (255,255,255), (x-5, y+25), (x+35, y+30+step), 3)
        pygame.draw.line(win, (255,255,255), (x-5, y+35), (x+35, y+20-step), 3)
    
    # Legs
    if action == 'kick':
        pygame.draw.line(win, (255,255,255), (x+15+leaning, y+50), (x+50, y+50), 3)
        pygame.draw.line(win, (255,255,255), (x+15+leaning, y+50), (x-5, y+70-step), 3)
    else:
        pygame.draw.line(win, (255,255,255), (x+15+leaning, y+50), (x-5, y+70-step), 3)
        pygame.draw.line(win, (255,255,255), (x+15+leaning, y+50), (x+35, y+70+step), 3)
    
    pygame.display.update()

# Game loop
run = True
clock = pygame.time.Clock()
step = 5

while run:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    moving = False
    action = None

    # Movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        moving = True
        leaning = -3
    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
        moving = True
        leaning = 3
    else:
        leaning = 0
    
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        moving = True

    # Jump
    if not jumping and keys[pygame.K_w]:
        jumping = True
        jump_vel = 10

    if jumping:
        player_y -= jump_vel
        jump_vel -= gravity
        if player_y >= ground_y:
            player_y = ground_y
            jumping = False
            jump_vel = 10

    # Attack
    if keys[pygame.K_a]:
        action = 'punch'
    elif keys[pygame.K_s]:
        action = 'kick'

    if moving:
        direction *= -1

    draw_player(player_x, player_y, direction*step, leaning, action)

pygame.quit()
