from pathlib import Path

from .ast_parser_6502 import AstParser6502


class AstParser6502Factory:
    GRAMMAR_FILE = Path(__file__).parent.parent.parent / "grammar" / "grammar_6502.lark"

    @classmethod
    def build(cls, grammar_file: str = None, start_tag: str = "start"):
        """

        :param grammar_file: Path to the 6502 grammar file
        :param start_tag: name of the tag which is the root node of the AST
        :return: new AstParser6502 object
        """
        if grammar_file is None:
            grammar_file = cls.GRAMMAR_FILE

        grammar = ""
        with open(grammar_file, "r") as f:
            grammar = f.read()

        return AstParser6502(grammar, start_tag)
