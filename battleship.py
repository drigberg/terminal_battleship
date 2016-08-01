import re
from random import randint

#set global variables -- needs namespace
coord_pattern = re.compile('\w\d')
col_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
encouraging_statements = [
    'Excellent!',
    'Wow!',
    'Muy bueno!!',
    'Hai il tocco d\'oro!',
    'Well, wouldja look\'t that!',
    'Hot damn!',
]

class Player(object):
    """Player object -- initializes with blank board"""
    def __init__(self, string):
        self.name = string
        self.board = {}
        self.ships = []
        for col in col_headers:
            self.board[col] = {}
            for row in range(1, 11):
                self.board[col][row] = "_"

class Ship(object):
    """Ship object -- initializes with occupied coordinates"""
    def __init__(self, name, coord, length):
        self.name = name
        self.coords = []
        for col in col_headers:
            self.board[col] = {}
            for row in range(1, 11):
                self.board[col][row] = "_"

def main():
    ready = raw_input('Ready to play? (y/n) ')
    if ready == 'y':
        game_setup()
    elif ready == 'n':
        print 'Oh. Fine, then.'
    else:
        print 'that wasn\'t even an option. you lose.'

def game_setup():
    """Establishes human and basic AI"""
    players = (
        Player("human"),
        Player("computer"),
    )

    ships = [
        {'name' : 'battleship', 'length': 4},
        {'name' : 'cruiser', 'length': 3},
        {'name' : 'sub', 'length': 3},
        {'name' : 'aircraft_carrier', 'length': 5},
        {'name' : 'patrol_boat', 'length': 2},
    ]

    for player in players:
        # for ship in ships:
        #     place_ship(player, ship)
        print "\n\n******* %s *******" % player.name
        printBoard(player.board)

def printBoard(board):
    """Prints gameboard with left and right borders"""
    for col, row_dict in board.items():
        row = []
        for n in range(0, 12):
            if n != 0 and n != 11:
                row.append(board[col][n])
            else:
                row.append('|')
        print "".join(row)

def place_ship(player, ship):
    """Retrieves starting coordinate and direction, verifies validity, passes occupied coordinates to new ship object"""
    while ship != "PLACED":
        if player.name == 'human':
            start_coord = raw_input("Patrol ship coordinate closest to A1? ")
            direction = raw_input("Ship's direction from starting coordinate? (right/down)")
        else:
            #if computer player, randomly places ship
            start_coord = "".join([col_headers[randint(0, 9)], str(randint(1, 10))])

        if validate_coordinate_and_direction(ship, start_coord, direction):
            new_ship = Ship(ship['name'], coord, ship['length'])
            player.ships.append(new_ship)
            ship = "PLACED"
            print encouraging_statements[randint(0, len(encouraging_statements)-1)]
        else:
            ship = ""

def validate_coordinate_and_direction(ship, start_coord, direction):
    if coord_pattern.match(start_coord):
        if direction == 'right':
            if
        elif direction == 'down':
            for n in range(int(start_coord[1:]), int(start_coord[1:]) + )
                if n <= 10:
                    coord = "".join([start_coord[0], str(n)])


    return False




if __name__ == '__main__':
    main()
