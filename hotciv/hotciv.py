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
        self._winner = version().createWinner()
        self._unitCreateStrategy = version().createUnit
        self._ageStrategy = version().createAging()
        self._turnCount = 0
        self._turn = RED
        self._age = -4000
        self._hasMoved = []
        
        # Stores the board: a list containing tuples (tile, unit, city)
        self._tileBoard, self._cityBoard, self._unitBoard = version().createMap(self._unitCreateStrategy)

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

    def getWinner(self):
        """Returns the winner"""

        return self._winner(self._age, self._cityBoard)
    
    def moveUnit(self, posFrom, posTo):
        """Moves a unit from 'posFrom' (row,col) to 'posTo' (row,col)"""
        unit = self.getUnitAt(posFrom)
        
        if not self._isMoveValid(posFrom, posTo):
            return False

        if isinstance(unit, ActiveUnit) and unit.isLocked():
            return False

        self.placeUnitAt(posTo, unit)
        self.placeUnitAt(posFrom, noUnit())
        self._hasMoved.append(posTo)

    def performUnitAction(self, pos):
        unit = self.getUnitAt(pos)
        response = unit.performAction()

        if isinstance(unit, noUnit):
            return
        
        # Performs building for settlers
        if response == 'buildCity':
            self.placeCityAt(pos, City(unit.getOwner()))
            self.placeUnitAt(pos, noUnit())
            
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
        self._age = self._ageStrategy(self._age)
        
        if self.getWinner() != False:
            return self.getWinner()
        
        for row,x in enumerate(self._cityBoard):
            for col,city in enumerate(x):
                city.nextRoundPrep()
                    
                for i in range(city.buyNewUnit()):
                    pos = self._spiralGenerator((row,col))
                    unit = self._unitCreateStrategy(city.getOwner(), city.getProduction())
                    self.placeUnitAt(pos, unit)

    def changeCityWorkforceAt(self, pos, balance):
        city = self.getCityAt(pos)
        city.changeWorkforce(balance)
    
    def changeCityProductionAt(self, pos, unit):
        """Changes the city at 'pos' (row,col)'s unit production to 'unit'"""
        city = self.getCityAt(pos)
        city.changeProduction(unit)

    ### Placement helpers
    def placeTileAt(self, pos, tile):
        row,col = pos
        
        self._tileBoard[row][col] = tile
        
    def placeCityAt(self, pos, city):
        row,col = pos
            
        self._cityBoard[row][col] = city
        

    def placeUnitAt(self, pos, unit):
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
        self.placeUnitAt(pos, unit, owner)

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
    def getAttack(self):
        pass
    def getDefense(self):
        pass
    def getUnitType(self):
        pass
    def getMoveCount(self):
        pass

# ---
class PassiveUnit:
    
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

# --- 
class ActiveUnit:
    
    def __init__(self, owner, unitType):
        """A Unit is an HotCiv character belonging to 'owner' of given type 'unitType'.
        Valid types are: ARCHER, LEGION, and SETTLER"""
        
        self._type = unitType
        self._owner = owner
        self._moveCount = 1
        self._isLocked = False
        self._attack = UNITATTACK[unitType]
        self._defense = UNITDEFENSE[unitType]
        
        UNITACTIONS = {ARCHER:self.fortify, LEGION:self.noAction,
                       SETTLER:self.buildCity, None: self.noAction}
        self._action = UNITACTIONS[unitType]

    def getOwner(self):
        """Returns the Unit's owner"""
        return self._owner
    
    def getUnitType(self):
        """Returns the Unit's type"""
        return self._type
    
    def getMoveCount(self):
        """Returns how many moves the Unit has per turn"""
        return self._moveCount

    def getAttack(self):
        return self._attack

    def getDefense(self):
        return self._defense
    
    def performAction(self):

        return self._action()

    def fortify(self):

        if self._defense == 6:
            self._defense = 3
            
        else:
            self._defense = 6

        if self._isLocked:
            self._isLocked = False
        else:
            self._isLocked = True
            
        return 'fortify'

    def buildCity(self):
        return 'buildCity'

    def noAction(self):
        return 'noAction'

    def isLocked(self):
        return self._isLocked
    
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
            self._production = unitType ###Unit(self._owner, unitType)
        else:
            return False


    def getFood(self):
        """Returns the amount of food that the City has"""
        return self._food
    
    def buyNewUnit(self):
        # Subtracts production points based on which unit is being produced
        
        if isinstance(self._production, noUnit):
            return -1
        
        unitCost = UNITCOSTS[self._production]
        
        if self._productionPoints >= unitCost and unitCost != -1:
            numOfUnits = self._productionPoints // unitCost
            self._productionPoints -= unitCost*numOfUnits
            return numOfUnits
                    
        return -1
    
    def nextRoundPrep(self):
        if self._workforceFocus == PRODUCTION:
            self._productionPoints += 6
            
# --------------------------------------------------------
def RedWinnerStrategy(year, cities):

    if year == -3000:
        return RED

    return False

# ----
def ConquerAllCitiesStrategy(year, cities):

    teams = []
    
    for row in cities:
        teams += [city.getOwner() for city in row if city.getOwner() != None]
    
    if len(teams) == 0:
        return False

    prev = teams[0]
    
    for team in teams:
        if team != prev:
            return False
        
        prev = team
    
    return prev

# ----
def LinearAgingStrategy(age):
    
    return age + 100

# ----
def VaryingAgingStrategy(age):
    # Maybe make this a little nicer?

    if -4000 <= age < -100:
        return age + 100

    if age == -100:
        return age + 99

    if age == -1:
        return age + 2

    if age == 1:
        return age + 49

    if 50 <= age < 1750:
        return age + 50

    if 1750 <= age < 1900:
        return age + 25

    if 1900 <= age < 1970:
        return age + 5

    return age + 1

# --------------------------------------------------------
def SimpleMap(unitCreateStrategy):
    tileBoard = [[Tile(PLAINS) for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    cityBoard = [[noCity() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    unitBoard = [[noUnit() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]

    ### Place items on board
    tileBoard[1][0] = Tile(OCEANS)
    tileBoard[0][1] = Tile(HILLS)
    tileBoard[2][2] = Tile(MOUNTAINS)

    cityBoard[1][1] = City(RED)
    cityBoard[4][1] = City(BLUE)

    unitBoard[2][0] = unitCreateStrategy(RED,ARCHER)
    unitBoard[3][2] = unitCreateStrategy(BLUE,LEGION)
    unitBoard[4][3] = unitCreateStrategy(RED,SETTLER)
    ###

    return tileBoard, cityBoard, unitBoard

# --------------------------------------------------------
def MapFromFile():

    tileBoard = [[]*WORLDSIZE]*WORLDSIZE
    cityBoard = [[noCity() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    unitBoard = [[noUnit() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    
    spaces = {'p':Tile(PLAINS), 'o':Tile(OCEANS), 'h':Tile(HILLS), 'm':Tile(MOUNTAINS),
              'r':City(RED), 'b':City(BLUE)}
    
    with open('map.txt', 'r') as f:
        pos = 0
        
        for x,line in enumerate(f):
            for char in line.rstrip():
                if char != " ":
                    try:
                        tileBoard[x].append(spaces[char.lower()])

                    # Invalid characters are replaced by PLAINS
                    except KeyError:
                        tileBoard[x].append(spaces['p'])

                    pos += 1
                    
                if char in ['r','b']:
                    tileBoard[x].append(spaces['p'])
                    cityBoard[x].append(spaces[char.lower()])
                    pos += 1

    for i in range(16):
        print(tileBoard[0][i].getTileType())
        #print(tileBoard[15][i].getTileType())
        
    return tileBoard, cityBoard, unitBoard

# --------------------------------------------------------
class AlphaCivFactory:
    
    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self, owner, unitType):
        return PassiveUnit(owner, unitType)

    def createMap(self, unitCreateStrategy):
        return SimpleMap(unitCreateStrategy)
    
# --------------------------------------------------------
class BetaCivFactory:
    
    def createWinner(self):
        return ConquerAllCitiesStrategy

    def createAging(self):
        return VaryingAgingStrategy

    def createUnit(self, owner, unitType):
        return PassiveUnit(owner, unitType)

    def createMap(self, unitCreateStrategy):
        return SimpleMap(unitCreateStrategy)
    
# --------------------------------------------------------
class GammaCivFactory:

    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self, owner, unitType):
        return ActiveUnit(owner, unitType)

    def createMap(self, unitCreateStrategy):
        return SimpleMap(unitCreateStrategy)
    
# --------------------------------------------------------
class DeltaCivFactory:

    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self, owner, unitType):
        return PassiveUnit(owner, unitType)

    def createMap(self, unitCreateStrategy):
        return MapFromFile()
    
