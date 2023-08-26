from dataclasses import dataclass

from players import Player
from renderers import Renderer
from logic.exceptions import InvalidMove
from logic.models import GameState, Grid, Mark
from logic.validators import validate_players

from typing import Callable, TypeAlias
ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class TicTacToe:
    player1: Player
    player2: Player
    renderer: Renderer

    error_handler: ErrorHandler | None = None

    # validate the players’ marks when instantiating the TicTacToe class
    def __post_init__(self):
        validate_players(self.player1, self.player2)

    def play(self, starting_mark: Mark = Mark("X")) -> None:
        game_state = GameState(Grid(), starting_mark)
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break # until the game is over
            player = self.get_current_player(game_state)
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)

    # map the current mark to a player object 
    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2