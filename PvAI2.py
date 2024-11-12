import pygame, os

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PvP Tic Tac Toe")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FPS = 60
turn = "X"
turns = 0

taken_spaces = []
spaces = ("10,10", "310,10", "610,10", "10,180", "310,180", "610,180", "10,350", "310,350", "610,350")
X_spaces = []
O_spaces = []

#Lines and icons

VERTLINE1 = pygame.Rect(290, 0, 15, HEIGHT)
VERTLINE2 = pygame.Rect(595, 0, 15, HEIGHT)

HORILINE1 = pygame.Rect(0, 160, WIDTH, 10)
HORILINE2 = pygame.Rect(0, 330, WIDTH, 10)

X_icon = pygame.image.load(os.path.join('assets', 'X_icon.png'))
O_icon = pygame.image.load(os.path.join('assets', 'O_icon.png'))

X_icon = pygame.transform.scale(X_icon, (270, 140))
O_icon = pygame.transform.scale(O_icon, (270, 140))

Blue_crown = pygame.image.load(os.path.join('assets', 'Blue_crown.png'))
Red_crown = pygame.image.load(os.path.join('assets', 'Red_crown.png'))
handshake = pygame.image.load(os.path.join('assets', 'handshake.png'))

Blue_crown = pygame.transform.scale(Blue_crown, (500, 500))
Red_crown = pygame.transform.scale(Red_crown, (500, 500))
handshake = pygame.transform.scale(handshake, (500, 500))


def O_win():
    okay = True
    while okay == True:

        WIN.fill(WHITE)
        WIN.blit(Blue_crown, (200, 30))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    okay = False


def X_win():
    okay = True
    while okay == True:
        WIN.fill(WHITE)
        WIN.blit(Red_crown, (200, 30))
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        okay = False


def draw():
    okay = True
    while okay == True:
        WIN.fill(WHITE)
        WIN.blit(handshake, (200, 30))
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        okay = False


def check_victory(X_spaces, O_spaces, real):
    # Possible winning combinations
    possibilities = [
        ("10,10", "310,10", "610,10"),     # Top row
        ("10,180", "310,180", "610,180"),   # Middle row
        ("10,350", "310,350", "610,350"),   # Bottom row
        ("10,10", "10,180", "10,350"),      # Left column
        ("310,10", "310,180", "310,350"),   # Middle column
        ("610,10", "610,180", "610,350"),   # Right column
        ("10,10", "310,180", "610,350"),    # Diagonal from top-left
        ("10,350", "310,180", "610,10")     # Diagonal from bottom-left
    ]
    
    # Check for a win in X or O spaces
    for player, list in [("X", X_spaces), ("O", O_spaces)]:
        for possibility in possibilities:
            if all(coordinate in list for coordinate in possibility):
                if real:
                    X_win() if player == "X" else O_win()
                return player  # Returns "X" or "O" when a win is detected
    
    # Check for a draw if all spaces are filled
    if len(X_spaces) + len(O_spaces) == 9:
        if real:
            draw()
        return "Draw"
    
    # Game not over yet
    return "N/A" if not real else False
                

def drawing():
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, VERTLINE1)
    pygame.draw.rect(WIN, BLACK, VERTLINE2)
    pygame.draw.rect(WIN, BLACK, HORILINE1)
    pygame.draw.rect(WIN, BLACK, HORILINE2)
    pygame.display.update()


def get_mapped_value(value, mapping):
    for (low, high), result in mapping.items():
        if low <= int(value) <= high:
            return result
    return None


def placement(x, y, turn, taken_spaces, X_spaces, O_spaces):
    # Define mappings for x and y ranges
    x_map = {
        (0, 290): 10,
        (300, 590): 310,
        (600, float('inf')): 610
    }

    y_map = {
        (0, 160): 10,
        (170, 330): 180,
        (340, float('inf')): 350
    }

    # Get image_x and image_y using the mappings
    image_x = get_mapped_value(x, x_map)
    image_y = get_mapped_value(y, y_map)

    found = False

    # Has space been taken?
    for item in taken_spaces:
        check_x, check_y = item.split(",")
        if int(image_x) == int(check_x) and int(image_y) == int(check_y):
            found = True

    # Dont place
    if found == True:
        return False
    
    elif found == False:
            WIN.blit(X_icon if turn == "X" else O_icon, (image_x, image_y))
            coords = str(image_x) + "," + str(image_y)
            taken_spaces.append(coords)
            X_spaces.append(coords) if turn == "X" else O_spaces.append(coords)
            pygame.display.update()
            return True


def AI_turn(X_spaces, O_spaces, spaces, turns, player, movemade):
    finals = []  # List to store results of each possible move
    over = check_victory(X_spaces, O_spaces, False)

    # Base case: Game has ended, return result
    if over != "N/A":
        return [turns, over, movemade]

    # Check if the AI can win, prioritize winning
    winning_move = None
    for space in spaces:
        if (space not in X_spaces) and (space not in O_spaces):
            # Simulate the AI's move
            if player == "X":
                X_spaces.append(space)
                if check_victory(X_spaces, O_spaces, False) == "X":  # AI wins
                    winning_move = space
                X_spaces.remove(space)
            else:
                O_spaces.append(space)
                if check_victory(X_spaces, O_spaces, False) == "O":  # AI wins
                    winning_move = space
                O_spaces.remove(space)

    # If a winning move is found, make that move
    if winning_move:
        return [turns, "N/A", winning_move]  # Make the winning move

    # If no winning move, check for blocking
    opponent = "X" if player == "O" else "O"
    blocking_move = None
    for space in spaces:
        if (space not in X_spaces) and (space not in O_spaces):
            # Simulate the opponent's move
            if opponent == "X":
                X_spaces.append(space)
                if check_victory(X_spaces, O_spaces, False) == "X":  # Opponent wins after this move
                    blocking_move = space
                X_spaces.remove(space)
            else:
                O_spaces.append(space)
                if check_victory(X_spaces, O_spaces, False) == "O":  # Opponent wins after this move
                    blocking_move = space
                O_spaces.remove(space)

    # If a blocking move is found, block it
    if blocking_move:
        return [turns, "N/A", blocking_move]  # Block opponent's win

    # If it's the first move (X goes first), prioritize center if available
    if turns == 0 and player == "O":
        center = "310,180"  # Center of the board
        if center not in X_spaces and center not in O_spaces:
            return [turns, "N/A", center]

    # If the center is taken, prioritize corners over sides
    corners = ["10,10", "610,10", "10,350", "610,350"]
    for corner in corners:
        if corner not in X_spaces and corner not in O_spaces:
            return [turns, "N/A", corner]  # Take a corner if available

    # If no corner is available, take a side (middle of edges)
    sides = ["310,10", "10,180", "310,350", "610,180"]
    for side in sides:
        if side not in X_spaces and side not in O_spaces:
            return [turns, "N/A", side]  # Take a side if available

    # Iterate over each possible space and simulate a move (fallback)
    for space in spaces:
        if (space not in X_spaces) and (space not in O_spaces):
            # Make the move based on the player
            if player == "X":
                X_spaces.append(space)
                result = AI_turn(X_spaces, O_spaces, spaces, turns + 1, "O", space)
                X_spaces.remove(space)  # Undo move
            else:
                O_spaces.append(space)
                result = AI_turn(X_spaces, O_spaces, spaces, turns + 1, "X", space)
                O_spaces.remove(space)  # Undo move

            finals.append(result)  # Append result of this move

    # Choose the best move based on priority: Win > Draw > Lose
    # Initialize best with a losing scenario (turns = 0, unfavorable state)
    best = [999, "X" if player == "O" else "O", "1000,1000"]
    # Track win, draw, and loss scenarios
    for information in finals:
        if information[1] == player:  # Winning move
            # If no previous win or if this win happens sooner
            if best[1] != player or information[0] < best[0]:
                best = information
        elif information[1] == "Draw":  # Draw, only if no winning move
            if best[1] != player and best[1] != "Draw":
                best = information
        elif information[1] != player and information[1] != "Draw":  # Losing move
            if information[0] < best[0]:  # Prioritize losing after most moves (least negative outcome)
                best = information

    # Print for debugging purposes
    print("Chosen move:", best)
    
    return best  # Return the best move found


def main(turn, taken_spaces, X_spaces, O_spaces, over):
    clock = pygame.time.Clock()
    turn = "X"
    drawing()
    while not over:
        clock.tick(FPS)
        x,y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True 

            # When click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if turn == "X":
                        done = placement(x, y, turn, taken_spaces, X_spaces, O_spaces)

                        if done:
                            over = check_victory(X_spaces, O_spaces, True)


                            bestmove = AI_turn(X_spaces, O_spaces, spaces, 0, "O", "")
                            x, y = bestmove[2].split(",")
                            WIN.blit(O_icon, (int(x), int(y)))
                            taken_spaces.append(bestmove[2])
                            O_spaces.append(bestmove[2])
                            pygame.display.update()
                            over = check_victory(X_spaces, O_spaces, True)
                            print("over:", over)
                            turn = "X"
    
    pygame.quit()

#Life support

over = False

if __name__ == "__main__":
    main(turn, taken_spaces, X_spaces, O_spaces, over)