from LetterLogic import LetterLogic
from LetterBoard import LetterBoard
from sys import argv
from os import system
import string

def analytics(ll, contains="", nth=1):
    contains = contains.upper()
    print "longest words%s:" % (" containing '%s'"%contains if contains else "")
    longests = ll.get_longest_words(contains, nth)
    print longests
    if longests != []:
        print "with length %d" % len(longests[0])

# Jeilanin
# game = LetterLogic(LetterBoard("TNBGHCRCESDRTFIBMKREEDVDG"))
# max
# game = LetterLogic(LetterBoard("BLVYDNRBRSPNGEMEHZSDHWBAJ"))
# brittany
#game = LetterLogic(LetterBoard("RNCNPLHNFVCCYPEAGMDFHRIPQ"))
#game = LetterLogic(LetterBoard("BRITTANYCAROLINEWALD#####"))
game = LetterLogic(LetterBoard("YSWFBTHAEQSHTTRVORIESPSSR"))

def run_turn(game):
    game.board.print_board()
    best_wd, best_bd = game.get_best_play(1)
    best_bd.print_board()
    print "BEST WORD:", best_wd
    

def run_game(game):
    game.board.print_board()
    player = 1
    while game.board.gameover() == 0:
        best_wd, best_bd = game.get_best_play(player)
        print "\nBEST: %s" % best_wd
        best_bd.print_board()
        game.play_word(best_wd, best_bd)
        player = -player
        
#if __name__ != "__main__":
#    analytics(game)
if __name__ == '__main__':
    conts = ""
    nth = 1
    for s in argv[1:]:
        if s[0] in string.digits:
            nth = int(s)
        else:
            conts = s
    
    analytics(game, conts, nth)
    
    #best_wd = "BLITZKRIEG"
    #best_bd = game.max_word_score_rec(best_wd, game.board.letterstring, game.board, -1)
    #game.play_word(best_wd, best_bd)
    #run_game(game)
    if conts == "" and nth == 1:
        """
        grid = [[ 0, -1,  1,  1,  1],\
                [ 1, -1,  0, -1,  1],\
                [-1, -1, -1, -1, -1],\
                [-1, -1,  0, -1, -1],\
                [-1, -1,  1, -1, -1]]
        grid = [[-1, -1,  0, -1,  0],\
                [-1,  0, -1,  0,  1],\
                [-1,  0, -1, -1, -1],\
                [ 1, -1, -1, -1, -1],\
                [ 1,  1, -1, -1,  0]]
        grid = [[-1, -1, -1, -1,  1],\
                [-1,  0,  1, -1, -1],\
                [-1, -1, -1, -1, -1],\
                [-1, -1,  0,  1,  1],\
                [ 1,  1,  0, -1,  1]]
        grid = [[ 0,  1,  1,  1,  1],\
                [-1,  1,  0,  1,  1],\
                [-1, -1, -1, -1, -1],\
                [-1, -1,  0, -1, -1],\
                [-1, -1, -1, -1, -1]]
        
        game.initialize(grid, [])"""
        
        run_game(game)
