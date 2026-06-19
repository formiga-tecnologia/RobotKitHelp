"""
=========================================================
 RoboKitHelp Compiler

 token.py
=========================================================
"""

from dataclasses import dataclass


@dataclass
class Token:

    type: str

    value: str

    line: int

    column: int = 1

    def __repr__(self):

        return (
            f"<{self.type} "
            f"'{self.value}' "
            f"L{self.line}>"
        )