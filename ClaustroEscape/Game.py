import pygame as pg
from pygame.locals import *

pg.init()

gameWindowWidth: int = 1440
hudWidth: int = 440

windowHeight = 1000
hudHeight = 1000
tileSize = 50
worldData = []

window = pg.display.set_mode((gameWindowWidth, windowHeight))
pg.display.set_caption("ClaustroEscape")
testColour = (0, 255 , 0)


# this variable makes no sense
hudDifference = gameWindowWidth - hudWidth

gameWindowWidth = hudDifference
# Take the pixels for the hud out of the gameWindow's width
''''
===============================================================================================================
                                         Surface definition section 
===============================================================================================================
'''
hudSurface = pg.Surface([hudWidth, hudHeight])
hudSurface.fill(testColour)


''''
===============================================================================================================
                                     End of surface definition section 
===============================================================================================================
'''

''''
===============================================================================================================
                                         Function definition section 
===============================================================================================================
'''


# code from https://github.com/russs123/Platformer/blob/master/Part_1-Create_World/platformer_tut1.py
def draw_grid():
    for line in range(0, 20):
        pg.draw.line(window, (255, 255, 255), (0, line * tileSize), (gameWindowWidth, line * tileSize))
        pg.draw.line(window, (255, 255, 255), (line * tileSize, 0), (line * tileSize, windowHeight))


def DrawSprite(sprite, _tileSize, colCount, rowCount):
    img = pg.transform.scale(sprite, (_tileSize, _tileSize))
    imgRect = img.get_rect()
    imgRect.x = colCount * _tileSize
    imgRect.y = rowCount * _tileSize
    tile = (img, imgRect)

    return tile


'''' 
Function that will create the walls and will return 2 dimensional array based on the height and width of the 
screen 
'''


def InitialiseWalls(width=gameWindowWidth, height=windowHeight):
    gridDiffX = width // tileSize
    gridDiffY = height // tileSize
    worldTiles = []
    for y in range(gridDiffY):
        xTiles = []
        for x in range(gridDiffX):
            if y == 0 or y == gridDiffY - 1:
                xTiles.append(1)
            else:
                if x == 0 or x == gridDiffX - 1:
                    xTiles.append(1)
                else:
                    xTiles.append(0)
        worldTiles.insert(y, xTiles)

    return worldTiles


'''' 
    Function that will "shrink" the walls. This will be called upon movement
    :parameter width and height- the width and the height of the new walls, they would be equal by default to the 
    windowSize - tileSize, giving the player 2 rounds before the shrinking, the first shrinking will be with resolution 
    of the screen 950,950 which will not move the wall at any direction since the number is not even. However on the 
    next movement the numbers will come to 900, 900 which will make the wall shrink
'''


def ShrinkWalls(width, height):
    originalState = InitialiseWalls()
    smallerState = InitialiseWalls(width, height)
    stateDiff = (len(originalState) - len(smallerState)) // 2

    newTiles = []

    if len(originalState) == len(smallerState):
        return originalState
    else:
        for y in range(len(originalState)):
            endTiles = []
            for x in range(len(originalState)):
                if y == stateDiff or y == len(originalState) - stateDiff - 1:
                    endTiles.append(1)
                else:
                    if x == stateDiff or x == len(originalState) - stateDiff - 1:
                        endTiles.append(1)
                    else:
                        endTiles.append(0)
            newTiles.insert(y, endTiles)

    return newTiles


''''
===============================================================================================================
                                    End of Function definition section
===============================================================================================================
'''

''''
===============================================================================================================
                                    Class definition section
===============================================================================================================
'''

''''
    Class that would create the world that is displayed on the player's screen. This class will contain all the tiles 
    that will be used for the game as a number that will be used whenever the world is drawn
'''


class CreateWorld:
    def __init__(self, _worldData):
        self.tileList = []

        # load sprites
        floorSprite = pg.image.load('Sprites/Tiles/FloorTile.png')
        spiralFloorSprite = pg.image.load('Sprites/Tiles/FloorTile1.png')

        rowCount = 0
        for row in _worldData:
            columnCount = 0
            for tile in row:
                # section for sprites to be drawn
                if tile == 1:
                    tile = DrawSprite(floorSprite, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)

                if tile == 2:
                    tile = DrawSprite(spiralFloorSprite, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)
                # end of section
                columnCount += 1
            rowCount += 1

    def DrawWorld(self):
        for tile in self.tileList:
            window.blit(tile[0], tile[1])


class Player:
    def __init__(self, x):
        self.x = x


''''
===============================================================================================================
                                            End of class definition section
===============================================================================================================
'''

worldData = InitialiseWalls()

player = Player(5)

isGameRunning = True
while isGameRunning:

    window.blit(hudSurface, (hudDifference, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isGameRunning = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                world = CreateWorld(worldData)

                gameWindowWidth -= tileSize
                windowHeight -= tileSize
                world.DrawWorld()
                worldData = ShrinkWalls(gameWindowWidth, windowHeight)

    pg.display.update()

pg.quit()
