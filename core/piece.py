"""
=========================================================
 RoboKitHelp Engine

 piece.py

 Estruturas declarativas da linguagem RKP.
=========================================================
"""

from dataclasses import dataclass, field


# =========================================================
# CLASSE BASE
# =========================================================

@dataclass
class Element:
    """
    Classe base de qualquer elemento gráfico.
    """

    type: str

    x: int = 0
    y: int = 0


# =========================================================
# RETÂNGULO
# =========================================================

@dataclass
class RectElement(Element):

    width: int = 10
    height: int = 10

    fill: str = "#FFFFFF"
    border: str = "#444444"
    radius: int = 0

    def __init__(
        self,
        x=0,
        y=0,
        width=10,
        height=10,
        fill="#FFFFFF",
        border="#444444",
        radius=0
    ):

        super().__init__("RECT", x, y)

        self.width = width
        self.height = height

        self.fill = fill
        self.border = border
        self.radius = radius


# =========================================================
# PEÇA
# =========================================================

@dataclass
class Piece:

    name: str = "Unnamed"

    elements: list = field(default_factory=list)

    # -----------------------------------------------------

    def add(self, element):

        self.elements.append(element)

    # -----------------------------------------------------

    def add_rect(
        self,
        x=0,
        y=0,
        width=10,
        height=10,
        fill="#FFFFFF",
        border="#444444",
        radius=0
    ):

        self.add(

            RectElement(

                x=x,
                y=y,

                width=width,
                height=height,

                fill=fill,
                border=border,
                radius=radius

            )

        )

    # -----------------------------------------------------

    @property
    def width(self):

        if not self.elements:
            return 0

        w = 0

        for e in self.elements:

            if hasattr(e, "width"):

                w = max(
                    w,
                    e.x + e.width
                )

        return w

    # -----------------------------------------------------

    @property
    def height(self):

        if not self.elements:
            return 0

        h = 0

        for e in self.elements:

            if hasattr(e, "height"):

                h = max(
                    h,
                    e.y + e.height
                )

        return h

    # -----------------------------------------------------

    def clear(self):

        self.elements.clear()

    # -----------------------------------------------------

    def __iter__(self):

        return iter(self.elements)

    # -----------------------------------------------------

    def __len__(self):

        return len(self.elements)

    # -----------------------------------------------------

    def __repr__(self):

        return (
            f"<Piece "
            f"{self.name} "
            f"Elements={len(self.elements)} "
            f"Size={self.width}x{self.height}>"
        )