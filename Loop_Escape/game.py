import pygame
import sys
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)- start_time
    score_surface = test_font.render(f'{current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (780,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(dragon_surf,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return[]
    
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    

pygame.init() 
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Loop Escape')
clock = pygame.time.Clock()

test_font = pygame.font.Font(None,50)

game_active = True
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/game_music.mp3')
bg_music.play(loops = -1)

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render('ESCAPE',False,'Purple')
text_rect = text_surface.get_rect(topright = (470,25))

scoree_surface = test_font.render('score = ',False,'Red')
scoree_rect = scoree_surface.get_rect(center = (680,50))

#snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frame[snail_frame_index]

dragon_frame_1 = pygame.image.load('graphics/dragon/dragon1.png').convert_alpha()
dragon_frame_2 = pygame.image.load('graphics/dragon/dragon2.png').convert_alpha()
dragon_frame = [dragon_frame_1,dragon_frame_2]
dragon_frame_index = 0
dragon_surf = dragon_frame[dragon_frame_index]

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load('graphics/character/boy_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/character/boy_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/character/boy_jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(topleft = (80,230))
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)



player_gravity = -20

player_dead = pygame.image.load('graphics/character/Dead.png').convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead,0,2)
player_dead_rect = player_dead.get_rect(center = (400,200))

game_name = test_font.render('LOOP ESCAPE FAILED!!',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press Space To Run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,200)

dragon_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(dragon_animation_timer,200)

#main game                           
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()
                    
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer :
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(dragon_surf.get_rect(bottomright = (randint(900,1100),210)))
                    
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0   
                snail_surf = snail_frame[snail_frame_index]
                
            if event.type == dragon_animation_timer:
                if dragon_frame_index == 0:
                    dragon_frame_index = 1
                else:
                    dragon_frame_index = 0
                dragon_surf = dragon_frame[dragon_frame_index]
                
                
    if game_active :
         
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        pygame.draw.rect(screen,'#c0e8ec',text_rect)
        screen.blit(text_surface,(325,25))
        screen.blit(scoree_surface,scoree_rect)
        score = display_score()
        
        #snail    
        #snail_rect.x -= 4
        #if snail_rect.right < -10: snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)

        #gravity
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        
        #player
        player_animation()
        screen.blit(player_surf,player_rect)
        
        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
    
        #coll
        game_active = collisions(player_rect,obstacle_rect_list)
        
            
    else:
        screen.fill('Purple')
        screen.blit(player_dead,player_dead_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        score_message = test_font.render(f'Your Score : {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
            
 
    
    pygame.display.update()
    clock.tick(80)
    