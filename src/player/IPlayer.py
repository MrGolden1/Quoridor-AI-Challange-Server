#
# IPlayer.py
# 

from src.action.IAction import * 
from src.action.FencePlacing import *


class IPlayer:
    def __init__(self, name = None, color = None , ):
        self.name   = name
        self.color  = color
        self.pawn   = None
        self.fences = []
        self.score  = 0
        self.startPosition = None
        self.endPositions = []
        self.fail = 0

    def play(self, board) -> IAction:
        pass

    def info(self) -> str:
        pass

    def movePawn(self, coord):
        #print("player %s moved his pawn to %s" % (self.name, coord))
        self.pawn.move(coord)

    def placeFence(self, coord, direction):
        #print("player %s place %s" % (self.name, FencePlacing(coord, direction)))
        fence = self.fences.pop()
        fence.place(coord, direction)

    def remainingFences(self):
        return len(self.fences)

    def hasWon(self):
        for endPosition in self.endPositions:
            if self.pawn.coord == endPosition:
                return True
        return False

    def __str__(self):
        return "%s (%s)" % (self.name, self.color.name)


