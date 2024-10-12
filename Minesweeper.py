###Minesweeper - A game of mine sweeper
import pygame; import random
#from pygame.locals import *
pygame.init()

### --- field_generator --- Generates arrays storing data about the game tiles. B/C/F/ ==Bomb/Clear/Flag/Unassigned
def field_generator():
    ##Creates arrays
    mine_placement = [["" for y in range(9)]for x in range(9)]#Stores tile type
    display_field = [["" for y in range(9)]for x in range(9)]#Stores tiles shown
    grid_cords_x = [[0 for z in range(2)] for x in range(9)]#Range of tile pos in x-axis
    grid_cords_y = [[0 for z in range(2)] for y in range(9)]#Range of tile pos in y-axis
    ##Asigns arrays
    for x in range(15):#Places bombs in random parts of the mine_placement list, B == Bomb
        stop = False
        while not stop:
            tempx = random.randint(0, 8); tempy = random.randint(0, 8)
            if mine_placement[tempx][tempy] == "":#Prevetns C from overwriting B placement
                mine_placement[tempx][tempy]="B"
                stop = True
    for y in range(10):#Places safe grids, C == Clear
        stop = False
        while not stop:
            tempx = random.randint(0, 8); tempy = random.randint(0, 8)
            if mine_placement[tempx][tempy] == "":#Prevetns C from overwriting B placement
                mine_placement[tempx][tempy]="C"
                display_field[tempx][tempy]="C"
                stop = True
    #Assigns range of each tile of the grid, forgot how it works
    pos1 = [x for x in range(42, 388, 41)]#Creates first value of range
    pos2 = [y for y in range(73, 463, 41)]#Creates second value of range
    for val1 in range(9):
        grid_cords_x[val1][0] = pos1[val1]
        grid_cords_y[val1][0] = pos1[val1]
    for val2 in range(9):
        grid_cords_x[val2][1] = pos2[val2]
        grid_cords_y[val2][1] = pos2[val2]    
    #Returns the arrays to be accessed by the rest of the program
    return(mine_placement, display_field, grid_cords_x, grid_cords_y)

### --- font_creation --- Creates a font and outputs it onto the screen
class font_creation:#Only negative is the font is drawn, it cannot be removed
    #Creates the font and its surface
    def __init__ (self, font_values, rect_values):
    #Creates the font
        font = pygame.font.Font(font_values[4], font_values[1])
        text = font.render(font_values[0], True, font_values[2], font_values[3])
    #Creates the font surface(rectangle)
        text_rect = text.get_rect()
        text_rect.center = (rect_values[0], rect_values[1])
    #Outputs the font onto a rectangle
        screen.blit(text, text_rect)
        pygame.display.flip()
        
### --- place_flag --- Places a flag image if the mouse_pos is in place and it is empty
def place_flag(mouse_position):
    x_index = -1 ; y_index = -1
    for x in range(9):#Checks for mouse in x-axis
        if (grid_cords_x[x][0] <= mouse_position[0]) and (mouse_position[0] <= grid_cords_x[x][1]):
            x_index=x
            break
    for y in range(9):#Checks for mouse in y-axis
        if (grid_cords_y[y][0] <= mouse_position[1]) and (mouse_position[1] <= grid_cords_y[y][1]):
            y_index=y
            break
    if (x_index > -1) and (y_index > -1):#Checks whether mouse pos was found
        if display_field[x_index][y_index] == "":#Checks if tile is empty
            screen.blit(flag_tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))#Blits flag
            pygame.display.flip()
            display_field[x_index][y_index] = "F"
        
### --- dig_ground --- Digs if mouse pos in grid and there is no image in grid, then performs a check for bomb
def dig_ground(mouse_position, mine_placement):
    x_index = -1 ; y_index = -1
    for x in range(9):#Checks for mouse in x-axis
        if (grid_cords_x[x][0] <= mouse_position[0]) and (mouse_position[0] <= grid_cords_x[x][1]):
            x_index=x
            break
    for y in range(9):#Checks for mouse in y-axis
        if (grid_cords_y[y][0] <= mouse_position[1]) and (mouse_position[1] <= grid_cords_y[y][1]):
            y_index=y
            break
    if (x_index > -1) and (y_index > -1):
        if (mine_placement[x_index][y_index] == ""):#Checks tile is digable
            if display_field[x_index][y_index] == "":#Checks nothing is displayed on that tile
                display_field[x_index][y_index] = "D"
                screen.blit(dug_tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
                pygame.display.flip()
                num_display(mine_placement, x_index, y_index)
        elif mine_placement[x_index][y_index] == "B":#Checks for bomb to end the game
            if display_field[x_index][y_index] == "":#Checks nothing is displayed on that tile
                display_field[x_index][y_index] = "D"#This line was missing and costed me 3 hours
                screen.blit(bomb_tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
                pygame.display.flip()
                pygame.time.wait(1000)
                game_over(False)#Ends the game
        
### --- remove_flag --- Removes a flag image if the mouse_pos is in place and there is a flag
def remove_flag(mouse_position, grid_cords_x, grid_cords_y, display_field):
    x_index = -1 ; y_index = -1#Default value for checking
    for x in range(9):#Checks for mouse in x-axis
        if grid_cords_x[x][0] <= mouse_position[0] <= grid_cords_x[x][1]:
            x_index=x
            break
    for y in range(9):#Checks for mouse in y-axis
        if grid_cords_y[y][0] <= mouse_position[1] <= grid_cords_y[y][1]:
            y_index=y
            break
    if (x_index > -1) and (y_index > -1):#Checks whether mouse pos was found
        if display_field[x_index][y_index] == "F":#Checks if tile is a flag
            temp = [grid_cords_x[x_index][0], grid_cords_y[y_index][0], 32, 32]#Green rect data
            pygame.draw.rect(screen, green, (pygame.Rect(temp)))#Blits rect over flag
            pygame.display.flip()
            display_field[x_index][y_index] = ""

### --- num_display ---Checks surrounding tiles for the total bombs
def num_display(mine_placement, x_index, y_index):
    search_areas = []
    total = 0
    for x in range((x_index - 1), (x_index + 2)):#Goes from left to right
        for y in range((y_index - 1), (y_index + 2)):#Goes from top to bottom
            search_areas.append([x, y])#Adds list of cords to check
    for coords in search_areas:
        try:#Uses try, except catch as some coords are outside of index
            if mine_placement[coords[0]][coords[1]] == "B":
                total += 1#Blame pygame if this displays more bombs then there are, nvm fixed
        except:
            print("Exception from num_display")#You need to put code here...
    if total == 0:#Wishing for switch statements
        screen.blit(num_0tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 1: 
          screen.blit(num_1tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 2: 
          screen.blit(num_2tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 3: 
          screen.blit(num_3tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 4: 
          screen.blit(num_4tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 5: 
          screen.blit(num_5tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 6: 
          screen.blit(num_6tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 7: 
          screen.blit(num_7tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    elif total == 8: 
          screen.blit(num_8tile, (grid_cords_x[x_index][0], grid_cords_y[y_index][0]))
    pygame.display.flip()
	    
### --- end_checker --- Checks whether all tiles the player has placed are in the correct place
def end_checker(display_field, mine_placement, game_over):
    total_digs_in_correct_place = 0
    total_flags_in_correct_place = 0
    for x in range(0, 9):
        for y in range(0, 9):
            if (mine_placement[x][y] == "") and (display_field[x][y] == "D"):
                total_digs_in_correct_place += 1
            elif (mine_placement[x][y] == "B") and (display_field[x][y] == "F"):
                total_flags_in_correct_place += 1
    if (total_digs_in_correct_place == 56) and (total_flags_in_correct_place == 15):
    #Bug here cause due to lack of line 92, causing te game to not end
        game_over(True)

### --- game_over --- Procedure which ends the game, output depends on parameter given
def game_over(over_type):
    pygame.event.clear()
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.MOUSEWHEEL)
    screen.fill(black)#This prevents gaps the end image doesn't cover
    if over_type == True:#Win
        screen.blit(win_screen, (25, 25))#Blits image
        font_creation(winning_font, (221, 221))#Shows message
    elif over_type == False:#Lose
        screen.blit(lose_screen, (25, 25))#Blits image
        font_creation(losing_font, (221, 221))#Shows message
    pygame.time.wait(2500)#Pauses
    for x in range(5, 0, -1):#Count down to close the program
        count_down_font = [f" Closing in : {x} ", 32, black, yellow, font]
        font_creation(count_down_font, (221, 36))
        pygame.time.wait(1000)
    pygame.quit()
    print("┌ -+-+-+-+-+- ┐\n  Game closed  \n└ -+-+-+-+-+- ┘")
    quit()

### --- Main Program --- Pygame based minesweeper
## -- Colour -- Initialises colour constants (R, G, B, a)
black = pygame.Color(0, 0, 0)
green = pygame.Color(34, 177, 76)#Chose this colour as it matches the one from the pixelart
blue = pygame.Color(59, 70, 191)
yellow = pygame.Color(224, 210, 9)
## -- Font values -- Creates font values used throughout the game
font = "Assets\Dhurjati-Regular.ttf"
losing_font = [" Game over --- Better luck next time!", 26, black, blue, font]#Pygame only renders text on a single line
winning_font = [" Game over --- Well done!", 26, black, blue, font]
## -- Images -- Loads images into the program
load_img = pygame.image.load
game_icon = load_img("Assets/icon_bomb.png")#Raw-string is required. Actually my pc was being stupid, ignore this#Never mind, depends on the system
flag_tile = load_img('Assets/tile_flag.png'); bomb_tile = load_img("Assets/tile_bomb.png")
dug_tile = load_img("Assets/tile_dug.png"); clear_tile = load_img("Assets/tile_clear.png")
win_screen = load_img("Assets\screen_win.png"); lose_screen = load_img("Assets/screen_lose.png")
num_0tile = load_img("Assets/num0_tile.png"); num_1tile = load_img("Assets/num1_tile.png")
num_2tile = load_img("Assets/num2_tile.png"); num_3tile = load_img("Assets/num3_tile.png")
num_4tile = load_img("Assets/num4_tile.png"); num_5tile = load_img("Assets/num5_tile.png")
num_6tile = load_img("Assets/num6_tile.png"); num_7tile = load_img("Assets/num7_tile.png")
num_8tile = load_img("Assets/num8_tile.png")
## -- Field Generator -- OMG THIS IS SO PAINFUL, this font looks cute tho
mine_placement, display_field, grid_cords_x, grid_cords_y = field_generator()
## -- Display section -- Initializes the display
pygame.display.set_caption("Mine Sweeper - PYGame version")
pygame.display.set_icon(game_icon)
screen = pygame.display.set_mode([442, 442])#I think I need graphing paper
#Initialises objects onto the surface
screen.fill(green)#Sets the scenery of a field ヽ(*⌒▽⌒*)ﾉ
for cord in range(37, 410, 41):#I don't get how the draw line works, does it draw px away from line or px total thickness
    pygame.draw.line(screen, black, (cord, 37), (cord, 405), 9)#Vertical lines
    pygame.draw.line(screen, black, (37, cord), (405, cord), 9)#Horizontal lines
pygame.draw.rect(screen, black, (pygame.Rect(32, 32, 378, 378)), 8, border_radius = 5)#Covers the corners I couldn't be bothered to fill
for x in range(9):#Searches through the display to blit any clear tiles
    for y in range(9):
        if mine_placement[x][y] == "C":
            screen.blit(clear_tile, (grid_cords_x[x][0], grid_cords_y[y][0]))
stop = False
while not stop:#Generates a number for the user to start
    tempx = random.randint(0, 8); tempy = random.randint(0, 8)
    if (display_field[tempx][tempy] == "") and (mine_placement[tempx][tempy] == ""):
        num_display(mine_placement, tempx, tempy)
        stop = True
pygame.display.flip()#(ᗒᗣᗕ)՞ WHY IS THE DRAWING SO HARD, THEY DON'T GO WHERE I WANT IT TO
## -- Extra -- Other actions before main game
clock = pygame.time.Clock()#Why is this so complicated "( – ⌓ – )
other_font = 'freesansbold.ttf'
### --- Main --- Game loop
while True:
    button_pressed = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("┌ -+-+-+-+-+- ┐\n  Game closed  \n└ -+-+-+-+-+- ┘")
            quit()
    if button_pressed[0] == True:#Place flag
        place_flag(mouse_position)
        end_checker(display_field, mine_placement, game_over)
        
        print(mine_placement, "/n", display_field)#For debugging/testing
        
    elif button_pressed[1] == True:#Dig ground
        dig_ground(mouse_position, mine_placement)
        end_checker(display_field, mine_placement, game_over)
        
        print(mine_placement, "/n", display_field)#For debugging/testing
        
    elif button_pressed[2] == True:#Remove flag
        remove_flag(mouse_position, grid_cords_x, grid_cords_y, display_field)
        
        print(mine_placement, "/n", display_field)#For debugging/testing
        
    clock.tick(50)

(((((((((((((((((())))))))))))))))))