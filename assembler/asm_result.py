from dataclasses import dataclass
from typing import Dict


@dataclass
class AsmResult:
    origin: int
    bytes_: bytes
    symbols: Dict[str, int]
