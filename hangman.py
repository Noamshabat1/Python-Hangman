
import hangman_helper as helper

"""
Magic variables:
"""
HINT_MESSAGE = "you have chosen a hint and will be presented to you now!"
WRONG_MESSAGE = "you have entered a wrong value please try again to enter"
WRONG_GUESS_MESSAGE = "you have chosen incorrectly"
WINING_MESSAGE = "Congratulation's you have won the hangman Game!!!"
PLAY_AGAIN = "Would you want to play again? your score is:"
RIGHT_GUESS_MESSAGE = "good job, you have chose correctly!"
LOST_MESSAGE = "you have lost the game, The word you have tried to guess was: "
REPEAT_ANSWER_MESSAGE = "you have been chose this letter before, please try " \
                        "again! "
MESSAGE_START = ("""
      Welcome to the Game Hangman! 

       _    _  
      | |  | |
      | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
      |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \ 
      | |  | | (_| | | | | (_| | | | | | | (_| | | | |
      |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                           __/ |
                          |___/ 
      let's play !!!                  
""")


def calc_score(pattern_diff):
    """
    calculate the score in cases of choosing the correct choice by the amount
    of letters.
    :param pattern_diff: the difference in the pattern.
    :return: the amount of point the player got.
    """
    return (pattern_diff * (pattern_diff + 1)) // 2


def update_word_pattern(word, pattern, letter):
    """
    the func creates a new pattern by a letter it been given.
    :param word: string that fits pattern
    :param string pattern: current pattern of word
    :param string letter: check if fits pattern
    :return: string of updated pattern
    """
    new_pattern = list(pattern)
    for i in range(len(word)):
        if letter == word[i]:
            new_pattern[i] = letter

    return "".join(new_pattern)


def validate_input(type_of_input, val):
    """
    checks if value of input fits type of input
    :param type_of_input:
    :param val: value of input
    :return: Boolean if input if valid
    """
    if type_of_input == helper.LETTER:
        if len(val) > 1:
            return False
        if val not in "abcdefghijklmnopqrstuvwxyz":
            return False
        return True

    elif type_of_input == helper.WORD:
        if not val.lower() == val:
            return False
        if not val.isalpha():
            return False
        return True

    elif type_of_input == helper.HINT:
        return True

    return False


def next_step_for_letter(state, input_from_player):
    """
    the func diturman how the program will reacts if the player will chose a
    letter.
    :param state: a dictionary that is updating the hole game.
    :param input_from_player: input from the player.
    :return: by each case the right response regarding his choice.
    """
    if input_from_player in state['wrong_guesses'] or input_from_player in \
            state['pattern']:
        state['msg'] = REPEAT_ANSWER_MESSAGE

    elif input_from_player in state['word']:
        letter_in_word = state['word'].count(input_from_player)
        state['pattern'] = update_word_pattern(state['word'], state['pattern'],
                                               input_from_player)
        state['score'] -= 1
        state['score'] += calc_score(letter_in_word)
        state['msg'] = RIGHT_GUESS_MESSAGE

    else:
        state['wrong_guesses'].append(input_from_player)
        state['score'] -= 1
        state['msg'] = WRONG_GUESS_MESSAGE

    return state


def next_step_for_word(state, input_from_player):
    """
    the func determine how the program will reacts if the player will chose a
    word.
    :param state: a dictionary that is updating the hole game.
    :param input_from_player: input from the player.
    :return: by each case the right response regarding his choice.
    """
    if input_from_player != state['word']:
        state['score'] -= 1
        state['msg'] = WRONG_MESSAGE
        state['wrong_words'].append(input_from_player)

    elif input_from_player == state['word']:
        word_of_word = state['pattern'].count('_')
        state['pattern'] = state['word']
        state['score'] -= 1
        state['score'] += calc_score(word_of_word)
        state['msg'] = WINING_MESSAGE
    return state


def next_step_for_hint(state, words_list):
    """
    the func determine how the program will reacts if the player will chose a
    hint.
    :param state: a dictionary that is updating the hole game.
    :param words_list : a word list that gives the option to the player.
    :return: by each case of choosing hint will give a list of possible hints.
    """
    short_hint_list = []
    state['score'] -= 1
    state['msg'] = HINT_MESSAGE
    filter_list = filter_words_list(words_list, state['pattern'],
                                    state['wrong_words'])

    if len(filter_list) <= helper.HINT_LENGTH:
        helper.show_suggestions(filter_list)
        return state

    for i in range(helper.HINT_LENGTH):
        num_f = (i * len(filter_list)) // helper.HINT_LENGTH
        short_hint_list.append(filter_list[num_f])

    helper.show_suggestions(short_hint_list)
    return state


def rond(state, words_list):
    """
    in each rond the func will carry through one rond in the game.
    :param state:  a dictionary that is updating the hole game.
    :param words_list: in case of cosing hint the rond func will carry it
    through.
    :return: the response for one rond of choice in the game of the player.
    """
    next_step = {
        helper.LETTER: next_step_for_letter,
        helper.WORD: next_step_for_word,
        helper.HINT: next_step_for_hint,
    }
    helper.display_state(state['pattern'],
                         state['wrong_guesses'],
                         state['score'],
                         state['msg'])

    type_of_input, input_from_player = helper.get_input()

    while not validate_input(type_of_input, input_from_player):
        state['msg'] = WRONG_MESSAGE
        helper.display_state(state['pattern'],
                             state['wrong_guesses'],
                             state['score'],
                             state['msg'])
        type_of_input, input_from_player = helper.get_input()

    if type_of_input == helper.HINT:
        next_step[helper.HINT](state, words_list)

    else:
        next_step[type_of_input](state, input_from_player)
    return state


def run_single_game(words_list, score):
    """
    this func carry through one hole single game.
    :param words_list: a list of word.
    :param score: the current score of the player in each rond his playing.
    :return: the score in the end of the game, a message and more information
    about the current game according to the results.
    """
    game_word = helper.get_random_word(words_list)
    pattern = "_" * len(game_word)
    state = {
        'wrong_words': [],
        'pattern': pattern,
        'wrong_guesses': [],
        'score': score,
        'word': game_word,
        'msg': MESSAGE_START
    }

    while True:
        state = rond(state, words_list)
        if state['score'] == 0:
            state['msg'] = LOST_MESSAGE
            helper.display_state(state['pattern'],
                                 state['wrong_guesses'],
                                 state['score'],
                                 state['msg'] + game_word)
            break

        if game_word == state['pattern']:
            state['msg'] = WINING_MESSAGE
            helper.display_state(state['pattern'],
                                 state['wrong_guesses'],
                                 state['score'],
                                 state['msg'])
            break

    return state['score']


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    the func is filtering word's that are not possible to be a hint word to
    the player.
    :param words: the word that came back from the pattern from the func
    "word_fits_pattern".
    :param pattern: the current pattern of the "game word"
    :param wrong_guess_lst: a list the condition wrong possible word's.
    :return: the right option to be the hint word that much the pattern.
    """
    filtered = []
    final_filtered_list = []
    for word in words:
        word_fits_pattern(filtered, pattern, word, wrong_guess_lst)

    for word in filtered:
        for word_index in range(len(pattern)):
            if word[word_index] == pattern[word_index] or pattern[
                word_index] == '_':
                if word_index == len(word) - 1:
                    final_filtered_list.append(word)
            else:
                break
    return final_filtered_list


def word_fits_pattern(filtered, pattern, word, wrong_guess_lst):
    """
    sub func that checks if a word fit a sorting pattern.
    :param filtered: word that cant be the word according to the pattern.
    :param pattern: the pattern of the "game word".
    :param word: a word that cane be right.
    :param wrong_guess_lst: a list that have the wrong guesses.
    :return: the right possible word list.
    """
    if len(word) != len(pattern):
        return False

    for index_letter in range(len(word)):
        if word[index_letter] in wrong_guess_lst:
            return False

    for letter in pattern:
        if letter != '_':
            occurrence = pattern.count(letter)
            if word.count(letter) != occurrence:
                return False

    filtered.append(word)


def main():
    """
    the main func that start the game and reacts to the results of the player
    and reacts according to the results and gives a possibility to play aging
    and save your score.
    :return: the solution according to the player score's.
    """
    words_list = helper.load_words("words.txt")
    game_round = 0
    final_score = helper.POINTS_INITIAL
    while final_score > 0:
        final_score = run_single_game(words_list, final_score)
        game_round += 1
        if final_score > 0:
            play_again = helper.play_again(
                PLAY_AGAIN + ' ' + str(final_score) + "and you played:" + str(
                    game_round) + "times")
            if play_again:
                continue
            else:
                break
        elif final_score == 0:
            play_again = helper.play_again(
                PLAY_AGAIN + str(final_score) + "and you played:" + str(
                    game_round) + "times")
            if play_again:
                game_round = 0
                final_score = helper.POINTS_INITIAL
                continue
            else:
                break


if __name__ == '__main__':
    main()
