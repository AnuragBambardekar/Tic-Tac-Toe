from tic_tac_toe.logic.models import Mark, Move, GameState
from functools import partial

"""
find the best move in a given game state, you can sort all 
possible moves by score and take the one with the highest value.

takes some game state and returns either the best move for the 
current player or None to indicate that no more moves are possible. 
"""
def find_best_move(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    """
    use of a partial function to freeze the value of the maximizer 
    argument, which doesn’t change across minimax() invocations.
    """
    bound_minimax = partial(minimax, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)

"""
returns the score associated with the move passed as an argument for 
the indicated maximizing player.
"""
def minimax(move: Move, maximizer: Mark, choose_highest_score: bool = False) -> int:
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    return (max if choose_highest_score else min)(
        minimax(next_move, maximizer, not choose_highest_score)
        for next_move in move.after_state.possible_moves
    )

