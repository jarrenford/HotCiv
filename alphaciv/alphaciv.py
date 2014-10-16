#!python2
# By: Jarren, Stetson, and Luke
# alphaciv.py

# Player implementation, since a class makes no
# pythonic sense.

from __future__ import print_function
from constants import *


class Game:
    def __init__(self):
        # Stores the board: a list containing tuples (tile, unit/city)
        self._turnCount = 1
        self._turn = RED
        self._age = 4000
        
        self._board = [(None, None)]*256
        self._board[17] = (City(RED), None)
        self._board[65] = (City(BLUE), None)
        self._board[16] = (Tile(OCEANS), None)
    
    def getTileAt(self, pos):
        obj = self._board[self._posToIndex(pos)][0]
        
        if obj.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS]:
            return obj
        else:
            return -1
    
    def getUnitAt(self, pos):
        obj = self._board[self._posToIndex(pos)][0]
        
        if obj.getTileType() in [ARCHER, LEGION, SETTLER]:
            return obj
        else:
            return -1
    
    def getCityAt(self, pos):
        obj = self._board[self._posToIndex(pos)][0]
        
        if obj.getTileType() == CITY:
            return obj
        else:
            return -1
    
    def getPlayerInTurn(self):
        return self._turn
    
    def getWinner(self):
        return RED
    
    def getAge(self):
        return self._age
    
    def moveUnit(self, posFrom, posTo):
        pass

    def endOfTurn(self):
        self._turnCount += 1
        
        if self._turnCount % 2 == 0:
            self._turn = BLUE
        else:
            self._turn = RED

        # Add endOfRound() function in future version
        self._age -= 50

    def changeCityWorkforceAt(self, pos, balance):
        pass

    def changeCityProductionAt(self, pos, produce):
        pass

    def _posToIndex(self, pos):
        row, col = pos
        return (row * 16) + col
# --------------------------------------------------------
class Unit:
    
    def __init__(self):
        # Container class with general unit commands.
        pass

    def getType(self):
        pass

    def getAttackingStrength(self):
        pass

    def getDefenseStrength(self):
        pass

    def getMoveCount(self):
        pass

# --------------------------------------------------------
class Tile:

    def __init__(self, tileType):
        self._production = None
        self._tileType = tileType

    def isPassable(self):
        pass

    def isBuildable(self):
        # Cannot build on this space, i.e. mountains, cities, and oceans.
        # Pretty much identical to isPassable, except prohibits building on
        # existing cities
        pass

    def getFood(self):
        pass

    def getTileType(self):
        return self._tileType

    def getProduction(self):
        return self._production

# --------------------------------------------------------
class City(Tile):

    def __init__(self, owner):
        self._owner = owner

    def getSize(self):
        pass

    def getOwner(self):
        return self._owner

    def getWorkforceFocus(self):
        pass

# --------------------------------------------------------
