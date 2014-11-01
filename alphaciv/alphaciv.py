#!python2
# By: Jarren, Stetson, and Luke
# alphaciv.py

from __future__ import print_function
from constants import *


class Game:
    def __init__(self):
        """A Game object manages a game of AlphaCiv, storing the board
        and its related commands."""
        
        self._turnCount = 0
        self._turn = RED
        self._age = 4000
        self._hasMoved = []

        # Stores the board: a list containing tuples (tile, unit, city)
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
        """Return the tile object at 'pos' (row,col) on the board"""
        tile = self._board[self._posToIndex(pos)][0]
        
        if tile.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS]:
            return tile
        else:
            return -1
    
    def getUnitAt(self, pos):
        """Return the unit object located at 'pos' (row,col) on the board"""
        row,col = pos

        if -1 >= row >= MAXRADIUS or -1 >= col >= MAXRADIUS:
            return -1
        
        unit = self._board[self._posToIndex(pos)][1]
        
        if unit == None:
            return -1
        
        return unit
    
    def getCityAt(self, pos):
        """Return the city object located at 'pos' (row,col) on the board"""
        city = self._board[self._posToIndex(pos)][2]
        
        if city == None:
            return -1
        
        return city

    def getPlayerInTurn(self):
        """Returns the player currently in turn"""
        return self._turn
    
    def getWinner(self):
        """Returns the game winner"""
        return RED
    
    def getAge(self):
        """Returns the current age"""
        return self._age
    
    def moveUnit(self, posFrom, posTo):
        """Moves a unit from 'posFrom' (row,col) to 'posTo' (row,col)"""
        unit = self.getUnitAt(posFrom)
        
        if not self._isMoveValid(posFrom, posTo):
            return False

        self._board[self._posToIndex(posFrom)][1] = None
        self._board[self._posToIndex(posTo)][1] = unit

        self._hasMoved.append(posTo)
    
    def endOfTurn(self):
        """Handles events at end of player's turn"""
        self._turnCount += 1
        
        if self._turnCount % 2 == 0:
            self._turn = RED
        else:
            self._turn = BLUE

        self._hasMoved = []

    def endOfRound(self):
        """Handles end-of-round events after each round"""
        self._age -= 100

        for index, square in enumerate(self._board):
            city = square[2]
            
            if city != None:
                city._nextRoundPrep(index)
                
                if city.getProduction() != None:
                    if city.getProduction().getUnitType() == ARCHER and city.getProductionPoints() >= 10:
                        city._changeProductionPoints(ARCHER)
                        self._placeUnitsInSpiral(Unit(city.getOwner(), ARCHER), index)

                    if city.getProduction().getUnitType() == LEGION and city.getProductionPoints() >= 15:
                        city._changeProductionPoints(LEGION)
                        self._placeUnitsInSpiral(Unit(city.getOwner(), LEGION), index)

                    if city.getProduction().getUnitType() == SETTLER and city.getProductionPoints() >= 30:
                        city._changeProductionPoints(SETTLER)
                        self._placeUnitsInSpiral(Unit(city.getOwner(), SETTLER), index)
                        
    def changeCityWorkforceAt(self, pos, balance):
        city = self.getCityAt(pos)
        city.changeWorkforce(balance)
    
    def changeCityProductionAt(self, pos, unit):
        """Changes the city at 'pos' (row,col)'s unit production to 'unit'"""
        city = self.getCityAt(pos)
        city.changeProduction(unit)

    def _isMoveValid(self, posFrom, posTo):
        # Helper function that determines whether or not a move is valid
        
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

    def _placeUnitsInSpiral(self, unit, cityIndex):

        pos = self._spiralGenerator(cityIndex)
        self._board[self._posToIndex(pos)][1] = unit

    def _spiralGenerator(self, index):
        # Helper function that handles placing units at the end of the round
        row,col = self._indexToPos(index)
        
        if self._isPlaceable((row,col)):
            return (row,col)

        for rad in range(1, MAXRADIUS-1):
            # Go across the top
            for colInc in range(rad):
                nPos = (row-rad, col+colInc)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go down right
            for rowInc in range(-rad, rad):
                nPos = (row+rowInc, col+rad)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go across the bottom
            for colInc in range(rad):
                nPos = (row+rad, col-colInc)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go up left
            for rowInc in range(rad, -rad):
                nPos = (row-rowInc, col-rad)

                if self._isPlaceable(nPos):
                    return nPos

    def _isPlaceable(self, pos):
        # Helper function that decides if a unit can be placed at 'pos'
        row,col = pos
        index = self._posToIndex(pos)
        
        if index == None:
            return False
        
        if -2 >= row >= MAXRADIUS or -2 >= col >= MAXRADIUS:
            return False
       
        if self._board[index][1] != None:
            return False
        
        if not self._board[index][0].isPassable():
            return False

        return True
    
    def _posToIndex(self, pos):
        # Helper function that translates 'pos' into an index of the game board
        if pos == None:
            return False
        row, col = pos

        if -1 >= row >= MAXRADIUS or -1 >= col >= MAXRADIUS:
            return False
        
        return (row * 16) + col


    def _indexToPos(self, index):
        # Helper function that translates an index of the game board into a 'pos' tuple
        return (index // 16, index % 16)
    
# --------------------------------------------------------
class Unit:
    
    def __init__(self, owner, unitType):
        """A Unit is an AlphaCiv character belonging to 'owner' of given type 'unitType'.
        Valid types are: ARCHER, LEGION, and SETTLER"""
        
        self._type = unitType
        self._owner = owner
        self._moveCount = 1

    def getOwner(self):
        """Returns the Unit's owner"""
        return self._owner
    
    def getUnitType(self):
        """Returns the Unit's type"""
        return self._type
    
    def getMoveCount(self):
        """Returns how many moves the Unit has per turn"""
        return self._moveCount

# --------------------------------------------------------
class Tile:

    def __init__(self, tileType):
        """A Tile represents a position on the board and its type, 'tileType'. Valid types
        are: PLAINS, OCEANS, HILLS, MOUNTAINS, and FORESTS"""

        self._tileType = tileType
        self._food = {PLAINS:3, OCEANS:1, HILLS:0,
                      MOUNTAINS:0, FORESTS:0}[tileType]
        self._production = int(self._food)
        
    def isPassable(self):
        """Returns whether or not a Unit can pass through the Tile"""
        
        if self._tileType in [MOUNTAINS, OCEANS]:
            return False
        
        return True

    def isBuildable(self):
        """Returns whether or not a City can be built on the Tile"""
        
        if self._tile == PLAINS:
            return True
        
        return False

    def getFood(self):
        """Returns the amount of food that the Tile produces"""
        return self._food

    def getTileType(self):
        """Returns the Tile's type"""
        return self._tileType

    def getProduction(self):
        """Returns the amount of production the tile produces"""
        return self._production

# --------------------------------------------------------
class City():

    def __init__(self, owner):
        """A City represents a city tile on the game board. It is the basis for
        a player's progression in AlphaCiv."""
        
        self._size = 1
        self._owner = owner
        self._workforceFocus = None
        self._food = 0
        self._production = None
        self._productionPoints = 0
        
    def getSize(self):
        """Returns the size of the City"""
        return self._size

    def getOwner(self):
        """Returns the owner of the City"""
        return self._owner

    def getWorkforceFocus(self):
        """Returns the workforce focus of the City"""
        return self._workforceFocus

    def changeWorkforceFocus(self, focus):
        """Changes the workforce focus of the City. Valid focuses are: PRODUCTION or FOOD"""
        
        if focus in [PRODUCTION, FOOD]:
            self._workforceFocus = focus
        else:
            return -1

    def getProductionPoints(self):
        """Returns the number of production points the City currently has"""
        return self._productionPoints
    
    def getProduction(self):
        """Returns the Unit that the City is currently producing"""
        
        if self._production == None:
            return self._production
        
        return self._production

    def changeProduction(self, unitType):
        """Changes the Unit that the city is currently producing when its workforce focus is
        on PRODUCTION"""
        
        if unitType in [ARCHER, LEGION, SETTLER]:
            self._production = Unit(self._owner, unitType)
        else:
            return -1

    def getFood(self):
        """Returns the amount of food that the City has"""
        return self._food
    
    def _nextRoundPrep(self, index):
        if self._workforceFocus == PRODUCTION:
            self._productionPoints += 6
        
    def _changeProductionPoints(self, unit):
        # Subtracts production points based on which unit is being produced
        if unit == ARCHER:
            self._productionPoints -= 10

        elif unit == LEGION:
            self._productionPoints -= 15

        elif unit == SETTLER:
            self._productionPoints -= 30

        else:
            return

# --------------------------------------------------------
