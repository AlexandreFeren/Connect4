import os
import time
import sys
from graphics import*

'''
1112221222111211122212221112111222122211121112221
'''
def gameLoop():
                                                #POST:  runs the main game loop
    global names
    global connect4                             #references connect4 as a global var
    global player                               #references global player
    global gameInput
    game = True                                 #condition for game loop
    turn = 1                                    #tracks turn number
    reset()                                     #resets global connect4
    player = 1                                  #sets first player as 1
    gameInput = ""
    clearBoard()
    while (game == True):                       #game loop
        if not(plop()):                         #takes input for plop. False return indicates full board
            return 0
        if player == 1:
            print("Turn " + str(turn) + ":  \n")#prints turn for start of each set (skip every other ply)
        else:
            print("\n")
        printConnect()                          #prints board
        drawBoard()                             #draws board to screen
        
        if (checkWins()):                       #if player has won, display that
            print("Player " + str(names[player-1]) + " has won!")
            return player
        if player%2 == 0:                       #if player 2 just played
            turn += 1                           #increment turn counter

        player = player%2+1                     #swaps player between 1 and 2
        
def bestOfX():
                                                #POST:  determines the winner of the majority of x matches
    global names                                #names of players
    wins = [0,0,0]                              #tracks who has won matches, maybe change to track who won what match
    while 1:
        try:
            x = int(input("1. Best of three 2. Best of 5\n"))
        except ValueError:                      #number was not entered
            print("enter a number")
            continue                            #restart loop
        if 1<=x<=2:                             #if input is in valid inputs, break out of loop
            break
        print("make sure your number is in the menu")
    if      x == 1: x = 3                       #swap input 1 to best of 3
    elif    x == 2: x = 5                       #swap input 2 to best of 5
    
    for i in range(x):
        wins[gameLoop()] += 1                 #increment the winner's index by 1

        #announcements for match being won
        if wins[1] + wins[2] >= x:              
            if wins[1] > wins[2]:
                print(names[1] + " has won the match")
            else:
                print(names[2] + " has won the match")
        elif wins[1] > int(x/2):
            print(names[1] + " has won the match")
            break                               #won before match x
        elif wins[2] > int(x/2):
            print(names[2] + " has won the match")
            break                               #won before match x

        
def shortcuts():
                                                #POST:  prints unlisted commands to the console
    print("names: change of names | more soon")
    
def nameChange():
                                                #POST:  changes the name of players to input
    global names
    names[0] = input("Enter player 1's name:    ")
    names[1] = input("Enter player 2's name:    ")
    if (names[0] == ""):
        names[0] = "Player 1"
    if (names[0] == ""):
        names[0] = "Player 2"

def end():
                                                #POST:  exits program
    sys.exit()
    
def printConnect(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  prints board setup to console
                                                #DEBUG: maybe add functionality to show what the win is
    for row in connect4:
        for column in row:
            print("|" + str(column), end="|")
        print(end="\n")
    print("---------------------")
    return None

def plop(debug = False, col = -1):
                                                #PRE:   takes in debug condition, and allows for a given start value
                                                #       to be able to read from a text file
                                                #POST:  drops piece onto board, higher indices first
                                                #DEBUG: no change, perhaps show "before" and "after"
    #global vars
    disallowedRows = 0
    global names
    global player
    global connect4
    global gameInput
    if col == -1:                                   #if the user is giving input in plop
        while 1:                                    #error catching loop, forces number from 1-7
            if (player == 1):   col = input("Enter what col (1-7): " + names[0] + ": ")
            else:               col = input("Enter what col (1-7): " + names[1] + ": ")
                
            try:                                    #test if col is a number
                col = int(col)
            except ValueError:
                print("Please enter a number")      #if number is not entered
                continue                            #restart loop
            if 1<=col<=7:                           #test if col is 1-7
                col -= 1
                if connect4[0][col] == 0:
                    break                           #break loop
                else:                               #check to see if there are open rows
                    for i in range(7):
                        if connect4[0][i] != 0:     #if row is full add it to disallowedRows
                            disallowedRows += 1
                    if debug:
                        print(str(disallowedRows) + " FULL ROWS")   #shows number of full rows (debug)
                    if disallowedRows >= 7:         #if all rows are full
                        if debug:
                            print("ALL ROWS FULL")  #show all rows are full
                        else:
                            print(names[0] + " and " + names[1] + " tied.")
                        return False                #return false for plopable
            print("number must be between 1 and 7")
            continue                                #restart loop
        gameInput += str(col)
    else:
        try:
            col = int(col)
        except ValueError:
            return
    #actual 'plop'
    for row in range(6):                        #loop through rows in the given column
        if (connect4[5-row][int(col)] == 0):    #if the spot is empty, set it to the player number
            connect4[5-row][int(col)] = player
            break
    return True
    #print("\n")
    
def checkWinV(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  tests vertical win condition
                                                #DEBUG: prints out True/False for win
    global player
    for col in range(7):                        #iterates through columns
        count = 0                               #sets counter of consecutive tiles for current player to 0 for the new column
        for row in range(6):                    #iterates through rows
            if connect4[row][col] == player:    #if the row and column at this location is the current player's increment count
                count += 1                      
            else:                               #otherwise reset the count
                count = 0                      
            if count >= 4:                      #if there is a winning col return true
                if debug:
                    print("checkWinV: \tTRUE")
                return True            
    if debug:
        print("checkwinV: \tFALSE")
    return False                                #no wins, return False

def checkWinH(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  tests horizontal win condition
                                                #DEBUG: prints out True/False for win

    global player
    for row in range(6):                        #loops through rows
        count = 0                               #sets counter of consecutive tiles for current player to 0 for the new row
        for col in range(7):                    #loops through columns
            if connect4[row][col] == player:    #if the row and column at this location is the current player's increment count
                count += 1                      
            else:                               #otherwise reset the count
                count = 0                      
            if count >= 4:                      #if there is a winning row return true
                if debug:
                    print("checkWinH: \tTRUE")
                return True
    if debug:
        print("checkWinH: \tFALSE")
    return False                                #no wins, return False


def checkWinDf(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  checks / facing diagonal win condition
                                                #DEBUG: prints out True/False for win
    global player
    global connect4
    for col in range(3,7):                      #all starting columns   (omit first 3 to avoid out of bounds)
        for row in range(3):                    #all starting rows      (omit first 3 to avoid out of bounds)
            count = 0
            for i in range(4):                  #iterates horizontally and diagonally simultaneously
                if connect4[row+i][col-i] == player:   #break after a piece not belonging to the player
                    count += 1
            #win test loop finished
            if count >= 4:                      #if there were 4 or more pieces, value is one less because of for loop rather than a counter
                if debug:
                    print("checkWinDf (/) : TRUE")
                return True
 
    if debug:
        print("checkWinDf: FALSE")
    return False
  



def checkWinDb(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  checks \ facing diagonal win condition
                                                #DEBUG: prints out True/False for win

    for col in range(4):                        #all starting columns   (omit first 3 to avoid out of bounds)
        for row in range(3):                    #all starting rows      (omit first 3 to avoid out of bounds)
            count = 0
            for i in range(4):                  #iterates horizontally and diagonally simultaneously
                if connect4[row+i][col+i] == player:
                    count += 1
            #win test loop finished
            if count >= 4:                      #if there were 4 or more pieces, value is one less because of for loop rather than a counter
                if debug:
                    print("checkWinDb (\) : TRUE")
                return True
    if debug:
        print("checkWinDb: FALSE")
    return False                                #exits to not be true


def checkWins(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  returns whether or not there is a win
                                                #DEBUG: calls win functions in debug mode
    if debug:                                   #checks all win conditions and prints them
        checkWinV(debug)
        checkWinH(debug)
        checkWinDf(debug)
        checkWinDb(debug)
    else:                                       #checks all win conditions and returns result
        win = False
        if win == False:
            win = checkWinV()
        if win == False:
            win = checkWinH()
        if win == False:
            win = checkWinDf()
        if win == False:
            win = checkWinDb()
        return win
    return False                                 #Default return for debug function

'''
def slice(row):
                                                #PRE:   ???
                                                #POST:  ???
                                                #DEBUG: ???
                                                #NOTES: NEEDS RENAMING, slice IS A KEYWORD
    maxRow = 6 - row
    done = False
    while (done != True):
        return 0
'''

def reset(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  resets board to 2D array of 0s
                                                #DEBUG: acknowledgement text
    global connect4
    connect4 = [[int(0) for col in range(7)],[int(0) for col in range(7)],
                [int(0) for col in range(7)],[int(0) for col in range(7)],
                [int(0) for col in range(7)],[int(0) for col in range(7)]]
    if debug:
        print("BOARD RESET")                    #logs the board reset (debug)


        
def switchPlayer(debug = False):
                                                #PRE:   takes in debug condition
                                                #POST:  swaps the player number
                                                #DEBUG: print current player to screen
    global player
    player =  player%2+1
    if debug:
        print("Player: " + player)

def export(debug = True):
    global connect4

    print("Board as String:")
    for row in connect4:
        for col in row:
            print(col, end = "")
    print("\n")
    print("Board as Input:")
    print(gameInput)

    
def setBoard(debug = True):
                                                #PRE:   debug only function
                                                #POST:  makes board from a string of inputs
                                                #DEBUG: uses the end part of plop to simply place a piece
    global player
    #due to the nature of the storage, as string works from any array, and as input requires a game
    #to have been played
    mode   = input("DEBUG MODE: PRESS 1 TO ENTER BOARD POSITION AS A STRING\n"
                   "        OR  PRESS 2 TO ENTER BOARD POSITION FROM INPUTS")
    if mode == "1":
        inputs = input("ENTER YOUR BOARD POSITION AS A STRING\n")
        for row in range(6):
            for col in range(7):
                connect4[row][col] = inputs[row*7+col:row*7+col+1]
    if mode == "2":
        inputs = input("ENTER YOUR BOARD POSITION AS INPUTS (0-6)")

        for ind in inputs:
            plop(True, ind)
            player = player%2+1

            
def drawBoard(w = 800,h = 800):
    color = color_rgb(100,0,0)
    for row in range(len(connect4)):
        for col in range(len(connect4[row])):
            if connect4[row][col] == 0:
                color = color_rgb(255,255,255)
            elif connect4[row][col] == 1:
                color = color_rgb(255,0,0)
            elif connect4[row][col] == 2:
                color = color_rgb(0,0,0)
            else:
                color = color_rgb(random.randrange(256),random.randrange(256),random.randrange(256))
            circle = Circle(Point((h-h/len(connect4))/len(connect4)*col + h/len(connect4)/2,(w-h/len(connect4))/len(connect4)*row + h/len(connect4)/2),(h-h/len(connect4))/(len(connect4)+1)/2)
            circle.setFill(color)
            circle.draw(win)
    
def clearBoard(w = 800, h = 800):
    color = color_rgb(0,0,255)                      #color is blue
    rect = Rectangle(Point(0,0),Point(800,800))     #creates initial board
    rect.setFill(color)                             #sets initial board color to color
    rect.draw(win)                                  #draws board to the window
    color = color_rgb(255,255,255)
    for i in range(len(connect4)):
        for j in range(len(connect4[0])):
            circle = Circle(Point((h-h/len(connect4))/len(connect4)*j + h/len(connect4)/2,(w-h/len(connect4))/len(connect4)*i + h/len(connect4)/2),(h-h/len(connect4))/(len(connect4)+1)/2)
            circle.setFill(color)
            circle.draw(win)


def debug():
                                                #POST:  manages debug functionality

    #dictionary for direct reference to functions
    debugFunctions = {1: plop, 2: checkWins, 3: switchPlayer, 4: printConnect, 5: setBoard, 6: export, 7: reset}
    debugging = True                            #loop condition
    while (debugging):
        while 1:                                #check for valid input (on given list)
            try:
                ans = int(input("0. exit debug, 1. plop, 2. checkWins, 3. switchplayer, " + \
                    "4. printConnect, 5. setBoard, 6. export board, 7. Reset #: (c to clear scene)\n"))
            except ValueError:                  #number was not entered
                continue
            if 0<=ans<=6:                       #if number is in listed options, break out of error checking loop
                break
        if ans == 0:                            #if 0 is given, breaks out of debug loop                           
            break                               
        debugFunctions[ans](True)               #call requested function


#global variable assignments
player = 1                                      #current players turn 
win = GraphWin("Connect Four", 800, 800, autoflush = False)            #creates window for graphics

connect4 = [[int(0) for col in range(7)],[int(0) for col in range(7)],
            [int(0) for col in range(7)],[int(0) for col in range(7)],
            [int(0) for col in range(7)],[int(0) for col in range(7)]]    
done = False                                    #condition for main loop
names = ["Player 1", "Player 2"]
gameInput = ""

#interface stuff, no parameters needed
playFunctions = {1:gameLoop, 2:bestOfX, 3:debug, 4: nameChange, 5:shortcuts, 6:end}
while(done != True):                            #main loop
    print("Welcome to connect 4:  \n")

    #takes input for function
    while 1:
        try:
            ans = int(input("1. Play game (simple), 2. play (standard),"
                               "3. debug, 4. change names, 5. Shortcut/secrets 6.quit "))
        except ValueError:                      #number was not entered
            continue
        if 1<=ans<=6:
            break

    playFunctions[ans]()                        #calls appropriate function from dictionary

    

