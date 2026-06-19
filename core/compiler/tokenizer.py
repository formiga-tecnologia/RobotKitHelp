"""
=========================================================
 RoboKitHelp Compiler

 tokenizer.py
=========================================================
"""

from pathlib import Path

from core.compiler.token import Token


class Tokenizer:

    # ------------------------------------------

    @staticmethod
    def tokenize(file_path):

        file_path = Path(file_path)

        tokens = []

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, raw in enumerate(file, start=1):

                line = raw.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                words = line.split()

                column = 1

                for word in words:

                    if word.isdigit():

                        token_type = "NUMBER"

                    elif word.startswith("#"):

                        token_type = "COLOR"

                    else:

                        token_type = "WORD"

                    tokens.append(

                        Token(

                            token_type,

                            word,

                            line_number,

                            column

                        )

                    )

                    column += len(word) + 1

        return tokens