# Improved version of the previous AI, this one relies solely on the minimaxing algorithm rather than relying on static assistance.
# This time I kept the move-deciding and scoring/recursion algorithms separate; AI_turn and minimax respectively.

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


def minimax(X_spaces, O_spaces, spaces, is_maximizing):
    result = check_victory(X_spaces, O_spaces, False)
    if result == "X":
        return -1  # AI loss
    elif result == "O":
        return 1   # AI win
    elif result == "Draw":
        return 0   # Draw

    '''
    If the AI in question is anticipating its own or its opponent's move. For example, if the AI is playing as X, 
    then is_maximising would be true when the Ai is deciding a move for X, and false when deciding a move for O, and vice versa.
    '''

    if is_maximizing:
        best_score = -float("inf")
        for move in spaces:
            if move not in X_spaces and move not in O_spaces:
                O_spaces.append(move)
                score = minimax(X_spaces, O_spaces, spaces, False)
                O_spaces.remove(move)
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in spaces:
            if move not in X_spaces and move not in O_spaces:
                X_spaces.append(move)
                score = minimax(X_spaces, O_spaces, spaces, True)
                X_spaces.remove(move)
                best_score = min(score, best_score)
        return best_score


def AI_turn(X_spaces, O_spaces, spaces):
    best_score = -float("inf")
    best_move = None

    # Cycles through each move and scores it, before comparing it to the current best scoring move to see which is better
    for move in spaces:
        if move not in X_spaces and move not in O_spaces:
            O_spaces.append(move)
            score = minimax(X_spaces, O_spaces, spaces, False)
            O_spaces.remove(move)
            if score > best_score:
                best_score = score
                best_move = move

    print("Chosen move:", best_move, "with score:", best_score)
    return best_move


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

                            bestmove = AI_turn(X_spaces, O_spaces, spaces)
                            x, y = bestmove.split(",")
                            WIN.blit(O_icon, (int(x), int(y)))
                            taken_spaces.append(bestmove)
                            O_spaces.append(bestmove)
                            pygame.display.update()
                            over = check_victory(X_spaces, O_spaces, True)
                            turn = "X"
    
    pygame.quit()

#Life support

over = False

if __name__ == "__main__":
    main(turn, taken_spaces, X_spaces, O_spaces, over)
