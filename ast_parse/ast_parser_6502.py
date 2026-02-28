from lark import Lark

from ast_parse.ASTBuilder import ASTBuilder


class AstParser6502:
    """
    Manages generating  a lark-style AST from a given 6502 grammar.
    """

    def __init__(self, grammar: str, start_tag: str = "start"):
        """
        :param grammar: grammar file contents
        :param start_tag: name of the start tag for the given grammar.
        NOTE: Currently no way to swap the Lark parser from anything other than
        lalr
        """
        self._parser = Lark(
            grammar, start=start_tag, parser="lalr", transformer=ASTBuilder()
        )

    def parse(self, text: str):
        # With transformer, this will already be your transformed Python result (a list)
        return self._parser.parse(text)
