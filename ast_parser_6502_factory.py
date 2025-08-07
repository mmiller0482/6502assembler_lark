from ast_parser_6502 import AstParser6502


class AstParser6502Factory:
    GRAMMAR_FILE = "grammar_6502.lark"

    @classmethod
    def build(cls, grammar_file: str = None):
        if grammar_file is None:
            grammar_file = cls.GRAMMAR_FILE

        grammar = ""
        with open(grammar_file, "r") as f:
            grammar = f.read()

        return AstParser6502(grammar)
