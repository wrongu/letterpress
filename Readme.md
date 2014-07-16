Letterpress AI
====

__LetterBoard.py:__ the class for the board itself

__LetterLogic.py:__ the logic of how to find the best word, etc

__Driver.py:__ the driver. 

---

How to use:
---

1. open Driver.py and set the `game` variable to whatever board you want to use
2. in \_\_main\_\_, set the grid to the current state. -1 for opponent, 0 for white, 1 for self
3. from the command line, navigate to the 'letterpress' directory use one of the following commands:

__run a full simulation__

    $ python Driver.py

__get longest words containing the letters P Q R__

    $ python Driver.py pqr

__get the 3rd longest words containing the letters P Q R__

    $ python Driver.py pqr 3
    
__get the 3rd longest words overall__

    $ python Driver.py 3

You get the idea..