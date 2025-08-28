import pytest

from ast_parser_6502 import AstParser6502
from ast_parser_6502_factory import AstParser6502Factory

@pytest.fixture
def gen_parser():
    def gen_parser_at_start(start_tag = "start"):
        return AstParser6502Factory.build(start_tag = start_tag)

    return gen_parser_at_start


@pytest.mark.parametrize("source, expected", [
    ("42", 42),
])

def test_parse_number(gen_parser, source: str, expected: int):
    parser = gen_parser("numeric_val")
    ast = parser.parse(source)
    # never reach assert because the grammar does not allow for simply returning a terminal.