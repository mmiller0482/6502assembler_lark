from ast_parser_6502 import AstParser6502
from ast_parser_6502_factory import AstParser6502Factory

if __name__ == "__main__":
    str_to_parse = '{"key": ["item0", "item1", 3.14]}'

    parser: AstParser6502 = AstParser6502Factory.build()
    ast = parser.parse(str_to_parse)
    print(ast)
