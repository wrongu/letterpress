from sys import argv
from Driver import run_turn, analytics
from LetterLogic import LetterLogic
from LetterBoard import LetterBoard

if __name__ == '__main__':
    lines = []
    with open('games/'+argv[1], 'r') as f:
        lines = f.readlines()
    # first line is 25 letters
    game = LetterLogic(LetterBoard(lines[0]))
    print "created game"
    # next 5 lines are current state of grid
    grid = [None]*5
    if len(lines) > 5:
        for i in range(5):
            strvals = lines[i+1].split() # splits on all whitespace
            nums = [int(val) for val in strvals]
            grid[i] = nums
            print nums
    # remaining lines are played words
    played_words = []
    for i in range(6, len(lines)):
        played_words.extend(lines[i].split())
    print grid,played_words
    game.initialize(grid, played_words)
    
    # run analytics for best words 1-3
    for i in range(1,3):
        analytics(game, "", i)
    
    # best word simulation
    run_turn(game)
