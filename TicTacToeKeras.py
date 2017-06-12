from keras.models import Sequential, model_from_json
from keras.layers import Dense
from TicTacToe import *
import numpy as np


def play_random_games(number_of_games):
    all_boards = []
    all_moves = []

    for each_game in range(number_of_games):
        fake_game = FakeGame()

        while not fake_game.game_over:
            if fake_game.current_move == 'X':
                fake_game.almost_random_move()
            else:
                fake_game.random_move()

        if fake_game.should_use_data:
            all_boards += fake_game.format_game_boards()
            all_moves += fake_game.moves

    return all_boards, all_moves


def play_model_based_games(number_of_games):
    all_boards = []
    all_moves = []

    model = get_model()

    for each_game in range(number_of_games):
        fake_game = FakeGame()

        while not fake_game.game_over:
            spaces_to_block = fake_game.look_for_two_in_a_row(-1)

            if len(spaces_to_block) == 0:
                # If there are no spots that it needs to go to it plays a random move
                board_to_predict = fake_game.board
                board_to_predict = np.reshape(board_to_predict, (-1, 9))
                fake_game.real_move(model.predict(board_to_predict)[0])
            if len(spaces_to_block) == 1:
                # If there is a spot that it needs to go to it goes there
                fake_game.play_piece(spaces_to_block[0] + 1)
            elif len(spaces_to_block) > 1:
                # If there are two spots in needs to go to it picks the first one
                fake_game.play_piece(spaces_to_block[0] + 1)

        if fake_game.should_use_data:
            all_boards += fake_game.format_game_boards()
            all_moves += fake_game.moves
        print each_game

    return all_boards, all_moves


def create_model():
    network = Sequential()

    network.add(Dense(12, input_dim=9, activation='relu'))
    network.add(Dense(128, activation='relu'))
    network.add(Dense(256, activation='relu'))
    network.add(Dense(512, activation='relu'))
    network.add(Dense(1024, activation='relu'))
    network.add(Dense(2048, activation='relu'))
    network.add(Dense(1014, activation='relu'))
    network.add(Dense(512, activation='relu'))
    network.add(Dense(256, activation='relu'))
    network.add(Dense(128, activation='relu'))
    network.add(Dense(9, activation='sigmoid'))

    network.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return network


def save_model(model):
    model_json = model.to_json()
    with open("hard_coded_model.json", "w") as json_file:
        json_file.write(model_json)

    model.save_weights("hard_coded_model.h5")


def get_model():
    json_file = open('hard_coded_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("hard_coded_model.h5")

    return loaded_model


def train_model(x, y):
    x = np.reshape(x, (-1, 9))
    y = np.reshape(y, (-1, 9))

    model = create_model()
    model.fit(x, y, epochs=10, batch_size=5)

    return model


# x, y = play_random_games(100000)
x, y = play_model_based_games(50000)

model = train_model(x, y)

save_model(model)

# model = get_model()

game = Game()

while True:
    events = pygame.event.get()
    game.create_board()
    if not game.game_over:
        if game.current_move == 'X':
            move = model.predict(np.reshape(game.board, (-1, 9)))
            move = move[0]
            formatted_move = []
            for i in move:
                i = round(i, 4)
                formatted_move.append(i)
            print formatted_move

            game.not_random_move(formatted_move)
        else:
            game.get_pos_to_play(events)
    pygame.display.update()


