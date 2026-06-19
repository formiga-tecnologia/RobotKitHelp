"""
=========================================================
 RoboKitHelp Engine
 Actor.py

 Classe base para qualquer objeto existente no mundo.

 Futuramente poderá representar:
    - Pixel
    - Sprite
    - Robô
    - Parede
    - Sensor
    - NPC
=========================================================
"""

from PySide6.QtGui import (
    QColor,
    QBrush,
    QPen
)

from PySide6.QtWidgets import QGraphicsRectItem


class Actor(QGraphicsRectItem):

    SIZE = 20

    def __init__(
        self,
        x=0,
        y=0,
        width=SIZE,
        height=SIZE,
        color=QColor(90, 200, 255)
    ):

        super().__init__(0, 0, width, height)

        # -------------------------
        # Aparência
        # -------------------------

        self.setBrush(QBrush(color))

        self.setPen(
            QPen(
                QColor(20, 20, 20),
                1
            )
        )

        # -------------------------
        # Posição
        # -------------------------

        self.setPos(x, y)

        # -------------------------
        # Flags
        # -------------------------

        self.setFlag(
            QGraphicsRectItem.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsRectItem.ItemIsSelectable,
            True
        )

        self.setFlag(
            QGraphicsRectItem.ItemSendsGeometryChanges,
            True
        )

        # Nome padrão

        self.name = "Actor"

    # =====================================================

    @property
    def x(self):
        return self.pos().x()

    @property
    def y(self):
        return self.pos().y()

    # =====================================================

    def move(self, dx, dy):
        """
        Move relativo.
        """

        self.setPos(
            self.x + dx,
            self.y + dy
        )

    # =====================================================

    def set_position(self, x, y):

        self.setPos(x, y)

    # =====================================================

    def get_position(self):

        return (
            self.x,
            self.y
        )

    # =====================================================

    def selected(self):

        return self.isSelected()

    # =====================================================

    def __repr__(self):

        return f"<Actor ({self.x:.0f},{self.y:.0f})>"