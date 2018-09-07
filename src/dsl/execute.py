from antlr4 import *

from parser.DSLSQLLexer import DSLSQLLexer
from parser.DSLSQLListener import DSLSQLListener
from parser.DSLSQLParser import DSLSQLParser
from parser.DSLSQLVisitor import DSLSQLVisitor


class XQLExec:
    def parse_xql(self, input_xql, listener):
        lexer = DSLSQLLexer(InputStream(input_xql))
        tokens = CommonTokenStream(lexer)
        parse = DSLSQLParser(tokens)
        tree = parse.statement()
        ParseTreeWalker().walk(listener, tree)


class XQLExecListener(DSLSQLListener):
    def exitSql(self, ctx):
        print(ctx.getChild(0).getText().lower())


def main():
    xql = """load json.`/path` as temp1;"""
    my_lister = XQLExecListener()
    p = XQLExec()
    p.parse_xql(xql, my_lister)


if __name__ == '__main__':
    main()
