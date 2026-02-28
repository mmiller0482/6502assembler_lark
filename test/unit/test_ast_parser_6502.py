import pytest

from assembler.ast_parse.ast_parser_6502 import AstParser6502
from assembler.ast_parse.ast_parser_6502_factory import AstParser6502Factory

@pytest.fixture
def gen_parser():
    def gen_parser_fixture(start_tag="start"):
        return AstParser6502Factory.build(start_tag=start_tag)

    return gen_parser_fixture

class TestAstParser6502:


    @pytest.mark.parametrize(
        "source, expected",
        [
            ("42", 42),
            ("$100", 256),
            ("%1011", 11)
        ],
    )
    def test_parse_number(self, gen_parser, source: str, expected: int):
        parser : AstParser6502 = gen_parser("numeric_val")
        ast = parser.parse(source)
        # never reach assert because the grammar does not allow for simply returning a terminal.
        assert ast == expected

    def test_comment(self, gen_parser):
        # Comment should do nothing :)
        parser : AstParser6502 = gen_parser("comment")
        ast = parser.parse(";comment")
        assert ast is None

    @pytest.mark.parametrize(
        "source, expected",
        [
            ("#42", 42),
            ("#$100", 256),
            ("#%1011", 11)
        ],
    )
    def test_immediate(self, gen_parser, source: str, expected: int):
        # Here we need to test that immediate hashing is performed correctly and
        # splits the hash string into two parts
        parser : AstParser6502 = gen_parser("immediate")
        ast = parser.parse(source)

        # TODO: need to comprehend from ast_builder code why immediate gets
        # generated the way it does
        assert isinstance(ast, dict)
        assert "mode" in ast
        assert ast["mode"] == "imm"

        assert "expr" in ast
        assert ast["expr"] == expected
