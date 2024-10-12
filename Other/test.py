import pygame
from pygame.locals import *

pygame.display.set_caption("Mine Sweeper - PYGame version")
screen = pygame.display.set_mode([442, 442])#I think I need graphing paper
#Initialises objects onto the surface
screen.fill((0, 255, 0))#Sets the scenery of a field ヽ(*⌒▽⌒*)ﾉ
#for cord in range(37, 410, 37):
    #pygame.draw.line(screen, black, (cord, 37), (cord, 400), 9)
    #pygame.draw.line(screen, black, (37, cord), (400, cord), 9)
#pygame.draw.rect(screen, black, (pygame.Rect(29, 29, 332, 332)), 8)#Covers the corners I couldn't be bothered to fill
pygame.draw.line(screen, (0, 0, 0), (37, 0), (400, 0), 9)
pygame.display.flip()#(ᗒᗣᗕ)՞ WHY IS THE DRAWING SO HARD, THEY DON'T GO WHERE I WANT IT TO
#for x in range(9):
    #for y in range(9):
       # screen.blit(bomb_tile, (grid_cords_x[x][0], grid_cords_y[y][0]))
        #pygame.display.flip()

#32px, 9x(9px, 32px), 9px, 32px, 41, 410, 41
## -- Extra -- Other actions before main game
clock = pygame.time.Clock()#Why is this so complicated "( – ⌓ – )
other_font = 'freesansbold.ttf'
score = [15, 85]#[Total Flags To Be Placed, Total Tiles To Dig]
### --- Main --- Game loop
while True:
    button_pressed = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("┌ -+-+-+-+-+- ┐\n  Game closed  \n└ -+-+-+-+-+- ┘")
            quit()
        elif button_pressed[0] == True:#Place flag
            #place_flag(mouse_position)
            score[0] -= 1
            print("Left clicked")
        elif button_pressed[1] == True:#Dig ground
            #dig_ground(mouse_position)#Removes bomb, Handles lose/continue[handles score, if score[0]==0 [win proced, else outputs num tiles] --- lose proced]
            print("Mouse wheel clicked")
        elif button_pressed[2] == True:#Remove flag
            #remove_flag(mouse_position)
            score[0] += 1
            print("Right clicked")
    clock.tick(10)
    
#I hate drawing