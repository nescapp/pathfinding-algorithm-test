"""
make a game with pygame to practice pathfinding algorithms. the main window should be a grid on which i can place obstacles (houses),  ennemies (trolls), one instance of the player and one instance of the target. The default functions should be get_direction() that returns a string "NORTH", "EAST", "WEST" and "SOUTH" to get the direction of the player, can_move() that returns false if there is an obstacle in front of the player in the direction he is facing, move() to move the player one cell in the direction he is facing , turn_left() and turn_right() to turn the player, is_on_target() that returns true if the player is on the target, and is_in_front_of_enemy() that returns true if there is an enemy in front of the player in the direction he is facing. The game uses a system of coordinates for each cell of the grid, the horizontal axis is the x axis which increases from left to right, the vertical axis is the y axis which increases from top to bottom. the furthest top left grid cell has the coordinates (0;0). There is a function get_x that returns the x coordinate of the player, get_y that returns the y coordinate of the player, get_target_x that returns the x coordinate of the target and get_target_y that returns the y coordinate of the target .combine everything in one file. indicate with a comment where my path finding algorithm should go, my algorithm should only execute once when I press space on my keyboard. There is a trail behind the player that shows me where the player has been and an source that shows me the direction of the player in the player cell. Please tell me if something is unclear or doesn't make sense
"""

import sys
import json
import pygame
import importlib

# Constants
GRID_SIZE = 60  
GRID_WIDTH = 16
GRID_HEIGHT = 12
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACK_TEXTURE = pygame.image.load("assets/back.png")
BACK_TEXTURE = pygame.transform.scale(BACK_TEXTURE, (GRID_SIZE, GRID_SIZE))
TARGET_TEXTURE = pygame.image.load("assets/target.png")
TARGET_TEXTURE = pygame.transform.scale(TARGET_TEXTURE, (GRID_SIZE, GRID_SIZE))
OBSTACLE_TEXTURE = pygame.image.load("assets/wall.png")
OBSTACLE_TEXTURE = pygame.transform.scale(OBSTACLE_TEXTURE, (GRID_SIZE, GRID_SIZE))
ENEMY_TEXTURE = pygame.image.load("assets/enemy.png")
ENEMY_TEXTURE = pygame.transform.scale(ENEMY_TEXTURE, (GRID_SIZE, GRID_SIZE))

NORTH = "NORTH"
EAST = "EAST"
SOUTH = "SOUTH"
WEST = "WEST"

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Player and target coordinates
player_x, player_y = 4, 7
target_x, target_y = 9, 3
player_direction = "SOUTH"  # Initial player direction

try:
    with open("map.json", "r") as f:
        map = json.load(f)
        obstacles = map["obstacles"]
        obstacles = [(int(x), int(y)) for x, y in obstacles]
        enemies = map["enemies"]
        enemies = [(int(x), int(y)) for x, y in enemies]
        player_x, player_y = map["player"]
        target_x, target_y = map["target"]
        player_direction = map["player_direction"]
        source = pygame.image.load("assets/source.png")
        source = pygame.transform.scale(source, (GRID_SIZE, GRID_SIZE))
        source = pygame.transform.rotate(source, 90)
        if player_direction == "NORTH":
            source = pygame.transform.rotate(source, 0)
        elif player_direction == "EAST":
            source = pygame.transform.rotate(source, 270)
        elif player_direction == "WEST":
            source = pygame.transform.rotate(source, 90)
        elif player_direction == "SOUTH":
            source = pygame.transform.rotate(source, 180)

except FileNotFoundError:
    # create the map.json file
    map = {"obstacles": [], "enemies": [], "player": [player_x, player_y], "target": [target_x, target_y], "player_direction": player_direction}
    with open("map.json", "w") as f:
        json.dump(map, f)
    obstacles = []
    enemies = []
    source = pygame.image.load("assets/source.png")
    source = pygame.transform.scale(source, (GRID_SIZE, GRID_SIZE))




trail = [(player_x, player_y)]  


def refresh_screen():
    """Does shit"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            window.blit(BACK_TEXTURE, (x, y))

    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window, WHITE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, WHITE, (0, y), (WINDOW_WIDTH, y))

    for obstacle in obstacles:
        window.blit(OBSTACLE_TEXTURE, (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE))
    for enemy in enemies:
        window.blit(ENEMY_TEXTURE, (enemy[0] * GRID_SIZE, enemy[1] * GRID_SIZE))
        

    for pos in trail:
        pygame.draw.rect(window, BLACK, (pos[0] * GRID_SIZE + GRID_SIZE // 2 - 2, pos[1] * GRID_SIZE + GRID_SIZE // 2 - 2, 4, 4))

    # Update the trail
    trail.append((player_x, player_y))
    if len(trail) > 50:  # Adjust the number of trail segments as needed
        trail.pop(0)

    window.blit(TARGET_TEXTURE, (target_x * GRID_SIZE, target_y * GRID_SIZE))
    window.blit(source, (player_x * GRID_SIZE, player_y * GRID_SIZE))

    pygame.display.flip()
    clock.tick(8)

# Game functions
def get_direction():
    return player_direction

def can_move():
    """This function returns False if there is an obstacle in front of the player in the direction he is facing"""
    if player_direction == "NORTH":
        return player_y > 0 and (player_x, player_y - 1) not in obstacles
    elif player_direction == "EAST":
        return player_x < GRID_WIDTH - 1 and (player_x + 1, player_y) not in obstacles
    elif player_direction == "SOUTH":
        return player_y < GRID_HEIGHT - 1 and (player_x, player_y + 1) not in obstacles
    elif player_direction == "WEST":
        return player_x > 0 and (player_x - 1, player_y) not in obstacles
    

def move():
    """Funtion to move the player one cell in the direction he is facing and prevent him from going off the grid and through obstacles"""
    global player_x, player_y
    if player_direction == "NORTH":
        if player_y > 0 and (player_x, player_y - 1) not in obstacles and (player_x, player_y - 1) not in enemies:
            player_y -= 1
    elif player_direction == "EAST":
        if player_x < GRID_WIDTH - 1 and (player_x + 1, player_y) not in obstacles and (player_x + 1, player_y) not in enemies:
            player_x += 1
    elif player_direction == "SOUTH":
        if player_y < GRID_HEIGHT - 1 and (player_x, player_y + 1) not in obstacles and (player_x, player_y + 1) not in enemies:
            player_y += 1
    elif player_direction == "WEST":
        if player_x > 0 and (player_x - 1, player_y) not in obstacles and (player_x - 1, player_y) not in enemies:
            player_x -= 1

    refresh_screen()


def turn_left():
    global player_direction, source
    if player_direction == "NORTH":
        player_direction = "WEST"
        source = pygame.transform.rotate(source, 90)
    elif player_direction == "EAST":
        player_direction = "NORTH"
        source = pygame.transform.rotate(source, 90)
    elif player_direction == "SOUTH":
        player_direction = "EAST"
        source = pygame.transform.rotate(source, 90)
    elif player_direction == "WEST":
        player_direction = "SOUTH"
        source = pygame.transform.rotate(source, 90)

    refresh_screen()

def turn_right():
    global player_direction, source
    if player_direction == "NORTH":
        player_direction = "EAST"
        source = pygame.transform.rotate(source, -90)
    elif player_direction == "EAST":
        player_direction = "SOUTH"
        source = pygame.transform.rotate(source, -90)
    elif player_direction == "SOUTH":
        player_direction = "WEST"
        source = pygame.transform.rotate(source, -90)
    elif player_direction == "WEST":
        player_direction = "NORTH"
        source = pygame.transform.rotate(source, -90)
    
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

def destroy_dark_force():
    global target_x, target_y
    if (player_x, player_y) == (target_x, target_y):
        print("\033[93mTarget destroyed\033[0m")

# Main game loop
running = True
while running:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                import your_code_here
                importlib.reload(your_code_here)
                

            if event.key == pygame.K_o:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (player_x, player_y) and (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (target_x, target_y):
                    if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) not in obstacles:
                        obstacles.append((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                        map["obstacles"].append([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                        json.dump(map, open("map.json", "w"))
                        if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) in enemies:
                            enemies.remove((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                            map["enemies"].remove([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                            json.dump(map, open("map.json", "w"))
                    else:
                        obstacles.remove((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                        map["obstacles"].remove([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                        json.dump(map, open("map.json", "w"))
            if event.key == pygame.K_e:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (player_x, player_y) and (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (target_x, target_y):
                    if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) not in enemies:
                        enemies.append((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                        map["enemies"].append([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                        json.dump(map, open("map.json", "w"))
                        if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) in obstacles:
                            obstacles.remove((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                            map["obstacles"].remove([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                            json.dump(map, open("map.json", "w"))
                    else:
                        enemies.remove((mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE))
                        map["enemies"].remove([mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE])
                        json.dump(map, open("map.json", "w"))
            if event.key == pygame.K_t:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (player_x, player_y) and (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (target_x, target_y):
                    target_x, target_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
                    map["target"] = [target_x, target_y]
                    json.dump(map, open("map.json", "w"))
            if event.key == pygame.K_p:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) not in obstacles and (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) not in enemies and not (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) == (target_x, target_y):
                    if (mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE) != (player_x, player_y):
                        player_x, player_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
                        map["player"] = [player_x, player_y]
                        json.dump(map, open("map.json", "w"))
                    else:
                        turn_left()
                        map["player_direction"] = get_direction()
                        json.dump(map, open("map.json", "w"))
            if event.key == pygame.K_x:
                # export the map as a table
                print("[")
                for y in range(GRID_HEIGHT):
                    print("[", end="")
                    for x in range(GRID_WIDTH):
                        if (x, y) in obstacles:
                            print("0", end="")
                        elif (x, y) in enemies:
                            print("4", end="")
                        elif (x, y) == (player_x, player_y):
                            print("2", end="")
                        elif (x, y) == (target_x, target_y):
                            print("3", end="")
                        else:
                            print("1", end="")
                        if x != GRID_WIDTH - 1:
                            print(",", end="")
                    print("]", end="")
                    if y != GRID_HEIGHT - 1:
                        print(",")

                print("\n]")
            if event.key == pygame.K_r:
                # reset the map
                player_x, player_y = map["player"]
                player_direction = map["player_direction"]
                source = pygame.image.load("assets/source.png")
                source = pygame.transform.scale(source, (GRID_SIZE, GRID_SIZE))
                if player_direction == "NORTH":
                    source = pygame.transform.rotate(source, 0)
                elif player_direction == "EAST":
                    source = pygame.transform.rotate(source, 270)
                elif player_direction == "WEST":
                    source = pygame.transform.rotate(source, 90)
                elif player_direction == "SOUTH":
                    source = pygame.transform.rotate(source, 180)

        refresh_screen()
    refresh_screen()
pygame.quit()
sys.exit()
