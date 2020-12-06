#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import os
import cursor
import random
import textwrap
import mmh3

import horta_trees

# ─────────────────────────────────────────────────╮
# Horta is a python program designed to generate   │
# pseudo random growing flower patterns in a       │
# terminal window.                                 │
#                                                  │
# It was made in 2020 by Lucas Bet as part of      │
# the CS50x Harvard Program.                       │
# ─────────────────────────────────────────────────╯

class Format:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'	
    END = '\033[0m'

class Tracker:
    current_x = None
    current_y = None
    present = None
    future = None

class Order:
    chance_exp = [None for n in range(100)]
    chance_col = [0, 0, 0]  # -1, 0, 1
    steps = None
    turn = None

# receive arguments / usage check

if len(sys.argv) < 2:
    print("")
    print("Mind your words! Run:")
    print(Format.BOLD + "python ./flowers.py seed size" + Format.END)
    print("A seed is any word. This will determine behavior.")
    print("Sizes are small (default), medium, large or auto.")
    print("")
    sys.exit(1)
elif len(sys.argv) > 2:
    size = sys.argv[2]
    seed = sys.argv[1]
else:
    seed = sys.argv[1]
    size = "small"

MAX_NUMBER_OF_ORDERS = 1000

if size == "large":
    ysize, xsize = 50, 120
    MAX_NUMBER_OF_ORDERS = 1200
elif size == "medium":
    ysize, xsize = 35, 110
    MAX_NUMBER_OF_ORDERS = 1100
elif size == "auto":
    console = os.get_terminal_size()
    ysize, xsize = console[1]-10, console[0]-10
    MAX_NUMBER_OF_ORDERS = 1500
else:
    ysize, xsize = 24, 50

# score, log and exit

class ScoreLog:
    points = 0
    discoveries = []
    
    @classmethod
    def new_discovery(cls, id):
        if id not in cls.discoveries:
            cls.discoveries.append(id)
    
    @classmethod
    def more_points(cls, value):
        cls.points += value

    @classmethod
    def print_log(cls):
        cls.names = [
            'Little Grass',
            'Park Trees',
            'Pine Trees',
            'Willow Trees',
            'Coconut Palms',
            'Small Mushrooms',
            Format.BOLD + 'Bamboos' + Format.END,
            Format.BOLD + 'Cactuses' + Format.END,
            Format.BOLD + 'Apple Trees' + Format.END,
            Format.BOLD + 'Wild Flowers' + Format.END,
            Format.BOLD + 'the Silversword' + Format.END,
            Format.BOLD + 'the Dragon Blood Tree' + Format.END,
            Format.BOLD + Format.PURPLE + 'the Baobab' + Format.END,
            Format.BOLD + Format.PURPLE + 'the CS50 Christmas Tree!' + Format.END,
            Format.BOLD + Format.PURPLE + 'the Binary Tree' + Format.END,
            Format.BOLD + Format.PURPLE + 'the ???' + Format.END,
            Format.BOLD + Format.PURPLE + 'the Amanita Muscaria' + Format.END,
            Format.BOLD + Format.PURPLE + 'the Ancient Fruit' + Format.END]
        
        cls.points = str(cls.points)
        print()
        print(Format.GREEN + "╭────────────────────────────────────────╼" + Format.END)


        log_string = f"Your seed >> " + Format.BLUE + f"{sys.argv[1]}" + Format.END + " scored a grand total of "+ Format.BOLD + Format.RED + f"{cls.points}" + Format.END + " points, and discovered "
        before_each_line = Format.GREEN + "│ " + Format.END

        discoveries_string = ''

        for i in range(len(cls.discoveries)):
            if i == 0:
                discoveries_string = '' + cls.names[cls.discoveries[i]]
            if i == 1:
                discoveries_string = discoveries_string + ', ' + cls.names[cls.discoveries[i]]
            if i == 2: 
                discoveries_string = discoveries_string + ' and ' + cls.names[cls.discoveries[i]]
        
        
        log_string = log_string + discoveries_string
        
        log_string = textwrap.indent(textwrap.fill(log_string, 52), before_each_line)

        print(log_string)

        print(Format.GREEN + "╰──────────╼ thanks for playing ╾────────╼" + Format.END)


        print()

import atexit
atexit.register(ScoreLog.print_log)
atexit.register(cursor.show)

# initialize seed

seed_numeric = mmh3.hash(seed)
random.seed(seed_numeric)

# initialize trees

tree_id_one  =  random.randint(0, 6)
tree_id_two  =  random.randint(3, 11)
tree_id_rare =  random.randint(12, 17)

tree_one  = horta_trees.ColorTree(str(tree_id_one),  random.randint(1,99))
tree_two  = horta_trees.ColorTree(str(tree_id_two),  random.randint(1,99))
tree_rare = horta_trees.ColorTree(str(tree_id_rare), random.randint(1,99))


# order initialization

Order.chance_col[0] = random.randint(0, 85)
Order.chance_col[2] = random.randint(0, 85)

while Order.chance_col[0] + Order.chance_col[2] > 100:
    Order.chance_col[0] -= 2
    Order.chance_col[2] -= 2
Order.chance_col[1] = 100 - (Order.chance_col[0] + Order.chance_col[2])

totalcount = 0
chance_pool = [-1, 0, 1]
while totalcount < 100:
    for n in range(3):
        for i in range(Order.chance_col[n]):
            Order.chance_exp[totalcount] = chance_pool[n]
            totalcount += 1


# tracker initialization

Tracker.present = seed_numeric % 4
Tracker.current_x = seed_numeric % xsize
Tracker.current_y = seed_numeric % ysize

# general globals

GLOBAL_GROWTH_RATE   = random.randint(50, 700)
GLOBAL_FADE_RATE     = random.randint(1, 10)
GLOBAL_GROWTH_CHANCE = random.randint(1, 4)
SEED_BIRTH_RATE      = random.randint(4, 15)

class Screen:
    background =  [" "]
    pixel =       [[" " for n in range(xsize)]   for n in range(ysize)]
    grown =       [[" " for n in range(xsize)]   for n in range(ysize)]
    frame_count = [[0 for n in range(xsize)]     for n in range(ysize)]
    is_tree =     [[False for n in range(xsize)] for n in range(ysize)]
    fade =        [[0 for n in range(xsize)]     for n in range(ysize)]

    @classmethod
    def update(cls):
        for y in range(ysize):
            for x in range(xsize):

                if cls.frame_count[y][x] > GLOBAL_GROWTH_RATE:
                    if  random.randint(0,100) < GLOBAL_GROWTH_CHANCE:
                        cls.pixel[y][x] = cls.grown[y][x]
                    
                if cls.fade[y][x] < 1 and not cls.is_tree[y][x]:
                    cls.pixel[y][x] = cls.background[0]
        
                if cls.is_tree[y][x]: cls.frame_count[y][x] += 1
                
                cls.fade[y][x] -= 1

caules_retos =  [
    Format.RED + "." + Format.END,
    Format.RED + ":" + Format.END, 
    Format.RED + "." + Format.END,
    Format.RED + ":" + Format.END]
x_operators =   [ 1,   0,  -1,   0 ]
y_operators =   [ 0,   1,   0,  -1 ]

class Lists:
    some_semiprimes = [57, 58, 62, 65, 69, 74, 77, 82, 85, 86, 87, 91,
                       93, 94, 95, 106, 111, 115, 118, 119, 121, 122, 123, 
                       129, 133, 134, 141, 142, 143, 145, 146, 155, 158, 
                       159, 161, 166, 169, 177, 178, 183, 185, 187, 194, 
                       201, 202, 203, 205, 206, 209, 213, 214, 215, 217, 
                       218, 219, 221, 226, 235, 237, 247, 249, 253, 254, 
                       259, 262, 265, 267, 274, 278, 287, 289, 291, 295, 
                       298, 299, 301, 302, 303, 305, 309, 314, 319, 321, 
                       323, 326, 327, 329, 334, 335, 339, 341, 346, 355, 
                       358, 361, 362, 365, 371, 377, 381, 382, 386, 391, 
                       393, 394, 395, 398, 403, 407, 411, 413, 415, 417, 
                       422, 427, 437, 445, 446, 447, 451, 453, 454, 458, 
                       466, 469, 471, 473, 478, 481, 482, 485, 489, 493, 
                       497, 501, 502, 505, 511, 514, 515, 517, 519, 526, 
                       527, 529, 533, 535, 537, 538, 542, 543, 545, 551, 
                       553, 554, 559, 562, 565, 566, 573, 579, 581, 583, 
                       586, 589, 591, 597, 611, 614, 622, 623, 626, 629, 
                       633, 634, 635, 649, 655, 662, 667, 669, 671, 674, 
                       679, 681, 685, 687, 689, 694, 695]
    
    some_fibonnaci_einstein_primes =   [359, 431, 433, 449, 509, 569, 571, 2971, 
                                        4723, 5387, 9311, 9677, 14431, 25561, 227, 
                                        233, 239, 251, 257, 263, 269, 281, 293, 311, 
                                        317, 347, 353, 359, 383, 389, 401, 419, 431, 
                                        443, 449, 461, 467, 479, 491, 503, 509, 521, 
                                        557, 563, 569, 587]
    
    some_palindromic_marsenic_primes = [31, 61, 89, 107, 127, 521, 607, 1279, 
                                       2203, 2281, 3217, 4253, 4423, 9689, 9941, 
                                       11213, 19937, 21701, 23209, 313, 353, 373, 
                                       383, 727, 757, 787, 797, 919, 929, 10301, 
                                       10501, 10601, 11311, 11411, 12421, 12721, 
                                       12821, 13331, 13831, 13931, 14341, 14741, 
                                       15451, 15551, 16061, 16361, 16561, 16661, 
                                       17471, 17971, 18181]

# hide cursor
cursor.hide()

try:
    for K in range(MAX_NUMBER_OF_ORDERS):

        # issue new order
        temp_random = random.randint(1, 9999)

        Order.steps = (temp_random % round(xsize / 10)) + 1
        Order.turn = Order.chance_exp[temp_random % 100]

        # first tracker update
        Tracker.future = (Tracker.present + Order.turn) % 4

        for frame in range(Order.steps):

            # the end of the order

            if frame == Order.steps - 1 and not Screen.is_tree[Tracker.current_y][Tracker.current_x]:

                Screen.grown[Tracker.current_y][Tracker.current_x] = (Format.GREEN + "." + Format.END)
                Screen.is_tree[Tracker.current_y][Tracker.current_x] = True

                temp_random = temp_random % 100

                if temp_random < SEED_BIRTH_RATE:

                    current_x_times_y           = Tracker.current_x * Tracker.current_y
                    index_on_fibonnaci_primes   = (temp_random)%len(Lists.some_fibonnaci_einstein_primes)
                    current_x_plus_y            = Tracker.current_x + Tracker.current_y

                    # protect the border of the screen
                    if Tracker.current_y > tree_rare.height:
                        if xsize - (tree_rare.x_offset - tree_rare.root) > Tracker.current_x > tree_rare.root:
            
                            # RARE TREE
                            if (current_x_times_y % Lists.some_fibonnaci_einstein_primes[index_on_fibonnaci_primes] < 10):

                                ScoreLog.more_points(100*tree_id_rare)
                                ScoreLog.new_discovery(tree_id_rare)
                                
                                tree_rare.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.pixel,
                                                Screen.is_tree, 
                                                "sap")

                                tree_rare.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.grown,
                                                Screen.is_tree, 
                                                "full")

                            # UNCOMMON TREE
                            elif (current_x_plus_y in Lists.some_palindromic_marsenic_primes 
                            or (Tracker.current_x + Tracker.current_y) % 37 == 0):

                                ScoreLog.more_points(50*tree_id_two)
                                ScoreLog.new_discovery(tree_id_two)
                    
                                tree_two.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.pixel,
                                                Screen.is_tree, 
                                                "sap")

                                tree_two.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.grown,
                                                Screen.is_tree, 
                                                "full")
                            
                            # COMMON TREE
                            elif (Tracker.current_x + Tracker.current_y) in Lists.some_semiprimes:

                                ScoreLog.more_points(10*tree_id_one)
                                ScoreLog.new_discovery(tree_id_one)
                        
                                tree_one.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.pixel,
                                                Screen.is_tree, 
                                                "sap")
                                                
                                tree_one.buffer(Tracker.current_y,
                                                Tracker.current_x, 
                                                Screen.grown,
                                                Screen.is_tree, 
                                                "full")

                Tracker.present = Tracker.future
            else:
                
                # every run except the last
                if not Screen.is_tree[Tracker.current_y][Tracker.current_x]:
                    Screen.pixel[Tracker.current_y][Tracker.current_x] = caules_retos[Tracker.present]
                    Screen.fade[Tracker.current_y][Tracker.current_x] = GLOBAL_FADE_RATE

            # second tracker update
            Tracker.current_x += x_operators[Tracker.present]
            Tracker.current_y += y_operators[Tracker.present]

            # wrap the screen
            if Tracker.current_x >= xsize:
                Tracker.current_x = 0
            elif Tracker.current_x < 0:
                Tracker.current_x = xsize - 1

            if Tracker.current_y >= ysize:
                Tracker.current_y = 0
            elif Tracker.current_y < 0:
                Tracker.current_y = ysize - 1

            Screen.update()

            # print the screen
            sys.stdout.write(chr(27) + "[2J")

            # print optmization
            # https://stackoverflow.com/questions/34828142/cmd-console-game-reduction-of-blinking
            # John Coleman
            print("\n".join(''.join(row) for row in Screen.pixel))

            time.sleep(0.01)

except KeyboardInterrupt:
    sys.exit()
