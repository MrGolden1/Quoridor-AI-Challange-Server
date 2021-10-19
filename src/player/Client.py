from src.player.IBot    import *
from src.action.IAction import * 
from src.action.FencePlacing import * 
from src.action.PawnMove import * 
from src.GridCoordinates import *

ACTION_FILE = 'Action.txt'
INFORMATION = 'Information.txt'

class Client(IBot):

    def setExeName(self,exeNmae = None):
        self.exeName = exeNmae


    def play(self, board) -> IAction:
        #print('i am at {}'.format(self.pawn.coord))        
        #f = open("possible.txt",'w')
        #f.write(str(len(board.storedValidPawnMoves[self.pawn.coord])))
        #for x in board.storedValidPawnMoves[self.pawn.coord]:
        #    f.write('\n' + str(x))
        #f.write('\n')
        #f.write(str(len(board.storedValidFencePlacings)))
        #for x in board.storedValidFencePlacings:
        #    f.write('\n' + str(x))
        #f.close()
        os.system(self.exeName + " < " + INFORMATION +  " > " + ACTION_FILE)
        Input = open(ACTION_FILE , 'r').read()
        if Input == '':
            return None
        action =  Input.split()
        if len(action) == 2 and action[0] == "To":
            fromCoord = self.pawn.coord
            y , x = action[1].split(',')
            toCoord = GridCoordinates(int(y),int (x))
            move = PawnMove(fromCoord,toCoord)
            return move
        elif len(action) == 3 and action[0] == 'H-fence' and action[1] == 'at':
            y , x = action[2].split(',')
            coord = GridCoordinates(int(y) , int(x))
            fencePlace = FencePlacing(coord,Fence.DIRECTION.HORIZONTAL)
            return fencePlace
        elif len(action) == 3 and action[0] == 'V-fence' and action[1] == 'at':
            y , x = action[2].split(',')
            coord = GridCoordinates(int(y) , int(x))
            fencePlace = FencePlacing(coord,Fence.DIRECTION.VERTICAL)
            return fencePlace
        return None
    
    def info(self):
        return self.exeName