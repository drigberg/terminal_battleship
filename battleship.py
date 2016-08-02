import re
from random import randint
import os
import time
import sys

class Player(object):
    """Player object -- initializes with blank board"""
    def __init__(self, string):
        self.name = string
        self.ships = []
        self.score = 0

class Ship(object):
    """Ship object -- initializes with occupied coordinates"""
    def __init__(self, name, coords):
        self.name = name
        self.score = 0
        self.coords = {}
        for coord in coords:
            self.coords[coord] = "okay"

class Battleship(object):
    def __init__(self):
        self.players = (
            Player("human"),
            Player("computer"),
        )
        self.ships = [
            {'name' : 'battleship', 'length': 4},
            {'name' : 'cruiser', 'length': 3},
            {'name' : 'sub', 'length': 3},
            {'name' : 'aircraft_carrier', 'length': 5},
            {'name' : 'patrol_boat', 'length': 2},
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
        self.status_display = {"hit" : "H", "okay" : "O"}
        self.loading_screen = [
            [
                "________________________________________________",
                "___XXX____X___XXXXX_XXXXX_X_____XXXX____________",
                "___X__X__X_X____X_____X___X_____X_______________",
                "___XXX__X_X_X___X_____X___X_____XXX_____________",
                "___X__X_X___X___X_____X___X_____X_______________",
                "___XXX__X___X___X_____X___XXXX__XXXX____________",
                "________________________________________________",
                "______________________OOO__O___O_OOOOO_OOOO_____",
                "_____________________O_____O___O___O___O___O____",
                "______________________OOO__OOOOO___O___OOOO_____",
                "_________________________O_O___O___O___O________",
                "______________________OOO__O___O_OOOOO_O________",
                "________________________________________________",
                "________________________________________________",
                "______LOADING___________________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "____XXX____X___XXXXX_XXXXX_X_____XXXX___________",
                "____X__X__X_X____X_____X___X_____X______________",
                "____XXX__X_X_X___X_____X___X_____XXX____________",
                "____X__X_X___X___X_____X___X_____X______________",
                "____XXX__X___X___X_____X___XXXX__XXXX___________",
                "________________________________________________",
                "_____________________OOO__O___O_OOOOO_OOOO______",
                "____________________O_____O___O___O___O___O_____",
                "_____________________OOO__OOOOO___O___OOOO______",
                "________________________O_O___O___O___O_________",
                "_____________________OOO__O___O_OOOOO_O_________",
                "________________________________________________",
                "________________________________________________",
                "_______LOADING__________________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "_____XXX____X___XXXXX_XXXXX_X_____XXXX__________",
                "_____X__X__X_X____X_____X___X_____X_____________",
                "_____XXX__X_X_X___X_____X___X_____XXX___________",
                "_____X__X_X___X___X_____X___X_____X_____________",
                "_____XXX__X___X___X_____X___XXXX__XXXX__________",
                "________________________________________________",
                "____________________OOO__O___O_OOOOO_OOOO_______",
                "___________________O_____O___O___O___O___O______",
                "____________________OOO__OOOOO___O___OOOO_______",
                "_______________________O_O___O___O___O__________",
                "____________________OOO__O___O_OOOOO_O__________",
                "________________________________________________",
                "________________________________________________",
                "________LOADING_________________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "____XXX____X___XXXXX_XXXXX_X_____XXXX___________",
                "____X__X__X_X____X_____X___X_____X______________",
                "____XXX__X_X_X___X_____X___X_____XXX____________",
                "____X__X_X___X___X_____X___X_____X______________",
                "____XXX__X___X___X_____X___XXXX__XXXX___________",
                "________________________________________________",
                "_____________________OOO__O___O_OOOOO_OOOO______",
                "____________________O_____O___O___O___O___O_____",
                "_____________________OOO__OOOOO___O___OOOO______",
                "________________________O_O___O___O___O_________",
                "_____________________OOO__O___O_OOOOO_O_________",
                "________________________________________________",
                "________________________________________________",
                "_________LOADING________________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "___XXX____X___XXXXX_XXXXX_X_____XXXX____________",
                "___X__X__X_X____X_____X___X_____X_______________",
                "___XXX__X_X_X___X_____X___X_____XXX_____________",
                "___X__X_X___X___X_____X___X_____X_______________",
                "___XXX__X___X___X_____X___XXXX__XXXX____________",
                "________________________________________________",
                "______________________OOO__O___O_OOOOO_OOOO_____",
                "_____________________O_____O___O___O___O___O____",
                "______________________OOO__OOOOO___O___OOOO_____",
                "_________________________O_O___O___O___O________",
                "______________________OOO__O___O_OOOOO_O________",
                "________________________________________________",
                "________________________________________________",
                "__________LOADING_______________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "____XXX____X___XXXXX_XXXXX_X_____XXXX___________",
                "____X__X__X_X____X_____X___X_____X______________",
                "____XXX__X_X_X___X_____X___X_____XXX____________",
                "____X__X_X___X___X_____X___X_____X______________",
                "____XXX__X___X___X_____X___XXXX__XXXX___________",
                "________________________________________________",
                "_____________________OOO__O___O_OOOOO_OOOO______",
                "____________________O_____O___O___O___O___O_____",
                "_____________________OOO__OOOOO___O___OOOO______",
                "________________________O_O___O___O___O_________",
                "_____________________OOO__O___O_OOOOO_O_________",
                "________________________________________________",
                "________________________________________________",
                "___________LOADING______________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "_____XXX____X___XXXXX_XXXXX_X_____XXXX__________",
                "_____X__X__X_X____X_____X___X_____X_____________",
                "_____XXX__X_X_X___X_____X___X_____XXX___________",
                "_____X__X_X___X___X_____X___X_____X_____________",
                "_____XXX__X___X___X_____X___XXXX__XXXX__________",
                "________________________________________________",
                "____________________OOO__O___O_OOOOO_OOOO_______",
                "___________________O_____O___O___O___O___O______",
                "____________________OOO__OOOOO___O___OOOO_______",
                "_______________________O_O___O___O___O__________",
                "____________________OOO__O___O_OOOOO_O__________",
                "________________________________________________",
                "________________________________________________",
                "____________LOADING_____________________________",
                "________________________________________________",
            ],
            [
                "________________________________________________",
                "____XXX____X___XXXXX_XXXXX_X_____XXXX___________",
                "____X__X__X_X____X_____X___X_____X______________",
                "____XXX__X_X_X___X_____X___X_____XXX____________",
                "____X__X_X___X___X_____X___X_____X______________",
                "____XXX__X___X___X_____X___XXXX__XXXX___________",
                "________________________________________________",
                "_____________________OOO__O___O_OOOOO_OOOO______",
                "____________________O_____O___O___O___O___O_____",
                "_____________________OOO__OOOOO___O___OOOO______",
                "________________________O_O___O___O___O_________",
                "_____________________OOO__O___O_OOOOO_O_________",
                "________________________________________________",
                "________________________________________________",
                "_____________LOADING____________________________",
                "________________________________________________",
            ]
        ]

    def main(self):
        self.animate(self.loading_screen, 5)
        self.game_setup()
        self.gameplay()

    def game_setup(self):
        """Establishes human and basic AI"""
        for player in self.players:
            for ship in self.ships:
                self.place_ship(player, ship)
            self.printBoard(player)

    def gameplay(self):
        turn = 0
        while self.players[0].score < 21 and self.players[1].score < 21:
            turn += 1
            for player in self.players:
                self.fire_torpedoes(player)

    def fire_torpedoes(self, player):
        if player.name == 'human':
            coord = raw_input("Admiral! Where should we fire next? ")
            print coord


    def printBoard(self, player):
        """Prints player's gameboard with left and right borders"""
        print "\n\n******* %s ******* \n" % player.name

        for n in range(0, 11):
            if n == 0:
                row = ["   "]
                for col in self.col_headers:
                    row.append(col)
            else:
                if n < 10:
                    row = [" %s|" % n]
                else:
                    row = ["%s|" % n]
                for col in  self.col_headers:
                    occupied = False
                    active_cell = "".join([col, str(n)])
                    for ship in player.ships:
                        if active_cell in ship.coords:
                            occupied = ship.coords[active_cell]
                    if occupied:
                        row.append(self.status_display[occupied])
                    else:
                        row.append("_")
                row.append("|")
            print "".join(row)


    def place_ship(self, player, ship):
        """Retrieves starting coordinate and direction, verifies validity, passes occupied coordinates to new ship object"""
        placed = False
        while placed == False:
            if player.name == 'human':
                start_coord = raw_input("%s coordinate closest to A1? " % ship['name'].title())
                direction = raw_input("%s's direction from starting coordinate? (right/down) " % ship['name'].title())
            else:
                #if computer player, randomly places ship
                start_coord = "".join([self.col_headers[randint(0, 9)], str(randint(1, 10))])
                direction = ["right", "down"][randint(0,1)]
            new_coords = self.find_new_coords(player, ship, start_coord, direction)
            if isinstance(new_coords, list):
                new_ship = Ship(ship['name'], new_coords)
                player.ships.append(new_ship)
                placed = True
                if player.name == 'human':
                    print "%s Your %s in on coordinates %s." % (self.encouraging_statements[randint(0, len(self.encouraging_statements)-1)], ship['name'], new_coords)
            else:
                if player.name == 'human':
                    print new_coords

    def find_new_coords(self, player, ship, start_coord, direction):
        """find matching coordinates on board given ship, starting coordinate, and direction"""
        #verify that the ship is on the board
        if self.validate_coordinate(start_coord):
            coords = []
            if direction == 'right':
                if self.col_headers.index(start_coord[0]) + ship['length'] <= 9:
                    for col in self.col_headers[self.col_headers.index(start_coord[0]):self.col_headers.index(start_coord[0]) + ship['length']]:
                        coord = "".join([col, start_coord[1:]])
                        coords.append(coord)
                else:
                    return "Not on the board -- too far to the right!"
            elif direction == 'down':
                if int(start_coord[1:]) + ship['length'] - 1 <= 10:
                    for n in range(int(start_coord[1:]), int(start_coord[1:]) + ship['length']):
                        coord = "".join([start_coord[0], str(n)])
                        coords.append(coord)
                else:
                    return "Not on the board -- too far down!"
            else:
                return "Please type \"up\" or \"down\" as the direction!"

            #check for overlap with other ships
            for coord in coords:
                collision = self.collision_check(player, coord)
                if collision:
                    return "This overlaps with your %s!" % collision
            #return coordinates if all checks passed
            return coords
        else:
            return "That is not a valid coordinate!!! It should look more like \"A1\" or \"J9\", \nand it should fit on columns A-J and rows 1-10."

    def validate_coordinate(self, coord):
        """ensure that player-given or random coordinate is on board"""
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

    def animate(self, frames, loops):
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=17, cols=48))
        while loops is not None:
            loops -= 1
            for n in range(len(frames)):
                time.sleep(0.08)
                os.system('cls' if os.name == 'nt' else 'clear')
                for row in frames[n]:
                    print row
            if loops == 0:
                for a in range(17):
                    time.sleep(0.08)
                    print ""
                os.system('cls' if os.name == 'nt' else 'clear')
                break


if __name__ == '__main__':
    b = Battleship()
    b.main()
