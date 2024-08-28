import sys
from random import choice
from math import inf
Moves={-1:" ♟️  ",0:"    ",1:" ♙️  "}

def draw_board(board_data):
    bg_black = "\u001b[48;5;237m"
    bg_white = "\u001b[48;5;245m"

    clear_to_eol = "\u001b[0m\u001b[K\n"

    board = ["1 ", bg_black, Moves[board_data[0][0]], bg_white, Moves[board_data[0][1]], bg_black, Moves[board_data[0][2]], clear_to_eol,
             "2 ", bg_white, Moves[board_data[1][0]], bg_black, Moves[board_data[1][1]], bg_white, Moves[board_data[1][2]], clear_to_eol,
             "3 ", bg_black, Moves[board_data[2][0]], bg_white, Moves[board_data[2][1]], bg_black, Moves[board_data[2][2]], clear_to_eol,
             "   A   B   C\n"];

    sys.stdout.write("".join(board))
def get_movement_direction(colour):
    direction = -1
    if colour == -1:
        direction = 1
    elif colour == 1:
        direction = -1
    else:
        raise ValueError("Invalid piece colour")

    return direction
def get_other_colour(colour):
    if colour == -1:
        return 1
    elif colour == 1:
        return -1
    else:
        raise ValueError("Invalid piece colour")
def get_allowed_moves(board_data, row, col):
    if board_data[row][col] == 0:
        return set()

    colour = board_data[row][col]
    other_colour = get_other_colour(colour)
    direction = get_movement_direction(colour)

    if (row + direction < 0 or row + direction > 2):
        return set() 

    allowed_moves = set()
    if board_data[row + direction][col] == 0:
        allowed_moves.add('F')
    if col > 0 and board_data[row + direction][col - 1] == other_colour:
        allowed_moves.add('L')
    if col < 2 and board_data[row + direction][col + 1] == other_colour:
        allowed_moves.add('R')

    return allowed_moves
def numberofAllowedMoves(board_data,colour):
    nom=0
    for i in range(3):
        for j in range(3):
            if(board_data[i][j]==colour):
                nom+=(len(get_allowed_moves(board_data,i,j)))
    return nom
def is_game_over(board_data,player):
    if board_data[0][0] == 1 or board_data[0][1] == 1 or board_data[0][2] == 1:
        return 1

    if board_data[2][0] == -1 or board_data[2][1] == -1 or board_data[2][2] == -1:
        return -1

    white_count = 0
    black_count = 0
    black_allowed_moves = []
    white_allowed_moves = []
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
    if(player==-1):
        if black_count == 0 or len(black_allowed_moves) == 0:
            return 1
    if(player==1):
        if white_count == 0 or len(white_allowed_moves) == 0:
            return -1
    return False
def getScore(board_data,player):
    if is_game_over(board_data,player)==1:
        return 10

    if is_game_over(board_data,player) == -1:
        return -10
    else:
        return 0
def getMoves(player,board_data):
    mov=[]
    for i in range(3):
        for j in range(3):
            if(board_data[i][j]==player):
                for k in get_allowed_moves(board_data,i,j):
                    mov.append(((i,j),k))
    return mov
def setMove(board_data, move, player):
    (row,col),Move=move
    direction = get_movement_direction(player)
    if Move == 'F' :
        board_data[row + direction][col] = board_data[row][col]
    elif Move == 'L' :
        board_data[row + direction][col - 1] = board_data[row][col]
    elif Move == 'R' :
        board_data[row + direction][col + 1] = board_data[row][col]
    board_data[row][col] = 0
def undoMove(board_data, move,player):
    (row,col),Move=move
    direction = get_movement_direction(player)
    if Move == 'F':
        board_data[row][col] = board_data[row+direction][col]
        board_data[row+direction][col] = 0
    elif Move == 'L':
        board_data[row][col] = board_data[row+direction][col-1]
        board_data[row+direction][col-1]=get_other_colour(player)
    elif Move == 'R':
        board_data[row][col] = board_data[row+direction][col+1]
        board_data[row+direction][col+1]=get_other_colour(player)
def abminimax(board_data,alpha, beta, player):
  row = -1
  col = -1
  m=0
  if is_game_over(board_data,player):
      return [row,col,m ,getScore(board_data,player)]

  else:
      for move in getMoves(player,board_data):
          setMove(board_data, move, player)
          score = abminimax(board_data, alpha, beta, -player)
          if player == 1:
              if score[3] > alpha:
                  alpha = score[3]
                  (row,col),m=move
          else:
              if score[3] < beta:
                  beta = score[3]
                  (row,col),m=move
          undoMove(board_data, move, player)
          if alpha >= beta:
              break
      if player == 1:
          return [row,col,m, alpha]

      else:
          return [row, col,m, beta]
def get_computer_move(board_data, colour):
    if(colour==1 and board_data[2][0] == 1 and board_data[2][1] == 1 and board_data[2][2] == 1):
        direction = get_movement_direction(colour)
        row=2
        col = choice([0, 1, 2])
        board_data[row + direction][col] = board_data[row][col]
        board_data[row][col] = 0
        return board_data
    else:
        result = abminimax(board_data, -inf, inf, colour)
        row=result[0]
        col=result[1]
        move=result[2]
        setMove(board_data, ((row,col),move), colour)
        return board_data
def get_human_move(board_data, colour):
    direction = get_movement_direction(colour)
    while True:
        piece_posn = input(f'What {Moves[colour]} do you want to move? ')

        valid_inputs = {'a1': (0,0), 'b1': (0,1), 'c1': (0,2),
                        'a2': (1,0), 'b2': (1,1), 'c2': (1,2),
                        'a3': (2,0), 'b3': (2,1), 'c3': (2,2)}
        if piece_posn.lower() not in valid_inputs:
            print("LOL that's not a valid position! Try again.")
            continue
        
        (row, col) = valid_inputs[piece_posn.lower()]
        piece = board_data[row][col]
        if piece == 0:
            print("What are you trying to pull, there's no piece in that space!")
            continue

        if piece != colour:
            print("LOL that's not your piece, try again!")
            continue

        allowed_moves = get_allowed_moves(board_data, row, col)

        if len(allowed_moves) == 0:
            print('LOL nice try. That piece has no valid moves.')
            continue

        move = list(allowed_moves)[0]
        if len(allowed_moves) > 1:
            move = input(f'What move do you want to make ({",".join(list(allowed_moves))})? ')
            if move.upper() not in allowed_moves:
                print('LOL that move is not allowed. Try again.')
                continue

        if move == 'F' or move == 'f':
            board_data[row + direction][col] = board_data[row][col]
        elif move == 'L' or move == 'l':
            board_data[row + direction][col - 1] = board_data[row][col]
        elif move == 'R' or move == 'r':
            board_data[row + direction][col + 1] = board_data[row][col]

        board_data[row][col] = 0
        return board_data
def play_game(Player):  
    board_data = [[-1, -1, -1],
                  [0, 0, 0],
                  [1, 1, 1]]
    
    last_player = -1
    next_player = 1
      
    while not is_game_over(board_data,next_player):
        draw_board(board_data)
        if(Player==1):
            board_data = get_human_move(board_data, next_player)
        else:
            board_data=get_computer_move(board_data, next_player)
        Player*=-1
        temp = last_player
        last_player = next_player
        next_player = temp
    draw_board(board_data)
    winner = Moves[is_game_over(board_data,next_player)]
    print(f'Congratulations {winner}!')
def start_game():
  while True:
    try:
        turn = int(input('Enter to play 1st or 2nd: '))
        if not (turn == 1 or turn == 2):
            print('Please pick 1 or 2')
        else:
            break
    except(KeyError, ValueError):
        print('Enter a number!')
  if turn == 2:
    currentPlayer = -1
  else:
    currentPlayer = 1
  play_game(currentPlayer)
print("=================================================")
print("HexaPawn using MINIMAX with ALPHA-BETA Pruning")
print("=================================================")
start_game()

    