from pathfind import * # keep this line to import all the functions from pathfind.py

while not is_on_target():
    # turn east if the target is east of the player
    if get_target_x() > get_x():
        while get_direction() != "EAST":
            turn_right()

        while get_x() < get_target_x():
            if can_move() and not is_in_front_of_enemy():
                move()
            else :
                while not can_move() or is_in_front_of_enemy():
                    while not can_move() or is_in_front_of_enemy():
                        turn_right()
                    move()
                    turn_left()
                if get_direction() != "EAST":
                    move()
                    turn_left()

        # turn north if the target is north of the player
        if get_target_y() < get_y():
            while get_direction() != "NORTH":
                turn_left()

            while get_y() > get_target_y():
                if can_move() and not is_in_front_of_enemy():
                    move()
                else :
                    while not can_move() or is_in_front_of_enemy():
                        while not can_move() or is_in_front_of_enemy():
                            turn_right()
                        move()
                        turn_left()
                    if get_direction() != "NORTH":
                        move()
                        turn_left()
        else:
            while get_direction() != "SOUTH":
                turn_right()

            while get_y() < get_target_y():
                if can_move() and not is_in_front_of_enemy():
                    move()
                else :
                    while not can_move() or is_in_front_of_enemy():
                        while not can_move():
                            turn_right()
                        move()
                        turn_left()
                    if get_direction() != "SOUTH":
                        move()
                        turn_left()

    # turn west if the target is west of the player
    else:
        while get_direction() != "WEST":
            turn_right()

        while get_x() > get_target_x():
            if can_move() and not is_in_front_of_enemy():
                move()
            else :
                while not can_move() or is_in_front_of_enemy():
                    while not can_move() or is_in_front_of_enemy():
                        turn_right()
                    move()
                    turn_left()
                if get_direction() != "WEST":
                    move()
                    turn_left()

        # turn north if the target is north of the player
        if get_target_y() < get_y():
            while get_direction() != "NORTH":
                turn_left()

            while get_y() > get_target_y():
                if can_move() and not is_in_front_of_enemy():
                    move()
                else :
                    while not can_move() or is_in_front_of_enemy():
                        while not can_move() or is_in_front_of_enemy():
                            turn_right()
                        move()
                        turn_left()
                    if get_direction() != "NORTH":
                        move()
                        turn_left()
        else:
            while get_direction() != "SOUTH":
                turn_right()

            while get_y() < get_target_y():
                if can_move() and not is_in_front_of_enemy():
                    move()
                else :
                    while not can_move() or is_in_front_of_enemy():
                        while not can_move():
                            turn_right()
                        move()
                        turn_left()
                    if get_direction() != "SOUTH":
                        move()
                        turn_left()




destroy_dark_force()