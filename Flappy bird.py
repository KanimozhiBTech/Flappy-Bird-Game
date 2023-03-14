import pygame
import sys
import random
#Game variables
floor_x_position=0
bg_x_position=0       
gravity=0.20
bird_y_movement=0
#All Functions
def draw_bg():
    screen.blit(bg_surface,(bg_x_position,0))
    screen.blit(bg_surface,(bg_x_position+288,0))
def floor_getting():
    screen.blit(floor_surface,(floor_x_position,450))
    screen.blit(floor_surface,(floor_x_position+288,450))
def create_pipe():
    random_height=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(400,random_height))     
    top_pipe=pipe_surface.get_rect(midbottom=(400,random_height-150))
    return bottom_pipe,top_pipe
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx-=2
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top<=-100 or bird_rect.bottom>=450:
        return False
    return True

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_y_movement*3,1)
    return new_bird
def bird_animation():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(78,bird_rect.centery))
    return new_bird, new_bird_rect

    



pygame.init()
screen=pygame.display.set_mode((288,512))
clock=pygame.time.Clock()


game_active=True

bg_surface=pygame.image.load('assets/background-day.png')
floor_surface=pygame.image.load('assets/base.png').convert()
#bird_surface=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_rect=bird_surface.get_rect(center=(78,256))
bird_downflap=pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap=pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]  

bird_rect=bird_surface.get_rect(center=(78,256))

BIRDFLAP=pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)


pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_list=[]
SPWANPIPE=pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE,1200)

pipe_height=[195,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400,410]


while True:                                                                        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
           pygame.quit()
           sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_y_movement=0 
                bird_y_movement-=7
            if event.key==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(78,256)
                bird_y_movement=0
            

        if event.type==SPWANPIPE:
            pipe_list.extend(create_pipe())
        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1   
            else:
                bird_index=0
            
        bird_surface,bird_rect=bird_animation() 
            
       

    
    floor_x_position-=1
    bg_x_position-=1
    floor_getting()


    draw_bg()
    if game_active:
        pipe_list=move_pipes(pipe_list)
        draw_pipe(pipe_list)
 

        bird_y_movement+=gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery+=bird_y_movement
        screen.blit(rotated_bird,bird_rect)

        game_active=check_collision(pipe_list)
        
    

    floor_getting()
    if floor_x_position<=-288 and bg_x_position<=-288:
        floor_x_position=0
        bg_x_position=0

        
    

    pygame.display.update()
    clock.tick(120)
