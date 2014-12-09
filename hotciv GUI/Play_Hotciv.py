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


def main():
    VERSION = SemiCivFactory
    
    game = HotCiv(VERSION)
    editor = MiniDrawApplication("HotCiv v1.0", HotCivFactory(game))
    editor.open()
    editor.setTool(NullTool())

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
