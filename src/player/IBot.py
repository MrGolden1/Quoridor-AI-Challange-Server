#
# IBot.py
# 

from src.player.IPlayer import *



class IBot(IPlayer):
    def __str__(self):
        return "[BOT] %s (%s)" % (self.name, self.color.name)