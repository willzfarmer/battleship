#!/usr/bin/env python

'''
Battleship! The Game

Will Farmer       <willzfarmer@gmail.com>
Michael Brughelli <michael.brughelli@gmail.com>
Tommy Gebhardt    <tommygebhardt@gmail.com>
Catherine Dewerd  <catherine.dewerd@colorado.edu>

Ship Classes:
    aircraft
    battleship
    submarine
    destroyer
    patrol

'''
r"""
%s
//What do you expect to find here? And if you find what you seek, will you truly be happy?
%s
//Thar be dragons here!



                                              ,....,. 
                                          ..''   .' 
                                       .'"       | 
                                    .''          \ 
                                 .''              \. 
                               .'                  ."., 
                             ,:'             ..,'"'   '...,..::/""..... 
                           /'"          .,'"'  .,',:,'""'         .,'' 
                         ,'.'      .,'"' ..,''' ""         .'   ."' 
                       ,'  \, ..,''  .,''. ..,'""        ./   ." 
                     ."     .,"  .,'".,"'./           ..''   / 
                    ,'    .'  ./'.,"'  .'  "'     ." '.     / 
                  .'   ./' ./"."\,..,''     '" ../,     ,  | 
                 ,   ./' .'./'|/     ............        ',| 
                /   /' ,'.".,'""\..... '""''''''  .::/'.., | 
               /  ." ,' ':\ ""''  |  ,      ''          '""   \ 
              /  /'.''. |:::::::""' ,' ' ''. ".,.,  ""'    .""' 
             | ." /.,":. ""..,   "\'.."'..  ;"'  '\.'""' ." \
             | \.:\.    '""./\ \  | ' '" .,"".           / 
             / \'   '"..     ", \  \,',     "'..  .,     ' 
            /.'",''..,  '\,   '\ ". '\'.,     , "'. "'.,| 
           .,'        '". ',    \ '.".. ''../'      "" __\ 
           '             \,',    \  '.'\..,  ","'  .'" 
                         |  |    '| ,\""'\/.  |  ." 
            ."          .|  .    / / ./'. '.".' /' 
            /'        ..|':""''\././  /   "  '/\.' 
           //  ./  .'"    /' ./'.' .'  | ..,  ':| 
         ./:  ,/   |",   ' ."'  :  '   |    .../:, 
        .'.'.\/   /.'           ''  .,   ..\' 
      .,\.\".'   /"    ,"' \...,      "\.\| ", 
     /    ./""''   ..:    ',|  "".,     '\  ', 
  .,' "'   \|     "".'".    '/  .| '\.     ", '\ 
 /          \.    ../,   "./ '\ |'  \/"" '".'\  \ 
/   '\\:.   \,"\::'  ./""'    ./|  .'     .'"/| '| 
' ,"\:"/""''  /'  ."\'  .., |:| .| |'    .'' .\|  ', 
|/  / /'    .'| /  |. \,    /'"/. |  |:\..," .||  \ 
'' /.'      //\|'  '\/\:.   :,/"'::.  ,   ..::'|  | 
            ||'/,    '\\/"\ '/|    '\ '"::::"| || . 
            || \\       "".   ...,  '.  \\...| |' | 
            ||  "\,         .".\, ". ', | \  '||  | 
             '              |\|'|\/.''\ | |\  ||  | 
                            ||\/"/| '\, ., / / /  , 
                             ' \  "   '"  / / .' / 
                                '      .'".' .' / 
                                  ..'"'.." ." ." 
                              .,"":.'""..'" ." 
                         .,:'"'"'  .'"  ..'" 
                       ." ."'..'""...,"' 
                    .." "    , ""' 
                   /  . :/"' 
                 .'  :/' 
                /  /' 
               / .' 
              / ' 
             /.' 
             ' 
"""

import sys
import os
import random
import time

try:
    import battleshipAI

    import numpy
    import argparse
except ImportError:
    print 'Error, Missing Libraries'
    sys.exit(0)

players = []

def main():
    args = get_args()
    clear_screen()
    establish_players(args)
    initialize_game(args)
    start_game(args)
    end_game(args)

def get_args():
    '''
    Gets user input from command line
    :returns: argument dictionary
    '''
    parser = argparse.ArgumentParser(description='Battleship, The Game!')
    parser.add_argument('-p', '--players', type=int, default=2, help='How many players')
    parser.add_argument('-g', '--gridsize', type=int, default=10, help='Grid Size')
    parser.add_argument('-a', '--auto', action='store_true', default=False, help='Auto Place Ships Randomly?')
    parser.add_argument('-s', '--simulation', action='store_true', default=False, help='Make all players AI?')
    parser.add_argument('-l', '--listing', type=str, nargs='+', default=None, help='List of players')
    parser.add_argument('-w', '--winner', action='store_false', default=True, help='Display only winning stats')
    parser.add_argument('-f', '--filename', type=str, default=None, help='File to write results')
    args = parser.parse_args()
    if args.listing: # Sets playercount to match listing in order to prevent collisions
        args.players = len(args.listing)
    return args

def clear_screen():
    '''
    Clears the screen and readies for the next state
    '''
    os.system('clear') # Simple os.system call

def establish_players(args):
    '''
    Determines players/adds to listing
    :param args: argument dictionary
    '''
    for number in range(args.players):                                          # Create player for the number of specified players
        new_player = Player(args.gridsize, number)
        players.append(new_player)                                              # Add the player to global player list
        if args.listing:                                                        # Setup AI for players depending on listing
            if args.listing[number] == 'a':
                players[number].ai = battleshipAI.BattleshipAI(players[number])
            elif args.listing[number] != 'h':                                   # This will die with invalid playertype
                print('UserWarning, Invalid PlayerType')
                sys.exit(0)
    for item in players:                                                        # Create a seperate guess grid per player for each player. These
        item.create_guess_grids()                                               # guess grids are stored in an array for that player
    if args.simulation:                                                         # If simulation was added, overwrite all playerAI with a new AI, regardless
        for player in players:                                                  # of specification
            player.ai = battleshipAI.BattleshipAI(player)

def initialize_game(args):
    '''
    Sets up the board for the player
    :param args: argument dictionary
    '''
    helpstring = "Please input coordinates like 'x:y:r' where r is either h or v for horizontal or vertical"
    shipsizes = [5, 4, 3, 3, 2]
    for current_player in players:                   # Iterate through players and create their ships
        switch(current_player.name)                  # Switch to the current player to prevent cheating
        if not current_player.ai:                    # Print help for current (human) player
            print(helpstring)
        for item in shipsizes:                       # Create new Ship and possibly autoplace
            current_player.add_ship(item, args.auto)
        print current_player.grid                    # After ships are placed, print the player's ship grid
        raw_input("Continue")
    clear_screen()

def start_game(args):
    '''
    Starts gameplay
    :param args: argument dictionary
    '''
    num_playing = len(players);                              # Establish initial playercount
    while num_playing >= 2:                                  # And continue playing until everyone save one dies
        for player in players:
            if player.get_state():                           # If the player is still alive,
                switch(player.name)                          # let them take their turn
                print('Available Grids')                     # Display all available enemy grids to shoot
                for item in player.guesses:
                    if item.pid != player.name:
                        print item.guesses
                if player.ai != None:                        # If the player has AI, use that to shoot
                    player.ai.shoot(players)
                else:                                        # Otherwise let them pick coordinates
                    p, x, y, = get_coords(player, args)
                    player.shoot(p,x,y)
                    raw_input('Press enter for next player')
        num_playing = 0;
        for p in players:                                    # Establish new playercount. If this is 1, quit
            if p.get_state():
                num_playing += 1

def end_game(args):
    '''
    Declares Winner and Ends Game
    :param args: argument dictionary
    '''
    clear_screen()
    for player in players: # Display Winner's Info
        if player.get_state():
            print('Congratulations Player %i! You have won!' %player.name)

    for player in players:
        if args.winner: # If winner flag, just display winner's info
            if player.get_state():
                print_grids(player)
        else:
            print_grids(player)

        if args.filename: # If a filename was supplied, write output to that name
            wfile = open(args.filename, 'w')
            for player in players:
                if player.get_state():
                    wfile.write('Congratulations Player %i! You have won!\n' %player.name)
            for player in players:
                wfile.write(format_grids(player))

def format_grids(player):
    '''
    Prints designated player grids
    :param player: Player() class object
    :returns: formatted string
    '''
    string = ''
    string += ("Player %i's ships:\n" %player.name)
    string += str((player.grid))
    string += ("\nPlayer %i's guesses:\n" %player.name)
    for item in player.guesses:
        string += str(item.guesses)
        string += '\n'
    return string

def print_grids(player):
    '''
    Prints designated player grids
    :param player: Player() class object
    '''
    print("Player %i's ships:" %player.name)
    print(player.grid)
    print("Player %i's guesses:" %player.name)
    for item in player.guesses:
        print item.guesses

def split_coords(usr_string):
    '''
    Gets user input and returns coordinates
    :param usr_string: formatted coordinate string
    :returns: p -- player ID
              x -- X coordinate
              y -- Y coordinate
    '''
    try: # Try to format string, die if failure
        p = int(usr_string.split(':')[0])
        x = int(usr_string.split(':')[1])
        y = int(usr_string.split(':')[2])
        return p, x, y
    except ValueError:
        return 0, -1, -1

def get_coords(player, args):
    '''
    Validates proper shooting input
    :param player: Player() class object
    :param args: argument dictionary
    :returns: p -- player ID
              x -- X coordinate
              y -- Y coordinate
    '''
    p, x, y = split_coords(  # Get initial user input
            raw_input(
                "Choose target player id and coordinates of shot (P:X:Y): "))
    while not players[p].get_state or p > len(players) or p < 0:
        p, x, y = split_coords( # If the player is dead, or has an invalid pid, try again
                    raw_input(
                        "Invalid Player Id: Choose another set for your shot: "))
    while p == player.name:
        p, x, y = split_coords( # If pid is player's pid, try again
                    raw_input(
                          "Pew Pew Pew! You just tried to shoot yourself: Choose another set for your shot: "))

    while (x < 0 or x > (args.gridsize - 1) or
            y < 0 or y > (args.gridsize - 1)):
        p, x, y = split_coords( # If the (x,y) position is outside the grid, try again
                    raw_input(
                          "Invalid Coordinates: Choose another set for your shot: "))

    return p, x, y

def switch(player_num):
    '''
    Clears screen and holds for player (player_num)
    :param player_num: PID for player to switch to
    '''
    if not players[player_num].ai: # First double-check that this isn't an AI
        clear_screen()
        text = 'PLAYER %i PLEASE CONTINUE' %player_num
        raw_input(text)

def gen_grid(size):
    '''
    Creates a 10x10 grid and returns
    :param size: Integer size of grid
    :returns: numpy.array() object (2D)
    '''
    a_grid = []
    for row in range(size):
        row = []
        for number in range(size):
            row.append(0)
        a_grid.append(row)
    grid = numpy.array(a_grid)
    return grid

class Player:
    def __init__(self, gridsize, name):
        '''
        Player Class
        Contains Shiplist and Grid
        :param gridsize: size of game grid
        :param name: player id name
        '''
        self.gridsize = gridsize
        self.grid     = gen_grid(gridsize)
        self.guesses  = []
        self.shiplist = []
        self.name     = name
        self.state    = True
        self.ai       = None

    def create_guess_grids(self):
        '''
        Creates guessing grids for multiple players
        '''
        for item in players: # See Guesses() class object
            new_grid = Guesses(self.gridsize, item.name)
            self.guesses.append(new_grid)

    def shoot(self, pid, x , y):
        '''
        Shoot at specified player at specified coordinates
        :param pid: Int player id
        :param x: Int X coordinate
        :param y: Int Y coordinate
        '''
        target = players[pid]                  # establish target
        for item in self.guesses:              # establish current target's guess grid
            if item.pid == pid:
                current_guesses = item.guesses
        for item in target.shiplist:           # Iterate through shiplist and register for hits
            result = item.register(x, y)
            if result == True:                 # Display relevant output to player
                print 'Hit!'
                current_guesses[y][x] = 1      # Change guess grid to show
                return None
            elif result == False:
                if current_guesses[y][x] == 0: # Change to miss only if we haven't hit there before
                    current_guesses[y][x] = -1
            else:
                current_guesses[y][x] = 1      # If we get a string back, it means we sunk their ship
                return None
        print 'Miss!'                          # If something odd happened, return a miss

    def get_rand_pos(self):
        '''
        Returns a random spot
        :returns: formatted coordinate string
        '''
        if random.randint(0,1) == 0:
            ort = 'v'
        else:
            ort = 'h'
        coord = '%i:%i:%s' %(random.randint(0, self.gridsize),
                             random.randint(0, self.gridsize), ort)
        return coord

    def add_ship(self, size, auto):
        '''
        Add a ship to the player
        :param size: size of the ship to add
        :param auto: boolean to auto place ship
        '''
        if auto:                                                                                 # If auto, get a random spot
            coord = self.get_rand_pos()
        else:                                                                                    # Otherwise, get human input
            coord = raw_input('Please Enter Location for Ship with Size %i (X:Y:R): ' %size)
        new_ship      = self.Ship(size, coord, self.gridsize)                                    # Create a ship there
        ship_conflict = new_ship.conflict(self.grid)                                             # Check for conflict
        start_time = time.time()                                                                 # Initiate a timer to prevent looping
        while ship_conflict == True:                                                             # Keep creating ships until no conflict
            current_time = time.time()                                                           # Set current time
            if current_time - start_time > 10:                                                   # Stop if we've gone over 10s
                print("Timout Error")
                sys.exit(0)
            if auto:                                                                             # Get another ship
                coord = self.get_rand_pos()
            else:                                                                                # Get another ship
                coord = raw_input('Please Enter Location for Ship with Size %i (X:Y:R): ' %size)
            new_ship      = self.Ship(size, coord, self.gridsize)
            ship_conflict = new_ship.conflict(self.grid)

        [x, y, r] = coord.split(':')                                                             # Obtain coordinates from variable
        x = int(x)
        y = int(y)

        for number in range(size):                                                               # Change player grid to show ship placement
            if r == 'v':
                    self.grid[y + number][x] = 1
            elif r == 'h':
                    self.grid[y][x + number] = 1

        self.shiplist.append(new_ship)                                                           # Add Ship() object to player's ship list
        if not auto:                                                                             # If human, print placement
            print self.grid

    def get_state(self):
        '''
        Refreshes state and returns
        :returns: current player state
        '''
        if not self.state:                # If the state is false, return false
            return self.state
        else:                             # Otherwise iterate through ships
            ship_state = False
            for ship in self.shiplist:
                for item in ship.hits:
                    if item != 0:         # If any ship has a hitbox left, we're alive
                        ship_state = True
            self.state = ship_state
            return self.state             # Return the player's state

    class Ship:
        def __init__(self, size, coord, gridsize):
            '''
            Ship Class
            :param size: Integer size of ship
            :param coord: Coordinate for the top of the ship (N/W)
            :param gridsize: Length of the grid's side
            '''
            self.hits      = []
            self.x         = int(coord.split(':')[0])
            self.y         = int(coord.split(':')[1])
            self.r         = coord.split(':')[2]
            self.size      = size
            self.test_grid = gen_grid(gridsize)
            self.state     = True

        def register(self, x0, y0):
            '''
            Registers a hit (or a miss)
            :param x0: X coordinate to check
            :param y0: Y coordinate to check
            :returns: boolean hit reply
            '''
            hit_confirm = False                                            # Initially assume we haven't been hit
            for i in range(len(self.hits)):                                # Iterate through hitboxes
                if self.hits[i] == ('%i:%i' %(y0, x0)):                    # If hitbox value == coordinate, we been hit
                    self.hits[i] = 0
                    hit_confirm = True

            if hit_confirm == True:                                        # If we been hit, determine ship's state
                self.state = False                                         # Assume Dead initially
                for item in self.hits:
                    if item != 0:
                        self.state = True                                  # If any hitboxes are left, we're still good baby!
                if self.state == False:                                    # Otherwise respond with a classic message
                    hit_confirm = 'You have sunk my ship! (%i)' %self.size
                    print hit_confirm                                      # Print that sexy message
            return hit_confirm

        def conflict(self, grid):
            '''
            Determines if there's a conflict between two ships
            :param grid: Player's grid to check against
            '''
                                                                                           # Establish there's room in the grid
            if self.r == 'v':                                                              # If the ship is vertical
                try:
                    for number in range(self.size):                                        # Test each spot to make sure the grid has room
                        self.test_grid[self.y + number][self.x]
                        self.hits.append('%i:%i' %(self.y + number, self.x))
                except IndexError:                                                         # "With great ERROR comes great CONFLICT"
                    return True
            elif self.r == 'h':                                                            # If the ship is horizontal
                try:
                    for number in range(self.size):                                        # Test each spot horizontally instead
                        self.test_grid[self.y][self.x + number]
                        self.hits.append('%i:%i' %(self.y, self.x + number))
                except IndexError:                                                         # "With great ERROR comes great CONFLICT"
                    return True
            else:
                return True                                                                # if no ERRORs, we have succeeded

                                                                                           # Establish we aren't running over any other ships and they're not close
            for number in range(self.size + 1):                                            # Check a larger range than we have ship
                if self.r == 'v':                                                          # If vertical
                    if number == self.size:                                                # If we have a larger number than hitboxes
                        pass                                                               # Skip this number
                    elif grid[self.y + number][self.x] > 0:                                # If there's something here, return CONFLICT
                        return True
                    try:                                                                   # Now try to access every element around the ship
                        for dom in range(-1,2):                                            # Grab every x value between [-1, 2)
                            for ran in range(-1, 2):                                       # Grab every y value between [-1, 2)
                                current_x = self.x + dom                                   # Establish current x value to check against
                                current_y = self.y + number + ran                          # Establish current y value to check against
                                if grid[current_y][current_x] > 0:                         # If anything is full, we have GREAT CONFLICT
                                    if ('%i:%i' %(current_y, current_x)) not in self.hits: # If this is us though, ignore!
                                        return True
                    except:                                                                # If we get an error, it means we ran out of grid. This is ok
                        pass
                elif self.r == 'h':                                                        # If horizontal
                    if number == self.size:                                                # If we gots a big number, skip it
                        pass
                    elif grid[self.y][self.x + number] > 0:                                # If there's a ship here, CONFLIIIIICT
                        return True
                    try:                                                                   # Same exact code as before, except with X iterator instead of Y
                        for ran in range(-1,2):
                            for dom in range(-1, 2):
                                current_x = self.x + number + dom
                                current_y = self.y + ran
                                if grid[current_y][current_x] > 0:
                                    if ('%i:%i' %(current_y, current_x)) not in self.hits:
                                        return True
                    except IndexError:                                                     # "With great ERROR comes great CONFLICT, but not here"
                        pass
            return False                                                                   # If we managed to avoid everything, WE WIN!

class Guesses:
    def __init__(self, size, pid):
        '''
        Guessing Grid Class
        :param size: Size of grid
        :param pid: player for which the grid belongs
        '''
        self.pid     = pid
        self.guesses = gen_grid(size)

if __name__=="__main__": # Run our code
    sys.exit(main())
