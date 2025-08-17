from ast_parser_6502 import AstParser6502
from ast_parser_6502_factory import AstParser6502Factory

if __name__ == "__main__":
    str_to_parse = """
A_LABEL0:
_LABEL1:
LABEL2:
$AF
%1011
#%10
    """

    parser: AstParser6502 = AstParser6502Factory.build()
    ast = parser.parse(str_to_parse)
    print(ast.pretty())
