# stub.py

import sys
sys.path.append(".")


import gameconstants as GameConstants


class StubTile:
  def __init__(self, ttype):
    self.type = ttype;

  def getTypeString(self):
    return self.type


class StubCity:
    
    redOwns = True
  
    def makeAChange(self):
        self.redOwns = not self.redOwns
  
    def getOwner(self):
        return GameConstants.RED if self.redOwns else GameConstants.BLUE

    def getSize(self):
        return 4 if self.redOwns else 9


class StubGame:

    def __init__(self, which):
        self.defineWorld(which)
    
    def getTileAt(self,  p):
        return self.world[p]


    def defineWorld(self, worldType):
        self.world = {}
        if worldType == 1:
            layout = [
                "...ooMooooo.....",
                "..ohhoooofffoo..",
                ".oooooMooo...oo.",
                ".ooMMMoooo..oooo",
                "...ofooohhoooo..",
                ".ofoofooooohhoo.",
                "...ooo..........",
                ".ooooo.ooohooM..",
                ".ooooo.oohooof..",
                "offfoooo.offoooo",
                "oooooooo...ooooo",
                ".ooMMMoooo......",
                "..ooooooffoooo..",
                "....ooooooooo...",
                "..ooohhoo.......",
                ".....ooooooooo.."
                ]
        else: 
            layout = [
                "...ooo..........",
                ".ooooo.ooohooM..",
                ".ooooo.oohooof..",
                "offfoooo.offoooo",
                "oooooooo...ooooo",
                ".ooMMMoooo......",
                ".....ooooooooo..",
                "...ooMooooo.....",
                "..ohhoooofffoo..",
                "...ofooohhoooo..",
                ".oooooMooo...oo.",
                ".ooMMMoooo..oooo",
                ".ofoofooooohhoo.",
                "..ooooooffoooo..",
                "....ooooooooo...",
                "..ooohhoo......."
                ]
         
        for r in range(GameConstants.WORLDSIZE):
            line = layout[r]
            for c in range(GameConstants.WORLDSIZE):
                tileChar = line[c]
                ttype = "error"
                if   tileChar == '.': ttype = GameConstants.OCEANS
                elif tileChar == 'o': ttype = GameConstants.PLAINS
                elif tileChar == 'M': ttype = GameConstants.MOUNTAINS
                elif tileChar == 'f': ttype = GameConstants.FOREST
                elif tileChar == 'h': ttype = GameConstants.HILLS
                self.world[(r,c)] = StubTile(ttype)

