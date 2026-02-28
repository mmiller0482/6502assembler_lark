from __future__ import annotations


from typing import Dict, List, Optional, Tuple

from assembler.asm_result import AsmResult
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

    def assemble(self) -> AsmResult:
        # --- Pass 1: symbols + sizing ---
        pc: Optional[int] = None
        origin: Optional[int] = None
        symbols: Dict[str, int] = {}

        for line in self.program:
            label = line.get("label")
            stmt = line.get("stmt")

            if stmt and stmt.get("type") == "org":
                pc = int(stmt["expr"])
                origin = pc
                if label:
                    symbols[label] = pc
                continue

            if pc is None:
                # require an origin before code/data
                if label:
                    raise AssemblerError(f"Label '{label}' defined before .org")
                if stmt:
                    raise AssemblerError("Statement before .org")
                continue

            if label:
                symbols[label] = pc

            if not stmt:
                continue

            if stmt["type"] == "instr":
                pc += Assembler6502._instruction_size(stmt)
            elif stmt["type"] == "byte":
                pc += len(stmt["values"])
            else:
                raise AssemblerError(
                    f"Unsupported statement type in smoke test: {stmt['type']}"
                )

        if origin is None:
            raise AssemblerError("Missing .org")

        # --- Pass 2: encode ---
        pc = origin
        out: List[int] = []

        for line in self.program:
            stmt = line.get("stmt")
            if not stmt:
                continue

            if stmt["type"] == "org":
                pc = int(stmt["expr"])
                # For a smoke test, assume one contiguous block starting at origin.
                # (Later you can support multiple segments.)
                if pc != origin and out:
                    raise AssemblerError(
                        "Multiple .org segments not supported in smoke test"
                    )
                continue

            if stmt["type"] == "instr":
                bytes_for_insn = Assembler6502._encode_instruction(stmt)
                out.extend(bytes_for_insn)
                pc += len(bytes_for_insn)
                continue

            if stmt["type"] == "byte":
                for v in stmt["values"]:
                    if not (0 <= v <= 0xFF):
                        raise AssemblerError(f".byte value out of range: {v:#x}")
                    out.append(v & 0xFF)
                    pc += 1
                continue

            raise AssemblerError(
                f"Unsupported statement type in smoke test: {stmt['type']}"
            )

        return AsmResult(origin=origin, bytes_=bytes(out), symbols=symbols)

    @staticmethod
    def _instruction_size(stmt: dict) -> int:
        mnem = stmt["mnemonic"]
        op = stmt.get("operand")

        if mnem == Op.BRK:
            return 1
        if mnem == Op.LDA:
            if op and op["mode"] == "imm":
                return 2
        if mnem == Op.STA:
            if op and op["mode"] == "mem":
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

        if mnem == Op.LDA and op and op["mode"] == "imm":
            val = op["expr"]
            if not (0 <= val <= 0xFF):
                raise AssemblerError(f"LDA immediate out of range: {val:#x}")
            return [OPCODES[(Op.LDA, AddrMode.imm)], val & 0xFF]

        if mnem == Op.STA and op and op["mode"] == "mem":
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
