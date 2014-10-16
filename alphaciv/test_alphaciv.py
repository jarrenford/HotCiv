#!python2
# By: Jarren, Stetson, and Luke
# test_alphaciv.py

import unittest
from alphaciv import *

class testAlphaCiv(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_RedGoesFirst(self):
        self.assertEqual(self.game.getPlayerInTurn(), RED)

    def test_BlueGoesSecond(self):
        self.game.endOfTurn()
        self.assertEqual(self.game.getPlayerInTurn(), BLUE)

# World Tests-------------------------------------------------------------------
    
    def test_RedCityAt1x1(self):
        self.assertEqual(self.game.getCityAt((1,1)).getOwner(), RED)

    def test_BlueCityAt4x1(self):
        self.assertEqual(self.game.getCityAt((4,1)).getOwner(), BLUE)

    def test_OceanAt1x0(self):
        self.assertEqual(self.game.getTileAt((1,0)).getTileType(), OCEANS)

    def test_HillsAt0x1(self):
        pass

    def test_MountainsAt2x2(self):
        pass

    def test_RedArcherAt2x0(self):
        pass

    def test_BlueLegionAt3x2(self):
        pass

    def test_RedSettlerAt4x3(self):
        pass

    def test_GameStartsAt4000BC(self):
        pass

    def test_GameAges100YearsEachRound(self):
        pass

    def test_RedWinsIn3000BC(self):
        pass

# Movement Tests----------------------------------------------------------------

    def test_unitsCantMoveOverMountain(self):
        pass

    def test_redCannotMoveBlueUnits(self):
        pass

# City Tests--------------------------------------------------------------------

    def test_CityProduces6ProductionAtRoundEnd(self):
        pass

    def test_CityPopulationSizeIs1(self):
        pass

    def test_RedAttacksAndDestroysBlue(self):
        pass

    def test_UnitPlacementIfCityIsVacant(self):
        pass

    def test_UnitPlacementIfCityIsOccupied(self):
        # Unit will go to the tile due north.
        pass

    def test_UnitPlacementIfCityAndNorthIsOccupied(self):
        # Unit will go clockwise to find an open tile.
        pass
    
    


unittest.main()
