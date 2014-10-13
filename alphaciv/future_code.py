# By: Jarren, Stetson, and Luke
# alphaciv.py

# ***NEED TO FINISH***
# - Implement Player class
# - Implement Position class

class Game:
    def __init__(self):
        pass
    
    def getTileAt(self, pos):
        pass
    
    def getUnitAt(self, pos):
        pass
    
    def getCityAt(self, pos):
        pass
    
    def getPlayerInTurn(self):
        pass
    
    def getWinner(self):
        pass
    
    def getAge(self):
        pass
    
    def moveUnit(self, posFrom, posTo):
        pass

    def endOfTurn(self):
        pass

    def changeCityWorkforceAt(self, pos, balance):
        pass

    def changeCityProductionAt(self, pos, produce):
        pass


# --------------------------------------------------------
class Unit:
    
    def __init__(self):
        # Container class with general unit commands.
        # gAS and gDS have been written out to show more
        # explicitly how the inheritence works.
        pass

    def getType(self):
        pass

    def getAttackingStrength(self):
        print(self.attack)

    def getDefenseStrength(self):
        print(self.defense)

    def getMoveCount(self):
        print(self.moveCount)

class Archer(Unit):

    def __init__(self):
        # We decided to use ints instead of strings, as
        # down the line we're probably going to be performing
        # comparisons, and various things (such as Archer
        # fortification) change the values.
        
        self.defense = 3
        self.attack = 2
        self.moveCount = 0
        
    def fortify(self):
        pass

class Legion(Unit):
    
    def __init__(self):
        self.defense = 2
        self.attack = 4
        self.moveCount = 0
    
class Settler(Unit):
    
    def __init__(self):
        self.defense = 3
        self.attack = 0
        self.moveCount = 0

    def buildCity(self):
        pass

# --------------------------------------------------------

class Tile:

    def __init__(self, tileType):
        pass

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
        pass

    def getProduction(self):
        pass

class City(Tile):

    def __init__(self):
        pass

    def getSize(self):
        pass

    def getOwner(self):
        pass

    def getWorkforceFocus(self):
        pass

# --------------------------------------------------------
