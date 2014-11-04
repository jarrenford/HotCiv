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
        self.assertEqual(self.game.getTileAt((0,1)).getTileType(), HILLS)

    def test_MountainsAt2x2(self):
        self.assertEqual(self.game.getTileAt((2,2)).getTileType(), MOUNTAINS)

    def test_RedArcherAt2x0(self):
        unit = self.game.getUnitAt((2,0))

        self.assertEqual(unit.getUnitType(), ARCHER)
        self.assertEqual(unit.getOwner(), RED)

    def test_BlueLegionAt3x2(self):
        unit = self.game.getUnitAt((3,2))

        self.assertEqual(unit.getUnitType(), LEGION)
        self.assertEqual(unit.getOwner(), BLUE)
    
    def test_RedSettlerAt4x3(self):
        unit = self.game.getUnitAt((4,3))

        self.assertEqual(unit.getUnitType(), SETTLER)
        self.assertEqual(unit.getOwner(), RED)

    def test_GameStartsAt4000BC(self):
        self.assertEqual(self.game.getAge(), 4000)

    def test_GameAges100YearsEachRound(self):
        g = Game()
        
        g.endOfRound()
        self.assertEqual(g.getAge(), 3900)
        g.endOfRound()
        self.assertEqual(g.getAge(), 3800)

    def test_RedWinsIn3000BC(self):
        g = Game()
        
        for i in range(10):
            g.endOfRound()

        self.assertEqual(g.getWinner(), RED)

# Movement Tests----------------------------------------------------------------

    def test_UnitsCantMoveOverMountain(self):
        g = Game()
        g.endOfTurn()
        
        self.assertEqual(g.moveUnit((3,2), (2,2)), False)

    def test_UnitsCantMoveOverOceans(self):
        g = Game()

        self.assertEqual(g.moveUnit((2,0), (1,0)), False)
    
    def test_UnitsCantMoveOverCities(self):
        g = Game()

        self.assertEqual(g.moveUnit((2,0), (1,1)), False)

    def test_UnitsCantMoveTwiceInTurn(self):
        g = Game()
        g.moveUnit((2,0), (2,1))
        self.assertEqual(g.moveUnit((2,1), (2,0)), False)

    def test_RedMovement(self):
        g = Game()
        g.moveUnit((2,0), (2,1))
        
        self.assertEqual(g.getUnitAt((2,1)).getOwner(), RED)
        
    def test_BlueMovement(self):
        g = Game()
        g.endOfTurn()
        g.moveUnit((3,2), (3,3))

        self.assertEqual(g.getUnitAt((3,3)).getOwner(), BLUE)
    
    def test_RedCannotMoveBlueUnits(self):
        g = Game()
        
        self.assertEqual(g.moveUnit((3,2), (3,3)), False)
    
    def test_BlueCannotMoveRedUnits(self):
        g = Game()
        g.endOfTurn()
        
        self.assertEqual(g.moveUnit((2,0), (2,1)), False)

    def test_RedAttacksAndDestroysBlue(self):
        g = Game()

        g.moveUnit((4,3), (3,2))
        self.assertEqual(g.getUnitAt((3,2)).getOwner(), RED)
        
    
# City Tests--------------------------------------------------------------------

    def test_CityProduces6ProductionAtRoundEnd(self):
        g = Game()
        city = g.getCityAt((1,1))
        city.changeWorkforceFocus(PRODUCTION)
        g.endOfRound()
        
        self.assertEqual(city.getProductionPoints(), 6)

    def test_CityPopulationSizeIs1(self):
        self.assertEqual(self.game.getCityAt((1,1)).getSize(), 1)

    def test_WorkforceFocus(self):
        g = Game()

        city = g.getCityAt((1,1))
        city.changeWorkforceFocus(FOOD)
        self.assertEqual(city.getWorkforceFocus(), FOOD)
        city.changeWorkforceFocus(PRODUCTION)
        self.assertEqual(city.getWorkforceFocus(), PRODUCTION)

    def test_ChangeCityProduction(self):
        g = Game()
        city = g.getCityAt((1,1))
        
        g.changeCityProductionAt((1,1), ARCHER)
        self.assertEqual(city.getProduction().getUnitType(), ARCHER)
        
        g.changeCityProductionAt((1,1), LEGION)
        self.assertEqual(city.getProduction().getUnitType(), LEGION)
        
        g.changeCityProductionAt((1,1), SETTLER)
        self.assertEqual(city.getProduction().getUnitType(), SETTLER)

    def test_UnitPlacementAroundCity(self):
        # Unit will go to the tile due north.

        for unit in [ARCHER, LEGION, SETTLER]:
            g = Game()
            city = g.getCityAt((1,1))
            city.changeWorkforceFocus(PRODUCTION)
            city.changeProduction(unit)

            # List of valid tiles to place at
            coords = [(1,1),(0,1),(0,2),(1,2),(2,1),(0,0),(0,3),
                      (1,3),(2,3),(3,3),(3,1),(3,0),(0,4),(1,4),
                      (2,4),(3,4),(4,4),(4,2),(4,0),(0,5),(1,5),
                      (2,5),(3,5),(4,5),(5,5),(5,4),(5,3),(5,2),
                      (5,1),(5,0)]

            # Test placement at valid tiles
            for pos in coords:
                g.endOfRound()
                g.endOfRound()
                
                if unit == LEGION:
                    g.endOfRound()
                    
                if unit == SETTLER:
                    g.endOfRound()
                    g.endOfRound()
                    g.endOfRound()

                self.assertEqual(g.getUnitAt(pos).getOwner(), RED)

            # Test placement at non-placable tiles
            for pos in [(1,0),(2,2)]:
                self.assertEqual(g.getUnitAt(pos), False)

            # Test for unit replacement
            self.assertEqual(g.getUnitAt((3,2)).getOwner(), BLUE)

            # Test placement outside of board
            self.assertEqual(g.getUnitAt((-1,0)), False)
            self.assertEqual(g.getUnitAt((0,-1)), False)
            self.assertEqual(g.getUnitAt((17,0)), False)
            self.assertEqual(g.getUnitAt((0,17)), False)

            for pos in [(-1,0),(0,-1),(17,0),(0,17)]:
                self.assertEqual(g.getUnitAt(pos), False)


        
unittest.main()
