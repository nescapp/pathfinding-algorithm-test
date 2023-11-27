from pathfind import * # keep this line to import all the functions
import time
while get_x() != get_target_x() or get_y() != get_target_y():
    while not can_move() or is_in_front_of_enemy():
        if is_on_target:
            destroy_dark_force()
        time.sleep(1)
        turn_left()
        time.sleep(1)
        if can_move():
            move()
            time.sleep(1)
            turn_right()

    move()

    objective = get_direction()
    if get_x() < get_target_x():
        objective = EAST
    else:
        objective = WEST
    if get_y() < get_target_y():
        objective = SOUTH
    else:
        objective = NORTH

    while get_direction() != objective:
        turn_left()

destroy_dark_force()