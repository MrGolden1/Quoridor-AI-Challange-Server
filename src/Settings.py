#
# Settings.py
# 

DEBUG     = True  # Display additionnal logs on console
INTERFACE = True  # Display window if true
TEMPO_SEC = 0  # Sleep time between each player, in seconds (default: 0)

TRACE = {
    "Path.BreadthFirstSearch": 0,
    "Path.Dijkstra": 0,
    "Board.validFencePlacings": 0,
    "Board.isValidFencePlacing": 0,
    "Board.validPawnMoves": 0,
    "Board.isValidPawnMove": 0,
    "Board.isFencePlacingBlocking": 0,
    "Board.updateStoredValidActionsAfterPawnMove": 0,
    "Board.updateStoredValidActionsAfterFencePlacing": 0
}

