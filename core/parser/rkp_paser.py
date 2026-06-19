from core.piece import Piece, RectElement


class RKPParser:

    def parse(self, text: str):

        piece = None
        current = None

        for raw in text.splitlines():

            line = raw.strip()

            if not line:
                continue

            tokens = line.split()

            cmd = tokens[0]

            if cmd == "PIECE":
                piece = Piece()

            elif cmd == "NAME":
                piece.name = " ".join(tokens[1:])

            elif cmd == "SIZE":
                piece._width = int(tokens[1])
                piece._height = int(tokens[2])

            elif cmd == "RECT":
                current = RectElement()   # 🔥 NOVA instância SEMPRE

            elif cmd == "POS":
                current.x = int(tokens[1])
                current.y = int(tokens[2])

            elif cmd == "SIZE_RECT":
                current.width = int(tokens[1])
                current.height = int(tokens[2])

            elif cmd == "COLOR":
                current.fill = tokens[1]
                current.border = tokens[1]

            elif cmd == "END":
                if current:
                    piece.add(current)
                    current = None  # 🔥 MUITO IMPORTANTE

        return piece