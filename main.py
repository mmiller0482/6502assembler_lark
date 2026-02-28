from typing import Dict, List

from assembler.assembler_6502 import AsmResult, assemble
from ast_parse.ast_parser_6502_factory import AstParser6502Factory

if __name__ == "__main__":
    src = """.org $C000
start:
    LDA #$10
    STA $00
    BRK ; done
"""
    parser = AstParser6502Factory.build()
    program: List[Dict] = parser.parse(src)

    for line in program:
        print(line)

    asm_result: AsmResult = assemble(program)
