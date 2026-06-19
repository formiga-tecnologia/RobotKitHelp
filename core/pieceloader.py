"""
=========================================================
 RoboKitHelp Engine

 piece_loader.py

 Responsável por ler arquivos .rkp
=========================================================
"""

from pathlib import Path

from core.piece import Piece


class PieceLoader:

    @staticmethod
    def load(file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        piece = Piece()

        current_rect = None

        with open(file_path, "r", encoding="utf-8") as file:

            for raw in file:

                line = raw.strip()

                # ----------------------------
                # Ignorar linhas vazias
                # ----------------------------

                if not line:
                    continue

                # Comentários

                if line.startswith("#"):
                    continue

                # Divide a linha

                parts = line.split()

                command = parts[0].upper()

                # ----------------------------
                # PIECE
                # ----------------------------

                if command == "PIECE":
                    continue

                # ----------------------------
                # NAME
                # ----------------------------

                if command == "NAME":

                    piece.name = " ".join(parts[1:])

                    continue

                # ----------------------------
                # RECT
                # ----------------------------

                if command == "RECT":

                    current_rect = {
                        "x": 0,
                        "y": 0,
                        "width": 10,
                        "height": 10,
                        "color": "#FFFFFF"
                    }

                    continue

                # ----------------------------
                # POS
                # ----------------------------

                if command == "POS":

                    current_rect["x"] = int(parts[1])
                    current_rect["y"] = int(parts[2])

                    continue

                # ----------------------------
                # SIZE
                # ----------------------------

                if command == "SIZE":

                    current_rect["width"] = int(parts[1])
                    current_rect["height"] = int(parts[2])

                    continue

                # ----------------------------
                # COLOR
                # ----------------------------

                if command == "COLOR":

                    current_rect["color"] = parts[1]

                    continue

                # ----------------------------
                # END
                # ----------------------------

                if command == "END":

                    if current_rect is not None:

                        piece.add_rect(

                            x=current_rect["x"],
                            y=current_rect["y"],
                            width=current_rect["width"],
                            height=current_rect["height"],
                            fill=current_rect["color"]

                        )

                        current_rect = None

                    continue

        return piece
