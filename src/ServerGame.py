#
# Game.py
# 

import random
import threading
import psutil
import queue

from src.Settings            import *
from src.interface.Color     import *
from src.interface.Board     import *
from src.interface.Pawn      import *
from src.player.Human        import *
from src.action.PawnMove     import *
from src.action.FencePlacing import *
from src.Path                import *
from src.player.Client       import *

INFORMATION = 'Information.txt'

class ThreadWithReturnValue(object):
    def __init__(self, target=None, args=(), **kwargs):
        self._que = queue.Queue()
        self._t = threading.Thread(target=lambda q,arg1,kwargs1: q.put(target(*arg1, **kwargs1)) ,
                args=(self._que, args, kwargs), )
        self._t.start()

    def join(self):
        self._t.join()
        return self._que.get()


class ServerGame:
    """
    Define players and game parameters, and manage game rounds.
    """

    DefaultColorForPlayer = [
        Color.RED,
        Color.BLUE,
        Color.GREEN,
        Color.ORANGE
    ]

    DefaultNameForPlayer = [
        "1",
        "2",
        "3",
        "4"
    ]

    def __init__(self, players, cols = 9, rows = 9, totalFenceCount = 20, squareSize = 32, innerSize = None , timeLimit = 1):
        if innerSize is None:
            innerSize = int(squareSize/8)
        self.totalFenceCount = totalFenceCount
        self.Playerfile = 'CURRENT_PLAYER.TXT'
        self.timeLimit = timeLimit
        # Create board instance
        board = Board(self, cols, rows, squareSize, innerSize)
        # Support only 2 or 4 players
        playerCount = min(int(len(players)/2)*2, 4)
        self.players = []
        # For each player
        for i in range(playerCount):
            if not INTERFACE and isinstance(players[i], Human):
                raise Exception("Cannot launch a blind game with human players")
            # Define player name and color
            if players[i].name is None:
                players[i].name = ServerGame.DefaultNameForPlayer[i]
            if players[i].color is None:
                players[i].color = ServerGame.DefaultColorForPlayer[i]
            # Initinialize player pawn
            players[i].pawn = Pawn(board, players[i])
            # Define player start positions and targets
            players[i].startPosition = board.startPosition(i)
            players[i].endPositions = board.endPositions(i)
            self.players.append(players[i])
        self.board = board
    def checkingTime(self , exeName):
        for sec in range(1 , self.timeLimit + 1):
            time.sleep(1)
            if self.doneTheTurn == True:
                return
            print('\r' + str(sec) + ' seconds passed' , end ='')
        #os.startfile("KillProcess.exe")
        #print(exeName)
        for proc in psutil.process_iter():
            #print(proc.name())
        # check whether the process name matches
            if proc.name() == exeName:
                try:
                    proc.kill()
                except(psutil.AccessDenied):
                    pass
                self.timeIsOver = True
                print('\nTime Finished')
    def start(self, roundCount = 1,firstTurn =1,LOG=''):
        namewin=''
        """
        Launch a series of rounds; for each round, ask successively each player to play. 
        """
        roundNumberZeroFill = len(str(roundCount))
        # For each round
        playerCount = len(self.players)
        #firstTurn = random.randrange(playerCount) 
        for roundNumber in range(1, roundCount + 1):
            # Reset board stored valid pawn moves & fence placings, and redraw empty grid
            self.board.initStoredValidActions()
            self.board.draw()
            #print("ROUND #%s: " % str(roundNumber).zfill(roundNumberZeroFill), end="")
            playerCount = len(self.players)
            # Share fences between players
            playerFenceCount = int(self.totalFenceCount/playerCount)
            self.board.fences, self.board.pawns = [], []
            #report of game 
            logs = []
            # For each player
            for i in range(playerCount):
                player = self.players[i]
                # Place player pawn at start position and add fences to player stock
                player.pawn.place(player.startPosition)
                for j in range(playerFenceCount):
                    player.fences.append(Fence(self.board, player))
            placedFences = []
            # Define randomly first player (coin toss)
            currentPlayerIndex = ( firstTurn + 1 ) % playerCount
            firstTurn += 1
            finished = False
            while not finished:
                player = self.players[currentPlayerIndex]
                print(player.name + ' : ' + str(player.color) )
                print(self.players[(currentPlayerIndex + 1) % playerCount].name + ' : ' + str(self.players[(currentPlayerIndex + 1) % playerCount].color) )
                #self.board.drawOnConsole()
                print('Turn of ' + player.name + ':')
                f = open(INFORMATION , 'w')
                f.write(str(player.pawn.coord).replace(',' , ' ') + '\n')
                if player.endPositions[0].row == 0:
                    f.write('UP\n')
                else :
                    f.write('DOWN\n')
                f.write(str(player.remainingFences()) + '\n')
                f.write(str(self.players[(currentPlayerIndex + 1) % playerCount].pawn.coord).replace(',' , ' ') + '\n')
                f.write(str(len(placedFences)) + '\n')
                for x in placedFences:
                    f.write(str(x).replace(',' , ' ').replace('at' ,'') + '\n')
                f.close()
                f = open("Logs.txt",'w')
                for m in logs:
                    f.write(m + '\n')
                f.close()
                #input()
                # The player chooses its action (manually for human players or automatically for bots)
                if isinstance(player,Client):
                    exe = player.info()
                    open(self.Playerfile,'w').write(exe)
                    self.timeIsOver = False
                    self.doneTheTurn = False
                    counter = threading.Thread(target = self.checkingTime , args = (exe,))
                    action = ThreadWithReturnValue(target =player.play , args =(self.board, ))
                    counter.start()                 
                    action = action.join()
                    self.doneTheTurn = True
                    counter.join()
                else :
                    action = player.play(self.board)

                if self.timeIsOver == True:
                    logs.append(player.name + ': ' + 'Over the time limit!')
                    currentPlayerIndex = (currentPlayerIndex + 1) % playerCount
                    os.system('cls')
                    continue


                if isinstance(action, PawnMove):
                    if self.board.isValidPawnMove(action.fromCoord,action.toCoord,self.board.storedValidPawnMoves[player.pawn.coord]):
                        player.movePawn(action.toCoord)
                        logs.append(player.name + ': ' + str(action))
                    else :
                        logs.append(player.name + ': ' + str(action) + ' Invlaid Pawn Move !' )
                        player.fail += 1
                    # Check if the pawn has reach one of the player targets
                    if player.hasWon():
                        finished = True
                        namewin=player.name
                        print("Player %s won" % player.name)
                        logs.append("Player %s won" % player.name)
                        player.score += 1
                        break
                elif isinstance(action, FencePlacing):
                    validFencePlacings = self.board.storedValidFencePlacings #board.validFencePlacings()
                    if self.board.isValidFencePlacing(action.coord, action.direction) and (action in validFencePlacings):
                        if player.remainingFences() == 0:
                            logs.append(player.name + ': ' + str(action) + ' you used all fences !')
                            player.fail += 1
                        elif self.board.isFencePlacingBlocking(action):
                            logs.append(player.name + ': ' + str(action) + ' Can\'t block the pawns ,Invlaid Fence Placing !' )
                            player.fail += 1
                        else:
                            player.placeFence(action.coord, action.direction)
                            placedFences.append(action)
                            self.board.info.updateInfo(player)
                            logs.append(player.name + ': ' + str(action))
                    else:
                        logs.append(player.name + ': ' + str(action) + ' Invlaid Fence Placing !')
                        player.fail += 1
                elif action == None:
                    logs.append(player.name + ': ' + str(action) + ' Uknown Command !')
                    player.fail += 1
                elif isinstance(action, Quit):
                    finished = True
                    print("Player %s quitted" % player.name)
                if(player.fail > 4):
                    finished = True
                    namewin=self.players[(currentPlayerIndex + 1) % playerCount].name
                    print('Too many Invalid action from player %s ' % player.name)
                    print("Player %s won" %  self.players[(currentPlayerIndex + 1) % playerCount].name)
                    logs.append("Player %s won" %  self.players[(currentPlayerIndex + 1) % playerCount].name)
                    self.players[(currentPlayerIndex + 1) % playerCount].score += 1
                    break
                currentPlayerIndex = (currentPlayerIndex + 1) % playerCount
                if INTERFACE:
                    #self.board.info.updateLines()
                    time.sleep(TEMPO_SEC)
                os.system('cls')
            input()
        print()
        f = open(LOG,'w')
        for m in logs:
            f.write(m + '\n')
        f.close()

        return namewin

        #self.board.drawOnConsole()
        # Display final scores
        print("FINAL SCORES: ")
        bestPlayer = self.players[0]
        for player in self.players:
            print("- %s: %d" % (str(player), player.score))
            if player.score > bestPlayer.score: 
            	bestPlayer = player
        print("Player %s won with %d victories!" % (bestPlayer.name, bestPlayer.score))

    def end(self):
        """
        Called at the end in order to close the window.
        """
        time.sleep(2)
        self.board.window.close()

