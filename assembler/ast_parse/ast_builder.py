# ----------------------------
# Transformer to convert tokens
# ----------------------------
from lark import Transformer, Token, v_args

from assembler.enums import OpcodeMnemonic, AddressingMode
from assembler.exceptions import AstParserError

# NOTES about transform methods:
# If transform is for a terminal, the arguments passed in is a single argument, for the terminal token.
# If transform is for a rule that consists of a literal + an already transformed token, only the value of the already transformed is returned.
# If the transform consists of one or more non-transformed tokens, all of those tokens are passed in as arguments.


@v_args(inline=True)
class AstBuilder(Transformer):
    MNEMONIC_MAP = {
        "LDA": OpcodeMnemonic.LDA,
        "STA": OpcodeMnemonic.STA,
        "BRK": OpcodeMnemonic.BRK,
    }

    # ---------- Terminals -> python ----------
    def DEC(self, tok: Token):
        return int(tok)

    def HEX(self, tok: Token):
        return int(tok[1:], 16)

    def BIN(self, tok: Token):
        return int(tok[1:], 2)

    def MNEMONIC(self, tok: Token):
        # TODO: Ask GPT if converting the raw mnemonic strings to enums at this
        # point is appropriate
        my_tok = str(tok)
        if my_tok not in self.MNEMONIC_MAP:
            raise AstParserError(f"Couldn't identify mnemonic: {my_tok}")
        return self.MNEMONIC_MAP[my_tok]

    # ---------- Atoms / expressions ----------
    def numeric_val(self, value):
        # value is already an int from DEC/HEX/BIN
        return value

    def immediate(self, _hash, expr):
        return {"mode": AddressingMode.imm, "expr": expr}

    def absolute_or_zp(self, expr):
        # we’ll decide zp vs abs later (during sizing/encoding)
        return {"mode": AddressingMode.mem, "expr": expr}

    # ---------- Labels ----------
    def label(self, ident: Token, _colon: Token = None):
        return str(ident)

    # ---------- Directives ----------
    def directive(self, tok, arg):
        # tok is a Token(ORG/BYTE) because ORG/BYTE are terminals
        name = str(tok)
        if name == ".org":
            return {"type": "org", "expr": arg}
        if name == ".byte":
            return {"type": "byte", "values": arg}
        return {"type": "directive", "name": name, "arg": arg}

    def expr_list(self, first, *rest):
        return [first, *rest]

    # ---------- Instructions ----------
    def instruction(self, mnemonic, operand=None):
        return {"type": "instr", "mnemonic": mnemonic, "operand": operand}

    # ---------- Comments / lines / program ----------
    def comment(self, _comment_tok):
        # drop it from AST
        return None

    def line(self, *items):
        label = None
        stmt = None

        for it in items:
            if it is None:
                continue
            if isinstance(it, Token) and it.type == "NEWLINE":
                continue
            if isinstance(it, str) and label is None:
                label = it
            elif isinstance(it, dict) and stmt is None:
                stmt = it

        if label is None and stmt is None:
            return None

        return {"type": "line", "label": label, "stmt": stmt}

    def start(self, *lines):
        # remove Nones from blank lines
        return [ln for ln in lines if ln is not None]
