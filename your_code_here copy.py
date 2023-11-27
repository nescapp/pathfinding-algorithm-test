from pathfind import * # keep this line to import all the functions

def get_direction_on_x(coor_on_x) :
    """return the direction to move on x axis"""
    if coor_on_x > 0 :
        return EAST
    else :
        return WEST

def get_direction_on_y(coor_on_y) :
    """return the direction to move on y axis"""
    if coor_on_y > 0 :
        return SOUTH
    else :
        return NORTH

def may_I_move() :
    return can_move() and not is_in_front_of_enemy()

def turn_left_until_can_move() :
    print("turning left until can move")
    while not may_I_move() :
        turn_left()
    move()


while not is_on_target() :
    print("starting over")
    coor_on_x = get_target_x() - get_x()

    while get_direction() != get_direction_on_x(coor_on_x) and not may_I_move():
        # turn left until the direction is correct
        turn_left()

    steps = 0
    totalSteps = abs(coor_on_x)

    while may_I_move() and steps < totalSteps :
        print("I can move, moving forward")
        move()
        steps = steps + 1

    if steps == totalSteps :
        # if the player has moved the correct number of steps
        coor_on_y = get_target_y() - get_y()

        while get_direction() != get_direction_on_y(coor_on_y) :
            turn_left()

        steps = 0
        totalSteps = abs(coor_on_y)
        while may_I_move() and steps < totalSteps :

            move()
            steps = steps + 1
        if steps != totalSteps :
            turn_left_until_can_move()
    else :
        turn_left_until_can_move()

destroy_dark_force()
