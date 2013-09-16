import sys
    
class Logic():
    wordlist = []
    playable_words = []
    board = None
    
    def __init__(self, letter_board):
        if not Logic.wordlist:
            print "loading wordlist..."
        with open('letterpress-wordlist/wordlist', 'r') as f:
            Logic.wordlist = [s.strip().upper() for s in f.readlines()]
            if Logic.wordlist:
                print "done"
            else:
                print "problems"
                sys.exit(1)
        self.board = letter_board
        self.get_playable_words()
    
    def get_playable_words(self):
        if not self.board:
            print "no board, no words!"
            return
        playables = []
        letters_dict = word_to_letter_dict(self.board.letterstring)
        # loop through all words and look for them in letters
        for bigword in Logic.wordlist:
            if len(bigword) > 1 and word_dict_is_sub(word_to_letter_dict(bigword), letters_dict):
                playables.append(bigword)
        self.playable_words = playables
        print "There are", len(Logic.wordlist), "words in the dict, and", len(playables), "can be played on this board"
    
    def get_words_with(self, test):
        words = []
        for w in self.playable_words:
            if word_contains(w, test):
                words.append(w)
        return words
    
    def get_longest_words(self, containing="", nth=1):
        words = []
        # make copy of playable words
        playables = self.playable_words[:]
        # find and remove 1st longest, 2nd longest, etc.. until reached nth, then return
        for i in range(nth):
            words = get_longest_strings(playables, containing)
            if i < nth-1:
                for w in words:
                    playables.remove(w)
        return words
    
    def get_best_play(self, player):
        max_score = -Board.win_score # start at lowest possible
        max_bd = self.board
        max_wd = ""
        N = len(self.playable_words)
        for n in range(N):
            w = self.playable_words[n]
            #sys.stdout.write("Searching words: %d%%\t%sbest (%d): %-18s\r" % (int(100*n/N), "%-20s" % w, max_score, max_wd) )
            #sys.stdout.flush()
            bd = self.max_word_score_rec(w, 0, self.board.letterstring, self.board.dupl(), player)
            score = bd.score(True)*player
            if score > max_score or (score == max_score and max_wd.find(w) == 0):
                print "new best:", w 
                max_score = score
                max_bd = bd
                max_wd = w
                if score == Board.win_score:
                    break
        return max_wd, max_bd
        
    def max_word_score_rec(self, word, word_i, choose_from, board, player):
        '''Recursively search for all board positions to play this word.
            This is a permutation algorithm for each possible location
            of each letter, it sets that location and recurses to the next
            letter.
        '''
        if word == "":
            return board
        else:
            best_board = board
            best_score = -Board.win_score
            for i in range(len(choose_from)):
                if word[word_i] == choose_from[i]:
                    used_char = choose_from[i]
                    choose_from[i] = '#'
                    rec_board = board.dupl()
                    rec_board.claim_letter(itor(i), itoc(i), player, check_surr=False)
                    bd = self.max_word_score_rec(rec_word, rec_choose, rec_board, player)
                    if bd:
                        # break early if winning play
                        score = bd.score(True)*player
                        if score == Board.win_score:
                            return bd
                        elif score > best_score:
                            best_score = score
                            best_board = bd
            return best_board
    
    def max_word_score(self, word, choose_from, board, player):
        used_letter = [False]*len(choose_from)
        for c in word:
            for i in range(len(choose_from)):
                if not used_letter[i] and c == choose_from[i]:
                    # claim letter, mark it as used
                    used_letter[i] = True
                    prev_val = board.claim_letter(itor(i), itoc(i), player, check_surr=False)
                    # get score
                    # TODO - this loop structure won't work and i'm remembering why i did recursion in the first place
                    # unclaim letter, mark it as unused
                    board.claim_letter(itor(i), itoc(i), prev_val, forced=True)
                    use_letter[i] = False
            
    
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

def word_to_letter_dict(word):
    """
    Convert a word to a dictionary that maps characters in that word 
    to a count of those characters
    """
    d = {}
    for c in word:
        d[c] = d.get(c, 0) + 1
    return d

def word_dict_is_sub(word_as_letter_dict, available_characters):
    """
    Return true iff the word specified by word_as_letter_dict (see word_to_letter_dict)
    is a subset of the characters in available_characters
    """
    for (char, count) in word_as_letter_dict.iteritems():
        if count > available_characters.get(char,0):
            return False
    return True
