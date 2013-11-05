from enum import Enum

class Position(Enum):
    pitcher = 1
    catcher = 2
    first_baseman = 3
    second_baseman = 4
    third_baseman = 5
    shortstop = 6
    left_fielder = 7
    center_fielder = 8
    right_fielder = 9
    
class Play(Enum):
    single = 1
    double = 2
    triple = 3
    homerun = 4
    # sacrifice = 5
    walk = 6
    strikeout = 7
    strikeout_looking = 8
    # balk = 9
    fielders_choice = 10
    hit_by_pitcher = 11
    wild_pitch = 12
    # pass_ball = 13
    stolen_base = 14
    double_play = 15
    error = 16
    sacrifice_fly = 17
    # intentional_walk = 18
    # foul_fly = 19
    force_out = 20
    fly_out = 21
    bunt = 22
    