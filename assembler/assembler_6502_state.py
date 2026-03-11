from typing import Optional, Dict


class Assembler6502State:
    def __init__(self):
        self.pc: Optional[int] = None
        self.origin: Optional[int] = None
        self.symbols: Dict[str, int] = {}

    def reset(self):
        self.pc = None
        self.origin = None
        self.symbols = {}
