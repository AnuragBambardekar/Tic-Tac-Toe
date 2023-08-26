from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.players import Player
    from models import Grid, GameState, Mark
"""
You import Grid conditionally. The TYPE_CHECKING constant is false at 
runtime, but third-party tools, such as mypy, will pretend it’s true 
when performing static type checking to allow the import statement to 
run.
"""
import re
# from models import Grid # causes error due to circular import

from exceptions import InvalidGameState



def validate_grid(grid:Grid) -> None:
        if not re.match(r"^[\sXO]{9}$", grid.cells):
            raise ValueError("Must contain 9 cells of: X, O, or space")
        
def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(
        game_state.grid, game_state.starting_mark, game_state.winner
    )

"""
marks left by one player must be either the same or greater by exactly 
one compared to the number of marks left by the other player.
"""
def validate_number_of_marks(grid: Grid) -> None:
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Wrong number of Xs and Os")
    
"""
The player who left more marks on the grid is guaranteed to be the 
starting player. If not, then you know that something must have gone 
wrong.
"""
def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Wrong starting mark")
    elif grid.o_count > grid.x_count:
        if starting_mark != "O":
            raise InvalidGameState("Wrong starting mark")
        
"""
there can only be one winner, and depending on who started the game, 
the ratio of Xs ans Os left on the grid will be different
"""
def validate_winner(
    grid: Grid, starting_mark: Mark, winner: Mark | None
) -> None:
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of Xs")
    elif winner == "O":
        if starting_mark == "O":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of Os")
        else:
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of Os")

"""
use the identity comparison again to check both players’ marks and 
prevent the game from starting when both players use the same mark.
"""          
def validate_players(player1: Player, player2: Player) -> None:
    if player1.mark is player2.mark:
        raise ValueError("Players must use different marks")