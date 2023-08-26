# define tic-tac-toe domain model objects
"""
domain model:
a domain model is a conceptual model of 
the domain that incorporates both behavior and data.
"""

import enum

# define Mark as a mixin class of the str and enum.Enum types
# inherit str and enum.Enum
class Mark(str,enum.Enum):
    CROSS = "X"
    NAUGHT = "O"

    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT