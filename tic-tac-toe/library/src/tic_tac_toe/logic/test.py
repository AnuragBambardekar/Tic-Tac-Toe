from models import Mark, Grid, GameState

print(Mark.CROSS)
print(Mark.NAUGHT)
print()
print(Mark["CROSS"])
print(Mark["NAUGHT"])
print()
print(Mark("X"))
print(Mark("O"))
print()
print(Mark("X").other)
print(Mark("O").other)
print()
print(Mark("X").name)
print()
print(Mark("X").value)
print()
print(Mark("X") == "X")
print()
print(Mark.CROSS == "X")

"""
store the grid in row-major order by concatenating 
the rows from top to bottom.
"""
def preview(cells):
    print(cells[:3], cells[3:6], cells[6:], sep="\n")

preview("XXOXO O  ")

"""
While using strings to represent the grid of cells is pretty 
straightforward, it falls short in terms of validating its shape 
and content. Other than that, plain strings can’t provide some extra, 
grid-specific properties that you might be interested in. For these 
reasons, you’ll create a new Grid data type on top of a string wrapped 
in an attribute
"""

print(Grid())
print()
print(Grid("XXOXO O  "))
print()
grid = Grid("OXXXXOOOX")
print(grid.x_count)
print(grid.o_count)
print(grid.empty_count)
# print(Grid("XO")) # ValueError: Must contain 9 cells of: X, O, or space

"""
such a cell combination is semantically incorrect because one player 
isn’t allowed to fill the entire grid with their mark.
"""
# print(GameState(Grid("XXXXXXXXX"))) # exceptions.InvalidGameState: Wrong number of Xs and Os

game_state = GameState(Grid())
print(game_state.game_not_started)
print(game_state.game_over)
print(game_state.tie)
print(game_state.winner is None)
print(game_state.winning_cells)

game_state = GameState(Grid("XOXOXOXXO"), starting_mark=Mark("X"))
print(game_state.starting_mark)
print(game_state.current_mark)
print(game_state.winner)
print(game_state.winning_cells)

game_state = GameState(Grid("XXOXOX  O"))
print(game_state.possible_moves)