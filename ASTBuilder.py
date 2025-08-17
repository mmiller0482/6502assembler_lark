# ----------------------------
# Transformer to convert tokens
# ----------------------------
from lark import Transformer, Token, v_args


@v_args(inline=True)
class ASTBuilder(Transformer):
    def label(self, ident: Token, _colon: Token = None):
        return {"type": "label", "name": str(ident)}

    def DEC(self, tok: Token):
        return int(tok)

    def HEX(self, tok: Token):
        return int(tok[1:], 16)

    def BIN(self, tok: Token):
        return int(tok[1:], 2)

    def numeric_val(self, value):
        return {"type": "number", "value": value}