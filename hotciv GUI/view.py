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
        
        self.variances = {"YEAR":self.updateYear}
        editor.drawing().add(yearText)
        yearText.draw(editor)
                          
    def notify(notification):
        self.variance[notification]()

    def getValue(self, key):
        return self.variances[key]

    def updateYear(self):
        yr = game.getYear()

        if yr < 0:
            yearText.setText(str(yr)[1:] + " BC")
        else:
            yearText.setText(str(yr) + " AD")

        yearText.draw(self.editor)
            
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
                image_name = t.getTileType()
                if image_name == GameConstants.OCEANS:
                    image_name = image_name + getCoastlineCoding(self.game, p)
                    pass
                img = im.getImage(image_name)
                g.drawImage(img, xpos, ypos, None)


class CityFigure(ImageFigure):

  def __init__(self, c, p):
      ImageFigure.__init__(self, "city", p)
      self.position = p
      self.city = c
      
  def draw(self, g):
    #draw background color
    g.setColor(GfxConstants.getColorForPlayer(self.city.getOwner()))
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



yearText = TextFigure("4000 BC", Point(GfxConstants.AGE_TEXT_X, GfxConstants.AGE_TEXT_Y) )

