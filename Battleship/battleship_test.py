import unittest
from battleship import Battleship

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
