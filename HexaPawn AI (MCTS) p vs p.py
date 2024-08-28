# Import necessary modules
import sys
import math
from random import choice
import copy

# Define the mapping of piece values to symbols to represent pieces on the board
Moves={-1:" ♟️  ",0:"    ",1:" ♙️  "}
# Dictionary to represent the game tree
tree=dict()

# Function to draw the game board
def draw_board(board_data):
    # ANSI escape codes for background colors
    bg_black = "\u001b[48;5;237m"
    bg_white = "\u001b[48;5;245m"

    # ANSI escape code to clear the line
    clear_to_eol = "\u001b[0m\u001b[K\n"

    # Board representation with pieces and colors
    board = ["1 ", bg_black, Moves[board_data[0][0]], bg_white, Moves[board_data[0][1]], bg_black, Moves[board_data[0][2]], clear_to_eol,
             "2 ", bg_white, Moves[board_data[1][0]], bg_black, Moves[board_data[1][1]], bg_white, Moves[board_data[1][2]], clear_to_eol,
             "3 ", bg_black, Moves[board_data[2][0]], bg_white, Moves[board_data[2][1]], bg_black, Moves[board_data[2][2]], clear_to_eol,
             "   A   B   C\n"];

    # Printing the board
    sys.stdout.write("".join(board))

# Function to determine the direction of movement for a given color   
def get_movement_direction(colour):
    direction = -1
    if colour == -1:
        direction = 1
    elif colour == 1:
        direction = -1
    else:
        raise ValueError("Invalid piece colour")

    return direction

# Function to get the opposite color
def get_other_colour(colour):
    if colour == -1:
        return 1
    elif colour == 1:
        return -1
    else:
        raise ValueError("Invalid piece colour")
    
# Function to get allowed moves for a given piece
def get_allowed_moves(board_data, row, col):
    if board_data[row][col] == 0:
        return set()

    colour = board_data[row][col]
    other_colour = get_other_colour(colour)
    direction = get_movement_direction(colour)

    if (row + direction < 0 or row + direction > 2):
        return set() 

    # Checking for valid moves
    allowed_moves = set()
    if board_data[row + direction][col] == 0:
        allowed_moves.add('F')
    if col > 0 and board_data[row + direction][col - 1] == other_colour:
        allowed_moves.add('L')
    if col < 2 and board_data[row + direction][col + 1] == other_colour:
        allowed_moves.add('R')

    return allowed_moves
# Function to check if the game is over
def is_game_over(board_data,player):

    # Check if the player has reached the opposite end
    if board_data[0][0] == 1 or board_data[0][1] == 1 or board_data[0][2] == 1:
        return 1

    if board_data[2][0] == -1 or board_data[2][1] == -1 or board_data[2][2] == -1:
        return -1

    # Check if any player has no pieces left or no valid moves
    white_count = 0
    black_count = 0
    black_allowed_moves = []
    white_allowed_moves = []

    # Count pieces and collect allowed moves for both players
    for i in range(3):
        for j in range(3):
            moves = get_allowed_moves(board_data, i, j)
            if board_data[i][j] == 1:
                white_count += 1
                if len(moves) > 0:
                    white_allowed_moves.append((i,j,moves))
            if board_data[i][j] == -1:
                black_count += 1
                if len(moves) > 0:
                    black_allowed_moves.append((i,j,moves))
    if player==-1:
        if black_count == 0 or len(black_allowed_moves) == 0:
            return 1
    if white_count == 0 or len(white_allowed_moves) == 0:
        return -1
    return False

# Function to get possible moves for a player
def getMoves(player,board_data):
    mov=[]
    for i in range(3):
        for j in range(3):
            if(board_data[i][j]==player):
                for k in get_allowed_moves(board_data,i,j):
                    mov.append(((i,j),k))
    return mov

# Function to set a move on the board
def setMove(board_data, move, player):
    (row,col), Move = move
    direction = get_movement_direction(player)

    if Move == 'F':
        if 0 <= row + direction < 3 and 0 <= col < 3:  
            board_data[row + direction][col] = board_data[row][col]
    elif Move == 'L':
        if 0 <= row + direction < 3 and 0 <= col - 1 < 3:
            board_data[row + direction][col - 1] = board_data[row][col]
    elif Move == 'R':
        if 0 <= row + direction < 3 and 0 <= col + 1 < 3:  
            board_data[row + direction][col + 1] = board_data[row][col]
    
    board_data[row][col] = 0

# Function to select a random child node from a promising node
def getRandomChildNode(promisingNode):
    randomChild=choice(tree[promisingNode][2])
    return randomChild

# Function to check if a simulation resulted in a win for a specific player
def checkStatus(w,colour):
    if(w==colour):
        return 1
    else:
        return 0
    
# Function to retrieve the parent node of a given node
def getparent(promisingNode):
    for parent in tree:
        if(promisingNode in tree[parent][2]):
            return parent

# Function to simulate random playouts from a given node
def simulateRandomPlayout(nodeToExplore, colour, board_data, num_simulations):
    total_wins = 0
    for _ in range(num_simulations):
        opponent = get_other_colour(colour)
        temp_board = copy.deepcopy(board_data)
        setMove(temp_board, nodeToExplore, opponent)
        tree[nodeToExplore] = [getparent(nodeToExplore), temp_board, getMoves(colour, temp_board), 0, 0]
        node = nodeToExplore
        player = opponent

         # Continue until the game is over
        while not is_game_over(temp_board, player):
            randomChild = getRandomChildNode(node)
            player *= -1
            setMove(temp_board, randomChild, player)
            opponent = get_other_colour(player)
            tree[randomChild] = [getparent(randomChild), temp_board, getMoves(opponent, temp_board), 0, 0]
            node = randomChild
        player *= -1

        # Update total wins based on the game outcome
        total_wins += checkStatus(is_game_over(tree[node][1], player), colour)
     # Return the win rate and the node  
    return total_wins / num_simulations, node

# Function to calculate the UCB1 score for a node
def ucb_score(total_visits, node_wins, parent_visits, win_rate):
    exploration_constant = math.sqrt(2)
    if total_visits == 0:
        return float('inf')
    exploitation = win_rate
    exploration = exploration_constant * math.sqrt(math.log(parent_visits) / total_visits)
    return exploitation + exploration

# Function for the selection phase of MCTS
def selection(board_data, colour, num_simulations):
    best_move = None
    best_ucb_score = float('-inf')
    
    for move in getMoves(colour, board_data):
        node = move
        parent = getparent(node)
        if parent is None:
            continue
        parent_visits = tree[parent][3]
        total_visits = tree[node][3]
        node_wins = tree[node][4]
        win_rate, _ = simulateRandomPlayout(node, colour, board_data, num_simulations)
        ucb = ucb_score(total_visits, node_wins, parent_visits, win_rate)
        
        if ucb > best_ucb_score:
            best_move = move
            best_ucb_score = ucb
    
    if best_move is None:
        return choice(getMoves(colour, board_data))
    
    return best_move

# Function to perform Monte Carlo Tree Search
def MCTS(board_data, colour, num_simulations=100000000000000):
    return selection(board_data, colour, num_simulations)

# Function to play the game
def get_computer_move(board_data, colour):
        result = MCTS(board_data,colour)
        (row,col)=result[0]
        move=result[1]
        setMove(board_data, ((row,col),move), colour)
        return board_data

# Function to get a move from the human player
def get_human_move(board_data, colour):
     # Determine the movement direction based on the piece color
    direction = get_movement_direction(colour)
    while True:
        # Ask the player for the piece they want to move
        piece_posn = input(f'What {Moves[colour]} do you want to move? ')
        # Dictionary mapping input positions to board coordinates
        valid_inputs = {'a1': (0,0), 'b1': (0,1), 'c1': (0,2),
                        'a2': (1,0), 'b2': (1,1), 'c2': (1,2),
                        'a3': (2,0), 'b3': (2,1), 'c3': (2,2)}
        
        # Validate the input position
        if piece_posn.lower() not in valid_inputs:
            print("LOL that's not a valid position! Try again.")
            continue
        # Get the row and column corresponding to the input position
        (row, col) = valid_inputs[piece_posn.lower()]
        # Check if there's a piece at the selected position
        piece = board_data[row][col]
        if piece == 0:
            print("What are you trying to pull, there's no piece in that space!")
            continue
        # Check if the selected piece belongs to the player
        if piece != colour:
            print("LOL that's not your piece, try again!")
            continue
        
        # Get the allowed moves for the selected piece
        allowed_moves = get_allowed_moves(board_data, row, col)
        # Check if the selected piece has valid moves
        if len(allowed_moves) == 0:
            print('LOL nice try. That piece has no valid moves.')
            continue
        # Choose the move automatically if there's only one option
        move = list(allowed_moves)[0]
        if len(allowed_moves) > 1:
             # If multiple moves are possible, ask the player to choose
            move = input(f'What move do you want to make ({",".join(list(allowed_moves))})? ')
            if move.upper() not in allowed_moves:
                print('LOL that move is not allowed. Try again.')
                continue
        
        # Apply the selected move to the board
        if move == 'F' or move == 'f':
            board_data[row + direction][col] = board_data[row][col]
        elif move == 'L' or move == 'l':
            board_data[row + direction][col - 1] = board_data[row][col]
        elif move == 'R' or move == 'r':
            board_data[row + direction][col + 1] = board_data[row][col]

        
        # Update the position of the selected piece
        board_data[row][col] = 0

        # Return the updated board state
        return board_data
    
# Function to play the game
def play_game(Player): 
    # Initial board state  
    board_data = [[-1, -1, -1],
                  [0, 0, 0],
                  [1, 1, 1]]
    
    last_player = -1
    next_player = 1
      
    while not is_game_over(board_data,next_player):
        # Draw the current board state
        draw_board(board_data)

        # Check which player is playing and get their move accordingly
        if(Player==1):
            # If it's the human player's turn, get their move   
            board_data = get_human_move(board_data, next_player)
        else:
            # If it's the computer's turn, let it make a move
            board_data=get_computer_move(board_data, next_player)
        # Switch the player for the next turn
        Player*=-1
        # Swap the last and next players for tracking purposes
        temp = last_player
        last_player = next_player
        next_player = temp
    # Draw the final board state
    draw_board(board_data)
    # Determine the winner and print the congratulations message
    winner = Moves[is_game_over(board_data,next_player)]
    print(f'Congratulations {winner}!')

# Function to start the game and determine player turns
def start_game():
   # Loop until valid input is received
  while True:
    try:
         # Prompt the player to choose their turn   
        turn = int(input('Enter to play 1st or 2nd: '))
         # Check if the input is valid
        if not (turn == 1 or turn == 2):
            print('Please pick 1 or 2')
        else:
            break
    except(KeyError, ValueError):
        print('Enter a number!')
  # Set the current player based on the chosen turn
  if turn == 2:
    currentPlayer = -1
  else:
    currentPlayer = 1

 # Start the game with the chosen player
  play_game(currentPlayer)

# Main function to start the game
print("==========================================")
print("HexaPawn using MonteCarlo Search Algorithm")
print("==========================================")
# Start the game
start_game()
