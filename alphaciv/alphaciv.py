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
        self._hasMoved = []
        
        self._board = [[Tile(PLAINS), None, None]]*256
        self._board[17] = [Tile(PLAINS), None, City(RED)]
        self._board[65] = [Tile(PLAINS), None, City(BLUE)]
        self._board[16] = [Tile(OCEANS), None, None]
        self._board[1] = [Tile(HILLS), None, None]
        self._board[34] = [Tile(MOUNTAINS), None, None]
        
        self._board[32] = [Tile(PLAINS), Unit(RED,ARCHER), None]
        self._board[50] = [Tile(PLAINS), Unit(BLUE,LEGION), None]
        self._board[67] = [Tile(PLAINS), Unit(RED,SETTLER), None]
    
    def getTileAt(self, pos):
        tile = self._board[self._posToIndex(pos)][0]
        
        if tile.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS]:
            return tile
        else:
            return -1
    
    def getUnitAt(self, pos):
        unit = self._board[self._posToIndex(pos)][1]

        if unit == None or self.getCityAt(pos) != -1:
            return -1

        return unit
    
    def getCityAt(self, pos):
        city = self._board[self._posToIndex(pos)][2]
        
        if city == None:
            return -1
        
        return city
    
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

        self._hasMoved.append(posTo)
    
    def endOfTurn(self):
        self._turnCount += 1
        
        if self._turnCount % 2 == 0:
            self._turn = RED
        else:
            self._turn = BLUE

        self._hasMoved = []

    def endOfRound(self):
        self._age -= 100

        for square in self._board:
            city = square[2]
            
            if city != None:
                city.nextRoundPrep()
        
    def changeCityWorkforceAt(self, pos, focus):
        pass

    def changeCityProductionUnitAt(self, pos, unit):
        city = self.getCityAt(pos)
        city.changeProductionUnit(unit)

    def _isMoveValid(self, posFrom, posTo):
        unit = self.getUnitAt(posFrom)
        mCount = unit.getMoveCount()
        toTile = self.getTileAt(posTo)

        if self.getCityAt(posTo) != -1:
            return False
        
        if posFrom in self._hasMoved:
            return False

        if unit.getOwner() != self.getPlayerInTurn():
            return False
        
        if toTile.isPassable() == False:
            return False
               
        if self.getUnitAt(posTo) != -1:
            if self.getUnitAt(posTo).getOwner() == self.getPlayerInTurn():
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
        self._tileType = tileType
        self._food = {PLAINS:3, OCEANS:1, HILLS:0,
                      MOUNTAINS:0, FORESTS:0}[tileType]
    
    def isPassable(self):
        if self._tileType in [MOUNTAINS, OCEANS]:
            return False
        
        return True

    def isBuildable(self):
        if self._tile == PLAINS:
            return True
        
        return False

    def getFood(self):
        return self._food

    def getTileType(self):
        return self._tileType

    def getProduction(self):
        return self._production

# --------------------------------------------------------
class City():

    def __init__(self, owner):
        self._size = 1
        self._owner = owner
        self._workforceFocus = None
        self._food = 0
        self._productionUnit = None
        self._productionPoints = 0
        
    def getSize(self):
        return self._size

    def getOwner(self):
        return self._owner

    def getWorkforceFocus(self):
        return self._workforceFocus

    def changeWorkforceFocus(self, focus):
        if focus in [PRODUCTION, FOOD]:
            self._workforceFocus = focus
        else:
            return -1

    def getProductionPoints(self):
        return self._productionPoints
    
    def getProductionUnit(self):
        return self._productionUnit

    def changeProductionUnit(self, unit):
        if unit in [ARCHER, LEGION, SETTLER]:
            self._productionUnit = unit
        else:
            return -1

    def getFood(self):
        return self._food
    
    def nextRoundPrep(self):
        if self._workforceFocus == PRODUCTION:
            self._productionPoints += 6
        

# --------------------------------------------------------
