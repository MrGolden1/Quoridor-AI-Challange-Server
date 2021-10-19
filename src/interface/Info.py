#
# Info.py
#

from lib.graphics            import *

from src.interface.IDrawable import *
from src.interface.Color     import *

class Info(IDrawable):
    def __init__(self, board):
        self.board = board
        self.width = board.infoBoardWidth
        self.top = board.height + board.innerSize * 2
        self.bottom = self.top + board.innerSize + board.squareSize * 2
        self.middle = board.width / 2
        self.space = (self.middle - (10 * board.innerSize) ) / 11
        self.p1 = []
        self.p2 = []

        self.lineBar1 =  Rectangle(Point(0 , self.board.height), Point( self.board.width , self.board.height))
        self.lineBar1.setWidth(2)
        self.lineBar1.setOutline(Color.BLUE.value)

        self.lineBar2 =  Rectangle(Point(0 , 0), Point( self.board.width ,0))
        self.lineBar2.setWidth(4)
        self.lineBar2.setOutline(Color.RED.value)

        for i in range(1 ,11):
            r = Rectangle(Point(self.space * i + ( i - 1 ) * board.innerSize , self.top) , Point(self.space * i + i * board.innerSize , self.bottom))
            r.setFill(Color.BLUE.value)
            r.setWidth(0)
            self.p1.append(r)

            r = Rectangle(Point(( self.space * i + ( i - 1 ) * board.innerSize ) + self.middle , self.top) , Point( ( self.space * i + i * board.innerSize ) + self.middle , self.bottom))
            r.setFill(Color.RED.value)
            r.setWidth(0)
            self.p2.append(r)

    def draw(self):
        for r in self.p1 :
            r.undraw()
        for r in self.p2:
            r.undraw()

        self.p1.clear()
        self.p2.clear()

        for i in range(1 ,11):
            r = Rectangle(Point(self.space * i + ( i - 1 ) * self.board.innerSize , self.top) , Point(self.space * i + i * self.board.innerSize , self.bottom))
            r.setFill(Color.BLUE.value)
            r.setWidth(0)
            self.p1.append(r)

            r = Rectangle(Point(( self.space * i + ( i - 1 ) * self.board.innerSize ) + self.middle , self.top) , Point( ( self.space * i + i * self.board.innerSize ) + self.middle , self.bottom))
            r.setFill(Color.RED.value)
            r.setWidth(0)
            self.p2.append(r)
        #self.lineBar1.draw(self.board.window)
        #self.lineBar2.draw(self.board.window)
        for r in self.p1 :
            r.draw(self.board.window)
        for r in self.p2:
            r.draw(self.board.window)

    def updateLines(self):
        self.lineBar1.undraw()
        self.lineBar2.undraw()
        self.lineBar1.draw(self.board.window)
        self.lineBar2.draw(self.board.window)

    def updateInfo(self , player ):
        if not INTERFACE:
            return 
        if player.color == Color.BLUE:
            self.p1[-1].undraw()
            self.p1[-1].setFill(Color.Lighter(Color.BLUE.value ,0.8))
            self.p1[-1].draw(self.board.window)
            self.p1.pop()
        elif player.color == Color.RED :
            self.p2[0].undraw()
            self.p2[0].setFill(Color.Lighter(Color.RED.value , 0.8))
            self.p2[0].draw(self.board.window)
            self.p2.pop(0)

