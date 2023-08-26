# extend the built-in Exception type
class InvalidGameState(Exception):
    """Raised when the game state is invalid."""

class InvalidMove(Exception):
    """Raised when the move is invalid."""