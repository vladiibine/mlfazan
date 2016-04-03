from __future__ import print_function
import random

def generate_corpus(size=100):
    """Return a list of elements of size `size`, containing random strings.
    """
    return {
            ''.join(
                    [random.choice('asdfgh') for __ in range(6)]
                ) for _ in range(size)
            }



def is_input_valid(previous_word, current_word, corpus):
    if previous_word[-2:] != current_word[:2]:
        return False

    if current_word not in corpus:
        return False

    return True
    

def has_closed_round(current_word, corpus):
    prefix = current_word[-2:]

    for word in corpus:
        if word.startswith(prefix):
            return False

    print('The current word {} closed the round. Choices: {}'
            .format(current_word, corpus))
    return True


class Game(object):
    def __init__(self, corpus=None, rounds=99):
        self.rounds = rounds
        if corpus is None:
            self.corpus = generate_corpus()
        else:
            self.corpus = corpus

    def get_winner(self, player1, player2):
        current_player = player2
        current_letter = player1.get_letter()
        print('Generated letter: ', current_letter)
        print('Choosing the first word.')
        current_word = player2.get_word(letter=current_letter)

        # Validate that the round doesn't start with a win
        while has_closed_round(current_word, self.corpus):
            current_word = player2.get_word(letter=current_letter)
        
        print('First word was chosen well: {}'.format(current_word))

        # play the thing
        while not has_closed_round(current_word, self.corpus):
            current_player = player1 if current_player is player2 else player2            
            current_word = current_player.get_word(previous=current_word)

        print('Player {} won with the word {}'
                .format(str(current_player), current_word))
    
        return current_player

    def run(self):
        """Plays the game for `self.rounds` rounds and returns the winner"""
        p1 = AveragePlayer(self.corpus, 1)
        p2 = AveragePlayer(self.corpus, 2)
        
        p1_wins = 0
        for _ in range(self.rounds):
            if p1 is self.get_winner(p1, p2):
                p1_wins += 1

        winner = p1 if p1_wins > self.rounds // 2 else p2
        print('Player {} won the game with {} games won out of {}'
                .format(str(winner), p1_wins, self.rounds))
        return winner


class AveragePlayer(object):
    def __init__(self, corpus, number):
        self.corpus = corpus
        self.number = number

    def get_word(self, previous=None, letter=None):
        if previous is not None:
            prefix = previous[-2:]
        else:
            prefix = letter

        candidates = [word for word in self.corpus if word.startswith(prefix)]

        selected_word = random.choice(candidates)
        print('Player {} generated word {}'.format(str(self), selected_word))

        return selected_word
    
    def get_letter(self):
        candidate_letters = [word[0] for word in self.corpus]
        return random.choice(candidate_letters)

    def __repr__(self):
        return '{}'.format(self.number)
