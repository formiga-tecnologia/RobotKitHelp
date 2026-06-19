"""
==========================================================
 RoboKitHelp Compiler

 compile_result.py

 Resultado de uma compilação.
==========================================================
"""

from dataclasses import dataclass, field


@dataclass
class CompileResult:

    # Peça compilada
    piece = None

    # Lista de erros
    errors: list = field(default_factory=list)

    # ----------------------------

    @property
    def success(self):

        return len(self.errors) == 0

    # ----------------------------

    def add_error(self, error):

        self.errors.append(error)

    # ----------------------------

    def clear(self):

        self.errors.clear()

        self.piece = None

    # ----------------------------

    def __bool__(self):

        return self.success

    # ----------------------------

    def __repr__(self):

        return (
            f"<CompileResult "
            f"success={self.success} "
            f"errors={len(self.errors)}>"
        )