from lark import Lark, Tree

from ASTBuilder import ASTBuilder


class AstParser6502:
    def __init__(self, grammar: str, start_tag: str = "start"):
        self._parser = Lark(grammar, start=start_tag, parser="lalr", transformer=ASTBuilder())

    def parse(self, text: str):
        val: Tree = self._parser.parse(text)
        return val
