from ast_parser_6502 import AstParser6502
from ast_parser_6502_factory import AstParser6502Factory

if __name__ == "__main__":
    src = """.org $C000
start:
    LDA #$10
    STA $00
    BRK ; done
"""
    parser = AstParser6502Factory.build()
    program = parser.parse(src)

    for line in program:
        print(line)