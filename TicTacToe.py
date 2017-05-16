import pygame
import random


class Game(object):
    def __init__(self):
        # 1 indicates that it is an X, -1 indicates an O, and 0 is a blank spot
        self.board = [0, 0, 0,
                      0, 0, 0,
                      0, 0, 0]
        self.current_move = 'X'
        self.game_over = False

        pygame.init()
        self.window = pygame.display.set_mode((600, 600))
        self.font = pygame.font.SysFont('monospace', 100)

        pygame.display.set_caption('Tic Tac Toe')
        self.window.fill((255, 255, 255))

    def create_board(self):
        # Vertical Lines
        pygame.draw.line(self.window, (0, 0, 0), (200, 600), (200, 0), 5)
        pygame.draw.line(self.window, (0, 0, 0), (400, 600), (400, 0), 5)

        # Horizontal Lines
        pygame.draw.line(self.window, (0, 0, 0), (600, 200), (0, 200), 5)
        pygame.draw.line(self.window, (0, 0, 0), (600, 400), (0, 400), 5)

        # Updates the window with the lines drawn
        pygame.display.update()

    def check_for_game_over(self):
        game_over_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # Loops over all the possible game overs to check if X or O won, or if there is a tie
        for game_over in game_over_positions:
            # Loops over the indexes in each possible game over
            x_count = 0
            o_count = 0
            for index in game_over:
                # If the piece is a X or an O add 1 to the desired number
                if self.board[index] == 1:
                    x_count += 1
                elif self.board[index] == -1:
                    o_count += 1

            # If the X or O count is three then there are three pieces in a row and its game over
            if x_count == 3:
                self.game_over = True
                text = self.font.render("X Wins!", True, (0, 0, 0))
                text_rect = text.get_rect(center=(300, 300))
                self.window.blit(text, text_rect)
                break
            elif o_count == 3:
                self.game_over = True
                text = self.font.render("O Wins!", True, (0, 0, 0))
                text_rect = text.get_rect(center=(300, 300))
                self.window.blit(text, text_rect)
                break

        if self.board.count(0) == 0 and not self.game_over:
            self.game_over = True
            text = self.font.render("Tie", True, (0, 0, 0))
            text_rect = text.get_rect(center=(300, 300))
            self.window.blit(text, text_rect)

    def place_piece(self, position):
        # Coordinates for the grid
        # (100, 100)  (300, 100)  (500, 100)
        # (100, 300)  (300, 300)  (500, 300)
        # (100, 500)  (300, 500)  (500, 500)

        # Calculates the piece number
        if position[0] <= 200:
            x = 100
            piece_number = 0
        elif position[0] <= 400:
            x = 300
            piece_number = 3
        else:
            x = 500
            piece_number = 6

        if position[1] <= 200:
            y = 100
            piece_number += 1
        elif position[1] <= 400:
            y = 300
            piece_number += 2
        else:
            y = 500
            piece_number += 3

        # Checks if the there is a piece there
        if self.board[piece_number - 1] == 0:
            if self.current_move == 'X':
                # Draws an X
                pygame.draw.line(self.window, (0, 0, 0), (x - 50, y - 50), (x + 50, y + 50), 5)
                pygame.draw.line(self.window, (0, 0, 0), (x - 50, y + 50), (x + 50, y - 50), 5)
                # Changes the board array
                self.board[piece_number - 1] = 1
                # Changes the turn
                self.current_move = 'O'
            else:
                # Draws an O
                pygame.draw.circle(self.window, (0, 0, 0), (x, y), 50, 5)
                # Changes the board array
                self.board[piece_number - 1] = -1
                # Changes the turn
                self.current_move = 'X'

        self.check_for_game_over()

    def get_pos_to_play(self, events):
        # Loops over all of the events recorded
        for event in events:
            # Checks if the event is a release of the mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # Saves the position of the mouse when it was released
                position = pygame.mouse.get_pos()
                # Places a piece with the position
                self.place_piece(position)

    def not_random_move(self, possible_moves):
        best_move = max(possible_moves)

        best_move = possible_moves.index(best_move)

        loop_count = 0

        while self.board[best_move] != 0:
            possible_moves[best_move] = 0
            best_move = max(possible_moves)
            best_move = possible_moves.index(best_move)
            loop_count += 1
            if loop_count > 20:
                self.random_move()
                best_move = -1
                break

        block = best_move

        if block == 0:
            self.place_piece((100, 100))
        elif block == 1:
            self.place_piece((100, 300))
        elif block == 2:
            self.place_piece((100, 500))
        elif block == 3:
            self.place_piece((300, 100))
        elif block == 4:
            self.place_piece((300, 300))
        elif block == 5:
            self.place_piece((300, 500))
        elif block == 6:
            self.place_piece((500, 100))
        elif block == 7:
            self.place_piece((500, 300))
        elif block == 8:
            self.place_piece((500, 500))

    def random_move(self):
        zeros = []
        counter = 0
        for piece in self.board:
            if piece == 0:
                zeros.append(counter)
            counter += 1

        if len(zeros) != 0:
            block = random.choice(zeros)

            if block == 0:
                self.place_piece((100, 100))
            elif block == 1:
                self.place_piece((100, 300))
            elif block == 2:
                self.place_piece((100, 500))
            elif block == 3:
                self.place_piece((300, 100))
            elif block == 4:
                self.place_piece((300, 300))
            elif block == 5:
                self.place_piece((300, 500))
            elif block == 6:
                self.place_piece((500, 100))
            elif block == 7:
                self.place_piece((500, 300))
            elif block == 8:
                self.place_piece((500, 500))

        # block += 1
        # return block


class FakeGame(object):
    def __init__(self):
        # 1 indicates that it is an X, -1 indicates an O, and 0 is a blank spot
        self.board = [0, 0, 0,
                      0, 0, 0,
                      0, 0, 0]
        self.current_move = 'X'
        self.game_over = False
        self.should_use_data = False
        self.boards = []
        self.moves = []

    def random_move(self):
        empty_indexes = []
        index_counter = 1

        # Collect the tiles that are empty
        for tile in self.board:
            if tile == 0:
                empty_indexes.append(index_counter)
            index_counter += 1

        # Selects a random index from the empty tiles
        random_spot_number = random.choice(empty_indexes)

        # Puts a piece on the spot it picked
        self.play_piece(random_spot_number)

    def almost_random_move(self):
        # Gets the spots that it should go in
        spaces_to_block = self.look_for_two_in_a_row(-1)

        if len(spaces_to_block) == 0:
            # If there are no spaces to block then it looks for the win
            spaces_to_block = self.look_for_two_in_a_row(1)
            print 'For the Win'

        if len(spaces_to_block) == 0:
            # If there are no spots that it needs to go to it plays a random move
            self.random_move()
        if len(spaces_to_block) == 1:
            # If there is a spot that it needs to go to it goes there
            self.play_piece(spaces_to_block[0] + 1)
        elif len(spaces_to_block) > 1:
            # If there are two spots in needs to go to it picks the first one
            self.play_piece(spaces_to_block[0] + 1)
            print spaces_to_block

    def real_move(self, prediction):
        should_play_piece = True
        # Rounds each element of a list to 4 decimal places
        formatted_prediction = []

        for probability in prediction:
            new_probability = round(probability, 4)
            formatted_prediction.append(new_probability)

        # Finds the largest element in the list and checks if it can go there
        # If the largest element is taken it goes to the second largest and so on
        best_move_index = formatted_prediction.index(max(formatted_prediction))

        while self.board[best_move_index] != 0:
            formatted_prediction[best_move_index] = 0
            best_move_index = formatted_prediction.index(max(formatted_prediction))
            if formatted_prediction.count(0) == 9:
                self.random_move()
                should_play_piece = False
                break

        if should_play_piece:
            self.play_piece(best_move_index + 1)

    def play_piece(self, spot_number):
        # Spot Numbers
        # 1  4  7
        # 2  5  8
        # 3  6  9
        # Subtract 1 from the spot number to get the index to change

        # Check if the spot is take, if there is a piece nothing happens
        if self.board[spot_number - 1] == 0:
            # Update the list with the move
            if self.current_move == 'X':
                # Save the current board and move to use a training data
                self.boards += self.board
                move_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                move_array[spot_number - 1] = 1
                self.moves.append(move_array)
                # Update the list with 1 to represent an X
                self.board[spot_number - 1] = 1
                self.current_move = 'O'
            else:
                # Update the list with -1 to represent an O
                self.board[spot_number - 1] = -1
                self.current_move = 'X'

        self.check_for_game_over()

    def look_for_two_in_a_row(self, piece_to_check):
        spaces_to_block = []
        # Defines the possible places for game over
        game_over_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # Loops over each possible place for game over
        for game_over_position in game_over_positions:
            opponent_spaces = []

            # Loops over the spaces in the places for game over
            for space in game_over_position:
                # If there is a piece in the space add the index of the piece to the opponent spaces
                if self.board[space] == piece_to_check:
                    opponent_spaces.append(space)

            # If there are two in a row then find the open space and append that to the spaces to block
            if len(opponent_spaces) == 2:
                # Finds which space to block
                for game_over_space in game_over_position:
                    if game_over_space not in opponent_spaces and self.board[game_over_space] != -piece_to_check:
                        spaces_to_block.append(game_over_space)

        return spaces_to_block

    def check_for_game_over(self):
        game_over_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # Loops over all the possible game overs to check if X or O won, or if there is a tie
        for game_over in game_over_positions:
            # Loops over the indexes in each possible game over
            x_count = 0
            o_count = 0
            for index in game_over:
                # If the piece is a X or an O add 1 to the desired number
                if self.board[index] == 1:
                    x_count += 1
                elif self.board[index] == -1:
                    o_count += 1

            # If the X or O count is three then there are three pieces in a row and its game over
            if x_count == 3:
                self.game_over = True
                self.should_use_data = True
                break
            elif o_count == 3:
                self.game_over = True
                break
            elif self.board.count(0) == 0:
                self.game_over = True
                self.should_use_data = True

    def format_game_boards(self):
        # Separates the list of boards into separate lists inside a list
        boards_to_edit = self.boards
        fixed_boards = []

        while len(boards_to_edit) > 0:
            appender = boards_to_edit[:9]
            fixed_boards.append(appender)
            del boards_to_edit[0:9]

        return fixed_boards
