from enum import Enum, auto

# TODO: Better name for this file ! Maybe constants?
# Point is to keep track of all the "shorthand" notations we're using througout
# the assembler.


class OpcodeMnemonic(Enum):
    LDA = auto()
    STA = auto()
    BRK = auto()


class AddressingMode(Enum):
    # TODO: Document what these addressing modes are
    # Actually, I'm not even sure that this is representing the addressing mode
    # Figure this out eventually.
    imm = auto()
    zp = auto()
    abs = auto()
    imp = auto()
    # TODO: What is mem? AstBuilder says we'll deal with it later
    mem = auto()
