#
# RandomBot.py
# 

import random

from src.player.IBot    import *
from src.action.IAction import * 



class RandomBot(IBot):
    def play(self, board) -> IAction:
        # 1 chance over 3 to place a fence
        #validFencePlacings = board.validFencePlacings()
        if random.randint(0, 2) == 0 and self.remainingFences() > 0 and len(board.storedValidFencePlacings) > 0:
            randomFencePlacing = random.choice(board.storedValidFencePlacings)
            #for x in board.storedValidFencePlacings:
            #    print(x)
            #print("------------")
            #print(randomFencePlacing)
            attempts = 5
            while board.isFencePlacingBlocking(randomFencePlacing) and attempts > 0:
                #print("Cannot place blocking %s" % randomFencePlacing)
                randomFencePlacing = random.choice(board.storedValidFencePlacings)
                attempts -= 1
            if (attempts == 0):
                validPawnMoves = board.storedValidPawnMoves[self.pawn.coord]
                return random.choice(validPawnMoves)
            return randomFencePlacing
        else:
            validPawnMoves = board.storedValidPawnMoves[self.pawn.coord] #board.validPawnMoves(self.pawn.coord)
            m = random.choice(validPawnMoves)
            print(m)
            return m