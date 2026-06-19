from pathlib import Path
from core.parser.rkp_paser import RKPParser


class Package:

    def __init__(self):
        self.pieces = {}
        self.parser = RKPParser()
        self.path = None

    def load(self, path):

        self.path = path
        self.pieces.clear()

        for file in Path(path).glob("*.rkp"):

            text = file.read_text(encoding="utf-8")

            piece = self.parser.parse(text)

            if piece is not None:
                self.pieces[file.stem] = piece

    def get(self, name):
        return self.pieces.get(name)

    def names(self):
        return list(self.pieces.keys())
