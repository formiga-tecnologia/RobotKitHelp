from core.piece import Piece, RectElement


class RKPParser:

    def parse(self, text: str):

        piece = None
        current = None

        for raw in text.splitlines():

            line = raw.strip()

            if not line or line.startswith("#"):
                continue

            tokens = line.split()

            if tokens[0] == "PIECE":
                piece = Piece()

            elif tokens[0] == "NAME":
                piece.name = " ".join(tokens[1:])

            elif tokens[0] == "SIZE":
                piece._width = int(tokens[1])
                piece._height = int(tokens[2])

            elif tokens[0] == "RECT":
                current = RectElement()

            elif tokens[0] == "POS":
                current.x = int(tokens[1])
                current.y = int(tokens[2])

            elif tokens[0] == "SIZE_RECT":
                current.width = int(tokens[1])
                current.height = int(tokens[2])

            elif tokens[0] == "COLOR":
                current.fill = tokens[1]
                current.border = tokens[1]

            elif tokens[0] == "END":
                if current and piece:
                    piece.add(current)
                    current = None

            elif tokens[0] == "END_PIECE":
                break

        return piece