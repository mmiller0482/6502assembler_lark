from lark import Lark, Tree


class AstParser6502:
    def __init__(self, grammar: str, start_tag: str = "value"):
        self._parser = Lark(grammar, start=start_tag)

    def parse(self, text: str):
        val: Tree = self._parser.parse(text)
        return val
