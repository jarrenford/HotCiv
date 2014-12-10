# gfxconstants.py

import gameconstants as gc
import java

## The size of the tile images used, in pixels
TILESIZE = 30;

## Offset the world map by these x and y values in pixels
MAP_OFFSET_X = 19;
MAP_OFFSET_Y = 15;

## When drawing the population size number on top of
## the city graphics, offset this x,y in pixels from
## top left corner of tile
CITY_SIZE_OFFSET_X = 8;
CITY_SIZE_OFFSET_Y = 24;

## When drawing units, this Y offset is subtracted to position their
## 'feet' on the tile
UNIT_OFFSET_Y = 0;
  
## === Constants that define positions for props on the gfx display
TURN_SHIELD_X = 559;
TURN_SHIELD_Y = 64;
AGE_TEXT_X = 535;
AGE_TEXT_Y = 23;
  
UNIT_SHIELD_X = 594;
UNIT_SHIELD_Y = 188;
UNIT_COUNT_X = 598;
UNIT_COUNT_Y = 256;

CITY_SHIELD_X = 595;
CITY_SHIELD_Y = 342;
WORKFORCEFOCUS_X = 590;
WORKFORCEFOCUS_Y = 444;
CITY_PRODUCTION_X = 595;
CITY_PRODUCTION_Y = 400;

# === Names of GIF files loaded by image manager
RED_SHIELD = "redshield";
BLUE_SHIELD = "blueshield";
NOTHING = "black";
  
def getXFromColumn(column):
    return column * TILESIZE + MAP_OFFSET_X
  
def getYFromRow(row):
    return row * TILESIZE + MAP_OFFSET_Y  

def getColorForPlayer(p):
    if p == gc.RED:
        return java.awt.Color.RED
    elif p == gc.BLUE:
        return java.awt.Color.CYAN
##    elif p == gc.YELLOW:
##        return java.awt.Color.YELLOW
##    elif p == gc.GREEN:
##        return java.awt.Color.GREEN
##    return java.awt.Color.WHITE

def getPositionFromXY(x,y):
    return ((y - MAP_OFFSET_Y) / TILESIZE, (x - MAP_OFFSET_X) / TILESIZE) 

