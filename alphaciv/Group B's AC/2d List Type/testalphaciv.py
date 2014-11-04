#testalphaciv.py
#Team B
#Bob, Alex, Nick, Zhongyang

from alphaciv import *
from gameconstants import *
import unittest

class TestAlphaCiv (unittest.TestCase):


    def cycleRound(self):
        """
        Make the game go through a complete round where both players take a turn.
        """
        self.game.endOfTurn()
        self.game.endOfTurn()

    def age1000Years(self):
        """
        Make the game age 1000 years
        """
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()
        self.cycleRound()

    def setUp(self):
        self.game = Game()
    
    def test_redIsFirstInTurn(self):
        """
        Make sure red player gets first turn
        """
        self.assertEquals(RED, self.game.getPlayerInTurn(), "Red should get first turn.")

    def test_redCityAt11(self):
        """
        Make sure red city starts at 1,1 at game initialization
        """
        self.assertEquals(RED,self.game.getCityAt((1,1)).getOwner(), "Red should have a city at 1,1")

    def test_blueCityAt41(self):
        """
        Make sure a blue city is at 4,1 at game initialization
        """
        self.assertEquals(BLUE,self.game.getCityAt((4,1)).getOwner(), "Blue should have a city at 4,1")

    def test_oceanAt10(self):
        """
        Make sure there is an ocean at 1,0 at game initialization
        """
        self.assertEquals(OCEAN, self.game.getTileAt((1,0)).getTypeString(), "Ocean should be at 1,0")

    def test_cityPopulationAt1(self):
        """
        Make sure the cities' populations are set to 1
        """
        self.assertEquals(1, self.game.getCityAt((1,1)).getSize(), "City population should be 1")
        self.assertEquals(1, self.game.getCityAt((4,1)).getSize(), "City population should be 1")

    def test_afterRedItIsBlueTurn(self):
        """
        Make sure blue gets a turn after red
        """
        self.game.endOfTurn()
        self.assertEquals(BLUE,self.game.getPlayerInTurn(),"Blue should have a turn after red")


    def test_redArcherAt20(self):
        """
        Make sure red archer is at 2,0 at game initialization
        """
        self.assertEquals(ARCHER, self.game.getUnitAt((2,0)).getTypeString(), "There should be an archer at 2,0")
        self.assertEquals(RED, self.game.getUnitAt((2,0)).getOwner(), "The archer at 2,0 should be red's")

    def test_blueLegionAt32(self):
        """
        Make sure blue legion is at 3,2 at game initialization
        """
        self.assertEquals(LEGION, self.game.getUnitAt((3,2)).getTypeString(), "There should be a legion at 3,2")
        self.assertEquals(BLUE, self.game.getUnitAt((3,2)).getOwner(), "The legion at 3,2 should be blue's")

    def test_redSettlerAt43(self):
        """
        Make sure red settler is at 4,3 at game initialization
        """
        self.assertEquals(SETTLER, self.game.getUnitAt((4,3)).getTypeString(), "There should be a settler at 4,3")
        self.assertEquals(RED, self.game.getUnitAt((4,3)).getOwner(), "The settler at 4,3 should be red's")

    def test_hillsAt01(self):
        """
        Make sure there is a hills at 0,1 at game initialization
        """
        self.assertEquals(HILLS, self.game.getTileAt((0,1)).getTypeString(), "Hills should be at 0,1")

    def test_mountainAt22(self):
        """
        Make sure there is a mountain at 2,2 at game initialization
        """
        self.assertEquals(MOUNTAIN, self.game.getTileAt((2,2)).getTypeString(), "Mountain should be at 2,2")

    def test_plainsFillOutBoard(self):
        """
        Make sure there are plains filling in tiles where the mountains, oceans, and hills are at game initialization
        """
        self.assertEquals(PLAINS, self.game.getTileAt((7,8)).getTypeString(), "Plains should be at 7,8")
        self.assertEquals(PLAINS, self.game.getTileAt((1,11)).getTypeString(), "Plains should be at 1,11")
        self.assertEquals(PLAINS, self.game.getTileAt((0,0)).getTypeString(), "Plains should be at 0,0")
        self.assertEquals(PLAINS, self.game.getTileAt((15,15)).getTypeString(), "Plains should be at 15,15")
        self.assertEquals(PLAINS, self.game.getTileAt((4,4)).getTypeString(), "Plains should be at 4,5")

    def test_noneCitiesFillOutBoard(self):
        """
        Make sure NONE cities fill out the board where the red and blue cities are not at game initialization
        """
        self.assertEquals(NONE, self.game.getCityAt((7,8)).getOwner(), "No city should be at 7,8")
        self.assertEquals(NONE, self.game.getCityAt((1,11)).getOwner(), "No city should be at 1,11")
        self.assertEquals(NONE, self.game.getCityAt((0,0)).getOwner(), "No city should be at 0,0")
        self.assertEquals(NONE, self.game.getCityAt((15,15)).getOwner(), "No city should be at 15,15")
        self.assertEquals(NONE, self.game.getCityAt((4,4)).getOwner(), "No city should be at 4,5")

    def test_noneUnitsFillOutBoard(self):
        """
        Make sure NONE units fill out the board where the red and blue units are not at game initialization
        """
        self.assertEquals(NONE, self.game.getUnitAt((7,8)).getTypeString(), "No unit should be at 7,8")
        self.assertEquals(NONE, self.game.getUnitAt((1,11)).getTypeString(), "No unit should be at 1,11")
        self.assertEquals(NONE, self.game.getUnitAt((0,0)).getTypeString(), "No unit should be at 0,0")
        self.assertEquals(NONE, self.game.getUnitAt((15,15)).getTypeString(), "No unit should be at 15,15")
        self.assertEquals(NONE, self.game.getUnitAt((4,4)).getTypeString(), "No unit should be at 4,5")

    def test_endOfRoundAge100Years(self):
        """
        Make sure the end of round ages the world 100 years
        """
        self.cycleRound()
        self.assertEquals(-3900, self.game.getAge(), "The age should be 3900 BC after one round")

    def test_redWinsAt3000BC(self):
        """
        Make sure the red player wins at 3000 BC
        """
        self.age1000Years()
        self.assertEquals(RED, self.game.getWinner(), "Red should win in 3000 BC")

    def test_moveUnits(self):
        """
        Make sure units game be moved, double check previous space and space moved to to make sure correct units are in each
        """
        self.assertTrue(self.game.moveUnit((4,3),(5,4)))
        self.assertEquals(SETTLER, self.game.getUnitAt((5,4)).getTypeString(), "There should be a settler at 5,4")
        self.assertEquals(NONE, self.game.getUnitAt((4,3)).getTypeString(), "There should be no unit at 4,3")

        self.game.endOfTurn()
        
        self.assertTrue(self.game.moveUnit((3,2),(3,3)))
        self.assertEquals(LEGION, self.game.getUnitAt((3,3)).getTypeString(), "There should be a legion at 3,3")
        self.assertEquals(NONE, self.game.getUnitAt((3,2)).getTypeString(), "There should be no unit at 3,2")

    def test_moveResetAtEndOfRound(self):
        """
        Make sure the move count resets for units at the end of each round
        """
        self.game.moveUnit((4,3),(5,4))
        self.assertEquals(0, self.game.getUnitAt((5,4)).getMoveCount(), "After the movement, the settler should have 0 moves left")
        self.cycleRound()
        self.assertEquals(1, self.game.getUnitAt((5,4)).getMoveCount(), "After the round, the settler should have 1 moves left")

    def test_oneUnitOnATileAtSameTime(self):
        """
        Make sure that units owned by the same player cannot be on the same tile at the same time
        """
        self.game.moveUnit((4,3),(5,2))
        self.game.moveUnit((2,0),(3,0))
        self.cycleRound()

        self.game.moveUnit((5,2),(5,1))
        self.game.moveUnit((3,0),(4,0))
        self.cycleRound()

        self.game.moveUnit((5,1),(5,0))
        self.game.moveUnit((4,0),(5,0))
        self.assertEquals(ARCHER, self.game.getUnitAt((4,0)).getTypeString(), "The archer should not have been able to move on the settler")
        self.assertEquals(SETTLER, self.game.getUnitAt((5,0)).getTypeString(), "The settler should not have been moved on by the archer")

    def test_blueAttackerAlwaysWins(self):
        """
        Make sure a blue attacking unit always wins
        """
        self.game.endOfTurn()
        self.game.moveUnit((3,2),(4,3))
        self.assertEquals(LEGION, self.game.getUnitAt((4,3)).getTypeString(), "The legion attacking should have defeated the defending settler")

    def test_redAttackerAlwaysWins(self):
        """
        Make sure a red attacking unit always wins
        """
        self.game.moveUnit((4,3),(3,2))
        self.assertEquals(SETTLER, self.game.getUnitAt((3,2)).getTypeString(), "The settler attacking should have defeated the defending legion")

    def test_unitsCantMoveOverMountain(self):
        """
        Make sure units cannot move onto mountains
        """
        self.game.endOfTurn()
        self.assertFalse(self.game.moveUnit((3,2),(2,2)))
        self.assertEquals(LEGION, self.game.getUnitAt((3,2)).getTypeString(), "The legion should not have been able to move on the mountain")

    def test_unitsCantMoveOverOcean(self):
        """
        Make sure units cannot move onto oceans
        """
        self.assertFalse(self.game.moveUnit((2,0),(1,0)))
        self.assertEquals(ARCHER, self.game.getUnitAt((2,0)).getTypeString(), "The archer should not have been able to move on the ocean")

    def test_playersCantMoveOtherPlayersUnits(self):
        """
        Make sure players cannot move other players' units
        """
        self.assertEquals(RED, self.game.getPlayerInTurn(), "It should be red's turn")
        self.assertFalse(self.game.moveUnit((3,2),(4,2)))
        self.assertEquals(LEGION, self.game.getUnitAt((3,2)).getTypeString(), "Red cannot move blue's units")
        self.assertTrue(self.game.moveUnit((4,3),(5,4)))
        self.assertEquals(SETTLER, self.game.getUnitAt((5,4)).getTypeString(), "Red can move its own units")
        
        self.game.endOfTurn()
        
        self.assertEquals(BLUE, self.game.getPlayerInTurn(), "It should be blue's turn")
        self.assertTrue(self.game.moveUnit((3,2),(4,2)))
        self.assertEquals(LEGION, self.game.getUnitAt((4,2)).getTypeString(), "Blue can move blue's units")
        self.assertFalse(self.game.moveUnit((5,4),(4,3)))
        self.assertEquals(SETTLER, self.game.getUnitAt((5,4)).getTypeString(), "Blue cannot move red's units")

    def test_movingOntoOpponentCityChangesOwner(self):
        """
        Make sure a unit moving onto an unoccupied (by units) opponent city changes the ownernship of the city
        """
        self.game.moveUnit((4,3),(3,2))
        self.cycleRound()
        self.game.moveUnit((3,2),(4,1))
        self.assertEquals(RED, self.game.getCityAt((4,1)).getOwner(), "Owner of the city at 4,1 should have gone from blue to red")
        

    def test_changeProductionType(self):
        """
        Make sure a city can have its production type changed
        """
        self.game.changeProductionInCityAt((1,1), ARCHER)
        self.assertEquals(ARCHER, self.game.getCityAt((1,1)).getProduction(), "Red should be producing archers")

    def test_produceUnits(self):
        """
        Make sure units can be produced
        """
        self.cycleRound()
        self.game.changeProductionInCityAt((1,1),ARCHER)
        self.assertEquals(NONE, self.game.getUnitAt((1,1)).getTypeString(),"There should be no unit on the city initially")
        self.cycleRound()
        self.assertEquals(ARCHER, self.game.getUnitAt((1,1)).getTypeString(),"There should be an archer on the city after getting enough production")
        self.cycleRound()
        self.cycleRound()
        self.assertEquals(ARCHER, self.game.getUnitAt((0,1)).getTypeString(),"There should be an archer on the city after getting enough production")

    def test_produceUnitsWithinGameConstraints(self):
        """
        Make sure all production constraints pass:
        1)Units cannot be produced on mountains or oceans
        2)Units cannot be produced on another unit of the same player
        3)Units produce by the algorithm of first check the city tile, then the tile directly north, followed by a clockwise spiral about the city
        4)Units produced on opponent units defeat the unit previously on the tile
        5)Units produced by one player on an opponents' city take over the city
        6)Units produced will not create a new city
        7)When all legal tiles are filled by one player's units, no more units produce on the board
        """
        self.game.changeProductionInCityAt((1,1),LEGION)
        
        self.age1000Years()
        self.age1000Years()
        self.age1000Years()
        self.age1000Years()
        self.age1000Years()
        
        self.assertEquals(NONE, self.game.getUnitAt((2,2)).getTypeString(), "Mountain should be at 2,2 / no unit")
        self.assertEquals(NONE, self.game.getUnitAt((1,0)).getTypeString(), "Ocean should be at 1,0 / no unit")
        self.assertEquals(ARCHER, self.game.getUnitAt((2,0)).getTypeString(), "There should be an archer at 2,0")
        self.assertEquals(NONE, self.game.getUnitAt((4,0)).getTypeString(), "Last unit placed should be at 4,4. Nothing on 4,0")
        self.assertEquals(LEGION, self.game.getUnitAt((4,1)).getTypeString(), "Unit should be on 4,1")
        self.assertEquals(SETTLER, self.game.getUnitAt((4,3)).getTypeString(), "Red settler should be at 4,3")
        self.assertEquals(RED, self.game.getUnitAt((3,2)).getOwner(),"Red legion should have defeated blue legion when placed")
        self.assertEquals(LEGION, self.game.getUnitAt((4,1)).getTypeString(), "Red legion should have been produced even on blue city")
        self.assertEquals(RED, self.game.getCityAt((4,1)).getOwner(), "Owner of the city at 4,1 should have gone from blue to red") 
        self.assertEquals(NONE,self.game.getCityAt((4,2)).getOwner(),"There should still be no city at 4,2")
        
        for ageQuick in range (0, 60):
            #Populate the board completely with red legions
            self.age1000Years()

        self.assertEquals(LEGION, self.game.getUnitAt((15,0)).getTypeString(), "Red legions should have filled the board in all open spaces with the last space being 15,0")

        
      
if __name__=='__main__':
    unittest.main()
