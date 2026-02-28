from typing import Dict, List

from assembler.assembler_6502 import AsmResult, Assembler6502
from assembler.ast_parse.ast_parser_6502_factory import AstParser6502Factory

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

    assembler: Assembler6502 = Assembler6502(program)
    asm_result: AsmResult = assembler.assemble()
