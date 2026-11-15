import pygame
import random as rand
import asyncio
import math as m
import os
# pygame setup
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Default.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 36)
start_time = pygame.time.get_ticks()
dt = 0

score = clock.tick()/100
vel = 550
b_vel = 450
angle = m.radians(90)
radius = 25

phase = 1
image_path = os.path.join("Sans.png")
player_image = pygame.image.load(image_path).convert_alpha()

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
circle_pos = pygame.Vector2(screen.get_width() / 2, 40)

def check_circle_rect_collision(circle_x, circle_y, radius, rect):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))

    # Calculate the distance between the circle's center and this closest point
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y

    # Compare squared distance to squared radius (avoids slow square root math)
    distance_squared = (distance_x ** 2) + (distance_y ** 2)
    return distance_squared <= (radius ** 2)

# 2. Track whether the title screen is active
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    elapsed_ms = pygame.time.get_ticks() - start_time
    elapsed_minutes = pygame.time.get_ticks() - start_time
    score = int(elapsed_ms / 1000)
    if (1300 >= b_vel >= -1300) and score <= 12:
        if b_vel < 0:
            b_vel -= elapsed_minutes/500
        else:
            b_vel += elapsed_minutes/500
    elif 12 < score < 15:
        b_vel = 2000



    circle_uno = pygame.draw.circle(screen, "white", (circle_pos.x,circle_pos.y), radius)
    border = pygame.draw.rect(screen, "white", (0,0, screen.get_width(), screen.get_height()),10)
    player = pygame.draw.rect(screen, "white", (player_pos.x, player_pos.y, 175, 25))
    border.clamp_ip(screen.get_rect())
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= vel * dt
    if keys[pygame.K_s]:
        player_pos.y += vel * dt
    if keys[pygame.K_a]:
        player_pos.x -= vel * dt
    if keys[pygame.K_d]:
        player_pos.x += vel * dt

    if player.x >= screen.get_width() or player.x <= 0 or player.y >= screen.get_height() or player.y <=0:
        running = False

    circle_pos.x += m.cos(angle) * b_vel * dt
    circle_pos.y += m.sin(angle) * b_vel * dt

    if circle_pos.y <= 0 or circle_pos.y >= screen.get_height() or circle_pos.x <= 0 or circle_pos.x >= screen.get_width():
        if circle_pos.y <= 0:
            circle_pos.y = radius+1
        if circle_pos.x <= 0:
            circle_pos.x = radius+1
        if circle_pos.x >= screen.get_width():
            circle_pos.x = screen.get_width()-(radius+1)
        if circle_pos.y >= screen.get_height():
            circle_pos.y = screen.get_height()-(radius+1)
        angle = rand.randint(rand.randint(1,90), rand.randint(90,179))
        angle *= -1
        m.radians(angle)
        b_vel*=-1

    if check_circle_rect_collision(circle_pos.x, circle_pos.y, radius, player):
        running = False
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))
    score_surface = font.render(f"Velocity: {b_vel}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 100))
    # flip() the display to put your work on screen
    pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()