import sys
sys.path.append("minidrawmod.jar")

from minidraw.framework import *
from minidraw.standard import *
from java.awt import *

import gfxconstants as GfxConstants
import gameconstants as GameConstants


class GameObserver:
    def __init__(self, game, editor):
        self.game = game
        self.editor = editor
        game.addObserver(self)
        
        self.variances = {"YEAR":self.updateYear,
                          "WORKFORCE":self.updateWorkforce,
                          "PRODUCTION":self.updateProduction,
                          "PLAYERTURN":self.updatePlayerInTurn,
                          "UNITMOVE":self.updateUnitPlacement}
        
        editor.drawing().add(yearText)

        # Define graphics objects
        self.workforceLoc = Point(GfxConstants.WORKFORCEFOCUS_X, GfxConstants.WORKFORCEFOCUS_Y)
        self.productionLoc = Point(GfxConstants.CITY_PRODUCTION_X, GfxConstants.CITY_PRODUCTION_Y)
        self.playerInTurnLoc = Point(GfxConstants.TURN_SHIELD_X, GfxConstants.TURN_SHIELD_Y)
        
        self.workforcePic = ImageFigure("hammer", self.workforceLoc)
        self.productionPic = ImageFigure("legion", self.productionLoc)
        self.playerInTurnPic = ImageFigure("redshield", self.playerInTurnLoc)
        
        editor.drawing().add(self.workforcePic)
        editor.drawing().add(self.productionPic)
        editor.drawing().add(self.playerInTurnPic)
        
    def notify(self, notification, *args):
        self.variances[notification](*args)

    def getValue(self, key):
        return self.variances[key]

    def updateYear(self):
        yr = self.game.getAge()

        if yr < 0:
            yearText.setText(str(yr)[1:] + " BC")
        else:
            yearText.setText(str(yr) + " AD")

    def updateWorkforce(self, pos):
        focus = self.game.getCityAt(pos).getWorkforceFocus()
        
        if  focus == "production":
            self.workforcePic.set("hammer", self.workforceLoc)
        elif focus == "food":
            self.workforcePic.set("apple", self.workforceLoc)

    def updateProduction(self, pos):
        unit = self.game.getCityAt(pos).getProduction()
        
        if unit == "legion":
            self.productionPic.set("legion", self.productionLoc)
        elif unit == "settler":
            self.productionPic.set("settler", self.productionLoc)
        elif unit == "archer":
            self.productionPic.set("archer", self.productionLoc)

    def updatePlayerInTurn(self):
        team = self.game.getPlayerInTurn() + "shield"

        self.playerInTurnPic.set(team, self.playerInTurnLoc)

    def updateUnitPlacement(self, posFrom, posTo, screenPosFrom, screenPosTo):
        tile = self.game.getTileAt(posFrom).getTileType()
        unit = self.game.getUnitAt(posFrom).getUnitType()

        toX, toY = screenPosTo
        fromX, fromY = screenPosFrom
        
        image = ImageFigure(unit, Point(toX, toY))
        editor.drawing().add(image)

        tile_image = ImageFigure(tile, Point(fromX, fromY))
        editor.drawing().add(tile_image)
            
class MapView(StdViewWithBackground):
    
    def __init__(self, editor, game):
        StdViewWithBackground.__init__(self, editor, "hotciv-background")
        self.game = game

    def drawBackground(self, g):
        StdViewWithBackground.drawBackground(self, g)

        im = ImageManager.getSingleton()
        for r in range(GameConstants.WORLDSIZE):
            for c in range(GameConstants.WORLDSIZE):
                p = (r,c)
                xpos = GfxConstants.getXFromColumn(c)
                ypos = GfxConstants.getYFromRow(r)
                
                t = self.game.getTileAt(p)
                tile_name = t.getTileType()
                
                u = self.game.getUnitAt(p)
                unit_name = u.getUnitType()

                c = self.game.getCityAt(p)
                
                if tile_name == GameConstants.OCEANS:
                    tile_name = tile_name + getCoastlineCoding(self.game, p)
                    pass
                
                tile = im.getImage(tile_name)
                g.drawImage(tile, xpos, ypos, None)

                if unit_name != None:
                    unit = im.getImage(unit_name)
                    g.drawImage(unit, xpos, ypos, None)

                if c != False:
                    city = CityFigure(c, Point(xpos,ypos))
                    city.draw(g)
                    
                    
class CityFigure(ImageFigure):

  def __init__(self, c, p):
      ImageFigure.__init__(self, "city", p)
      self.position = p
      self.city = c
      
  def draw(self, g):
    #draw background color
    color = self.city.getOwner()
    if color == "blue":
        g.setColor(Color.blue)
    else:
        g.setColor(Color.red)
        
    g.fillRect( self.position.x+1, self.position.y+1, 
                GfxConstants.TILESIZE-2, 
                GfxConstants.TILESIZE-2 )
  
    ImageFigure.draw(self,g)

    g.setColor(Color.white)

    font = Font("Helvetica", Font.BOLD, 24)
    g.setFont(font);
    
    size = str(self.city.getSize())
    g.drawString(size,
                 self.position.x + GfxConstants.CITY_SIZE_OFFSET_X,
                 self.position.y + GfxConstants.CITY_SIZE_OFFSET_Y);


def getCoastlineCoding(game, center):
    row,col = center
    coding = ['0','0','0','0']

    offsetRow = [-1,0,+1,0]
    offsetCol = [ 0,+1,0,-1]

    for i in range(4):
        r = row+offsetRow[i]
        c = col+offsetCol[i]
        if (0 <= r < GameConstants.WORLDSIZE and
            0 <= c < GameConstants.WORLDSIZE and
            game.getTileAt((r,c)).getTileType() != GameConstants.OCEANS):

            coding[i] = '1'
            
    return "".join(coding);


class TextFigure(AbstractFigure):

    def __init__(self, text, position):
        self.position = position
        self.text = text
        self.fFont = Font("Serif", Font.BOLD, 20)
        self.metrics = None
      
    def setText(self, newText):
        self.willChange()
        self.text = newText
        self.changed()
        
    def basicMoveBy(self, dx, dy):
        self.position.translate(dx, dy)

    def displayBox(self):
        extent = self.__textExtent()
        return Rectangle(self.position.x, self.position.y, extent.width, extent.height)

    def draw(self, g):
        g.setFont(self.fFont);
        g.setColor(Color.white);
        self.metrics = g.getFontMetrics(self.fFont);
        g.drawString(self.text, self.position.x, self.position.y + self.metrics.getAscent())


    def __textExtent(self):
        # metrics may not have been defined yet if no drawing
        # has occurred, however the error is removed upon first
        # redrawing.

        if not self.metrics:
            fWidth = 50
            fHeight = 20
        else:
            fWidth = self.metrics.stringWidth(self.text)
            fHeight = self.metrics.getHeight()

        return Dimension(fWidth, fHeight)


# More graphics objects
yearText = TextFigure("4000 BC", Point(GfxConstants.AGE_TEXT_X, GfxConstants.AGE_TEXT_Y) )
