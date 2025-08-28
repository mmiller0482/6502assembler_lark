from pathlib import Path

from ast_parser_6502 import AstParser6502


class AstParser6502Factory:
    GRAMMAR_FILE = Path(__file__).parent / "grammar_6502.lark"

    @classmethod
    def build(cls, grammar_file: str = None, start_tag: str = "start"):
        if grammar_file is None:
            grammar_file = cls.GRAMMAR_FILE

        grammar = ""
        with open(grammar_file, "r") as f:
            grammar = f.read()

        return AstParser6502(grammar, start_tag)
