#To-Do:
#       -complete torpedo logic
#       -create logs of player + computer torpedoes; display accordingly on
#           player's board and player's fog-of-war view of other board
#       -finish explosion animation
#       -animation for misses?
#       -"computer is thinking" screen
#       -feature: ships move one space every turn unless wrecked
#       -enable multiplayer over network
#       -enable messages in multiplayer


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
    """all gameplay logic"""
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

    def main(self):
        self.animate(animations.loading_screen, 5)
        self.game_setup()
        self.gameplay()

    def game_setup(self):
        """Establishes human and basic AI"""
        for player in self.players:
            for ship in self.ships:
                self.place_ship(player, ship)
            self.printBoard(player)

    def gameplay(self):
        """alternate turns between players until a player wins"""
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
        print "******* %s ******* \n" % player.name

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
            print "".join(row)


    def place_ship(self, player, ship):
        """Retrieves starting coordinate and direction, verifies validity, passes occupied coordinates to new ship object"""
        #adjust treatment of screen size to actually display messages
        placed = False
        while placed == False:
            if player.name == 'human':
                self.printBoard(player)
                print "\n"
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
                    # print "%s Your %s in on coordinates %s." % (self.encouraging_statements[randint(0, len(self.encouraging_statements)-1)], ship['name'], new_coords)
                    print self.encouraging_statements[randint(0, len(self.encouraging_statements)-1)]

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

    def animate(self, frame_list, loops):
        """takes in list of frames, iterates at hard-coded framerate"""
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=17, cols=48))
        while loops is not None:
            loops -= 1
            for n in range(len(frame_list)):
                #clears screen once entire frame has been displayed
                time.sleep(0.08)
                os.system('cls' if os.name == 'nt' else 'clear')
                for row in frame_list[n]:
                    print row
            if loops == 0:
                for a in range(17):
                    time.sleep(0.08)
                    print ""
                os.system('cls' if os.name == 'nt' else 'clear')
                break

class Animations(object):
    #class containing all frames for animations
    def __init__(self):
        self.loading_screen = [
            [
                "                                                ",
                "   XXX    X   XXXXX XXXXX X     XXXX      *     ",
                "   X  X  X X    X     X   X     X               ",
                "   XXX  X X X   X     X   X     XXX             ",
                "   X  X X   X   X     X   X     X               ",
                "   XXX  X   X   X     X   XXXX  XXXX            ",
                "                                                ",
                "     *                OOO  O   O OOOOO OOOO     ",
                "                     O     O   O   O   O   O    ",
                "                      OOO  OOOOO   O   OOOO     ",
                "                         O O   O   O   O        ",
                "            *         OOO  O   O OOOOO O        ",
                "                                                ",
                "                                                ",
                "      LOADING                                   ",
                "         *                              *       ",
            ],
            [
                "                                                ",
                " *  XXX    X   XXXXX XXXXX X     XXXX           ",
                "    X  X  X X    X     X   X     X              ",
                "    XXX  X X X   X     X   X     XXX            ",
                "    X  X X   X   X     X   X     X              ",
                "    XXX  X   X   X     X   XXXX  XXXX           ",
                "                *                *              ",
                "                     OOO  O   O OOOOO OOOO      ",
                "             *      O     O   O   O   O   O     ",
                "                     OOO  OOOOO   O   OOOO      ",
                "  *                     O O   O   O   O         ",
                "                     OOO  O   O OOOOO O         ",
                "                                                ",
                "                             *                  ",
                "       LOADING                                  ",
                "                               *                ",
            ],
            [
                "        *                                       ",
                "     XXX    X   XXXXX XXXXX X *   XXXX          ",
                "     X  X  X X    X     X   X     X             ",
                "     XXX  X X X   X     X   X     XXX           ",
                "     X  X X   X   X     X   X     X    *        ",
                "     XXX  X   X   X     X   XXXX  XXXX          ",
                "                                                ",
                "                    OOO  O   O OOOOO OOOO       ",
                "    *              O     O   O   O   O   O      ",
                "                    OOO  OOOOO   O   OOOO       ",
                "                       O O   O   O   O     *    ",
                "                    OOO  O   O OOOOO O          ",
                "                                                ",
                "                            *                   ",
                "        LOADING                                 ",
                "                                *               ",
            ],
            [
                "         *                                      ",
                "    XXX    X   XXXXX XXXXX X     XXXX           ",
                "    X  X  X X    X     X   X     X              ",
                "    XXX  X X X   X     X   X     XXX         *  ",
                "    X  X X   X   X     X   X     X              ",
                "    XXX  X   X   X     X   XXXX  XXXX           ",
                "                                                ",
                "      *              OOO  O   O OOOOO OOOO      ",
                "                    O     O   O   O   O   O     ",
                "                     OOO  OOOOO   O   OOOO      ",
                "             *          O O   O   O   O         ",
                "          *          OOO  O   O OOOOO O         ",
                "  *                                             ",
                "                                           *    ",
                "         LOADING         *                      ",
                "                                               ",
            ],
            [
                "                                        (       ",
                "   XXX    X   XXXXX XXXXX X     XXXX            ",
                "   X  X  X X    X     X   X     X               ",
                "   XXX  X X X   X     X   X     XXX             ",
                "   X  X X   X   X     X   X     X         *     ",
                "   XXX  X   X   X     X   XXXX  XXXX            ",
                "    *                                           ",
                "                  *   OOO  O   O OOOOO OOOO     ",
                "                     O     O   O   O   O   O    ",
                "         *            OOO  OOOOO   O   OOOO     ",
                "                         O O   O   O   O        ",
                "                      OOO  O   O OOOOO O        ",
                "   *                                        *   ",
                "                                 *              ",
                "          LOADING           *                   ",
                "                                                ",
            ],
            [
                "                                                ",
                "    XXX    X   XXXXX XXXXX X     XXXX       *   ",
                "    X  X  X X    X     X   X     X              ",
                "    XXX  X X X   X     X   X     XXX            ",
                "    X  X X   X   X     X   X     X       *      ",
                "    XXX  X   X   X     X   XXXX  XXXX           ",
                "              *                                 ",
                "                     OOO  O   O OOOOO OOOO      ",
                "                    O     O   O   O   O   O     ",
                "     *               OOO  OOOOO   O   OOOO      ",
                "                        O O   O   O   O       * ",
                "              *      OOO  O   O OOOOO O         ",
                "                                                ",
                "                                                ",
                "           LOADING                 *            ",
                "                                                ",
            ],
            [
                "  *                  *                          ",
                "     XXX    X   XXXXX XXXXX X     XXXX     *    ",
                "     X  X  X X    X     X   X     X             ",
                "     XXX  X X X   X     X   X     XXX           ",
                "     X  X X   X   X     X   X     X             ",
                "     XXX  X   X   X     X   XXXX  XXXX          ",
                "                *                               ",
                "                    OOO  O   O OOOOO OOOO       ",
                "                   O     O   O   O   O   O      ",
                "                    OOO  OOOOO   O   OOOO       ",
                "                       O O   O   O   O          ",
                "        *           OOO  O   O OOOOO O          ",
                "                          *                     ",
                "                                                ",
                "            LOADING                *            ",
                "       *                                        ",
            ],
            [
                "             *                       *          ",
                "    XXX    X   XXXXX XXXXX X     XXXX           ",
                "    X  X  X X    X     X   X     X              ",
                "    XXX  X X X   X     X   X     XXX            ",
                "    X  X X   X   X     X   X     X       *      ",
                "    XXX  X   X   X     X   XXXX  XXXX           ",
                "   *                                            ",
                "                     OOO  O   O OOOOO OOOO      ",
                "              *     O     O   O   O   O   O     ",
                "                     OOO  OOOOO   O   OOOO      ",
                "                        O O   O   O   O         ",
                "                     OOO  O   O OOOOO O         ",
                "     *                                          ",
                "                                  *             ",
                "             LOADING                            ",
                "                        *                       ",
            ]
        ]
        self.explosion = [
            [
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
            ],
            [
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
                "                                                ",
            ],
        ]


if __name__ == '__main__':
    animations = Animations()
    b = Battleship()
    b.main()
