"""
make a game with pygame to practice pathfinding algorithms. the main window should be a grid on which i can place obstacles (houses),  ennemies (trolls), one instance of the player and one instance of the target. The default functions should be get_direction() that returns a string "NORTH", "EAST", "WEST" and "SOUTH" to get the direction of the player, can_move() that returns false if there is an obstacle in front of the player in the direction he is facing, move() to move the player one cell in the direction he is facing , turn_left() and turn_right() to turn the player, is_on_target() that returns true if the player is on the target, and is_in_front_of_enemy() that returns true if there is an enemy in front of the player in the direction he is facing. The game uses a system of coordinates for each cell of the grid, the horizontal axis is the x axis which increases from left to right, the vertical axis is the y axis which increases from top to bottom. the furthest top left grid cell has the coordinates (0;0). There is a function get_x that returns the x coordinate of the player, get_y that returns the y coordinate of the player, get_target_x that returns the x coordinate of the target and get_target_y that returns the y coordinate of the target .combine everything in one file. indicate with a comment where my path finding algorithm should go, my algorithm should only execute once when I press space on my keyboard. There is a trail behind the player that shows me where the player has been and an arrow that shows me the direction of the player in the player cell. Please tell me if something is unclear or doesn't make sense
"""

import pygame
import sys
import time

# Constants
GRID_SIZE = 50
GRID_WIDTH = 16
GRID_HEIGHT = 12
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Player and target coordinates
player_x, player_y = 4, 7
target_x, target_y = 9, 3
player_direction = "SOUTH"  # Initial player direction

# create obstacles
obstacles = [(7,7), (8,7), (9,7), (10,7), (11,7), (9,2), (9,4), (9,5)]
obstacle_edit_mode = True

# create enemies
enemies = []

# Initialize game variables
trail = [(player_x, player_y)]  # Trail of player's movement
arrow = pygame.image.load("arrow.png")  # Replace with your arrow image
arrow = pygame.transform.scale(arrow, (GRID_SIZE, GRID_SIZE))
arrow = pygame.transform.rotate(arrow, 180)

def refresh_screen():
    # Draw trail and arrow
    for pos in trail:
        pygame.draw.rect(window, GREEN, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    window.blit(arrow, (player_x * GRID_SIZE, player_y * GRID_SIZE))
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(window, BLUE, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(window, RED, (enemy[0] * GRID_SIZE, enemy[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw target
    pygame.draw.rect(window, WHITE, (target_x * GRID_SIZE, target_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


    # Update the trail
    trail.append((player_x, player_y))
    if len(trail) > 5:  # Adjust the number of trail segments as needed
        trail.pop(0)

    draw_grid()
    pygame.display.flip()
    clock.tick(30)

# Game functions
def get_direction():
    return player_direction

def can_move():
    """This function returns False if there is an obstacle in front of the player in the direction he is facing"""
    if player_direction == "NORTH":
        return (player_x, player_y - 1) not in obstacles
    elif player_direction == "EAST":
        return (player_x + 1, player_y) not in obstacles
    elif player_direction == "SOUTH":
        return (player_x, player_y + 1) not in obstacles
    elif player_direction == "WEST":
        return (player_x - 1, player_y) not in obstacles
    

def move():
    """Funtion to move the player one cell in the direction he is facing and prevent him from going off the grid and through obstacles"""
    global player_x, player_y, player_direction
    if player_direction == "NORTH":
        if player_y > 0 and (player_x, player_y - 1) not in obstacles:
            player_y -= 1
    elif player_direction == "EAST":
        if player_x < GRID_WIDTH - 1 and (player_x + 1, player_y) not in obstacles:
            player_x += 1
    elif player_direction == "SOUTH":
        if player_y < GRID_HEIGHT - 1 and (player_x, player_y + 1) not in obstacles:
            player_y += 1
    elif player_direction == "WEST":
        if player_x > 0 and (player_x - 1, player_y) not in obstacles:
            player_x -= 1    

    refresh_screen()



def turn_left():
    global player_direction, arrow
    if player_direction == "NORTH":
        player_direction = "WEST"
        arrow = pygame.transform.rotate(arrow, 90)
    elif player_direction == "EAST":
        player_direction = "NORTH"
        arrow = pygame.transform.rotate(arrow, 90)
    elif player_direction == "SOUTH":
        player_direction = "EAST"
        arrow = pygame.transform.rotate(arrow, 90)
    elif player_direction == "WEST":
        player_direction = "SOUTH"
        arrow = pygame.transform.rotate(arrow, 90)

    refresh_screen()

def turn_right():
    global player_direction, arrow
    if player_direction == "NORTH":
        player_direction = "EAST"
        arrow = pygame.transform.rotate(arrow, -90)
    elif player_direction == "EAST":
        player_direction = "SOUTH"
        arrow = pygame.transform.rotate(arrow, -90)
    elif player_direction == "SOUTH":
        player_direction = "WEST"
        arrow = pygame.transform.rotate(arrow, -90)
    elif player_direction == "WEST":
        player_direction = "NORTH"
        arrow = pygame.transform.rotate(arrow, -90)
    
    refresh_screen()

def is_on_target():
    return (player_x, player_y) == (target_x, target_y)

def is_in_front_of_enemy():
    """This function returns True if there is an enemy in front of the player in the direction he is facing"""
    if player_direction == "NORTH":
        return (player_x, player_y - 1) in enemies
    elif player_direction == "EAST":
        return (player_x + 1, player_y) in enemies
    elif player_direction == "SOUTH":
        return (player_x, player_y + 1) in enemies
    elif player_direction == "WEST":
        return (player_x - 1, player_y) in enemies

def get_x():
    return player_x

def get_y():
    return player_y

def get_target_x():
    return target_x

def get_target_y():
    return target_y

def destroy_target():
    global target_x, target_y
    target_x, target_y = -1, -1


# Function to draw the grid
def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, WHITE, (0, y), (WINDOW_WIDTH, y))

# Main game loop
running = True
while running:
    window.fill((0, 0, 0))

    # add obstacles on clicked cells
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if (mouse_x // GRID_SIZE, mouse_y // GRID_SIZE) not in obstacles:
            obstacles.append((mouse_x // GRID_SIZE, mouse_y // GRID_SIZE))
        else:
            obstacles.remove((mouse_x // GRID_SIZE, mouse_y // GRID_SIZE))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Implement your pathfinding algorithm here
                # Update the player's movement based on the pathfinding result
                # You can use functions like get_direction(), can_move(), move(), etc.

                pass

    # Draw the grid
    refresh_screen()
    

pygame.quit()
sys.exit()
