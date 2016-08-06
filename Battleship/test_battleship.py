import unittest
from battleship import Battleship, Ship

class BattleshipTestCase(unittest.TestCase):
    def test_board_functions(self):
        battleship = Battleship()
        table = ["bat", "puppy", "lcdsoundsystem"]
        normalized_table = battleship.normalize_rows(table, 16)
        self.assertEqual(len(table[0]), 16)
        self.assertEqual(len(table[1]), 16)
        self.assertEqual(len(table[2]), 16)

    def test_other_player(self):
        battleship = Battleship()
        player1 = battleship.players[0]
        player2 = battleship.players[1]
        self.assertEqual(battleship.other_player(player1), player2)
        self.assertEqual(battleship.other_player(player2), player1)

    def test_coordinate_validation(self):
        battleship = Battleship()
        dummy_coords = [
            "A1",
            "A01",
            "A10",
            "J1",
            "J10",
            "J11",
            "W1",
            "W11",
            "&99",
            "&9",
            "A100",
        ]
        self.assertEqual(battleship.validate_coordinate(dummy_coords[0]), True)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[1]), True)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[2]), True)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[3]), True)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[4]), True)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[5]), False)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[6]), False)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[7]), False)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[8]), False)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[9]), False)
        self.assertEqual(battleship.validate_coordinate(dummy_coords[10]), False)

    def test_coordinate_manipulation(self):
        battleship = Battleship()
        coord_set = [
            ["A1", "A2", "A3"],
            ["A3", "A4", "A5"],
            ["A1"],
            ["A10"],
            ["A3"],
            ["D3"],
            ["J5"]
        ]

        #test below
        self.assertEqual(battleship.below_coord(coord_set[0]), "A4")
        self.assertEqual(battleship.below_coord(coord_set[1]), "A6")
        self.assertEqual(battleship.below_coord(coord_set[2]), "A2")

        #test above
        self.assertEqual(battleship.below_coord(coord_set[3]), "A11")
        self.assertEqual(battleship.above_coord(coord_set[0]), "A0")
        self.assertEqual(battleship.above_coord(coord_set[1]), "A2")

        #test right
        self.assertEqual(battleship.right_coord(coord_set[2]), "B1")
        self.assertEqual(battleship.right_coord(coord_set[5]), "E3")
        self.assertEqual(battleship.right_coord(coord_set[6]), None)

        #test left
        self.assertEqual(battleship.left_coord(coord_set[2]), None)
        self.assertEqual(battleship.left_coord(coord_set[5]), "C3")
        self.assertEqual(battleship.left_coord(coord_set[6]), "I5")



    def test_collision_during_setup(self):
        battleship = Battleship()
        player = battleship.players[0]
        player.ships.append(Ship("Ship_1", ["A1", "I10"]))
        player.ships.append(Ship("Ship_2", ["B1", "J10"]))

        self.assertEqual(battleship.collision_check(player, "A1"), "Ship_1")
        self.assertEqual(battleship.collision_check(player, "B1"), "Ship_2")
        self.assertEqual(battleship.collision_check(player, "I10"), "Ship_1")
        self.assertEqual(battleship.collision_check(player, "J10"), "Ship_2")
        self.assertEqual(battleship.collision_check(player, "B6"), False)

    def test_ship_placement(self):
        battleship = Battleship()
        player = battleship.players[0]
        player.ships.append(Ship("Ship_1", ["A1", "B1"]))
        player.ships.append(Ship("Ship_2", ["A8", "B8"]))

        aircraft_carrier = battleship.ship_types[4]
        patrol_boat = battleship.ship_types[0]

        self.assertEqual(battleship.find_ship_coords_or_give_error(player, patrol_boat, "A2", "right"), ["A2", "B2"])
        self.assertEqual(battleship.find_ship_coords_or_give_error(player, aircraft_carrier, "A2", "down"), ["A2", "A3", "A4", "A5", "A6"])
        self.assertEqual(battleship.find_ship_coords_or_give_error(player, patrol_boat, "A1", "right"), "***This overlaps with your Ship_1!***")
        self.assertEqual(battleship.find_ship_coords_or_give_error(player, patrol_boat, "B8", "right"), "***This overlaps with your Ship_2!***")
