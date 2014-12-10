from __future__ import with_statement
import sys
sys.path.append("minidrawmod.jar")

from minidraw.standard import *
from minidraw.framework import *

from java.awt import *
from java.awt.event import *
from javax.swing import *

import gfxconstants as GfxConstants
import gameconstants as GameConstants

from view import *
from hotciv import *


class ChangeAgeTool(NullTool):

    def __init__(self, game):
        self.game = game

    def mouseDown(self, e, x, y):
        #self.game.moveUnit((5,3), (6,3), screenPosFrom=(x,y), screenPosTo=(x, y+15))
        #self.game.endOfRound()
        self.game.changeCityProductionAt((4,5), "archer")
        self.game.endOfTurn()

class MoveUnitTool(NullTool):

    def __init__(self, game):
        self.game = game
        self.fromScreen = (0,0)
        
        self.fromPos = (0,0)
        self.toPos = (0,0)

    def mouseDown(self, e, x, y):
        self.fromScreen = (x,y)
        self.fromPos = GfxConstants.getPositionFromXY(x,y)

    def mouseUp(self, e, x, y):
        self.toPos = GfxConstants.getPositionFromXY(x,y)
        screenPosTo = (x,y)
        self.game.moveUnit(self.fromPos, self.toPos, screenPosFrom=self.fromScreen, screenPosTo=screenPosTo)

    
def main():
    VERSION = SemiCivFactory
    
    game = HotCiv(VERSION)
    editor = MiniDrawApplication("HotCiv v1.0", HotCivFactory(game))
    editor.open()
    editor.setTool(ChangeAgeTool(game))

    observer = GameObserver(game, editor)

class HotCivFactory(Factory):

    def __init__(self, g):
        self.game = g
        
    def createDrawingView(self, editor):
        return MapView(editor, self.game)

    def createDrawing(self, editor):
        return StandardDrawing()

    def createStatusField(self, editor):
        return None
    
    
if __name__ == "__main__":
    main()
