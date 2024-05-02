import numpy as np

# parameters

# Bellman's formula parameters
alfa = .15
beta = .60
gamma = .99

# game parameters
win_points = 1.0
draw_points = 0.5
loss_points = 0

# simulation parameters
num_of_games_random = 1000 # how many games in random simulation
num_of_games_first = 2000 # how many games in simulation choosing the best first move
num_of_games_next = 5000 # how many games for every simulation after first move selection
num_of_simulations = 10 # how many simulations after first move selection


# find every place attacked by the opponent
def under_attack(board, number_opp, king_find=True, knight_find=True, rook_find=True):
    attacked_places = []

    # white pieces
    if number_opp == 1:

        # king
        if king_find:
            for i in [board.index("♔") - 1, board.index("♔") + 1]:
                if i in range(8):
                    if board[i] != "♘" and board[i] != "♖":
                        attacked_places.append(i)
        # knight
        if knight_find:
            if "♘" in board:
                for i in [board.index("♘") - 2, board.index("♘") + 2]:
                    if i in range(8):
                        if board[i] != "♔" and board[i] != "♖":
                            attacked_places.append(i)
        # rook
        if rook_find:
            if "♖" in board:
                # left side
                pos = board.index("♖") - 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos -= 1
                if board[pos] != "♘" and board[pos] != "♔":
                    attacked_places.append(pos)
                # right side
                pos = board.index("♖") + 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos += 1
                if board[pos] != "♘" and board[pos] != "♔":
                    attacked_places.append(pos)

    # black pieces
    else:
        # king
        if king_find:
            for i in [board.index("♚") - 1, board.index("♚") + 1]:
                if i in range(8):
                    if board[i] != "♞" and board[i] != "♜":
                        attacked_places.append(i)
        # knight
        if knight_find:
            if "♞" in board:
                for i in [board.index("♞") - 2, board.index("♞") + 2]:
                    if i in range(8):
                        if board[i] != "♚" and board[i] != "♜":
                            attacked_places.append(i)
        # rook
        if rook_find:
            if "♜" in board:
                # left side
                pos = board.index("♜") - 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos -= 1
                if board[pos] != "♞" and board[pos] != "♚":
                    attacked_places.append(pos)
                # right side
                pos = board.index("♜") + 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos += 1
                if board[pos] != "♞" and board[pos] != "♚":
                    attacked_places.append(pos)

    return attacked_places


# what choices the player has?
def poss_choices(board, number, check=False):
    choices = []

    # white pieces
    if number == 1:

        # king
        for i in [board.index("♔") - 1, board.index("♔") + 1]:
            if i in range(7):
                if board[i] != "♘" and board[i] != "♖":
                    hyp_board = board[:]
                    hyp_board[hyp_board.index("♔")] = " "
                    hyp_board[i] = "♔"
                    attacked = under_attack(hyp_board, 1 + number % 2)
                    if i not in attacked:
                        choices.append(("♔", i))
        # knight
        if "♘" in board:
            for i in [board.index("♘") - 2, board.index("♘") + 2]:
                if i in range(7):
                    if board[i] != "♔" and board[i] != "♖":
                        hyp_board = board[:]
                        hyp_board[hyp_board.index("♘")] = " "
                        hyp_board[i] = "♘"
                        if hyp_board.index("♔") not in under_attack(hyp_board, 1 + number % 2, king_find=False,
                                                                    knight_find=False):
                            choices.append(("♘", i))
        # rook
        if "♖" in board:
            # left side
            pos = board.index("♖") - 1
            while board[pos] == " ":
                choices.append(("♖", pos))
                pos -= 1
            if board[pos] != "♘" and board[pos] != "♔":
                choices.append(("♖", pos))
            # right side
            pos = board.index("♖") + 1
            while board[pos] == " ":
                choices.append(("♖", pos))
                pos += 1
            if board[pos] != "♘" and board[pos] != "♔":
                choices.append(("♖", pos))

        # if there is a check, verify your moves if they prevent from this check
        if check:
            l = len(choices)
            for i in range(l):
                piece_hyp, move_hyp = choices[i][0], choices[i][1]
                hyp_board = board[:]
                hyp_board[hyp_board.index(piece_hyp)] = " "
                hyp_board[move_hyp] = piece_hyp
                if hyp_board.index("♔") not in under_attack(hyp_board, 1 + number % 2, king_find=False):
                    choices.append(choices[i])
            choices = choices[l:] if len(choices) != l else []

    # black pieces
    else:

        # king
        for i in [board.index("♚") - 1, board.index("♚") + 1]:
            if i in range(8):
                if board[i] != "♞" and board[i] != "♜":
                    hyp_board = board[:]
                    hyp_board[hyp_board.index("♚")] = " "
                    hyp_board[i] = "♚"
                    attacked = under_attack(hyp_board, 1 + number % 2)
                    if i not in attacked:
                        choices.append(("♚", i))
        # knight
        if "♞" in board:
            for i in [board.index("♞") - 2, board.index("♞") + 2]:
                if i in range(8):
                    if board[i] != "♚" and board[i] != "♜":
                        hyp_board = board[:]
                        hyp_board[hyp_board.index("♞")] = " "
                        hyp_board[i] = "♞"
                        if hyp_board.index("♚") not in under_attack(hyp_board, 1 + number % 2, king_find=False,
                                                                    knight_find=False):
                            choices.append(("♞", i))
        # rook
        if "♜" in board:
            # left side
            pos = board.index("♜") - 1
            while board[pos] == " ":
                choices.append(("♜", pos))
                pos -= 1
            if board[pos] != "♞" and board[pos] != "♚":
                choices.append(("♜", pos))
            # right side
            pos = board.index("♜") + 1
            while board[pos] == " ":
                choices.append(("♜", pos))
                pos += 1
            if board[pos] != "♞" and board[pos] != "♚":
                choices.append(("♜", pos))

        # if there is a check, verify your moves if they prevent from this check
        if check:
            l = len(choices)
            for i in range(l):
                piece_hyp, move_hyp = choices[i][0], choices[i][1]
                hyp_board = board[:]
                hyp_board[hyp_board.index(piece_hyp)] = " "
                hyp_board[move_hyp] = piece_hyp
                if hyp_board.index("♚") not in under_attack(hyp_board, 1 + number % 2, king_find=False):
                    choices.append(choices[i])
            choices = choices[l:] if len(choices) != l else []

    return choices

# printing the board
def board_print(board):
    print("-" * (40 - board.count(" ")))
    l = ""
    for i in range(8): l += "| " + board[i] + " "
    l += "|"
    print(l)
    print("-" * (40 - board.count(" ")))

# initializing choices_ai dictionary
def initialize(cond=()):
    choices_ai = {}
    choices_points = {}
    for x in poss_choices(["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"], 1):
        hyp_board = ["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"]
        hyp_board[hyp_board.index(x[0])] = " "
        hyp_board[x[1]] = x[0]
        choices_points[tuple(hyp_board)] = 1 if x == cond else beta
    choices_ai[tuple(["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"])] = choices_points
    return choices_ai

choices_ai = initialize()

# verifying whether the next board state is after white's move or not
def white_move(board_curr, board_next):
    for piece in ["♔", "♘", "♖"]:
        if piece in board_next:
            if board_curr.index(piece) != board_next.index(piece): return True
    return False


# chess 1d gameplay
def chess1d_gameplay(inform=True, res_inform=True, random=False, player=False):
    # starting board
    board_play = ["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"]
    if inform: board_print(board_play)

    # white always goes first
    moving_player = 1
    check = False
    board_states = []

    # the game
    while True:

        # inform about checks
        if inform and check: print("Check!")

        # stalemate - player has no moves and there is no check
        if poss_choices(board_play, moving_player) == [] and not check:
            if res_inform: print("Stalemate!")
            if inform: print("White has no moves") if moving_player == 1 else print("Black has no moves")

            # leave only a tie and other player moves for this position
            if not random:
                new_choice = choices_ai[tuple(board_play)]
                del_boards = []
                for board in new_choice.keys():
                    if white_move(board_play, board) != (moving_player == 1):
                        del_boards.append(board)
                for boards in del_boards: del new_choice[boards]
                new_choice["tie"] = draw_points
                choices_ai[tuple(board_play)] = new_choice
            return "tie"

        # if some position repeats three times during a game - we have a stalemate
        if board_states.count(board_play) == 3:
            if res_inform: print("Stalemate!")
            if inform: print("The same position has repeated three times")
            return "tie"

        # if the only pieces left are kings, it's definitely a draw
        if board_play.count(" ") == 6:
            if res_inform: print("Stalemate!")
            if inform: print("The are only kings on the board")
            choices_ai[tuple(board_play)] = {"tie": draw_points}
            return "tie"

        # who is moving
        if inform: print("White moves") if moving_player == 1 else print("Black moves")

        # possible choices
        choices_list = poss_choices(board_play, moving_player, check=check)

        # taking a move from the random player or real player (black)
        if moving_player == 2 or random:

            # real player move
            if player:

                # taking a move from the player
                move, place = "", -1
                while move not in ["k", "n", "r"] or place not in range(8):
                    move = str(input("King - k, knight - n, rook - r: "))
                    place = int(input("Which position (1-8): ")) - 1

                # convert a letter into a piece
                if move == "k":
                    piece = "♚"
                elif move == "n":
                    piece = "♞"
                else:
                    piece = "♜"

                # combine move and place and find if the move is legal and if it is not - inform that it is not
                move_and_place = (piece, place)
                if move_and_place not in poss_choices(board_play, moving_player, check=check):
                    print("This move is unavailable for you!")
                    board_print(board_play)
                    continue

            # random move
            else:
                move_and_place = choices_list[np.random.randint(len(choices_list))]

            # the board after a random move is the best board for the random player
            if not random:
                best_board = board_play[:]
                best_board[best_board.index(move_and_place[0])] = " "
                best_board[move_and_place[1]] = move_and_place[0]
                best_board = tuple(best_board)

        # choosing a move for white with the best possible value
        if not random:
            if moving_player == 1:
                boards_and_moves = {}
                for i in choices_list:
                    hyp_board = board_play[:]
                    hyp_board[hyp_board.index(i[0])] = " "
                    hyp_board[i[1]] = i[0]
                    boards_and_moves[tuple(hyp_board[:])] = i

                # take into consideration that in choices_ai there are both black and white moves
                all_moves = choices_ai[tuple(board_play)]
                white_moves = {}
                for choice in all_moves:
                    if white_move(tuple(board_play), choice): white_moves[choice] = all_moves[choice]
                try:
                    best_value = max(white_moves.values())
                except:
                    return "errors"

                # find all moves with the best possible value and choose one
                bests = [x for x in white_moves.keys() if white_moves[x] == best_value]
                best_board = bests[np.random.randint(len(bests))]
                move_and_place = boards_and_moves[best_board]

            # if there is no continuation defined after a move, create possibilities for both white and black with beta value assigned
            if tuple(best_board) not in choices_ai.keys():
                choices_points = {}
                for i in range(1, 3):
                    king = "♚" if i == 1 else "♔"
                    if best_board.index(king) in under_attack(best_board, i, king_find=False):
                        hyp_check = True
                    else:
                        hyp_check = check
                    potential_choices = poss_choices(list(best_board), 1 + i % 2, check=hyp_check)

                    # if there is no next move for any player, then it has to be a win () or a draw
                    if potential_choices == []:
                        king = "♚" if i == 1 else "♔"
                        if best_board.index(king) in under_attack(best_board, moving_player, king_find=False):
                            choices_points["win/lose"] = win_points if king == "♚" else loss_points
                        else:
                            choices_points["tie"] = draw_points
                    else:
                        for x in potential_choices:
                            hyp_board = list(best_board)[:]
                            hyp_board[hyp_board.index(x[0])] = " "
                            hyp_board[x[1]] = x[0]
                            choices_points[tuple(hyp_board[:])] = beta
                choices_ai[tuple(best_board)] = choices_points

            # find the best value in the next move
            all_moves = choices_ai[tuple(best_board)]
            white_or_black_moves = {}
            for choice in all_moves:
                if choice in ["tie", "win/lose"] or white_move(tuple(best_board), choice) != (moving_player == 1):
                    white_or_black_moves[choice] = all_moves[choice]
            try:
                next_best_value = max(white_or_black_moves.values())
            except:
                return "errors"

            # assign a value to the chosen move using the Bellman's formula
            choices_ai[tuple(board_play)][best_board] = (1 - alfa) * best_value + alfa * gamma * next_best_value

        # make the chosen move
        piece, place = move_and_place[0], move_and_place[1]
        board_play[board_play.index(piece)] = " "
        board_play[place] = piece
        if inform: board_print(board_play)
        board_states.append(board_play[:])
        # checks
        king = "♚" if moving_player == 1 else "♔"
        if board_play.index(king) in under_attack(board_play, moving_player, king_find=False):
            check = True

            # checkmate
            if poss_choices(board_play, 1 + moving_player % 2, check=check) == []:
                if inform: print("Checkmate!")
                if res_inform:
                    print("White wins!") if moving_player == 1 else print("Black wins!")
                return "white" if moving_player == 1 else "black"

        # if there is no more check - deny it
        else:
            check = False
        moving_player = 1 + moving_player % 2

# random simulation
res_count = {"white": 0, "black": 0, "tie": 0, "errors": 0}
for i in range(num_of_games_random):
    result = chess1d_gameplay(inform=False, res_inform = False, random = True)
    res_count[result] += 1
print("Random simulation: " + str(res_count))
print("Winrate: " + str(round(res_count["white"]/num_of_games_random, 4)*100) + "%")
print("")

# simulation for every first move possible and select what gives you the best output
choices_ai_copies = {}

# for every first move possible, create choices_ai dictionary
for first_move in poss_choices(["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"], 1):
    choices_ai = initialize(first_move)

    # simulation
    res_count = {"white": 0, "black": 0, "tie": 0, "errors": 0}
    for i in range(num_of_games_first):
        result = chess1d_gameplay(inform=False, res_inform=False)
        res_count[result] += 1

    # save the move with its winrate
    winrate = res_count["white"] / num_of_games_first
    choices_ai_copies[winrate] = first_move

# select best move of every move considered
highest_winrate_move = choices_ai_copies[max(choices_ai_copies.keys())]

# show the best move
print("Best first move: " + str(highest_winrate_move))
print("")

# train 10 times using the best move from previous simulations
final_res = [0 for i in range(num_of_simulations)]
best_score = 0
best_dict = {}
for j in range(num_of_simulations):
    choices_ai = initialize(highest_winrate_move)

    # single simulation
    res_count = {"white": 0, "black": 0, "tie": 0, "errors": 0}
    for i in range(num_of_games_next):
        result = chess1d_gameplay(inform=False, res_inform=False)
        res_count[result] += 1
    print("Simulation " + str(j + 1) + ": " + str(res_count))
    final_res[j] = res_count["white"] / num_of_games_next * 100  # percentage
    if final_res[j] > best_score:
        best_score = final_res[j]
        best_dict = choices_ai

# show the results
print("")
print("Highest winrate: " + str(round(max(final_res), 2)) + "%")
print("Average winrate: " + str(round(sum(final_res) / num_of_simulations, 2)) + "%")
print("Lowest winrate: " + str(round(min(final_res), 2)) + "%")

print("Wanna play with the best one? (yes/no)")
ans = ""
while ans not in ["yes", "no"]:
    ans = str(input()).lower()

if ans == "yes":
    choices_ai = best_dict
    chess1d_gameplay(inform=True, res_inform=True, player=True)

while ans != "no":
    print("Wanna play more?")
    ans = ""
    while ans not in ["yes", "no"]:
        ans = str(input()).lower()
    if ans == "yes": chess1d_gameplay(inform=True, res_inform=True, player=True)
