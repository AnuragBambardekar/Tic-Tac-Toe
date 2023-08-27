import abc
import time
import random

from tic_tac_toe.logic.models import Mark, GameState, Move
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move

"""
An abstract class is one that you can’t instantiate because its objects 
wouldn’t stand on their own. Its only purpose is to provide the skeleton 
for concrete subclasses.
"""
class Player(metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's the other player's turn")
        
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state."""

"""
extends Player by adding an additional member, .delay_seconds, 
to its instances, which by default is equal to 250 milliseconds. 
"""
class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer's move in the given game state."""

"""
implement a computer player picking moves at random
"""
class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        # try:
        #     return random.choice(game_state.possible_moves)
        # except IndexError:
        #     return None
        return game_state.make_random_move()
        
"""
This computer player will always try to find the best tic-tac-toe 
move with AI and Python. 
"""
class MinimaxComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        # return find_best_move(game_state)
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)