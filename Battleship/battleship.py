#Possible to-dos:
#   -update: better AI
#   -update: write more tests
#   -update: separate input and gameplay logic
#   -update: show length of ships during placement
#   -update: allow for lowercase letters in coordinates
#   -update: refactor for more efficient testing
#   -update: display both players' final boards at end of game
#   -update: distinguish between winner and loser at end of game
#   -update: query both players' names and display in messages
#
#   -feature: allow for easy/hard difficulty, with different board sizes
#   -feature: ships move one space every turn unless wrecked
#   -feature: enable multiplayer over network
#       -enable messages in multiplayer
#   -feature: allow boat placement with arrow keys and interactive view
#
#   -bug fix: get rid of text that flashes in between animations during firing phase
#   -bug fix: account for special characters in coordinate validation, add to tests
#
#   -frills: add standard animation where admiral shouts "FIRE TORPEDOES TO A2", etc

import re
from random import randint
import os
import time
import sys

from battleship_animations import Animations

class Player(object):
    """Player object -- contains list of ships, log of moves, and score based on destroyed ships"""
    def __init__(self, string):
        self.type = string
        self.ships = []
        self.score = 0
        self.log = {}

class Ship(object):
    """Ship object -- initializes with occupied, undamaged coordinates"""
    def __init__(self, name, coords):
        self.name = name
        self.score = 0
        self.coords = {}
        for coord in coords:
            self.coords[coord] = "undamaged"

class Battleship(object):
    """all gameplay logic"""
    def __init__(self):
        self.players = (
            Player("human"),
            Player("computer"),
        )
        self.ship_types = [
            {'name' : 'patrol_boat', 'length': 2},
            {'name' : 'cruiser', 'length': 3},
            {'name' : 'sub', 'length': 3},
            {'name' : 'battleship', 'length': 4},
            {'name' : 'aircraft_carrier', 'length': 5},
        ]
        self.col_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.encouraging_statements = [
            'Excellent!',
            'Wow!',
            'Muy bueno!!',
            'Hai il tocco d\'oro!',
            'Well, wouldja look\'t that!',
            'Hot damn!',
        ]
        self.status_display = {
            "hit" : "X",
            "undamaged" : "O",
            "miss" : "O"
        }
        self.standard_frame_rate = 13
        self.turn = 0

    def main(self):
        self.game_setup()
        self.gameplay()

    def game_setup(self):
        """each player places their ships after the loading animation"""
        animations.animate(animations.loading_screen, 4, self.standard_frame_rate)
        for player in self.players:
            for ship in self.ship_types:
                self.place_ship(player, ship)

    def gameplay(self):
        """alternate turns between players until a player wins"""
        while self.players[0].score < 17 and self.players[1].score < 17:
            self.turn += 1
            self.printBoards(self.players[0])
            for player in self.players:
                self.firing_phase(player)
        else:
            print "SOMEONE WON!!!! THE GAME IS OVER, AFTER %s TURNS!" % self.turns

    def place_ship(self, player, ship):
        """Retrieves starting coordinate and direction, verifies validity, passes occupied coordinates to new ship object"""
        #adjust treatment of screen size to actually display messages
        placed = False
        while placed == False:
            coord_and_direction = self.get_coord_and_direction(player, ship)
            ship_coords_or_error = self.find_ship_coords_or_give_error(player, ship, coord_and_direction['start_coord'], coord_and_direction['direction'])

            #if valid coordinate and layout were given, place ship;
            #otherwise, print error for humans and continue loop
            if isinstance(ship_coords_or_error, list):
                player.ships.append(Ship(ship['name'], ship_coords_or_error))
                placed = True
                if player.type == 'human':
                    print "\n%s" % self.encouraging_statements[randint(0, len(self.encouraging_statements)-1)]
            else:
                if player.type == 'human':
                    print ship_coords_or_error

    def get_coord_and_direction(self, player, ship):
        """retrieve placement of ship"""
        if player.type == 'human':
            self.printBoards(player)
            start_coord = raw_input("%s coordinate closest to A1? " % ship['name'].title())
            direction = raw_input("%s's direction from starting coordinate? (right/down) " % ship['name'].title())
        else:
            #if computer player, randomly places ship
            start_coord = self.random_coordinate()
            direction = ["right", "down"][randint(0,1)]
        return {'start_coord': start_coord, 'direction': direction}

    def find_ship_coords_or_give_error(self, player, new_ship, start_coord, direction):
        """find matching coordinates on board given ship, starting coordinate, and direction"""
        #verify that the ship is on the board
        if self.validate_coordinate(start_coord):
            coords = []
            if direction == 'right':
                if self.col_headers.index(start_coord[0]) + new_ship['length'] <= 9:
                    for col in self.col_headers[self.col_headers.index(start_coord[0]):self.col_headers.index(start_coord[0]) + new_ship['length']]:
                        coord = "".join([col, start_coord[1:]])
                        coords.append(coord)
                else:
                    return "***Not on the board!***"
            elif direction == 'down':
                if int(start_coord[1:]) + new_ship['length'] - 1 <= 10:
                    for n in range(int(start_coord[1:]), int(start_coord[1:]) + new_ship['length']):
                        coord = "".join([start_coord[0], str(n)])
                        coords.append(coord)
                else:
                    return "***Not on the board!***"
            else:
                return "***Please type \"up\" or \"down\" as the direction!***"

            #check for overlap with other ships
            for coord in coords:
                collision = self.collision_check(player, coord)
                if collision:
                    return "***This overlaps with your %s!***" % collision
            #return coordinates if all checks passed
            return coords
        else:
            return "***Invalid coordinate! It should look more like \"A1\" or \"J9\", \nand it should fit on columns A-J and rows 1-10.***"

    def validate_coordinate(self, coord):
        """ensure that coordinate is on board"""
        #look up with this regex works for row 10
        coord_pattern = re.compile('\w\d')
        if coord_pattern.match(coord):
            if coord[0] in self.col_headers:
                if int(coord[1:]) >= 1 and int(coord[1:]) <=10:
                    return True
        return False

    def collision_check(self, player, coord):
        """check for collisions during setup"""
        for ship in player.ships:
            if coord in ship.coords:
                return ship.name
        return False

    def random_coordinate(self):
        """generate random coordinate from A1 to J10"""
        return "".join([self.col_headers[randint(0, 9)], str(randint(1, 10))])

    def other_player(self, player):
        """return opposite player"""
        return self.players[self.players.index(player) - 1]

    def firing_phase(self, player):
        """get coordinate that hasn't already been chosen by player--check for hit and log result"""
        shot_fired = False
        while shot_fired == False:
            if player.type == 'human':
                coord = raw_input("Admiral! Where should we fire next? ")
            else:
                animations.animate(animations.comp_is_thinking, 3, self.standard_frame_rate)
                coord = self.random_coordinate()
                #display computer's move for time proportional to standard frame rate; followed by hit or miss animation
                print "Computer is firing at %s!" % coord
                time.sleep(1.0/self.standard_frame_rate * 13)
            if self.validate_coordinate(coord):
                if coord in player.log:
                    print "***Admiral, you already fired there!***"
                else:
                    shot_fired = True
                    for ship in self.other_player(player).ships:
                        if coord in ship.coords:
                            player.log[coord] = "hit"
                            if ship.coords[coord] == "undamaged":
                                animations.animate(animations.hit, 1, self.standard_frame_rate)
                                ship.coords[coord] = "hit"
                                print "***%s hit %s's %s!***" % (player.type, self.other_player(player).type, ship.name.replace("_", " "))
                                #check to see if ship is completely wrecked -- make own function
                                for ship_segment in ship.coords:
                                    if ship.coords[ship_segment] == "undamaged":
                                        break
                                else:
                                    player.score += len(ship.coords)
                                    animations.animate(animations.sunk, 1, self.standard_frame_rate)
                            break
                    else:
                        animations.animate(animations.miss, 1, self.standard_frame_rate)
                        player.log[coord] = "miss"
            else:
                if player.type == 'human':
                    print "***Invalid coordinate!***"

    def printBoards(self, player):
        """Print player's gameboard with left and right borders"""
        player_board = self.generate_player_board(player)
        log_board = self.generate_log_board(player)
        print "\n****** you ******            ******* them *****\n"
        for n in range(len(log_board)):
            print "%s      %s" % (player_board[n], log_board[n])

    def generate_player_board(self, player):
        """Print a board with labeled axes and player's ships, with damage"""
        rows = []
        for n in range(0, 11):
            #row 1 is column headers
            if n == 0:
                row = ["   "]
                for col in self.col_headers:
                    row.append(col)
            else:
                #y axis has vertical line; needs special treatment for two-digit numbers
                if n < 10:
                    row = [" %s|" % n]
                else:
                    row = ["%s|" % n]
                #check if cell is occupied by ship segement
                for col in self.col_headers:
                    occupied = False
                    active_cell = "".join([col, str(n)])
                    for ship in player.ships:
                        if active_cell in ship.coords:
                            occupied = ship.coords[active_cell]
                    if occupied:
                        row.append(self.status_display[occupied])
                    else:
                        row.append(" ")
                row.append("|")
            rows.append("".join(row))
        return self.normalize_rows(rows, 24)

    def generate_log_board(self, player):
        """Print a board with labeled axes and all locations of player's moves"""
        rows = []
        for n in range(0, 11):
            #row 1 is column headers
            if n == 0:
                row = ["   "]
                for col in self.col_headers:
                    row.append(col)
            else:
                #y axis has vertical line; needs special treatment for two-digit numbers
                if n < 10:
                    row = [" %s|" % n]
                else:
                    row = ["%s|" % n]
                #check if cell is occupied by ship segement
                for col in self.col_headers:
                    active_cell = "".join([col, str(n)])
                    if active_cell in player.log:
                        row.append(self.status_display[player.log[active_cell]])
                    else:
                        row.append(" ")
                row.append("|")
            rows.append("".join(row))
        return self.normalize_rows(rows, 16)

    def normalize_rows(self, table, length):
        """sets all rows in table to same length"""
        for n in range(len(table)):
            if len(table[n]) < length:
                for x in range(length - len(table[n])):
                    table[n] += " "
        return table

if __name__ == '__main__':
    animations = Animations()
    b = Battleship()
    b.main()
