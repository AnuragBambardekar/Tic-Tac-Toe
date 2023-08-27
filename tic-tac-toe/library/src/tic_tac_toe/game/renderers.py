import abc

from tic_tac_toe.logic.models import GameState

"""
This could’ve been implemented as a regular function because the renderer 
exposes only a single operation while getting the whole state through an 
argument. However, concrete subclasses may need to maintain an additional 
state, such as the application’s window, so having a class may come in 
handy at some point.
"""
class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, game_state: GameState) -> None:
        """Render the current game state."""