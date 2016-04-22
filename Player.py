# File: Player.py
# Author(s) names AND netid's: James Whang (syw973)
# Date: 4/21/2016
# I worked individually on this project and all work is my own.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        # enemy player
        self.opponent = Player(self.opp, self.type, self.ply)

        # Check terminal conditions
        if board.gameOver(): # Game done
            return self.score(board), -1
        elif ply == 0:
            return self.score(board), board.legalMoves(self)[0] # give up, whatever is the first one

        alpha = -INFINITY
        beta = -INFINITY
        score = -INFINITY
        move = -1

        for action in board.legalMoves(self):
            # make a new board
            nb = deepcopy(board)
            nb.makeMove(self, action) # make the move with given action
            action_score = self.alphaBetaMinMove(nb, alpha, beta, ply-1)
            if action_score > score:
                move = action
                score = action_score
            alpha = max(alpha, score)

        return (score, move)

    def alphaBetaMaxMove(self, board, alpha, beta, ply):
        """ Find the max value for this player """
        # Check terminal condition
        if board.gameOver() or ply is 0:
            return self.score(board)
        max_score = -INFINITY
        for action in board.legalMoves(self): # examine all feasible actions
            # make a new board
            nb = deepcopy(board)
            nb.makeMove(self, action)
            # find opponent's move
            max_score = max(max_score, self.alphaBetaMinMove(nb, alpha, beta, ply-1))
            if (max_score >= beta): # if our score is geq beta, return this score
                return max_score
            alpha = max(alpha, max_score) # update alpha
        return max_score

    def alphaBetaMinMove(self, board, alpha, beta, ply):
        """ Find the minimax value for the opponent """
        if board.gameOver() or ply is 0:
            return self.score(board)
        score = INFINITY
        for action in board.legalMoves(self.opponent): # Examine all feasible actions by the opponent
# make a new board
            nb = deepcopy(board)
            nb.makeMove(self.opponent, action)
            score = min(score, self.alphaBetaMaxMove(nb, alpha, beta, ply-1))
            if (score <= alpha):
                return score
            beta = min(beta, score)
        return score
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.MTCSMove(board, self.ply)
            print "choose move", move, "with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply = 0):
        Player.__init__(self, playerNum, playerType, ply) 

        self.p1score = 0 # player 1 score
        self.p2score = 0 # player 2 score

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board

        # first add what's in each player's mancala
        self.p1score += board.scoreCups[0] 
        self.p2score += board.scoreCups[1]

        # evaluate the cups on my side
        self.p1score += sum(board.getPlayersCups(1))
        self.p1score += sum(board.getPlayersCups(2))

        # TODO: update the weights of each cup

        if self.num == 1:
            return self.p1score
        else:
            return self.p2score

