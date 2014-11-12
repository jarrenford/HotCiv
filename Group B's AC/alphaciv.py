#alphaciv.py
#Team B
#Bob, Alex, Nick, Zhongyang
#CS 270

from gameconstants import *
    
    
class Game:
    """
    Game is the central interface for accessing and modifying the HotCiv game
    """

    def __init__(self):
        """
        The constructor for the Game class creates and initializes a number of instance variables for use in the game
        playerInTurn: Keeps track of the player who has control of the current turn
        cityBoard: Creates a 2D board with default city set up to keep track of the cities in the game
        tileBoard: Creates a 2D board with default tile set up to keep track of the tiles in the game
        unitBoard: Creates a 2D board with default unit set up to keep track of the units in the game
        age: Keeps track of the year in the game with negative numbers representing BC era
        winner: Stores the winner of the game when one is decided
        """

        #Red always has the first turn in AlphaCiv
        self.playerInTurn = RED

        #Initializing the three levels of boards to keep track of cities, tiles, and units respectively
        self.cityBoard = [[City(NONE) for x in range (0, WORLDSIZE)]for y in range (0,WORLDSIZE)]
        self.tileBoard = [[Tile(PLAINS) for x in range (0, WORLDSIZE)]for y in range (0,WORLDSIZE)]
        self.unitBoard = [[Unit(NONE, NONE) for x in range (0, WORLDSIZE)]for y in range (0,WORLDSIZE)]

        #Initial set up of the cities in AlphaCiv
        self.cityBoard [1][1] = City(RED)
        self.cityBoard [4][1] = City(BLUE)

        #Initial set up of the tiles in AlphaCiv
        self.tileBoard [1][0] = Tile(OCEAN)
        self.tileBoard [0][1] = Tile(HILLS)
        self.tileBoard [2][2] = Tile(MOUNTAIN)

        #Initial set up of the units in AlphaCiv
        self.unitBoard [2][0] = Unit(ARCHER, RED)
        self.unitBoard [3][2] = Unit(LEGION, BLUE)
        self.unitBoard [4][3] = Unit(SETTLER, RED)

        #Age of the game starts at 4000 BC
        self.age = -4000

        self.winner = NONE

    
    def getTileAt(self, position):
        """
        Returns a specific tile
        Precondition: position is a valid position in the world.
        @param: "position" is the position in the world that must be returned.
        @return: The tile at position "position"
        """
        row, col = position
        return self.tileBoard[row][col]
    
    def getUnitAt(self, position):
        """
        Returns a specific unit
        Precondition: position is a valid position in the world.
        @param: "position" is the position in the world that must be returned.
        @return: The unit at position "position"
        """        
        row, col = position
        return self.unitBoard[row][col]
    
    def getCityAt(self, position):
        """
        Returns a specific city
        Precondition: position is a valid position in the world.
        @param: "position" is the position in the world that must be returned.
        @return: The city at position "position"
        """ 
        row, col = position
        return self.cityBoard[row][col]
    
    def getPlayerInTurn(self):
        """
        Return the player that is in turn (able to move units and manage cities)
        @return: The player in turn
        """
        return self.playerInTurn
    
    def getWinner(self):
        """
        Return the player that has won the game
        @return: The player that has won the game or NONE if no player has won
        """
        return self.winner
    
    def getAge(self):
        """
        Return the age of the world. Negative numbers represent BC era while positive numbers
        represent AD era.
        @return: World age
        """
        return self.age
    
    def moveUnit(self, positionFrom, positionTo):
        """
        Move a unit from one position to another.
        If that position is occupied by an opponent, the attacker wins the battle and takes the spot.
        If that position is occupied by an opponent city, the city is overtaken by the moving unit's owner.
        Units cannot move onto mountains or oceans.
        Units cannot move on a tile with another unit owned by the same owner.
        Players cannot move out of turn.
        Precondition: The "positionFrom" parameter has a unit on that position
        Precondition: "positionFrom" and "positionTo" are within the parameters of the world
        @param: "positionFrom" is the position where the unit is now
        @param: "positionTo" is the position where the unit should move to
        @return: True if the move is valid (within game rules) and False if the move is invalid
        """
        row0, col0 = positionFrom
        row1, col1 = positionTo
        
        unitFrom = self.getUnitAt((row0,col0))
        unitTo = self.getUnitAt((row1,col1))
        tileTo = self.getTileAt((row1,col1)).getTypeString()

        #The amount of tiles the unit can move
        unitMoveCount = unitFrom.getMoveCount()

        #The column and rows being moved over
        colMove = abs(col1 - col0)
        rowMove = abs(row1 - row0)

        #Since tiles can be traversed diagonally, the maximum distance needed to move the unit from one space to another is the maximum of the rows traversed and columns traversed
        maxDistanceMoved = max(rowMove, colMove)

        #Check for legal move conditions
        if (maxDistanceMoved<=unitMoveCount and unitTo.getOwner()!= unitFrom.getOwner() and tileTo != MOUNTAIN and tileTo!= OCEAN and unitFrom.getOwner() == self.getPlayerInTurn()):
            self.unitBoard[row1][col1] = unitFrom
            self.unitBoard[row0][col0] = Unit(NONE, NONE)
            self.getUnitAt((row1,col1))._move(maxDistanceMoved)
            
            #Check if moving unit is moving onto an opposing city
            if (self.getCityAt((row1,col1)).getOwner()!=NONE and self.getCityAt((row1,col1)).getOwner()!=self.getPlayerInTurn()):
                self.getCityAt((row1,col1)).owner = unitFrom.getOwner()
                
            return True

        return False

        
    
    def endOfTurn(self):
        """
        Tell the game that the current player has finished their turn. The next player is then in turn.
        If all players have had their turns, do end-of-round processing:
        A) Restore all unit's move counts
        B) Produce production in all cities
        C) Produce units in all cities (if enough production)
        D) Increment the world age
        """

        #If it was red's turn, it is now blue's turn
        if (self.playerInTurn==RED):
            self.playerInTurn=BLUE

        #If it was blue's turn, then all player's have had a turn and the round is over
        else:
            self.playerInTurn=RED

            self.age = self.age + 100

            #If the world reaches an age of 3000 BC, red is declared the winner.
            if (self.age == -3000):
                self.winner = RED

            #Iterates through the board to find cities and units
            for row in range (0,WORLDSIZE):
                for col in range (0, WORLDSIZE):

                    #Reset all units' move counts for the new round
                    if self.getUnitAt((row,col)).getTypeString() != NONE:
                        self.getUnitAt((row,col))._setMoveCount()

                    #Finds all players' cities for end of round city management
                    if self.getCityAt((row,col)).getOwner() != NONE:

                        cityOfInterest = self.getCityAt((row,col))

                        #Give the identified city the amount of production it creates per round
                        cityOfInterest.production = cityOfInterest.production + cityOfInterest.productionPerRound

                        #Produces a unit for the city based on its set production type and amount of accumulated production
                        newUnit = cityOfInterest._produceUnit()

                        #If a unit was produced, place it in a legal spot
                        if (newUnit.getTypeString()!=NONE):
                            self._placeUnit(row, col, cityOfInterest, newUnit)
                        
                      
    def changeWorkFocusInCityAt(self, position, workFocus):
        """
        Not used in AlphaCiv
        """
        pass
    
    def changeProductionInCityAt(self, position, unitType):
        """
        Change the type of unit a city will produce next.
        Precondition: There is a city at "position"
        @param: "position" is the position of the city whose production should be changed
        @param: "unitType" is the new unit type to be produced by the city
        """
        self.getCityAt(position)._changeProduction(unitType)
    
    def performUnitActionAt(self, position):
        """
        Not used in AlphaCiv
        """
        pass


    def _placeUnit(self, row, col, cityOfInterest, newUnit):
        """
        A private method for the Game class that places units from a city at the end of a round.
        Place the unit by starting on the city tile, progressing to the spot directly north (if there is a unit on the city already)
        and then progressing to clockwise adjacent tiles until an open, legal spot is identified.
        @param: "row" is the row of the city
        @param: "col" is the column of the city
        @param: "cityOfInterest" is the city producing the unit
        @param: "newUnit" is the unit to be produced by the city
        """
        unitRow, unitCol = row, col

        level = 1
        unitPlaceable = False

        #Check if the city tile has no unit on it, if it does, denote it as a placeable space
        if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
            unitPlaceable = True

        #If the city tile was not open, commence searching for an open tile. Do not enter loop if unit board is full.
        while (not unitPlaceable and self._unitWorldNotFull(newUnit.getOwner())):
            unitRow = row
            unitCol = col

            #Checks all adjacent tiles to see if the unit can be placed in those spaces. If it can, break out of for loop checking placeability and while loop incrementing adjacency levels
            unitRow = unitRow - level
            if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                unitPlaceable = True
            
            if (unitPlaceable):
                break

            for unitCheck in range (0, level):
                unitCol = unitCol + 1
                if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                    unitPlaceable = True
                    break
                
            if (unitPlaceable):
                break

            for unitCheck in range (0, 2*level):
                unitRow = unitRow + 1
                if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                    unitPlaceable = True
                    break
                
            if (unitPlaceable):
                break

            for unitCheck in range (0, 2*level):
                unitCol = unitCol -1
                if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                    unitPlaceable = True
                    break

            if (unitPlaceable):
                break

            for unitCheck in range (0, 2*level):
                unitRow = unitRow - 1
                if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                    unitPlaceable = True
                    break

            if (unitPlaceable):
                break

            for unitCheck in range (0, level):
                unitCol = unitCol + 1
                if (self._unitPlaceable(unitRow, unitCol, cityOfInterest)):
                    unitPlaceable = True
                    break

            level = level + 1

        #Once a placeable unit tile has been found, place the unit if the unit world is not full.
        if (self._unitWorldNotFull(newUnit.getOwner())):
            self.unitBoard[unitRow][unitCol] = newUnit
            #If unit is being placed on an opponent's city, take over the city.
            if (self.getCityAt((unitRow,unitCol)).getOwner()!=NONE and self.getCityAt((unitRow, unitCol)).getOwner()!=newUnit.getOwner()):
                self.getCityAt((unitRow,unitCol)).owner = newUnit.getOwner()
    
    def _unitPlaceable(self, unitRow, unitCol, city):
        """
        A private method for the _placeUnit method within the Game class that checks if a unit can be placed in a given position by a city
        A unit is placeable in a position if:
        A) The position for the unit to be placed in are within the board constraints.
        B) The unit at the position of placement is not owned by the city who is placing the new unit. If an opponent's unit is on the tile, it is "defending" and is defeated off the tile.
        C) The tile at the position of placement is not a mountain or an ocean.
        @param: "unitRow" is the row of the position of placement.
        @param: "unitCol" is the column of the position of placement.
        @param: "city" is the city producing the unit.
        """
        return (unitRow>=0 and unitRow<WORLDSIZE and unitCol>=0 and unitCol<WORLDSIZE and self.getUnitAt((unitRow,unitCol)).getOwner()!= city.getOwner() and self.getTileAt((unitRow,unitCol)).getTypeString() != MOUNTAIN and self.getTileAt((unitRow,unitCol)).getTypeString() != OCEAN)

    def _unitWorldNotFull(self, owner):
        """
        A private method for the _placeUnit method within the Game class that checks the world to see if the unit board's legal positions are completely filled by the player's units
        @param: "owner" is the player being checked against the units' owners on the board
        @return: True if all legal unit tiles on the board are filled by the player of interests' units. False otherwise.
        """
        for unitRow in range (0,WORLDSIZE):
            for unitCol in range (0, WORLDSIZE):
                if (self.getUnitAt((unitRow,unitCol)).getOwner() != owner and self.getTileAt((unitRow,unitCol)).getTypeString()!=MOUNTAIN and self.getTileAt((unitRow,unitCol)).getTypeString() !=OCEAN):
                    return True
        return False


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        
class City:
    """
    City is a class that knows its owner, size, production type, and work force focus
    """

    #Constants for the amount of production that each unit costs for use in the City class
    _ARCHERCOST = 10
    _LEGIONCOST = 15
    _SETTLERCOST = 30
    
    def __init__(self, owner):
        """
        The constructor for the City class creates and initializes a number of instance variables for use with each city
        owner: The player who owns the city
        size: The size of the city
        production: The accumulated production
        productionPerRound: The production accumulated per round
        productionType: The type of unit produced by the city
        """
        self.owner = owner
        self.size = 1
        self.production = 0
        self.productionPerRound = 6
        self.productionType = NONE
        
    def getOwner(self):
        """
        Return the owner of the city
        @return: The player owning the city
        """
        return self.owner
    
    def getSize(self):
        """
        Return the size of the population
        @return: The population size
        """
        return self.size
    
    def getProduction(self):
        """
        Return the unit type being produced by the city
        @return: The unit type under production
        """
        return self.productionType
    
    def getWorkforceFocus(self):
        """
        Not used in AlphaCiv
        """
        pass
    
    def _changeProduction(self, unitType):
        """
        Private method for the City class to change the unit type under production
        @param: "unitType" is the unit type to be produced
        """
        self.productionType = unitType

    def _produceUnit(self):
        """
        Private method for the City class to produce a unit at the end of a round if able
        Only produces a unit if that type is selected as the productionType and if enough production is accumulated for that unit's cost
        @return: The new unit to be produced or a NONE unit if the necessary items for a unit to be produced are not available
        """
        if (self.productionType == ARCHER):
            if (self.production >= City._ARCHERCOST):
                self.production = self.production - City._ARCHERCOST
                return Unit(self.productionType, self.owner)

        if (self.productionType == LEGION):
            if (self.production >= City._LEGIONCOST):
                self.production = self.production - City._LEGIONCOST
                return Unit(self.productionType, self.owner)

        if (self.productionType == SETTLER):
            if (self.production >= City._SETTLERCOST):
                self.production = self.production - City._SETTLERCOST
                return Unit(self.productionType, self.owner)
        else:
            return Unit(NONE, NONE)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Unit:
    """
    Unit is a class that knows the units type name, owner, and defensive and attacking strengths
    """

    #Constants within Unit to define the move count for each unit type
    _ARCHERMOVECOUNT = 1
    _LEGIONMOVECOUNT = 1
    _SETTLERMOVECOUNT = 1
    
    def __init__(self, unitType, owner):
        """
        The constructor for the Unit class creates and initializes a number of instance variables for use with each unit
        unitType: The type of unit (ARCHER, SETTLER, LEGION, etc.)
        owner: The player who owns the unit
        moveCount = the number of tiles the unit can move per round (set through private method)
        """
        self.unitType = unitType
        self.owner = owner
        
        self._setMoveCount()
        
    def getTypeString(self):
        """
        Return the type of the unit
        @return: Unit type as defined in gameconstants.py
        """
        return self.unitType
    
    def getOwner(self):
        """
        Return the owner of the unit
        @return: The player controlling the unit
        """
        return self.owner
    
    def getMoveCount(self):
        """
        Return the move distance left for the unit for the current round
        @return: The move count
        """
        return self.moveCount
    
    def getDefensiveStrength(self):
        """
        Not used in AlphaCiv
        """
        pass
    def getAttackingStrength(self):
        """
        Not used in AlphaCiv
        """
        pass
    
    def _move(self, moveAmount):
        """
        Private method for the Unit class that allows the move count of the unit to be
        updated when a move occurs in the Game class
        @param: "moveAmount" the amount of tiles moved by the unit
        """
        self.moveCount = self.moveCount - moveAmount

    def _setMoveCount(self):
        """
        Private method for the Unit class that allows setting the unit's move count at unit creation
        as well as resetting of the unit's move count at the end of each round based on which unit type it is
        """
        if (self.getTypeString() == ARCHER):
            self.moveCount = Unit._ARCHERMOVECOUNT
        elif (self.getTypeString() == LEGION):
            self.moveCount =  Unit._LEGIONMOVECOUNT
        elif (self.getTypeString() == SETTLER):
            self.moveCount =  Unit._SETTLERMOVECOUNT


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Tile:
    """
    The Tile class knows its tile type
    """
    def __init__(self, tileType):
        """
        The constructor for the Tile class creates and initializes the instance variables needed for a tile
        tileType = The type of tile (MOUNTAIN, OCEAN, PLAINS, etc.)
        """
        self.tileType = tileType
    def getTypeString(self):
        """
        Return the tile type
        @return: The tile type as defined in gameconstants.py
        """
        return self.tileType
    

