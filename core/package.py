"""
=========================================================
 RoboKitHelp Engine

 package.py

 Responsável por carregar e gerenciar todas
 as peças disponíveis no sistema.
=========================================================
"""

from pathlib import Path

from core.compiler.tokenizer import Tokenizer
from core.pieceloader import PieceLoader


class Package:

    def __init__(self):

        self.folder = None

        self._pieces = {}

        self._errors = {}

    # -------------------------------------------------

    def clear(self):

        self._pieces.clear()
        self._errors.clear()

    # -------------------------------------------------

    def load(self, folder):

        """
        Carrega todas as peças da pasta.
        """

        self.clear()

        self.folder = Path(folder)

        self.folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for file in sorted(
            self.folder.glob("*.rkp")
        ):

            self.load_piece(file)

    # -------------------------------------------------

    def load_piece(self, file):

        try:

            # Tokenização
            Tokenizer.tokenize(file)

            # Carrega peça
            piece = PieceLoader.load(file)

            self._pieces[piece.name] = piece

        except Exception as error:

            self._errors[file.stem] = str(error)

    # -------------------------------------------------

    def reload(self):

        if self.folder:

            self.load(self.folder)

    # -------------------------------------------------

    def names(self):

        return sorted(self._pieces.keys())

    # -------------------------------------------------

    def pieces(self):

        return list(self._pieces.values())

    # -------------------------------------------------

    def get(self, name):

        return self._pieces.get(name)

    # -------------------------------------------------

    def exists(self, name):

        return name in self._pieces

    # -------------------------------------------------

    def errors(self):

        return self._errors

    # -------------------------------------------------

    def has_errors(self):

        return len(self._errors) > 0

    # -------------------------------------------------

    def count(self):

        return len(self._pieces)

    # -------------------------------------------------

    def __len__(self):

        return len(self._pieces)

    # -------------------------------------------------

    def __iter__(self):

        return iter(self._pieces.values())

    # -------------------------------------------------

    def __repr__(self):

        return (
            f"<Package "
            f"Pieces={len(self)} "
            f"Errors={len(self._errors)}>"
        )