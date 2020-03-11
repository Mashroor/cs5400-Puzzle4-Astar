#!/usr/bin/env python3
import sys
import time
from queue import Queue, PriorityQueue

winCond = False
#-------------------------gameBoard class definition-----------------------------
class gameBoard:
    #Constructor
    def __init__(self, x, y, z, spawnArr, movestring, nums):
        self.width = x
        self.height = y
        self.spawns = list(spawnArr)
        self.goal = z
        self.moves = movestring
        self.numMoves = nums
        self.board = [[0 for i in range(x)] for j in range(y)]

    # < operator overload, check for heuristic
    def __lt__(self, other):
        return self.numMoves < other.numMoves

    def copyBoard(self):

        #create new board object, this will be returned
        lhs = gameBoard(self.width, self.height, self.goal, self.spawns, self.moves, self.numMoves)
        #index by index, reassign each tile
        for i in range(self.height):
            for j in range(self.width):
                lhs.board[i][j] = self.board[i][j]
        return lhs

    #PrettyPrint function
    def printBoard(self, timer):
        print("%d" % ((time.time() - timer) * 1000000))
        print(self.numMoves)
        print(self.moves)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                content = print(self.board[i][j], end = " ")
            print("")

    #Check for finish condition, iterative. End on self.goal
    def checkFinish(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == self.goal:
                    return True
        return False

    #Using a spawn array, spawn new tiles in specific order
    def spawnNewTile(self):
        #Assign new value to spawned tile; replace the spawned tile to back of spawn list
        newTile = self.spawns[0]
        self.spawns.append(self.spawns.pop(0))
        self.currentPos = 0

        if self.board[0][0] == 0:
            self.board[0][0] = newTile
            return
        elif self.board[0][len(self.board[0])-1] == 0:
            self.board[0][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][len(self.board[0])-1] == 0:
            self.board[len(self.board)-1][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][0] == 0:
            self.board[len(self.board)-1][0] = newTile
        else:
            return

    #Following functions are for movement on board, tile collapsing
    def mvUp(self):
        self.moves += "U"
        self.numMoves += 1
        # Condense board
        for h in range(self.width):
            for i in range(self.width):
                for j in range(self.height-1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(self.width):
            for j in range(self.height- 1):
                if self.board[j+1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j+1][i]
                    self.board[j+1][i] = 0
        # Re-condense board
        for h in range(self.width):
            for i in range(self.width):
                for j in range(self.height- 1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvDown(self):
        self.moves += "D"
        self.numMoves += 1
        # Condense board
        for h in range(self.width):
            for i in range(self.width):
                for j in range(self.height-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(self.width):
            for j in range(self.height-1, 0, -1):
                if self.board[j-1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j-1][i]
                    self.board[j-1][i] = 0
        # Condense board
        for h in range(self.width):
            for i in range(self.width):
                for j in range(self.height-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvLeft(self):
        self.moves += "L"
        self.numMoves += 1
        #Condense board
        for h in range(self.height):
            for i in range(self.height):
                for j in range(self.width-1, 0, -1):
                    if self.board[i][j-1] == 0:
                        self.board[i][j] = self.board[i][j-1]
                        self.board[i][j-1] = 0
        #Add tiles
        for i in range(self.height):
            for j in range(self.width-1):
                if self.board[i][j+1] == self.board[i][j]:
                    self.board[i][j] = self.board[i][j] + self.board[i][j+1]
                    self.board[i][j+1] = 0
        #Re-condense board
        for h in range(self.height):
            for i in range(self.height):
                for j in range(self.width - 1, 0, -1):
                    if self.board[i][j - 1] == 0:
                        self.board[i][j - 1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

    def mvRight(self):
        self.moves += "R"
        self.numMoves += 1
        #Condense board
        for h in range(self.height):
            for i in range(self.height):
                for j in range(self.width-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        # Add tiles
        for i in range(self.height):
            for j in range(self.width-1, 0, -1):
                if self.board[i][j] == self.board[i][j-1]:
                    self.board[i][j] = self.board[i][j-1] + self.board[i][j]
                    self.board[i][j-1] = 0
        #Re-condense board
        for h in range(self.height):
            for i in range(self.height):
                for j in range(self.width-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

#----------------------- end of gameBoard class ---------------------------------

#A* Algorithm Code
def a_star(input, winChk):
    # create a priority queue
    pq = PriorityQueue()
    #create a hash table to store visited states; futher pruning of tree <State, Visted?>
    visited = []
    #push first state into priority queue
    pq.put(input, 0)
    #store first state into hash table, mark as visited
    visited = {input.moves:True}

    while (not(winChk) and not(pq.empty())):
        #pop top of priority queue
        a = pq.get()
        visited = {a.moves:True}
        # evaluate children of a, 4 states created
        stU = a.copyBoard()
        stD = a.copyBoard()
        stL = a.copyBoard()
        stR = a.copyBoard()

        #generate move states
        stU = stU.mvUp()
        stD = stD.mvDown()
        stL = stL.mvLeft()
        stR = stR.mvRight()

        #determine if redundant move, and if the move is new,
        #push states, f(n) into priority queue to be checked on next iteration
        #F(n) = g(n) + h(n), where g(n) == the path cost of the next node (depth in our case)
        #and h(n) is our heuristic function (admissible)
        if stU.board != a.board and not(stU.moves in visited):
            stU.spawnNewTile()
            pq.put(stU, (a.numMoves) + h(stU))
        if stD.board != a.board and not(stD.moves in visited):
            stD.spawnNewTile()
            pq.put(stD,(a.numMoves) + h(stD))
        if stL.board != a.board and not(stL.moves in visited):
            stL.spawnNewTile()
            pq.put(stL, (a.numMoves) + h(stL))
        if stR.board != a.board and not(stR.moves in visited):
            stR.spawnNewTile()
            pq.put(stR, (a.numMoves) + h(stR))
        #check for win condition
        if stU.checkFinish():
            input = stU
            winChk = True
        if stD.checkFinish():
            input = stD
            winChk = True
        if stL.checkFinish():
            input = stL
            winChk = True
        if stR.checkFinish():
            input = stR
            winChk = True

    return input, winChk

#Heuristic function, take in board
#Methodology: add point totals that scale with each tile
def h(state):
    pointTotal = 0
    for i in range(len(state.board)):
        for j in range(len(state.board[i])):
            count = 1
            if state.board[i][j] > 2:
                while(state.board[i][j]%(2**count) == 0):
                    count += 1
                count -=1
            pointTotal += state.board[i][j]*count
    
    pointTotal = pointTotal/(state.width * state.height)
    
    return (state.goal - pointTotal)

#--------------------------- Problem Solving ------------------------------------
#set timer
start_time = time.time()
#Read input.txt, or test cases
goal = int(input())
width, height = map(int, input().split())
spawnList = list(map(int, input().split()))
#instantiate a new gameBoard, then fill board with input
x = gameBoard(width, height, goal, spawnList, "", 0)
for i in range(len(x.board)):
    x.board[i] = list(map(int, input().split()))

#check for solved game on input
if x.checkFinish():
    winCond = True

#initiate a* algorithm
x, winCond = a_star(x, winCond)

#finish state
#time converted to microsenconds
if winCond:
    x.printBoard(start_time)
