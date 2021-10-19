# TODO: 
# OK Use GridCoordinates class instead of col/row
# OK Param graphical interface (disable draw functions...)
# OK Split source files
#    Handle exec paramsp
# OK Check if fence placing will not block a player
# OK Create algorithms for path finding
#    BuilderBot: maximise other pawns path
# OK PERFORMANCE ISSUES: store valid fence placings, valid pawn moves with updates
# OK Check blocking fence using path without pawns (one path could exist but cannot be currently accessible because of a pawn) (DFS)
# OK Blocking fence checking failed on testing path with the future fence -> update valid pawn moves when appending fence in method isFencePlacingBlocking

from src.Settings          import *
from src.Game              import *
from src.ServerGame        import *
from src.player.Human      import *
from src.player.RandomBot  import *
from src.player.RunnerBot  import *
from src.player.BuilderBot import *
from src.player.Client     import *
import os

def Start(Cl1,Cl2,first,Logs):
    namewin=''
    game = ServerGame([ # 2 or 4
        #Human("Human"),
        #BuilderBot("Benoit"),
        #RunnerBot("ali"),
        Cl1 ,
        Cl2 ,
        #Cl1,
        #BuilderfBot("Clément"),
        #RandomBot("r"),
        #Human("Pierre")
    ], totalFenceCount = 20, cols = 9, rows = 9 , timeLimit = 2)
    namewin=game.start(1,first,'Logs/' + Logs) # rounds
    game.end()
    return namewin
def main():
    """
    Main function of quoridor. 
    Create a game instance and launch game rounds.
    """
    #my = Client("A")
    #you = Client("B")f
    #my.setExeName("Test.exe")
    #you.setExeName("Test.exe")
    f = open('cnt.txt' , 'r')
    cnt = f.readlines()
    cnt = int(cnt[0])
    f.close()
    print(cnt)
    f = open('Players.txt' , 'r')
    players = f.readlines()
    for i in range(cnt,len(players),2):
        players[i] = players[i].replace('\n' , '' )
        players[i + 1] = players[i + 1].replace('\n' , '' )
        Cl1 = Client((players[i]+'.exe'))
        Cl1.setExeName('Agents\\' + (players[i]+'.exe'))
        Cl2 = Client((players[i+1]+'.exe'))
        Cl2.setExeName('Agents\\' + (players[i+1]+'.exe'))
        Log = str(players[i]) + '_' + str(players[i + 1]) + '_' + str(int((((i//2)+1)%2))) + '.txt'
        name = Start(Cl1,Cl2,int(((i//2)%2)),Log)
        ff = open('win.txt','a')
        ff.write(str(players[i]) + ' ' + str(players[i + 1]) + ' ' + name.replace('.exe','') + ' ' + str(int((((i//2)+1)%2))) + '\n')
        ff.close()
        ff = open('cnt.txt','w')
        ff.write(str(i+2))
        ff.close()
        #input()
    #global TRACE
    #print("TRACE")
    #for i in TRACE:
    #	print("%s: %s" % (i, TRACE[i]))

main()