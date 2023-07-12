# GitHub:
# https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_sprite_and_sprite_mask.md
#
# Stack Overflow:
# https://stackoverflow.com/questions/58662215/check-collision-between-a-image-and-a-line/58662648#58662648

import math
import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

moving_object = pygame.image.load('ranxbomberinverse.jpg').convert_alpha()
obstacle = pygame.Surface((200, 200), pygame.SRCALPHA)
moving_object_mask = pygame.mask.from_surface(moving_object)
angle = 0
red = 1

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    moving_object_rect = moving_object.get_rect(center = pygame.mouse.get_pos())
    #moving_object_rect = moving_object.get_rect(center = (window.get_width() // 2, window.get_height() // 2 - 70))

    vec = round(math.cos(angle * math.pi / 180) * 100), round(math.sin(angle * math.pi / 180) * 100)
    angle = (angle + 1) % 360
    obstacle.fill(0)
    pygame.draw.line(obstacle, (255, 255, 0), (100 - vec[0], 100 - vec[1]), (100 + vec[0], 100 + vec[1]), 5)
    obstacle_mask = pygame.mask.from_surface(obstacle)
    obstacle_rect = obstacle.get_rect(center = window.get_rect().center)

    offset = (obstacle_rect.x - moving_object_rect.x), (obstacle_rect.y - moving_object_rect.y)
    background_color = (0, 0, 0)
    if moving_object_mask.overlap(obstacle_mask, offset):
        red = min(255, red+4)
        background_color = (red, 0, 0)
    else: 
        red = 1

    window.fill(background_color)
    window.blit(moving_object, moving_object_rect)
    window.blit(obstacle, obstacle_rect)
    pygame.display.flip()

pygame.quit()
exit()