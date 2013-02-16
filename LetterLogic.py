from itertools import combinations
from LetterBoard import itoc, itor
import sys

class LetterLogic():
    
    wordlist = []
    playable_words = []
    board = None
    
    def __init__(self, letter_board):
        if not LetterLogic.wordlist:
            print "loading"
            with open("/Users/Richard/Documents/python/wordlist_big.txt") as f:
                LetterLogic.wordlist = f.readline().split(" ")
            print "done"
        self.board = letter_board
        self.get_playable_words()
    
    def get_playable_words(self):
        if not self.board:
            print "no board, no words!"
            return
        letters = ''.join(self.board.letterstring)
        n = 0
        N = len(LetterLogic.wordlist)
        # 2 options:
        #   loop through wordlist or do permutations of letters
        for bigword in LetterLogic.wordlist:
            l_temp = letters
            #print l_temp
        
            #print "[%s]:" % bigword,
            builtword = ""
            can_make_word = True
            for c in bigword:
                i = l_temp.find(c)
                if i == -1:
                    #print builtword
                    can_make_word = False
                    break
                else:
                    builtword = builtword + c
                    l_temp = l_temp[:i] + l_temp[i+1:]
            if can_make_word:
                self.playable_words.append(bigword)
            # if not (bigword.find('A') >= 0 or bigword.find('B') >= 0):
            #    raw_input("press a key")
            n = n+1
    
    def get_words_with(self, test):
        words = []
        for w in self.playable_words:
            if word_contains(w, test):
                words.append(w)
        return words
    
    def get_longest_words(self, containing="", nth=1):
        words = []
        playables = self.playable_words
        for i in range(nth):
            words = get_longest_strings(playables, containing)
            for w in words:
                playables.remove(w)
        return words
    
    def get_best_play(self, player):
        max_score = -51
        max_bd = self.board
        max_wd = ""
        N = len(self.playable_words)
        for n in range(N):
            w = self.playable_words[n]
            sys.stdout.write("Searching words: %d%%\t%sbest (%d): %-18s\r" % (int(100*n/N), "%-20s" % w, max_score, max_wd) )
            sys.stdout.flush()
            if(len(w) > 1):
                bd = self.max_word_score(w, self.board.letterstring, self.board.dupl(), player)
                score = bd.score(True)*player
                if score > max_score or (score == max_score and max_wd.find(w) == 0):
                    max_score = score
                    max_bd = bd
                    max_wd = w
                    if score == 51:
                        break
        return max_wd, max_bd
        
    def max_word_score(self, word, choose_from, board, player):
        # print "max_word_score(%s, %s, %s)" % (word, choose_from, ("None" if board == None else "board"))
        if word == "":
            return board
        else:
            best_board = None
            best_score = -51 # min possible is -50
            for i in range(len(choose_from)):
                if word[0] == choose_from[i]:
                    rec_word = word[1:]
                    rec_choose = choose_from[:i]+"#"+choose_from[i+1:]
                    rec_board = board.dupl()
                    rec_board.claim_letter(itor(i), itoc(i), player, check_surr=False)
                    bd = self.max_word_score(rec_word, rec_choose, rec_board, player)
                    if bd:
                        # break early if winning play
                        score = bd.score(True)*player
                        if score == 51:
                            return bd
                        elif score > best_score:
                            best_score = score
                            best_board = bd
            return best_board
    
    def play_word(self, word, new_board):
        N = len(self.playable_words)
        n = 0
        while n < N:
            if word.find(self.playable_words[n]) == 0:
                print "removing %s" % self.playable_words[n]
                self.playable_words = self.playable_words[:n] + self.playable_words[n+1:]
                N = N-1
            else:
                n = n+1
        self.board = new_board
    
    def initialize(self, territory_grid, played_words=[]):
        for i in range(5):
            for j in range(5):
                if territory_grid[i][j] != 0:
                    self.board.claim_letter(i,j,territory_grid[i][j])
        for w in played_words:
            self.play_word(w, self.board)
##################
## HELPER STUFF ##
##################

def word_contains(word, test):
    for c in test:
        i = word.find(c)
        if i == -1:
            return False
        else:
            word = word[:i] + word[i+1:]
    return True

def get_longest_strings(strings, containing):
        words = []
        maxlen = 0
        for w in strings:
            if word_contains(w,containing):
                if len(w) == maxlen:
                    words.append(w)
                elif len(w) > maxlen:
                    words = [w]
                    maxlen = len(w)
        return words