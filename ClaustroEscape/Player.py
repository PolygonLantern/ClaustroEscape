import pygame as pg


def DrawSprite(sprite, _tileSize, colCount, rowCount):
    img = pg.transform.scale(sprite, (_tileSize, _tileSize))
    imgRect = img.get_rect()
    imgRect.x = colCount * _tileSize
    imgRect.y = rowCount * _tileSize
    tile = (img, imgRect)

    return tile


class Player:
    # load player sprites
    playerSprite = pg.image.load('Sprites/Player/Player_Right.png')

    def __init__(self, playerPosition, width_height):
        self.rowPos = playerPosition[0]
        self.colPos = playerPosition[1]
        self.width = width_height[0]
        self.height = width_height[1]
        self.tileNumber = 10

    def DrawPlayerTile(self):
        return DrawSprite(self.playerSprite, self.width, self.colPos, self.rowPos)

    def GetPlayerX(self):
        return self.rowPos

    def GetPlayerY(self):
        return self.colPos

    def GetPlayerTileNumber(self):
        return self.tileNumber
