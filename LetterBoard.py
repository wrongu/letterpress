import string, sys, math
from termcolor import cprint
from copy import deepcopy

class LetterBoard():
    
    safe_weight = 1.1
    
    def __init__(self, letters_as_str):
        # instance variables
        self.letterstring = ""
        self.letters = [None]*5
        self.territory = [None]*5
        
        # start it
        for i in range(5):
            self.letters[i] = [None]*5
            self.territory[i] = [0]*5
            
        i = 0; j=0
        for c in letters_as_str:
            c = c.upper()
            if c in string.ascii_uppercase:
                self.letters[i][j] = c
                self.letterstring = self.letterstring + c
                j = j+1
                if j > 4:
                    i=i+1
                    j = 0
        # self.make_letterdict()
    
    def dupl(self):
        return deepcopy(self)
    
    def make_letterdict(self):
        for c in self.letterstring:
            self.letterdict[c] = self.letterstring.count(c)
    
    def get_letters(self):
        return self.letterstring
    
    def gameover(self):
        """returns 1 if won, 0 if not over, -1 if lost
        """
        count_1 = 0
        for i in range(5):
            for j in range(5):
                if self.get_territory(i,j) == 0:
                    return 0
                elif self.get_territory(i,j) > 0:
                    count_1 = count_1 + 1
        if count_1 >= 13:
            return 1
        else:
            return -1
    
    def score(self, update=False):
        if update:
            for i in range(5):
                for j in range(5):
                    self.update_surrounding(i,j)
        endgame = self.gameover()
        if endgame == 0:
            return sum([sum(row) for row in self.territory])
        else:
            return 51 * endgame
        
    def update_surrounding(self, row, col):
        surrounded = True
        # Logic for -1 side
        if(self.get_territory(row, col) < 0):
            if row > 0 and self.get_territory(row-1, col) >= 0:
                surrounded &= False
            if row < 4 and self.get_territory(row+1, col) >= 0:
                surrounded &= False
            if col > 0 and self.get_territory(row, col-1) >= 0:
                surrounded &= False
            if col < 4 and self.get_territory(row, col+1) >= 0:
                surrounded &= False
            # having checked all orthogonal spaces, set to safe or 1
            if surrounded:
                self.claim_letter(row, col, -self.safe_weight, True)
            else:
                self.claim_letter(row, col, -1, True)
        # Logic for +1 side
        elif(self.get_territory(row, col) > 0):
            if row > 0 and self.get_territory(row-1, col) <= 0:
                surrounded &= False
            if row < 4 and self.get_territory(row+1, col) <= 0:
                surrounded &= False
            if col > 0 and self.get_territory(row, col-1) <= 0:
                surrounded &= False
            if col < 4 and self.get_territory(row, col+1) <= 0:
                surrounded &= False
            if surrounded:
                self.claim_letter(row, col, self.safe_weight, True)
            else:
                self.claim_letter(row, col, 1, True)

    def claim_letter(self, row, col, set_to, forced=False, check_surr=True):
        if forced:
            self.territory[row][col] = set_to
        else:
            if(abs(self.get_territory(row,col)) != LetterBoard.safe_weight):
                self.territory[row][col] = set_to
                if check_surr:
                    self.update_surrounding(row, col)
                    if row > 0:
                        self.update_surrounding(row-1, col)
                    if row < 4:
                        self.update_surrounding(row+1, col)
                    if col > 0:
                        self.update_surrounding(row, col-1)
                    if col < 4:
                        self.update_surrounding(row, col+1)
        
    def get_territory(self, row, col):
        """returns one from (-2, -1, 0, 1, 2)
        """
        return self.territory[row][col]
        
    def get_letter(self, row, col):
        return self.letters[row][col]
    
    def print_board(self):
        print "==============="
        for i in range(5):
            for j in range(5):
                high = ''
                bld = False
                if abs(self.get_territory(i,j)) == LetterBoard.safe_weight:
                    bld = True
                if self.get_territory(i,j) < 0:
                    high = 'on_magenta'
                    if bld:
                        high = 'on_red'
                elif self.get_territory(i,j) > 0:
                    high = 'on_cyan'
                    if bld:
                        high = 'on_blue'
                if high == '':
                    sys.stdout.write(" %c " % self.get_letter(i,j))
                else:
                    cprint(" "+self.get_letter(i,j)+" ", 'white', high, end='')
            print ""
        print "==============="

def itor(i):
    return int(i / 5)

def itoc(i):
    return i % 5