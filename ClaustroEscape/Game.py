import pygame as pg
from pygame.locals import *

pg.init()
clock = pg.time.Clock()

gameWindowWidth: int = 1440
hudWidth: int = 440

windowHeight = 1000
hudHeight = 1000
tileSize = 200
worldData = []

mainGameSurface = pg.display.set_mode((gameWindowWidth, windowHeight))
pg.display.set_caption("ClaustroEscape")

hudColour = (0, 255, 0)

# this variable is the playable size of the field. This way we can have some screen space for some HUD
gameWindowSize = gameWindowWidth - hudWidth
gameWindowWidth = gameWindowSize

''''
===============================================================================================================
                                         Surface definition section 
===============================================================================================================
'''
hudSurface = pg.Surface([hudWidth, hudHeight])
hudSurface.fill(hudColour)

wallsSurface = pg.Surface([gameWindowWidth, windowHeight])

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
        pg.draw.line(mainGameSurface, (255, 255, 255), (0, line * tileSize), (gameWindowWidth, line * tileSize))
        pg.draw.line(mainGameSurface, (255, 255, 255), (line * tileSize, 0), (line * tileSize, windowHeight))


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
    Function that will keep track of the things that we need to draw on the screen.
'''


def RedrawLoop():
    mainGameSurface.blit(hudSurface, (hudDifference, 0))
    mainGameSurface.blit(wallsSurface, (0, 0))


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
    Class that would create the walls that is displayed on the player's screen. This class will contain all the tiles 
    that will be used for the game as a number that will be used whenever the walls is drawn
'''


class Player:
    # load player sprites
    playerSprite = pg.image.load('Sprites/Player/Player_Right.png')

    def __init__(self, colCount, rowCount, width, height):
        self.rowPos = rowCount
        self.colPos = colCount
        self.width = width
        self.height = height
        self.tileNumber = 4

    def DrawPlayerTile(self):
        return DrawSprite(self.playerSprite, tileSize, self.colPos, self.rowPos)

    def GetPlayerX(self):
        return self.rowPos

    def GetPlayerY(self):
        return self.colPos

    def GetPlayerTileNumber(self):
        return self.tileNumber


class CreateWalls:
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

    def DrawShiftingWalls(self):
        for tile in self.tileList:
            wallsSurface.blit(tile[0], tile[1])


''''
===============================================================================================================
                                            End of class definition section
===============================================================================================================
'''

''''
===============================================================================================================
                                            Start of Main Loop
===============================================================================================================
'''

worldData = InitialiseWalls()
isGameRunning = True
while isGameRunning:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isGameRunning = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                walls = CreateWalls(worldData)

                gameWindowWidth -= tileSize
                windowHeight -= tileSize

                walls.DrawShiftingWalls()
                worldData = ShrinkWalls(gameWindowWidth, windowHeight)

    # set a frame rate
    clock.tick(60)

    RedrawLoop()

    pg.display.update()

pg.quit()
''''
===============================================================================================================
                                            End of Main Loop
===============================================================================================================
'''