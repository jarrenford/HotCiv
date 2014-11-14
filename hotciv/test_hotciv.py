#!python2
# By: Jarren, Stetson, and Luke
# test_betaciv.py

import unittest
from hotciv import *

class testCiv(unittest.TestCase):

    def setUp(self):
        self.game = HotCiv(AlphaCivFactory)

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
        self.assertEqual(self.game.getAge(), -4000)

    def test_GameAges100YearsEachRound(self):
        g = HotCiv(AlphaCivFactory)
        
        g.endOfRound()
        self.assertEqual(g.getAge(), -3900)
        g.endOfRound()
        self.assertEqual(g.getAge(), -3800)

    def test_RedWinsIn3000BC(self):
        g = HotCiv(AlphaCivFactory)
        
        for i in range(10):
            g.endOfRound()

        self.assertEqual(g.getWinner(), RED)

# Movement Tests----------------------------------------------------------------

    def test_UnitsCantMoveOverMountain(self):
        g = HotCiv(AlphaCivFactory)
        g.endOfTurn()
        
        self.assertEqual(g.moveUnit((3,2), (2,2)), False)

    def test_UnitsCantMoveOverOceans(self):
        g = HotCiv(AlphaCivFactory)

        self.assertEqual(g.moveUnit((2,0), (1,0)), False)
    
    def test_UnitsCantMoveOverCities(self):
        g = HotCiv(AlphaCivFactory)

        self.assertEqual(g.moveUnit((2,0), (1,1)), False)

    def test_UnitsCantMoveTwiceInTurn(self):
        g = HotCiv(AlphaCivFactory)
        g.moveUnit((2,0), (2,1))
        self.assertEqual(g.moveUnit((2,1), (2,0)), False)

    def test_RedMovement(self):
        g = HotCiv(AlphaCivFactory)
        g.moveUnit((2,0), (2,1))
        
        self.assertEqual(g.getUnitAt((2,1)).getOwner(), RED)
        
    def test_BlueMovement(self):
        g = HotCiv(AlphaCivFactory)
        g.endOfTurn()
        g.moveUnit((3,2), (3,3))

        self.assertEqual(g.getUnitAt((3,3)).getOwner(), BLUE)
    
    def test_RedCannotMoveBlueUnits(self):
        g = HotCiv(AlphaCivFactory)
        
        self.assertEqual(g.moveUnit((3,2), (3,3)), False)
    
    def test_BlueCannotMoveRedUnits(self):
        g = HotCiv(AlphaCivFactory)
        g.endOfTurn()
        
        self.assertEqual(g.moveUnit((2,0), (2,1)), False)

    def test_RedAttacksAndDestroysBlue(self):
        g = HotCiv(AlphaCivFactory)

        g.moveUnit((4,3), (3,2))
        self.assertEqual(g.getUnitAt((3,2)).getOwner(), RED)
    
# City Tests--------------------------------------------------------------------

    def test_CityProduces6ProductionAtRoundEnd(self):
        g = HotCiv(AlphaCivFactory)
        city = g.getCityAt((1,1))
        city.changeWorkforceFocus(PRODUCTION)
        g.endOfRound()
        
        self.assertEqual(city.getProductionPoints(), 6)

    def test_CityPopulationSizeIs1(self):
        self.assertEqual(self.game.getCityAt((1,1)).getSize(), 1)

    def test_WorkforceFocus(self):
        g = HotCiv(AlphaCivFactory)

        city = g.getCityAt((1,1))
        city.changeWorkforceFocus(FOOD)
        self.assertEqual(city.getWorkforceFocus(), FOOD)
        city.changeWorkforceFocus(PRODUCTION)
        self.assertEqual(city.getWorkforceFocus(), PRODUCTION)

    def test_ChangeCityProduction(self):
        g = HotCiv(AlphaCivFactory)
        city = g.getCityAt((1,1))
        
        g.changeCityProductionAt((1,1), ARCHER)
        self.assertEqual(city.getProduction(), ARCHER)
        
        g.changeCityProductionAt((1,1), LEGION)
        self.assertEqual(city.getProduction(), LEGION)
        
        g.changeCityProductionAt((1,1), SETTLER)
        self.assertEqual(city.getProduction(), SETTLER)

    def test_UnitPlacementAroundCity(self):
        g = HotCiv(AlphaCivFactory)
        city = g.getCityAt((1,1))
        city.changeWorkforceFocus(PRODUCTION)
        city.changeProduction(ARCHER)
        
        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((1,1)).getOwner(), RED)
        
        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((0,1)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((0,2)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((1,2)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound() # Test invalid placement
        self.assertEqual(g.getUnitAt((2,2)).getOwner(), None)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((2,1)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((2,0)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((1,0)).getOwner(), None)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((0,0)).getOwner(), RED)

        g.endOfRound()
        g.endOfRound()
        self.assertEqual(g.getUnitAt((0,3)).getOwner(), RED)

        # Test invalid placement
        self.assertRaises(TypeError, g.getUnitAt((-1,0)))
        self.assertRaises(TypeError, g.getUnitAt((0,-1)))
        self.assertRaises(TypeError, g.getUnitAt((16,0)))
        self.assertRaises(TypeError, g.getUnitAt((0,16)))


class testBetaCiv(unittest.TestCase):

    def test_Aging(self):
        g = HotCiv(BetaCivFactory)

        self.assertEqual(g.getAge(), -4000)
        
        for i in range(39):
            g.endOfRound()

        self.assertEqual(g.getAge(), -100)

        g.endOfRound()
        self.assertEqual(g.getAge(), -1)

        g.endOfRound()
        self.assertEqual(g.getAge(), 1)

        g.endOfRound()
        self.assertEqual(g.getAge(), 50)

        for i in range(34):
            g.endOfRound()
        self.assertEqual(g.getAge(), 1750)

        for i in range(6):
            g.endOfRound()
        self.assertEqual(g.getAge(), 1900)

        for i in range(14):
            g.endOfRound()
        self.assertEqual(g.getAge(), 1970)

        for i in range(30):
            g.endOfRound()
        self.assertEqual(g.getAge(), 2000)

    def test_Winning(self):
        g = HotCiv(BetaCivFactory)
        g.placeCityAt((4,1), City(RED))
        
        self.assertEqual(g.getWinner(), RED)

class testGammaCiv(unittest.TestCase):
    
    def test_ArcherFortify(self):
        g = HotCiv(GammaCivFactory)

        unit = g.getUnitAt((2,0))
        g.performUnitAction((2,0))
        
        unit = g.getUnitAt((2,0))
        self.assertEqual(unit.getDefense(), 6)

        # Test movement locking
        self.assertFalse(g.moveUnit((2,0),(2,1)))
        self.assertTrue(isinstance(g.getUnitAt((2,1)), noUnit))

        # Unfortify unit
        unit.performAction()
        self.assertEqual(unit.getDefense(), 3)
        
        g.moveUnit((2,0),(2,1))
        self.assertEqual(g.getUnitAt((2,1)).getOwner(), RED)

        

    def test_SettlerBuild(self):
        g = HotCiv(GammaCivFactory)

        unit = g.getUnitAt((4,3))
        g.performUnitAction((4,3))

        unit = g.getUnitAt((4,3))
        self.assertTrue(isinstance(unit, noUnit))

        city = g.getCityAt((4,3))
        self.assertTrue(isinstance(city, City))
        self.assertEqual(city.getOwner(), RED)
        
class testDeltaCiv(unittest.TestCase):

    def testMapFromFile(self):
        g = HotCiv(DeltaCivFactory)

        self.assertEqual(g.getTileAt((0,0)).getTileType(), OCEANS)
        self.assertEqual(g.getTileAt((0,3)).getTileType(), PLAINS)
        self.assertEqual(g.getTileAt((0,5)).getTileType(), MOUNTAINS)
        
        self.assertEqual(g.getTileAt((1,1)).getTileType(), OCEANS)
        self.assertEqual(g.getTileAt((1,3)).getTileType(), HILLS)
        self.assertEqual(g.getTileAt((1,9)).getTileType(), FORESTS)

        self.assertEqual(g.getTileAt((2,0)).getTileType(), OCEANS)
        self.assertEqual(g.getTileAt((2,1)).getTileType(), PLAINS)
        self.assertEqual(g.getTileAt((2,6)).getTileType(), MOUNTAINS)

        self.assertEqual(g.getTileAt((3,0)).getTileType(), OCEANS)
        self.assertEqual(g.getTileAt((3,1)).getTileType(), PLAINS)
        self.assertEqual(g.getTileAt((3,3)).getTileType(), MOUNTAINS)

        self.assertEqual(g.getTileAt((4,0)).getTileType(), OCEANS)
        self.assertEqual(g.getTileAt((4,3)).getTileType(), PLAINS)
        self.assertEqual(g.getCityAt((4,5)).getOwner(), BLUE)
        self.assertEqual(g.getTileAt((4,8)).getTileType(), HILLS)

        self.assertEqual(g.getCityAt((9,12)).getOwner(), RED)

        self.assertEqual(g.getTileAt((15,15)).getTileType(), OCEANS)
        
if __name__ == "__main__":
    unittest.main()
