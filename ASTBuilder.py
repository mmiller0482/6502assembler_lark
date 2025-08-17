# ----------------------------
# Transformer to convert tokens
# ----------------------------
from lark import Transformer, Token, v_args

# NOTES about transform methods:
# If transform is for a terminal, the arguments passed in is a single argument, for the terminal token.
# If transform is for a rule that consists of a literal + an already transformed token, only the value of the already transformed is returned.
# If the transform consists of one or more non-transformed tokens, all of those tokens are passed in as arguments.

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

    def immediate(self, value):
        return {"type": "immediate", "value": value}