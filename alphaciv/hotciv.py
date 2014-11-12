#!python2
# By: Jarren, Stetson, and Luke
# hotciv.py

from __future__ import print_function
from constants import *

class HotCiv:
    def __init__(self, version):
        """A Game object manages a game of HotCiv, storing the board
        and its related commands."""

        self._version = version
        self._winner = version.createWinner()
        self._turnCount = 0
        self._turn = RED
        self._age = 4000
        self._hasMoved = []
        
        
        # Stores the board: a list containing tuples (tile, unit, city)
        self._tileBoard = [[Tile(PLAINS) for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
        self._cityBoard = [[noCity() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
        self._unitBoard = [[noUnit() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]

        ### Place items on board
        self._placeTileOnBoard((1,0), Tile(OCEANS))
        self._placeTileOnBoard((0,1), Tile(HILLS))
        self._placeTileOnBoard((2,2), Tile(MOUNTAINS))

        self._placeCityOnBoard((1,1), City(RED))
        self._placeCityOnBoard((4,1), City(BLUE))

        self._placeUnitOnBoard((2,0), Unit(RED,ARCHER))
        self._placeUnitOnBoard((3,2), Unit(BLUE,LEGION))
        self._placeUnitOnBoard((4,3), Unit(RED,SETTLER))
        ###
        
    def getTileAt(self, pos):
        """Return the tile object at 'pos' (row,col) on the board"""
        row,col = pos
        tile = self._tileBoard[row][col]
        
        if tile.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS]:
            return tile
        else:
            return False
    
    def getUnitAt(self, pos):
        """Return the unit object located at 'pos' (row,col) on the board"""
        row,col = pos

        if (WORLDSIZE <= row or -1 >= row
            or WORLDSIZE <= col or col <= -1):
            return False
        
        return self._unitBoard[row][col]
    
    def getCityAt(self, pos):
        """Return the city object located at 'pos' (row,col) on the board"""
        row,col = pos
        city = self._cityBoard[row][col]
        
        if isinstance(city, noCity):
            return False
        
        return city

    def getPlayerInTurn(self):
        """Returns the player currently in turn"""
        return self._turn
    
    def getAge(self):
        """Returns the current age"""
        return self._age

    def getWinner(self, year):
        """Returns the winner"""

        return self._winner(year)
    
    def moveUnit(self, posFrom, posTo):
        """Moves a unit from 'posFrom' (row,col) to 'posTo' (row,col)"""
        unit = self.getUnitAt(posFrom)
        
        if not self._isMoveValid(posFrom, posTo):
            return False

        self._placeUnitOnBoard(posTo, unit)
        self._placeUnitOnBoard(posFrom, noUnit())
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

        for row,x in enumerate(self._cityBoard):
            for col,city in enumerate(x):
                city.nextRoundPrep()
                    
                for i in range(city.buyNewUnit()):
                    pos = self._spiralGenerator((row,col))
                    unit = Unit(city.getOwner(), city.getProduction())
                    self._placeUnitOnBoard(pos, unit)

    def changeCityWorkforceAt(self, pos, balance):
        city = self.getCityAt(pos)
        city.changeWorkforce(balance)
    
    def changeCityProductionAt(self, pos, unit):
        """Changes the city at 'pos' (row,col)'s unit production to 'unit'"""
        city = self.getCityAt(pos)
        city.changeProduction(unit)

    ### Placement helpers
    def _placeTileOnBoard(self, pos, tile):
        row,col = pos
        
        self._tileBoard[row][col] = tile
        
    def _placeCityOnBoard(self, pos, city):
        row,col = pos
            
        self._cityBoard[row][col] = city
        

    def _placeUnitOnBoard(self, pos, unit):
        row,col = pos
        
        self._unitBoard[row][col] = unit
    ###
    
    def _isMoveValid(self, posFrom, posTo):
        # Helper function that determines whether or not a move is valid
        fromRow, fromCol = posFrom
        toRow, toCol = posTo
        
        unit = self.getUnitAt(posFrom)
        mCount = unit.getMoveCount()
        toTile = self.getTileAt(posTo)

        if self.getCityAt(posTo) != False:
            return False
        
        if posFrom in self._hasMoved:
            return False

        if unit.getOwner() != self.getPlayerInTurn():
            return False
        
        if toTile.isPassable() == False:
            return False
               
        if self.getUnitAt(posTo) != False:
            if self.getUnitAt(posTo).getOwner() == self.getPlayerInTurn():
                return False

        if any([abs(fromRow-toRow) > mCount,
                abs(fromCol-toCol) > mCount]):
            return False

        return True

    def _placeUnitsInSpiral(self, cityPos, unit, owner):

        pos = self._spiralGenerator(cityPos)
        self._placeUnitOnBoard(pos, unit, owner)

    def _spiralGenerator(self, pos):
        # Helper function that handles placing units at the end of the round
        row,col = pos
        
        if self._isPlaceable(pos):
            return pos

        for rad in range(1, WORLDSIZE-1):
            # Go across the top
            for colInc in range(rad):
                nPos = (row-rad, col+colInc)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go down right
            for rowInc in range(-rad, rad+1):
                nPos = (row+rowInc, col+rad)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go across the bottom
            for colInc in range(row-rad, row):
                nPos = (row+rad, col-colInc)
                
                if self._isPlaceable(nPos):
                    return nPos

            # Go up left
            for rowInc in range(-rad, rad+1):
                nPos = (row-rowInc, col-rad)

                if self._isPlaceable(nPos):
                    return nPos

    def _isPlaceable(self, pos):
        # Helper function that decides if a unit can be placed at 'pos'
        row,col = pos
    
        if (WORLDSIZE <= row or -1 >= row
            or WORLDSIZE <= col or col <= -1):
            return False
       
        if isinstance(self._unitBoard[row][col], noCity):
            return False

        if not self.getTileAt(pos).isPassable():
            return False

        if self.getUnitAt(pos).getOwner() == self._turn:
            return False

        return True
    
# --------------------------------------------------------
class noUnit:

    def __init__(self):
        pass
    def getOwner(self):
        pass
    def getUnitType(self):
        pass
    def getMoveCount(self):
        pass

# ---
class Unit:
    
    def __init__(self, owner, unitType):
        """A Unit is an HotCiv character belonging to 'owner' of given type 'unitType'.
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

class noCity:
    def __init__(self):
        pass
    def getSize(self):
        pass
    def getOwner(self):
        pass
    def getWorkforceFocus(self):
        pass
    def changeWorkforceFocus(self, focus):
        pass
    def getProduction(self):
        return noUnit()
    def changeProduction(self, unitType):
        pass
    def getFood(self):
        pass
    def buyNewUnit(self):
        return -1
    def nextRoundPrep(self):
        pass
    def __changeProductionPoints(self, unit):
        pass
# ---
class City:

    def __init__(self, owner):
        """A City represents a city tile on the game board. It is the basis for
        a player's progression in HotCiv."""
        
        self._size = 1
        self._owner = owner
        self._workforceFocus = None
        self._food = 0
        self._production = noUnit()
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
            return False

    def getProductionPoints(self):
        return self._productionPoints
    
    def getProduction(self):
        """Returns the Unit that the City is currently producing"""

        return self._production

    def changeProduction(self, unitType):
        """Changes the Unit that the city is currently producing when its workforce focus is
        on PRODUCTION"""
        
        if unitType in [ARCHER, LEGION, SETTLER]:
            self._production = Unit(self._owner, unitType)
        else:
            return False


    def getFood(self):
        """Returns the amount of food that the City has"""
        return self._food
    
    def buyNewUnit(self):
        # Subtracts production points based on which unit is being produced
        unitCost = UNITCOSTS[self._production.getUnitType()]
        
        if self._productionPoints >= unitCost and unitCost != -1:
            numOfUnits = self._productionPoints // unitCost
            self._productionPoints -= unitCost*numOfUnits
            return numOfUnits
                    
        return -1
    
    def nextRoundPrep(self):
        if self._workforceFocus == PRODUCTION:
            self._productionPoints += 6
            
# --------------------------------------------------------
def RedWinnerStrategy(year):

    if year == 3000:
        return RED

    return False

def ConquerAllCitiesStrategy(year):

    return False
    
def LinearAgingStrategy():
    pass

def VaryingAgingStrategy():
    pass

# --------------------------------------------------------
class AlphaCivFactory:
    
    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

# --------------------------------------------------------
class BetaCivFactory:
    
    def createWinner(self):
        return ConquerAllCitiesStrategy

    def createAging(self):
        return VaryingAgingStrategy

# --------------------------------------------------------
