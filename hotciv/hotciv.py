#!python2
# By: Jarren, Stetson, and Luke
# hotciv.py

from __future__ import print_function
from constants import *
from random import randint

class HotCiv:
    def __init__(self, version):
        """A Game object manages a game of HotCiv, storing the board
        and its related commands."""

        self._version = version
        self._winner = version().createWinner()
        self._unitCreateStrategy = version().createUnit()
        self._ageStrategy = version().createAging()
        self._workForceStrategy = version().createWorkforceStrategy()
        self._turnCount = 0
        self._turn = RED
        self._age = -4000
        self._roundCount = 0
        self._hasMoved = []
        self._successfulAttacks = {RED:0, BLUE:0}
        
        # Stores the board: a list containing tuples (tile, unit, city)
        maps = version().createMap()
        self._tileBoard, self._cityBoard, self._unitBoard =\
                         maps(self._unitCreateStrategy)

    def getTileAt(self, pos):
        """Return the tile object at 'pos' (row,col) on the board"""
        row,col = pos
        tile = self._tileBoard[row][col]
        
        if tile.getTileType() in [OCEANS, MOUNTAINS, PLAINS, HILLS, FORESTS]:
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

        if (WORLDSIZE <= row or -1 >= row
            or WORLDSIZE <= col or col <= -1):
            return False
        
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
        
        return self._winner(self._age, self._cityBoard,
                            self._successfulAttacks, self._roundCount)
    
    def moveUnit(self, posFrom, posTo, random=True):
        """Moves a unit from 'posFrom' (row,col) to 'posTo' (row,col)"""
        unitFrom = self.getUnitAt(posFrom)
        unitTo = self.getUnitAt(posTo)
        unitAttackDefenseStrategy = self._version().createUnitAttackDefenseStrategy()

        attackingAdjacentUnitCount = self.getAdjacentUnitCount(posFrom)
        defendingAdjacentUnitCount = self.getAdjacentUnitCount(posTo)

        if random:
            die1 = randint(1,6)
            die2 = randint(1,6)
        else:
            die1 = 1
            die2 = 1

        if not self._isMoveValid(posFrom, posTo):
            return False
        
        if isinstance(unitFrom, ActiveUnit) and unitFrom.isLocked():
            return False
          
        if not isinstance(unitTo, noUnit) and unitTo.getOwner() !=\
           unitFrom.getOwner():
            
            if not isinstance(self.getCityAt(posTo), noCity):
                terrain = "city"
            else:
                terrain = self.getTileAt(posTo).getTileType()

            if not unitAttackDefenseStrategy(unitFrom, unitTo,
                                             terrain,
                                             attackingAdjacentUnitCount,
                                             defendingAdjacentUnitCount,
                                             die1, die2):
    
                self.placeUnitAt(posFrom, noUnit())
                return
        
        if isinstance(self.getCityAt(posTo), City) and\
           self.getCityAt(posTo).getOwner() != unitFrom.getOwner():
            self.getCityAt(posTo).conquerCity()
            
        # Was successful attack
        self._incrementSuccessfulAttacks(unitFrom.getOwner())
        self.placeUnitAt(posTo, unitFrom)   
        self.placeUnitAt(posFrom, noUnit())
        self._hasMoved.append(posTo)
        
    def getAdjacentUnitCount(self, pos):
        """Gets the number of Units that are touching, but not on, 'pos'"""
        row,col = pos
        total = 0

        posList = [(row-1,col), (row-1,col+1), (row,col+1), (row+1,col+1),
         (row+1,col), (row+1,col-1), (row,col-1), (row-1,col-1)]

        for loc in posList:
            if not self.getUnitAt(loc):
                pass
                
            elif self.getUnitAt(loc).getOwner() == self.getUnitAt(pos).getOwner():
                total += 1

        return total
        
    def performUnitAction(self, pos):
        """Tells unit at 'pos' to perform its action:
        Archers - Fortify (increase defense by 3, but cannot move)
        Settlers - Build city"""
        
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
        self._roundCount += 1

        winner = self.getWinner()
        if winner in [RED, BLUE]:
            return winner
        
        for row,x in enumerate(self._cityBoard):
            for col,city in enumerate(x):
                adjacentItemList = self._itemAroundLocationGenerator((row,col))
                self._workForceStrategy(city, adjacentItemList)
                city.increaseSize()
                    
                for i in range(city.buyNewUnit()):
                    pos = self._spiralGenerator((row,col))
                    unit = self._unitCreateStrategy(city.getOwner(), city.getProduction())
                    self.placeUnitAt(pos, unit)

    def changeCityWorkforceAt(self, pos, balance):
        """Changes the workforce of city at 'pos' to 'balance'"""
        city = self.getCityAt(pos)
        city.changeWorkforce(balance)
    
    def changeCityProductionAt(self, pos, unit):
        """Changes the city at 'pos' (row,col)'s unit production to 'unit'"""
        city = self.getCityAt(pos)
        city.changeProduction(unit)

    ### Placement methods
    def placeTileAt(self, pos, tile):
        """Places a tile on the board"""
        row,col = pos
        
        self._tileBoard[row][col] = tile
        
    def placeCityAt(self, pos, city):
        """Places a city on the board"""
        row,col = pos
            
        self._cityBoard[row][col] = city
        

    def placeUnitAt(self, pos, unit):
        """Places a unit on the board"""
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
        # Helper function that puts units on the board
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
        # Decides if a unit can be placed at 'pos'
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

    def _incrementSuccessfulAttacks(self, team):
        # Handles counting successful attacks for both players
        
        if self._version == ZetaCivFactory and self._roundCount >= 20:
            self._successfulAttacks[team] += 1
            return

        if self._version == ZetaCivFactory and self._roundCount < 20:
            return

        self._successfulAttacks[team] += 1
            
    def _itemAroundLocationGenerator(self, pos):
        # Generates a list of tiles that surround the given pos, for use with cities

        if self.getCityAt(pos) == False:
            return False
        
        row, col = pos
        adjacentItemList = []
        
        posList = [(row-1,col), (row-1,col+1), (row,col+1), (row+1,col+1),
        (row+1,col), (row+1,col-1), (row,col-1), (row-1,col-1)]
        
        for loc in posList:
            if self.getCityAt(loc) != False:
                adjacentItemList.append(CITY)
            else:
                adjacentItemList.append(self.getTileAt(loc))

        return adjacentItemList
               
# --------------------------------------------------------
class noUnit:
    
    def __init__(self):
        """Dummy class for filling the unit board"""
        pass
    def getOwner(self):
        pass
    def getAttackStrength(self):
        pass
    def getDefenseStrength(self):
        pass
    def getUnitType(self):
        pass
    def getMoveCount(self):
        pass

# ---
class NoActionUnit:
    
    def __init__(self, owner, unitType):
        """A NoActionUnit is an HotCiv character belonging to 'owner' of given type 'unitType'.
        Valid types are: ARCHER, LEGION, and SETTLER. NoActionUnits are different from ActiveUnits
        in that they cannot perform 'actions,' such as Archer fortification."""
        
        self._type = unitType
        self._owner = owner
        self._moveCount = 1
        self._attack = UNITATTACK[unitType]
        self._defense = UNITDEFENSE[unitType]

    def getOwner(self):
        return self._owner
    
    def getUnitType(self):
        return self._type
    
    def getMoveCount(self):
        """Returns how many moves the Unit has per turn"""
        return self._moveCount

    def getAttackStrength(self):
        return self._attack

    def getDefenseStrength(self):
        return self._defense

# --- 
class ActiveUnit:
    
    def __init__(self, owner, unitType):
        """An ActiveUnit is an HotCiv character belonging to 'owner' of given type 'unitType'.
        Valid types are: ARCHER, LEGION, and SETTLER. ActiveUnits are different from NoActionUnits
        in that they can perform 'actions,' such as Archer fortification."""
        
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
        return self._owner
    
    def getUnitType(self):
        return self._type
    
    def getMoveCount(self):
        """Returns how many moves the Unit has per turn"""
        return self._moveCount

    def getAttackStrength(self):
        return self._attack

    def getDefenseStrength(self):
        return self._defense
    
    def performAction(self):
        """Perform the unit's action"""

        return self._action()

    def fortify(self):
        """Archer fortification"""

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
        """Settler city building"""
        return 'buildCity'

    def noAction(self):
        """Legion units perform no action"""
        return 'noAction'

    def isLocked(self):
        """Returns whether or not the Archer is locked"""
        return self._isLocked
    
# --------------------------------------------------------
class Tile:

    def __init__(self, tileType):
        """A Tile represents a position on the board and its type, 'tileType'. Valid types
        are: PLAINS, OCEANS, HILLS, MOUNTAINS, and FORESTS"""

        self._tileType = tileType
        self._food = {PLAINS:3, OCEANS:1, HILLS:0,
                      MOUNTAINS:0, FORESTS:0}[tileType]
        self._production = {FORESTS:3, MOUNTAINS:1, HILLS:2,
                            PLAINS:0, OCEANS:0}[tileType]
        
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
        """Dummy city used to fill the city board"""
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
    def increaseSize(self):
        pass
    
# ---
class City:

    def __init__(self, owner):
        """A City represents a city tile on the game board. It is the basis for
        a player's progression in HotCiv."""
        
        self._size = 1
        self._owner = owner
        self._workforceFocus = None
        self._foodPoints = 0
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

    def getFoodPoints(self):
        return self._foodPoints
    
    def getProduction(self):
        """Returns the Unit that the City is currently producing"""

        return self._production

    def changeProduction(self, unitType):
        """Changes the Unit that the city is currently producing when its workforce focus is
        on PRODUCTION"""
        
        if unitType in [ARCHER, LEGION, SETTLER]:
            self._production = unitType 
        else:
            return False

    def addFoodPoints(self, amount):
        self._foodPoints += amount

    def addProductionPoints(self, amount):
        self._productionPoints += amount

    def getFood(self):
        """Returns the amount of food that the City has"""
        return self._food
    
    def buyNewUnit(self):
        # Subtracts production points based on which unit is being produced
        
        if isinstance(self._production, noUnit):
            return False
        
        unitCost = UNITCOSTS[self._production]
        
        if self._productionPoints >= unitCost and unitCost != -1:
            numOfUnits = self._productionPoints // unitCost
            self._productionPoints -= unitCost*numOfUnits
            return numOfUnits
                    
        return False

    def conquerCity(self):
        if self._owner == RED:
            self._owner = BLUE
        else:
            self._owner = RED

    def increaseSize(self):
        if self._size >= 9:
            return
        
        if self._foodPoints > 5+(self._size*3):
            self._size += 1
            self._foodPoints = 0
            
# --------------------------------------------------------
def RedWinnerStrategy(year, cities, count, rounds):
    # Red wins at 3000BC

    if year == -3000:
        return RED

    return False

# --------------------------------------------------------
def ConquerAllCitiesStrategy(year, cities, count, rounds):
    # If all cities on the map are of one team, that team wins

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

# --------------------------------------------------------
def ThreeSuccessfulAttacksWinsStrategy(year, cities, count, rounds):
    # After three successful attacks, the team that has those attacks wins
    redWins, blueWins = count[RED], count[BLUE]
    
    if redWins >= 3:
        return RED
    if blueWins >= 3:
        return BLUE
    return False

# --------------------------------------------------------
def SuddenDeathWinsStrategy(year, cities, count, rounds):
    # Up until 20 rounds, all cities must be conquered to win. After that,
    # when three units are killed the opposite team wins
    if rounds < 20:
        return ConquerAllCitiesStrategy(year, cities, count, rounds)
    return ThreeSuccessfulAttacksWinsStrategy(year, cities, count, rounds)

# --------------------------------------------------------
def LinearAgingStrategy(age):
    
    return age + 100

# --------------------------------------------------------
def VaryingAgingStrategy(age):

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
    # Manually generated map, following AlphaCiv format
    
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
def MapFromFile(unitCreateStrategy):
    """Creates the map from a file called 'map.txt'. The file must be 16 rows of 16
    characters, excluding spaces.
    'p':plains, 'o':oceans, 'h':hills, 'm':mountains,
    'f':forests, 'r':red city, 'b':blue city"""

    tileBoard = [[] for i in range(WORLDSIZE)]
    cityBoard = [[noCity() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    unitBoard = [[noUnit() for col in range(WORLDSIZE)] for row in range(WORLDSIZE)]
    
    spaces = {'p':Tile(PLAINS), 'o':Tile(OCEANS), 'h':Tile(HILLS), 'm':Tile(MOUNTAINS),
              'f':Tile(FORESTS), 'r':City(RED), 'b':City(BLUE)}
    
    with open('map.txt', 'r') as f:
        pos = 0
        
        for x,line in enumerate(f):
            for char in line.rstrip():
                if char != " ":
                    if char.lower() in ['r','b']:
                        tileBoard[x].append(spaces['p'])
                        cityBoard[x][pos%16] = spaces[char.lower()]
                        pos += 1
                        
                    else:
                        try:
                            tileBoard[x].append(spaces[char.lower()])

                        # Invalid characters are replaced by PLAINS
                        except KeyError:
                            tileBoard[x].append(spaces['p'])

                        pos += 1
                        
        return tileBoard, cityBoard, unitBoard

# --------------------------------------------------------
def AttackerAlwaysWinsStrategy(attackingUnit, defendingUnit, battleground,
                               attackingAdjacentUnitCount,
                               defendingAdjacentUnitcount,
                               die1, die2):
    
    return True

# --------------------------------------------------------
def CompareAttackDefenseStrategy(attackingUnit, defendingUnit, battleground,
                                 attackingAdjacentUnitCount,
                                 defendingAdjacentUnitCount,
                                 die1, die2):
    # Winning in battle is determined by comparing attack and defense of the two
    # units, the terrain, and a factor of randomness

    terrainFactor = {PLAINS:1, HILLS:2, FORESTS:2, "city":3}
    attackStrength = (attackingUnit.getAttackStrength() +\
                      attackingAdjacentUnitCount) * terrainFactor[battleground]
    defenseStrength = (defendingUnit.getDefenseStrength() +\
                       defendingAdjacentUnitCount) * terrainFactor[battleground]

    # In Risk, in the event of equality, defense wins
    if attackStrength == defenseStrength:
        return False
    
    return attackStrength * die1 > defenseStrength * die2

# --------------------------------------------------------
def SixPerTurnStrategy(city, adjacentTileList):
    
    if city.getWorkforceFocus() == PRODUCTION:
        city.addProductionPoints(6)

# --------------------------------------------------------
def SmartWorkforceStrategy(city, adjacentItemList):

    if adjacentItemList == False:
        return

    for item in adjacentItemList:
        if item == CITY and city.getWorkforceFocus() == PRODUCTION:
            city.addProductionPoints(1)

        elif item == CITY and city.getWorkforceFocus() == FOOD:
            city.addFoodPoints(1)
            
        elif city.getWorkforceFocus() == PRODUCTION:
            city.addProductionPoints(item.getProduction())

        else:
            city.addFoodPoints(item.getFood())
            
# --------------------------------------------------------
class AlphaCivFactory:
    
    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return SimpleMap

    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy
    
    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class BetaCivFactory:
    
    def createWinner(self):
        return ConquerAllCitiesStrategy

    def createAging(self):
        return VaryingAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return SimpleMap

    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy
    
    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class GammaCivFactory:

    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return ActiveUnit

    def createMap(self):
        return SimpleMap
    
    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy

    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class DeltaCivFactory:

    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return MapFromFile
    
    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy

    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class EpsilonCivFactory:

    def createWinner(self):
        return ThreeSuccessfulAttacksWinsStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return SimpleMap

    def createUnitAttackDefenseStrategy(self):
        return CompareAttackDefenseStrategy

    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class ZetaCivFactory:

    def createWinner(self):
        return SuddenDeathWinsStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return SimpleMap

    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy

    def createWorkforceStrategy(self):
        return SixPerTurnStrategy
    
# --------------------------------------------------------
class EtaCivFactory:

    def createWinner(self):
        return RedWinnerStrategy

    def createAging(self):
        return LinearAgingStrategy

    def createUnit(self):
        return NoActionUnit

    def createMap(self):
        return SimpleMap

    def createUnitAttackDefenseStrategy(self):
        return AttackerAlwaysWinsStrategy

    def createWorkforceStrategy(self):
        return SmartWorkforceStrategy

# --------------------------------------------------------    
class SemiCivFactory:

    def createWinner(self):
        return ThreeSuccessfulAttacksWinsStrategy

    def createAging(self):
        return VaryingAgingStrategy

    def createUnit(self):
        return ActiveUnit

    def createMap(self):
        return MapFromFile

    def createUnitAttackDefenseStrategy(self):
        return CompareAttackDefenseStrategy

    def createWorkforceStrategy(self):
        return SmartWorkforceStrategy
