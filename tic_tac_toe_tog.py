"""
  
 module name: tic_tac_toe_fun.py
 purpose    : game for tic_tac_toe 
  Notes:
    - Use 'toggle' to switch player
    - Use a list  [0,'X','O'] to define player, players[1] == 'X' and players[-1] == 'O'
    - Use random.choice function to determine who go first

"""

from IPython.display import clear_output
import random


##########################################################################################
# Function Name :   display_board
# Purpose       :   Display board from list a and b
# Parameters
#              a:   A list of available board
#              b:   A list of tic_tac_toe board
##########################################################################################


def display_board(a,b):
    print('Available   TIC-TAC-TOE\n'+
           '  moves\n\n  '+
          a[7]+'|'+a[8]+'|'+a[9]+'        '+b[7]+'|'+b[8]+'|'+b[9]+'\n  '+
          '-----        -----\n  '+
          a[4]+'|'+a[5]+'|'+a[6]+'        '+b[4]+'|'+b[5]+'|'+b[6]+'\n  '+
          '-----        -----\n  '+
          a[1]+'|'+a[2]+'|'+a[3]+'        '+b[1]+'|'+b[2]+'|'+b[3]+'\n')

##########################################################################################
# Function Name :   place_marker
# Purpose       :   Base on position to assign 'marker' to 'board' and ' ' to 'available'
# Parameters
#       marker  :   The marker would be 'X' or 'O'
#       position:   The position would be number 1-9
##########################################################################################


def place_marker(board, available, marker, position):
    board[position] = marker
    available[position] = ' '

##########################################################################################
# Function Name :   win_check
# Purpose       :   Check if someone has won the game
# Parameters
#       mark    :   marker would be 'X' or 'O'
#       board   :   tic_tac_toe board board
##########################################################################################


def win_check(board,mark):
    
    return ((board[7] == mark and board[8] == mark and board[9] == mark) or # across the top
    (board[4] == mark and board[5] == mark and board[6] == mark) or # across the middle
    (board[1] == mark and board[2] == mark and board[3] == mark) or # across the bottom
    (board[7] == mark and board[4] == mark and board[1] == mark) or # down the middle
    (board[8] == mark and board[5] == mark and board[2] == mark) or # down the middle
    (board[9] == mark and board[6] == mark and board[3] == mark) or # down the right side
    (board[7] == mark and board[5] == mark and board[3] == mark) or # diagonal
    (board[9] == mark and board[5] == mark and board[1] == mark)) # diagonal




##########################################################################################
# Function Name :   full_board_check
# Purpose       :   Check if tic_tac_toe board board is available
# Parameter
#       board   :   tic_tac_toe board board
##########################################################################################



def full_board_check(board):
    for position in range(1,10):
        if board[position] == ' ':
            return False
            break
    return True
##########################################################################################
# Function Name :   player_choice
# Purpose       :   Choice the available position 
# Parameter
#       board   :   tic_tac_toe board board
#       cho_ava :   A list of available choice
#       player  :   Player 'X' or 'O'
##########################################################################################


def player_choice(board, player, cho_ava):
    position = 0    
    while position not in cho_ava or not board[position] == ' ' :
        position = int(input('Hi player {}, choose your next position: {} '.format(player, cho_ava)))
        if position not in cho_ava:
           print ('You enter incorrect number {}. The correct number should be in {}. please try again'.format(position, cho_ava)) 
    return position

##########################################################################################
# Function Name :   play_game
# Purpose       :   Play the game 
#                   - Invoke display_board to display available board and tic_tac_toe board
#                   - Invoke player_choice to choice the available position
#                   - Invoke place_marker to update available board and tic_tac_toe board
#                   - Invoke win_check to check if there is a winner  
# Parameter
#     board     :   tic_tac_toe board
#     available :   Available board
#     cho_ava   :   A list of available choice
#     player    :   Player 'X' or 'O'
#     game_on   :   Booleen variable to determine to continue the game or not 
##########################################################################################

def play_game(board, available, cho_ava, player,  game_on):
    display_board(available, board)
   
    position = player_choice(board, player , cho_ava)
    cho_ava.remove(position)  
    
    place_marker(board, available, player, position)
    
    if win_check(board, player):
       display_board(available, board)
       print('Hi player {}, congratulations! You have won the game!'.format(player))
       game_on = False
       return game_on 
    else:         
       if full_board_check(board):             
          display_board(available, board)
          print('The game is a draw!')
          game_on = False
          return  game_on
       else:
          return  game_on  


##########################################################################################
# Main process start here
#   - Use while loops and the functions to play the game
##########################################################################################


if __name__ == '__main__':
  print('Welcome to Tic Tac Toe!')
  while True:
    # Reset the board
    theBoard  = [' '] * 10                          # Initialize cells in tic_tac_toe board as blank
    available = [str(num) for num in range(0,10)]   # A list comprehension to define available cells 
    cho_ava   = [num for num in range(1,10)]        # A list of available choice
    players   = [0,'X','O']                         # players[1] == 'X' and players[-1] == 'O'

    toggle    = random.choice((-1,1))               # Apply random.choice to choose a random element from -1 or 1
    player    = players[toggle]
    print(' %s will go first.'%(player))
    game_on   = True
    input('Hit Enter to continue')
        
    while game_on:
          player = players[toggle]   
          game_on=play_game(theBoard, available, cho_ava, player, game_on)
          toggle *= -1                      
          print("game_on", game_on)

    replay = input('Do you want to play again? Enter Yes or No: ').lower().startswith('y')   # return true if input 'Yes'
    if not replay:
           break        
