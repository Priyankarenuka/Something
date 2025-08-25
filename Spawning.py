import pygame, random

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

# Enemy setup
enemy_x, enemy_y = WIDTH//2 - 150, HEIGHT-120
enemy_speed = 6  # <-- slightly faster than player
enemy_dir = 1
enemy_lean = 0
enemy_action = None
enemy_jumping = False
enemy_jump_vel = 10
enemy_timer = 0   # timer for delay

def draw_player(x, y, step, leaning, action, color=(255,255,255)):
    # Head
    pygame.draw.circle(win, color, (x+15, y+10), 10)
    
    # Torso
    pygame.draw.line(win, color, (x+15, y+20), (x+15+leaning, y+50), 3)
    
    # Arms
    if action == 'punch':
        pygame.draw.line(win, color, (x-5, y+25), (x+50, y+25), 3)
        pygame.draw.line(win, color, (x-5, y+35), (x+15, y+20), 3)
    else:
        pygame.draw.line(win, color, (x-5, y+25), (x+35, y+30+step), 3)
        pygame.draw.line(win, color, (x-5, y+35), (x+35, y+20-step), 3)
    
    # Legs
    if action == 'kick':
        pygame.draw.line(win, color, (x+15+leaning, y+50), (x+50, y+50), 3)
        pygame.draw.line(win, color, (x+15+leaning, y+50), (x-5, y+70-step), 3)
    else:
        pygame.draw.line(win, color, (x+15+leaning, y+50), (x-5, y+70-step), 3)
        pygame.draw.line(win, color, (x+15+leaning, y+50), (x+35, y+70+step), 3)

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

    # Movement (Player)
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
    if keys[pygame.K_UP]:  # <-- upward movement
        player_y -= player_speed
        moving = True

    # Keep player inside screen
    player_x = max(0, min(player_x, WIDTH-30))
    player_y = max(0, min(player_y, HEIGHT-30))

    # Jump (Player)
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

    # Attack (Player)
    if keys[pygame.K_a]:
        action = 'punch'
    elif keys[pygame.K_s]:
        action = 'kick'

    if moving:
        direction *= -1

    # -------- Enemy movement: chase player with delay --------
    enemy_timer += 1
    if enemy_timer > 5:   # <-- delay enemy update (higher number = more delay)
        if enemy_x < player_x:
            enemy_x += enemy_speed
            enemy_lean = 3
            enemy_dir *= -1
        elif enemy_x > player_x:
            enemy_x -= enemy_speed
            enemy_lean = -3
            enemy_dir *= -1

        if enemy_y < player_y:
            enemy_y += enemy_speed
        elif enemy_y > player_y:
            enemy_y -= enemy_speed

        enemy_timer = 0  # reset delay timer

    # Enemy jump physics
    if enemy_jumping:
        enemy_y -= enemy_jump_vel
        enemy_jump_vel -= gravity
        if enemy_y >= ground_y:
            enemy_y = ground_y
            enemy_jumping = False
            enemy_jump_vel = 10

    # -------- Keep enemy inside screen + respawn if out --------
    if enemy_x < 0 or enemy_x > WIDTH-30 or enemy_y < 0 or enemy_y > HEIGHT-30:
        enemy_x = random.randint(50, WIDTH-50)
        enemy_y = random.randint(50, HEIGHT-150)

    enemy_x = max(0, min(enemy_x, WIDTH-30))
    enemy_y = max(0, min(enemy_y, HEIGHT-30))

    # -------- Draw everything --------
    win.fill((0,0,0))
    draw_player(player_x, player_y, direction*step, leaning, action, (255,255,255)) # Player white
    draw_player(enemy_x, enemy_y, enemy_dir*step, enemy_lean, enemy_action, (255,0,0)) # Enemy red
    pygame.display.update()

pygame.quit()
