# define tic-tac-toe domain model objects
"""
domain model:
a domain model is a conceptual model of 
the domain that incorporates both behavior and data.
"""

import enum
import re
from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.validators import validate_grid, validate_game_state
from tic_tac_toe.logic.exceptions import InvalidMove

# eight winning patterns for each of the two players
WINNING_PATTERNS = (
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

# define Mark as a mixin class of the str and enum.Enum types
# so, we inherit str and enum.Enum
class Mark(str,enum.Enum):
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT

"""
define Grid as a frozen data class to make its instances immutable so 
that once you create a grid object, you won’t be able to alter its cells.
"""
@dataclass(frozen=True)
class Grid:
    cells: str = " " * 9

    """
    to check whether the given value of the .cells attribute is exactly 
    nine characters long and contains only the expected characters—that 
    is, "X", "O", or " ". 
    """
    def __post_init__(self) -> None:
        # if not re.match(r"^[\sXO]{9}$", self.cells):
        #     raise ValueError("Must contain 9 cells of: X, O, or space")
        # Moved above two lines to a separate function in validators.py
        validate_grid(self)
    

    """
    The three properties return the current number of crosses, naughts, 
    and empty cells, respectively. Because your data class is immutable, 
    its state will never change, so you can cache the computed property 
    values with the help of the @cached_property decorator from the 
    functools module.
    """ 
    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")

    @cached_property
    def o_count(self) -> int:
        return self.cells.count("O")

    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")

"""
Data transfer Object (DTO) whose main purpose is to carry data, as it 
doesn’t provide any behavior through methods or dynamically computed 
properties.

Check whether a given move is valid, along with validating a specific 
grid cell combination, in a class responsible for managing the game’s 
state
"""
@dataclass(frozen=True)
class Move:
    mark: Mark
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"

@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark("X") # default value of Mark("X") for the starting player’s mark

    def __post_init__(self) -> None:
        validate_game_state(self)

    """
    The current player’s mark will be the same as the starting player’s 
    mark when the grid is empty or when both players have marked an equal
    number of cells. In practice, you only need to check the latter 
    condition because a blank grid implies that both players have zero 
    marks in the grid. To determine the other player’s mark, you can take
    advantage of your .other property in the Mark enum.
    """
    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other

    """
    evaluating the current state of the game.
    """ 
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9
    
    """
    Conversely, you can conclude that the game has finished when there’s 
    a clear winner or there’s a tie
    """
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    """
    Tie Case
    """
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0
    
    """
    Winner Case
    """
    @cached_property
    def winner(self) -> Mark | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None
    
    """
    also want to know the matched winning cells to differentiate them 
    visually. In this case, you can add a similar property, which uses a 
    list comprehension to return a list of integer indices of the winning 
    cells.
    """
    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []
    
    """
    a fixed list of possible moves, which you can find by filling the 
    remaining empty cells in the grid with the current player’s mark
    """
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append(self.make_move_to(match.start()))
        return moves
    
    def make_move_to(self, index: int) -> Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(
            mark=self.current_mark,
            cell_index=index,
            before_state=self,
            after_state=GameState(
                Grid(
                    self.grid.cells[:index]
                    + self.current_mark
                    + self.grid.cells[index + 1:]
                ),
                self.starting_mark,
            ),
        )