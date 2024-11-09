rows, cols = 8,8
board = []
SYMBOLS = {
    "V_SEP": " | ", 
    "H_SEP": "-"     
}
colors = {
    'W' : 'B',
    'B' : 'W'
}


def start_board(rows, cols):
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i+j)%2 == 0:
                if i<3:
                    row.append('W')
                elif i>4:
                    row.append('B') 
                else:
                    row.append('0')
            else:
                row.append(' ')
        board.append(row)
        row = []
    return(board)


def moves(start, finish, color, board):
    i_start, j_start = start
    i_finish, j_finish = finish
    global second_turn
    global last_used_piece
    # Check for regular piece 
    if board[i_start][j_start] == color.upper():
        # Regular move
        if abs(i_finish - i_start) == 1 and abs(j_start - j_finish) == 1 and board[i_finish][j_finish] == '0':
            if color == 'W' and i_start < i_finish:  
                board[i_start][j_start] = '0'
                if i_finish == 7:
                    board[i_finish][j_finish] = 'w'
                else:
                    board[i_finish][j_finish] = 'W'
                return True
            elif color == 'B' and i_start > i_finish:  
                board[i_start][j_start] = '0'
                if i_finish == 0:
                    board[i_finish][j_finish] = 'b'
                else:
                    board[i_finish][j_finish] = 'B'
                return True
            else:
                print(f"This is not the right direction for {color}, try again")
                return False

        # Jumping over an opponent's piece
        elif abs(i_finish - i_start) == 2 and abs(j_start - j_finish) == 2 and board[i_finish][j_finish] == '0':
            middle_i = (i_start + i_finish) // 2
            middle_j = (j_start + j_finish) // 2
            if board[middle_i][middle_j].upper() == colors[color]:  
                
                if color == 'W':  
                    board[i_start][j_start] = '0'
                    board[i_finish][j_finish] = 'W'
                    board[middle_i][middle_j] = '0'  
                    if (can_continue_eating(i_finish, j_finish, board, color)):
                        print('You can continue eating with this piece or input 0 0 and 0 0 to skip your turn')
                        second_turn = True
                        last_used_piece = (i_finish, j_finish)
                    else: second_turn = False
                    return not (can_continue_eating(i_finish, j_finish, board, color))
                    
                elif color == 'B':  
                    board[i_start][j_start] = '0'
                    board[i_finish][j_finish] = 'B'
                    board[middle_i][middle_j] = '0'  
                    if (can_continue_eating(i_finish, j_finish, board, color)):
                        print('You can continue eating with this piece or input 0 0 and 0 0 to skip your turn')
                        second_turn = True
                        last_used_piece = (i_finish, j_finish)
                    else: second_turn = False
                    return not (can_continue_eating(i_finish, j_finish, board, color))
                else:
                    print(f"This is not the right direction for {color} to eat, try again")
                    return False
            else:
                print('There is no opponent piece to jump over.')
                return False

    # King move
    elif board[i_start][j_start] == color.lower() and board[i_finish][j_finish] == '0':
        if abs(i_finish - i_start) == abs(j_finish - j_start):
            step_i = 1 if i_finish > i_start else -1
            step_j = 1 if j_finish > j_start else -1

        # Check for friendly pieces on the way
            for i in range(1, abs(i_finish - i_start)):
                check_i = i_start + i * step_i
                check_j = j_start + i * step_j
                if board[check_i][check_j].upper() == color:
                    print('There is a friendly piece on your way')
                    return False
                elif board[check_i][check_j].upper() == colors[color]:
                    board[check_i][check_j] = '0'

        # Move the king to the destination
            board[i_start][j_start] = '0'
            board[i_finish][j_finish] = color.lower()
            if (can_continue_king_eating(i_finish, j_finish, board, color)):
                print('You can continue eating with this piece or input 0 0 and 0 0 to skip your turn')
                second_turn = True
                last_used_piece = (i_finish, j_finish)
            else: second_turn = False
            return not (can_continue_king_eating(i_finish, j_finish, board, color))

        else:
            print('You cannot move the king this way')
            return False


#Check for game ending
def end_game(board,color):
 
    pieces_left = any(color in row for row in board)
    if not pieces_left:
        print(f"Player {color} has no pieces left! Game Over!")
        return True
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == color:
                if has_valid_move(board, i, j, color):
                    return False
    
    print(f"Player {color} has no valid moves! Game Over!")
    return True

def has_valid_move(board, i, j, color):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    piece = board[i][j]

    if piece.upper() == color:
        for di, dj in directions:
            ni, nj = i + di, j + dj

            if 0 <= ni < len(board) and 0 <= nj < len(board[i]) and board[ni][nj] == '0':
                return True

            ni_jump, nj_jump = i + 2 * di, j + 2 * dj
            if (
                0 <= ni_jump < len(board)
                and 0 <= nj_jump < len(board[i])
                and board[ni][nj].upper() == colors[color] 
                and board[ni_jump][nj_jump] == '0'         
            ):
                return True

    
    elif piece.lower() == color.lower():
        for di, dj in directions:
            ni, nj = i + di, j + dj
            while 0 <= ni < len(board) and 0 <= nj < len(board[i]):
                if board[ni][nj] == '0':
                    return True

               
                if board[ni][nj].upper() == colors[color]:
                    ni_jump, nj_jump = ni + di, nj + dj
                    if (
                        0 <= ni_jump < len(board)
                        and 0 <= nj_jump < len(board[i])
                        and board[ni_jump][nj_jump] == '0'
                    ):
                        return True
                    break  

                ni += di
                nj += dj

    return False

end = False    
color = 'W'
board = start_board(rows, cols)

def mark_possible_moves(board, color):
    
    marked_board = [row[:] for row in board]

    for i in range(len(board)):
        for j in range(len(board[i])):
            piece = board[i][j]

            if piece.upper() == color.upper(): 
                directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

                # Regular piece moves
                if piece == color.upper():
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < len(board) and 0 <= nj < len(board[i]) and board[ni][nj] == '0':
                            marked_board[ni][nj] = '*'

                        # Jumping over an opponent's piece
                        ni_jump, nj_jump = i + 2 * di, j + 2 * dj
                        if (
                            0 <= ni_jump < len(board)
                            and 0 <= nj_jump < len(board[i])
                            and board[ni][nj].upper() == colors[color] 
                            and board[ni_jump][nj_jump] == '0' 
                        ):
                            marked_board[ni_jump][nj_jump] = '*'

                # King piece moves
                elif piece.lower() == color.lower():
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        while 0 <= ni < len(board) and 0 <= nj < len(board[i]):
                            if board[ni][nj] == '0':
                                marked_board[ni][nj] = '*'
                            elif board[ni][nj].upper() == colors[color]:
                                ni_jump, nj_jump = ni + di, nj + dj
                                if (
                                    0 <= ni_jump < len(board)
                                    and 0 <= nj_jump < len(board[i])
                                    and board[ni_jump][nj_jump] == '0'
                                ):
                                    marked_board[ni_jump][nj_jump] = '*'
                                break
                            else:
                                break

                            ni += di
                            nj += dj

    return marked_board

def print_board_with_moves(board, marked_board, rows):
    print("    " + " | ".join(str(i) for i in range(len(board[0]))))
    print(SYMBOLS["H_SEP"] * (len(board[0]) * 4 + 1))

    for i in range(rows):
        row = board[i]
        marked_row = marked_board[i]

        row_display = []
        for j in range(len(row)):
            if marked_row[j] == '*':
                row_display.append('*')
            else:
                row_display.append(row[j])

        print(f"{i} | " + SYMBOLS["V_SEP"].join(row_display))

        if i < len(board) - 1:
            print(SYMBOLS["H_SEP"] * (len(board[0]) * 4 + 2))

def can_continue_eating(i, j, board, color):
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    opponent_color = colors[color]

    for di, dj in directions:
        ni, nj = i + di, j + dj
        middle_i, middle_j = i + di // 2, j + dj // 2

        # Check if the destination and middle cells are within bounds
        if (
            0 <= ni < len(board) and 0 <= nj < len(board[0])  
            and board[ni][nj] == '0' 
            and board[middle_i][middle_j].upper() == opponent_color  
        ):
            return True  

    return False  


def can_continue_king_eating(i, j, board, color):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    opponent_color = colors[color]

    for di, dj in directions:
        ni, nj = i + di, j + dj
        opponent_found = False  

        while 0 <= ni < len(board) and 0 <= nj < len(board[0]):
            if board[ni][nj] == '0' and opponent_found:
                
                return True
            elif board[ni][nj].upper() == color:
                
                break
            elif board[ni][nj].upper() == opponent_color:
                if opponent_found:
                    
                    break
                opponent_found = True  
            else:
                opponent_found = False

            
            ni += di
            nj += dj

    return False  

# Game
end = False    
color = 'W'
board = start_board(rows, cols)
second_turn = False
last_used_piece =()

board = [
    ['W', ' ', '0', ' ', '0', ' ', '0', ' '],
    [' ', '0', ' ', 'B', ' ', '0', ' ', '0'],
    ['0', ' ', '0', ' ', '0', ' ', 'B', ' '],
    [' ', '0', ' ', '0', ' ', 'B', ' ', '0'],
    ['0', ' ', '0', ' ', '0', ' ', '0', ' '],
    [' ', '0', ' ', '0', ' ', 'B', ' ', '0'],
    ['0', ' ', '0', ' ', 'w', ' ', '0', ' '],
    [' ', '0', ' ', '0', ' ', '0', ' ', '0']
] #for debugging

while not end:
    marked_board = mark_possible_moves(board, color)
    print_board_with_moves(board, marked_board, rows)
    print('Your color:', color)

    try:
        start_input = input("Input starting position (i j): ")
        finish_input = input("Input finish position (i j): ")

        # Try to convert input into two integers
        start = tuple(map(int, start_input.split()))
        finish = tuple(map(int, finish_input.split()))
        # Ensure there are exactly two integers for each input
        if len(start) != 2 or len(finish) != 2:
            print("Invalid input, please enter exactly two integers separated by space.")
            continue
    except ValueError:
        print("Invalid input, please enter valid integers.")
        continue
    if start == (0, 0) and finish == (0, 0):
        color = colors[color]
        second_turn = False
        continue
    if second_turn:
        if start != last_used_piece:
            print('Uou are supposed to play the same piece')
            continue
    if not (0<=start[1]<=7 and 0<=start[0]<=7 and 0<=finish[1]<=7 and 0<=finish[1]<=7):
        print('Invalid coordinates')
        continue
    if moves(start, finish, color, board):
        color = colors[color]
        end = end_game(board, color)
    else:
        continue
