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
        self._turnCount = 0
        self._turn = RED
        self._age = 4000
        
        self._board = [[Tile(PLAINS), None]]*256
        self._board[17] = [City(RED), None]
        self._board[65] = [City(BLUE), None]
        self._board[16] = [Tile(OCEANS), None]
        self._board[1] = [Tile(HILLS), None]
        self._board[34] = [Tile(MOUNTAINS), None]
        
        self._board[32] = [Tile(PLAINS), Unit(RED,ARCHER)]
        self._board[50] = [Tile(PLAINS), Unit(BLUE,LEGION)]
        self._board[67] = [Tile(PLAINS), Unit(RED,SETTLER)]
    
    def getTileAt(self, pos):
        obj = self._board[self._posToIndex(pos)][0]
        
        if obj.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS]:
            return obj
        else:
            return -1
    
    def getUnitAt(self, pos):
        unit = self._board[self._posToIndex(pos)][1]

        if unit == None:
            return -1

        return unit
    
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
        unit = self.getUnitAt(posFrom)
        
        if not self._isMoveValid(posFrom, posTo):
            return False
        
        self._board[self._posToIndex(posFrom)][1] = None
        self._board[self._posToIndex(posTo)][1] = unit

    
    def endOfTurn(self):
        self._turnCount += 1
        
        if self._turnCount % 2 == 0:
            self._turn = RED
        else:
            self._turn = BLUE

        # Add endOfRound() function in future version
        self._age -= 50

    def changeCityWorkforceAt(self, pos, balance):
        pass

    def changeCityProductionAt(self, pos, produce):
        pass

    def _isMoveValid(self, posFrom, posTo):
        unit = self.getUnitAt(posFrom)
        mCount = unit.getMoveCount()
        toTile = self.getTileAt(posTo)

        if unit.getOwner() != self.getPlayerInTurn():
            return False
        
        if toTile.isPassable() == False:
            return False
               
        if self.getUnitAt(posTo) != -1:
            return False

        if any([abs(posFrom[0]-posTo[0]) > mCount,
                abs(posFrom[1]-posTo[1] > mCount)]):
            return False

        return True
    
    def _posToIndex(self, pos):
        row, col = pos
        return (row * 16) + col
# --------------------------------------------------------
class Unit:
    
    def __init__(self, owner, unitType):
        # Container class with general unit commands.
        self._type = unitType
        self._owner = owner
        self._moveCount = 1

    def getOwner(self):
        return self._owner
    
    def getUnitType(self):
        return self._type

    def getAttackingStrength(self):
        pass

    def getDefenseStrength(self):
        pass

    def getMoveCount(self):
        return self._moveCount

# --------------------------------------------------------
class Tile:

    def __init__(self, tileType):
        self._production = None
        self._tileType = tileType

    def isPassable(self):
        if self._tileType in [MOUNTAINS, OCEANS, CITY]:
            return False
        
        return True

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
        self._production = None
        self._tileType = CITY
        self._owner = owner

    def getSize(self):
        pass

    def getOwner(self):
        return self._owner

    def getWorkforceFocus(self):
        pass

# --------------------------------------------------------
