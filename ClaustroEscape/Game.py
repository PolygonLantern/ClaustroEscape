import pygame as pg
import random
import AStar
import Player

pg.init()
clock = pg.time.Clock()

gameWindowWidth: int = 1440
hudWidth: int = 440
windowHeight = 1000
hudHeight = 1000

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
    gridDiffX = (width + tileSize) // tileSize
    gridDiffY = (height + tileSize) // tileSize
    wallTiles = []
    for y in range(gridDiffY):
        xTiles = []
        for x in range(gridDiffX):
            if y == 0 or y == gridDiffY - 1:
                xTiles.append(3)
            else:
                if x == 0 or x == gridDiffX - 1:
                    xTiles.append(3)
                else:
                    xTiles.append(7)

        wallTiles.insert(y, xTiles)

    return wallTiles


def InitialiseWorld(width=gameWindowWidth, height=windowHeight):
    gridDiffX = width // tileSize
    gridDiffY = height // tileSize
    worldTiles = []

    for y in range(gridDiffY):
        xTiles = []
        for x in range(gridDiffX):
            if x == gridDiffX // 2 and y == gridDiffY // 2:
                xTiles.append(0)
            else:
                xTiles.append(random.randint(0, 1))
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
                    endTiles.append(3)
                else:
                    if x == stateDiff or x == len(originalState) - stateDiff - 1:
                        endTiles.append(3)
                    else:
                        endTiles.append(7)
            newTiles.insert(y, endTiles)

    return newTiles


''''
    Function that will keep track of the things that we need to draw on the screen.
'''


def RedrawLoop():
    world = World(worldData)
    walls = World(wallData)

    player.DrawPlayerTile()

    world.DrawWorld()
    walls.DrawWorld()

    mainGameSurface.blit(hudSurface, (gameWindowSize, 0))
    mainGameSurface.blit(wallsSurface, (0, 0))


def CheckForValidStartPoint(_worldData):
    possibleStarts = []

    for x in range(0, len(_worldData[1])):
        if _worldData[1][x] == 0:
            possibleStarts.append(x)

    def SetPlayerStartingPos():
        X = 0
        _hasAWay = False
        for i in possibleStarts:
            startPoint = [1, i]
            endPoint = [10, 10]
            cost = 1
            path = AStar.search(_worldData, cost, startPoint, endPoint)

            if path is not None:
                X = i
                _hasAWay = True
                break

        # print(path)
        return X, 1, _hasAWay

    _playerX, _playerY, hasAWay = SetPlayerStartingPos()

    # print(playerY, playerX)

    return _playerX, _playerY, hasAWay


''''
===============================================================================================================
                                    End of Function definition section
===============================================================================================================
'''

''''
===============================================================================================================
    Game Legend:
        (Tile Numbers - What they represent)
        0 - Ground/Gravel. The floor of the level
        3 - Shifting Walls
        2 - Obstacles
        4 - Player
===============================================================================================================
'''
''''
===============================================================================================================
                                         Variables definition section 
===============================================================================================================
'''

tileSize = 50
worldData = InitialiseWorld()
wallData = InitialiseWalls()

playerX = CheckForValidStartPoint(worldData)[0]
playerY = CheckForValidStartPoint(worldData)[1]

player = Player.Player((playerX, playerY), (tileSize, tileSize))
mainGameSurface = pg.display.set_mode((gameWindowWidth, windowHeight))
pg.display.set_caption("ClaustroEscape")

hudColour = (0, 255, 0)

# this variable is the playable size of the field. This way we can have some screen space for some HUD
gameWindowSize = gameWindowWidth - hudWidth
gameWindowWidth = gameWindowSize
''''
===============================================================================================================
                                 End of variables definition section 
===============================================================================================================
'''

''''
===============================================================================================================
                                         Surface definition section 
===============================================================================================================
'''
hudSurface = pg.Surface([hudWidth, hudHeight])
hudSurface.fill(hudColour)

wallsSurface = pg.Surface([gameWindowWidth, windowHeight])

playerSurface = pg.Surface([gameWindowWidth, windowHeight])

''''
===============================================================================================================
                                     End of surface definition section 
===============================================================================================================
'''

''''
===============================================================================================================
                                    Class definition section
===============================================================================================================
'''


class World:

    def __init__(self, _worldData):
        self.tileList = []

        # load sprites
        floorSprite = pg.image.load('Sprites/Tiles/FloorTile.png')
        spiralFloorSprite = pg.image.load('Sprites/Tiles/FloorTile1.png')
        testObstacle = pg.image.load('Sprites/Tiles/TestObstacle.png')
        testCenterSprite = pg.image.load('Sprites/Tiles/TestCenterSprite.png')

        rowCount = 0
        for row in _worldData:
            columnCount = 0
            for tile in row:
                # section for sprites to be drawn
                if tile == 0:
                    tile = DrawSprite(floorSprite, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)

                if tile == 1:
                    tile = DrawSprite(testObstacle, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)

                if tile == 3:
                    tile = DrawSprite(spiralFloorSprite, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)

                if tile == -1:
                    tile = DrawSprite(testCenterSprite, tileSize, columnCount, rowCount)
                    self.tileList.append(tile)

                # end of section
                columnCount += 1
            rowCount += 1

    def DrawWorld(self):
        for tile in self.tileList:
            wallsSurface.blit(tile[0], tile[1])


class Obstacle:
    def __init__(self, obstacleWidth, obstacleHeight):
        self.width = obstacleWidth
        self.height = obstacleHeight

    def GetWidth(self):
        return self.width

    def GetHeight(self):
        return self.height


class LevelObstacles(Obstacle):
    pass


''''
    Class that would create the walls that is displayed on the player's screen. This class will contain all the tiles 
    that will be used for the game as a number that will be used whenever the walls is drawn
'''


class CreateWalls(Obstacle):
    def __init__(self, _worldData, obstacleWidth, obstacleHeight):
        super().__init__(obstacleWidth, obstacleHeight)


''''
===============================================================================================================
                                            End of class definition section
===============================================================================================================
'''

''''
===============================================================================================================
                                            Start of World Initialisation
===============================================================================================================
'''
lookingForValidStartPoint = True

while lookingForValidStartPoint:

    if CheckForValidStartPoint(worldData)[2] is False:
        worldData = InitialiseWorld()
        wallData = InitialiseWalls()
        playerX = CheckForValidStartPoint(worldData)[0]
        playerY = CheckForValidStartPoint(worldData)[1]

    else:
        lookingForValidStartPoint = False

worldData[1][playerX] = player.GetPlayerTileNumber()

''''
===============================================================================================================
                                            End of World Initialisation
===============================================================================================================
'''

''''
===============================================================================================================
                                            Start of Main Loop
===============================================================================================================
'''

isGameRunning = True
while isGameRunning:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isGameRunning = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                gameWindowWidth -= tileSize
                windowHeight -= tileSize

                wallData = ShrinkWalls(gameWindowWidth, windowHeight)

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
