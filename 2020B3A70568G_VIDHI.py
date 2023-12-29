#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import time
class GameTreePlayer:
    
    def __init__(self):
        self.count = 0 #declared count to count the number of recursive calls
        pass
    
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        alpha = float('-inf')
        beta = float('inf')
        start_game = FourConnect()
        start_game.SetCurrentState(currentState)
        score, move = self.h_minimax_part_b(5, 2, start_game, alpha, beta) #uncomment to use alpha-beta pruning
        # score, move = self.h_minimax_part_a(5, 2, start_game) #uncomment this to use simple minimax
        return move

    def CoinRowAfterAction(self, board, action):
        cRow = -1
        c=action
        for r in range(5,-1,-1):
            if board[r][c]==0:
                cRow=r
                break
        return cRow

    # this is the first evaluation function, it just counts the number of pieces of the players
    def evaluation_function_one(self, board, player, gamestate):
        if gamestate.winner == 2:
            return 5000
        elif gamestate.winner == 1:
            return -1000
        opp_player = 1 if player == 2 else 2
        player_score = sum(row.count(player) for row in board)
        opponent_score = sum(row.count(opp_player) for row in board)
        return player_score - opponent_score

    #this is the second evaluation, it is a basic evaluation function
    def evaluation_function_two(self, board):
        if board.winner == 2:
            return 1000
        elif board.winner == 1:
            return -1000
        else: 
            return 0
        
    def score_func_for_eval_three(self, board, player):
        score = 0
        #Priority is given to the center column, where more connections are possible
        center_cols = [row[3] for row in board]  #Taking the center column separately
        player_count = center_cols.count(player)
        score += player_count * 3
 
        #Checking for horizontal scores 
        for row in board:
            for col in range(4): 
                part = row[col:col+4]
                score += self.individual_score_function(part, player)
 
        #Checking for vertical scores
        for col in range(7):
            col_array = [board[row][col] for row in range(6)]  
            for row in range(3):
                part = col_array[row:row+4]
                score += self.individual_score_function(part, player)
 
        #Checking for positive sloped diagonal scores
        for row in range(3, 6):
            for col in range(4):
                part = [board[row-i][col+i] for i in range(4)]
                score += self.individual_score_function(part, player)
 
        #Checking for negative sloped diagonal scores
        for row in range(3):
            for col in range(4):
                part = [board[row+i][col+i] for i in range(4)]
                score += self.individual_score_function(part, player)
 
        return score
    
    #gives scores for different parts of the gameboard (better description report)
    def individual_score_function(self, part, player):
        score = 0
        opp_player = 1 if player == 2 else 2
 
        if part.count(player) == 4:
            score += 100
        elif part.count(player) == 3 and part.count(0) == 1:
            score += 5
        elif part.count(player) == 2 and part.count(0) == 2:
            score += 2

        if part.count(opp_player) == 3 and part.count(0) == 1:
            score -= 4
        return score
    
    #A little advanced evaluation function 
    def evaluation_function_three(self, game):
        player_score = self.score_func_for_eval_three(game.GetCurrentState(), 2)
        opponent_score = self.score_func_for_eval_three(game.GetCurrentState(), 1)
       
        return player_score - opponent_score #The net score from GameTreePlayer's perspective
    
    def evaluation_function_four(self, player, board, gamestate):
        score1 = 0.15 * self.evaluation_function_one(gamestate, player, board)
        score2 = 0.15 * self.evaluation_function_two(board)
        score3 = 0.7 * self.evaluation_function_three(board)
        return score1+score2+score3

    #this heuristic checks the center column first and then 1 column away, then 2 and atlast 3
    def moving_order_heuristic(self):
        center_column = 3
        column_order = [center_column, center_column - 1, center_column + 1, center_column - 2, center_column + 2, center_column - 3, center_column + 3]
        return column_order
    
    #makes copy of the board and makes the recursive call from GameTreePlayer level of minimax function of part a
    def max_player(self, board, col_num, depth_of_tree):
        new_board = copy.deepcopy(board)
        new_board.GameTreePlayerAction(col_num)
        current_score, a = self.h_minimax_part_a(depth_of_tree-1, 1, new_board)
        return current_score
    
    #makes copy of the board and makes the recursive call from MyopicPlayer level of minimax function of part a
    def min_player(self, board, depth_of_tree):
        new_board = copy.deepcopy(board)
        new_board.MyopicPlayerAction()
        current_score, a = self.h_minimax_part_a(depth_of_tree - 1, 2, new_board)
        return current_score

    #Minimax function to select next action of GameTreePlayer 
    def h_minimax_part_a(self, depth_of_the_tree, player_type, board):
        #base condition to check if required depth is reached or a winner has been found
        if depth_of_the_tree == 0 or board.winner is not None:
            curr_state = board.GetCurrentState()
            return self.evaluation_function_four(player_type, board, curr_state), None #uncomment the evaluation function lines one by one to see output
            # return self.evaluation_function_three(board), None
            # return self.evaluation_function_two(board), None
            # return self.evaluation_function_one(curr_state, player_type, board), None


        if player_type == 2:
            eval_score = -99999999
            best_col = None
            for col in range(7):
                if self.CoinRowAfterAction(board.GetCurrentState(), col) != -1:
                    current_score = self.max_player(board, col, depth_of_the_tree)
                    if current_score > eval_score:
                        eval_score = current_score
                        best_col = col
            return eval_score, best_col
        else:
            eval_score = 99999999
            worst_col = None
            for col in range(7):
                if self.CoinRowAfterAction(board.GetCurrentState(), col) != -1:
                    current_score = self.min_player(board, depth_of_the_tree)
                    if current_score < eval_score:
                        eval_score = current_score
                        worst_col = col
            return eval_score, worst_col   

    #makes copy of the board and makes the recursive call from GameTreePlayer level of minimax function of part b
    def max_player_part_b(self, board, col_num, depth_of_tree, alpha, beta):
        new_board = copy.deepcopy(board)
        new_board.GameTreePlayerAction(col_num)
        score, _ = self.h_minimax_part_b(depth_of_tree - 1, 1, new_board, alpha, beta)
        return score

    #makes copy of the board and makes the recursive call from MyopicPlayer level of minimax function of part b
    def min_player_part_b(self, board, depth_of_tree, alpha, beta):
        new_board = copy.deepcopy(board)
        new_board.MyopicPlayerAction()
        score, _ = self.h_minimax_part_b(depth_of_tree - 1, 2, new_board, alpha, beta)
        return score 

    #Minimax function with alpha-beta pruning to select next action of game tree player 
    def h_minimax_part_b(self, depth_of_the_tree, player_type, board, alpha, beta):
        self.count+=1 #counts the number of recursive calls
        # Base condition: check if required depth is reached or a winner has been found
        if depth_of_the_tree <= 0 or board.winner is not None:
            curr_state = board.GetCurrentState()
            # return self.evaluation_function_four(player_type, board, curr_state), None
            return self.evaluation_function_three(board), None
            # return self.evaluation_function_two(board), None
            # return self.evaluation_function_one(curr_state, player_type, board), None

        if player_type == 2:
            eval_score = -9999999
            best_col = None
            for col in self.moving_order_heuristic(): #uncomment this to use move ordering heuristic and comment next line
            # for col in range(7): 
                if self.CoinRowAfterAction(board.GetCurrentState(), col) != -1:
                    current_score = self.max_player_part_b(board, col, depth_of_the_tree, alpha, beta)
                    if current_score > eval_score:
                        eval_score = current_score
                        best_col = col
                    alpha = max(alpha, current_score)
                    #condition for pruning
                    if beta <= alpha:
                        break
            return eval_score, best_col
        else: 
            eval_score = 9999999
            worst_col = None
            for col in self.moving_order_heuristic(): #uncomment this to use move ordering heuristic and comment next line
            # for col in range(7):
                if self.CoinRowAfterAction(board.GetCurrentState(), col) != -1:
                    current_score = self.min_player_part_b(board, depth_of_the_tree, alpha, beta)
                    if current_score < eval_score:
                        eval_score = current_score
                        worst_col = col
                    beta = min(beta, current_score)
                    #condition for pruning
                    if beta <= alpha:
                        break
            return eval_score, worst_col

def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    numOfWins = 0
    moves = 0
    games = 50
    win_time = 0
    total_recurv_calls = 0
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    for _ in range(games):
        start_time = time.time()
        fourConnect = FourConnect()
        fourConnect.PrintGameState()
        gameTree = GameTreePlayer()
        
        move=0
        while move<42: #At most 42 moves are possible
            if move%2 == 0: #Myopic player always moves first
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner == 2:
                numOfWins+=1
                moves += move
                win_time += time.time() - start_time
                break
            elif fourConnect.winner is not None:
                break
        
        total_recurv_calls += gameTree.count
        if fourConnect.winner==None:
            print("Game is drawn.")
        else:
            print("Winner : Player {0}\n".format(fourConnect.winner))
            
        print("Moves : {0}".format(move))        

    avg_moves = 0
    if numOfWins == 0:
        avg_moves = float('inf')
    else:
        avg_moves = moves/numOfWins
    
    av_time = 0
    if numOfWins == 0:
        av_time = float('inf')
    else:
        av_time = win_time/numOfWins
    print("Time taken: ", av_time)
    print(f"Total recursive calls = {total_recurv_calls}")
    print(f"Number of wins out of {games}: ", numOfWins)
    print(f"Average moves to win: {avg_moves} \n")
    

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2020B3A70568G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    # RunTestCase()


if __name__=='__main__':
    main()
