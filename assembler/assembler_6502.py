from __future__ import annotations


from typing import Dict, List, Optional, Tuple

from assembler.asm_result import AsmResult
from assembler.assembler_6502_state import Assembler6502State
from assembler.exceptions import AssemblerError
from assembler.enums import OpcodeMnemonic as Op, AddressingMode as AddrMode

OPCODES: Dict[Tuple[Op, AddrMode], int] = {
    (Op.LDA, AddrMode.imm): 0xA9,
    (Op.STA, AddrMode.zp): 0x85,
    (Op.STA, AddrMode.abs): 0x8D,
    (Op.BRK, AddrMode.imp): 0x00,
}


class Assembler6502:
    def __init__(self, program: List[dict]):
        self.program = program
        self.state = Assembler6502State()

    # Properties
    @property
    def pc(self) -> Optional[int]:
        return self.state.pc

    @pc.setter
    def pc(self, value: int):
        self.state.pc = value

    @property
    def symbols(self) -> Dict[str, int]:
        return self.state.symbols

    @symbols.setter
    def symbols(self, value: Dict[str, int]):
        self.state.symbols = value

    @property
    def origin(self) -> Optional[int]:
        return self.state.origin

    @origin.setter
    def origin(self, value: int):
        self.state.origin = value

    def assemble(self) -> AsmResult:
        self.state.reset()
        self._assemble_pass_1()
        out = self._assemble_pass_2()
        return AsmResult(origin=self.origin, bytes_=bytes(out), symbols=self.symbols)

    def _assemble_pass_1(self):
        # --- Pass 1: self.symbols + sizing ---
        for line in self.program:
            label = line.get("label")
            stmt = line.get("stmt")

            if stmt and stmt.get("type") == "org":
                self.pc = int(stmt["expr"])
                self.origin = self.pc
                if label:
                    self.symbols[label] = self.pc
                continue

            if self.pc is None:
                # require an self.origin before code/data
                if label:
                    raise AssemblerError(f"Label '{label}' defined before .org")
                if stmt:
                    raise AssemblerError("Statement before .org")
                continue

            if label:
                self.symbols[label] = self.pc

            if not stmt:
                continue

            if stmt["type"] == "instr":
                self.pc += Assembler6502._instruction_size(stmt)
            elif stmt["type"] == "byte":
                self.pc += len(stmt["values"])
            else:
                raise AssemblerError(
                    f"Unsupported statement type in smoke test: {stmt['type']}"
                )

        if self.origin is None:
            raise AssemblerError("Missing .org")

    def _assemble_pass_2(self) -> List[int]:
        # --- Pass 2: encode ---
        self.pc = self.origin
        out: List[int] = []

        for line in self.program:
            stmt = line.get("stmt")
            if not stmt:
                continue

            if stmt["type"] == "org":
                self.pc = int(stmt["expr"])
                # For a smoke test, assume one contiguous block starting at self.origin.
                # (Later you can support multiple segments.)
                if self.pc != self.origin and out:
                    raise AssemblerError(
                        "Multiple .org segments not supported in smoke test"
                    )
                continue

            if stmt["type"] == "instr":
                bytes_for_insn = Assembler6502._encode_instruction(stmt)
                out.extend(bytes_for_insn)
                self.pc += len(bytes_for_insn)
                continue

            if stmt["type"] == "byte":
                for v in stmt["values"]:
                    if not (0 <= v <= 0xFF):
                        raise AssemblerError(f".byte value out of range: {v:#x}")
                    out.append(v & 0xFF)
                    self.pc += 1
                continue

            raise AssemblerError(
                f"Unsupported statement type in smoke test: {stmt['type']}"
            )

        return out

    @staticmethod
    def _instruction_size(stmt: dict) -> int:
        mnem = stmt["mnemonic"]
        op = stmt.get("operand")

        if mnem == Op.BRK:
            return 1
        if mnem == Op.LDA:
            if op and op["mode"] == AddrMode.imm:
                return 2
        if mnem == Op.STA:
            if op and op["mode"] == AddrMode.mem:
                # choose later; but sizing depends on value being zp or abs.
                # For smoke test (numeric only), we can decide now.
                v = op["expr"]
                return 2 if Assembler6502._is_zp(v) else 3

        raise AssemblerError(f"Unsupported instruction for smoke test: {mnem} {op}")

    @staticmethod
    def _encode_instruction(stmt: dict) -> List[int]:
        mnem = stmt["mnemonic"]
        op = stmt.get("operand")

        if mnem == Op.BRK:
            return [OPCODES[(Op.BRK, AddrMode.imp)]]

        if mnem == Op.LDA and op and op["mode"] == AddrMode.imm:
            val = op["expr"]
            if not (0 <= val <= 0xFF):
                raise AssemblerError(f"LDA immediate out of range: {val:#x}")
            return [OPCODES[(Op.LDA, AddrMode.imm)], val & 0xFF]

        if mnem == Op.STA and op and op["mode"] == AddrMode.mem:
            addr = op["expr"]
            if Assembler6502._is_zp(addr):
                return [OPCODES[(Op.STA, AddrMode.zp)], addr & 0xFF]
            if not (0 <= addr <= 0xFFFF):
                raise AssemblerError(f"STA address out of range: {addr:#x}")
            lo = addr & 0xFF
            hi = (addr >> 8) & 0xFF
            return [OPCODES[(Op.STA, AddrMode.abs)], lo, hi]

        raise AssemblerError(f"Unsupported instruction for smoke test: {mnem} {op}")

    @staticmethod
    def _is_zp(value: int) -> bool:
        return 0 <= value <= 0xFF
