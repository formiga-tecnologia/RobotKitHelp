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
            cmd = tokens[0].upper()

            if cmd == "PIECE":
                piece = Piece()

            elif cmd == "NAME" and piece is not None:
                piece.name = " ".join(tokens[1:])

            elif cmd == "SIZE" and piece is not None and current is None:
                piece.declared_width = int(tokens[1])
                piece.declared_height = int(tokens[2])

            elif cmd == "RECT":
                current = RectElement()

            elif cmd == "POS" and current:
                current.x = int(tokens[1])
                current.y = int(tokens[2])

            elif cmd in ("SIZE", "SIZE_RECT") and current:
                current.width = int(tokens[1])
                current.height = int(tokens[2])

            elif cmd in ("FILL", "COLOR") and current:
                current.fill = tokens[1]

                if cmd == "COLOR":
                    current.border = tokens[1]

            elif cmd == "BORDER" and current:
                current.border = tokens[1]

            elif cmd == "END" and current is not None and piece is not None:
                piece.add(current)
                current = None

        return piece
