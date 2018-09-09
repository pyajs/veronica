from antlr4 import *
from parser.DSLSQLLexer import DSLSQLLexer
from parser.DSLSQLListener import DSLSQLListener
from parser.DSLSQLParser import DSLSQLParser
# from parser.DSLSQLVisitor import DSLSQLVisitor
from adaptor import *


class XQLExec:
    def parse_xql(self, input_xql, listener):
        lexer = DSLSQLLexer(InputStream(input_xql))
        tokens = CommonTokenStream(lexer)
        parse = DSLSQLParser(tokens)
        tree = parse.statement()
        ParseTreeWalker().walk(listener, tree)


class XQLExecListener(DSLSQLListener):
    AdaptorDict = {
        "load": LoadAdaptor(),
        "connect": ConnectAdaptor(),
    }

    def __init__(self):
        self._env = dict()
        self.last_select_table = None

    def exitSql(self, ctx):
        self.AdaptorDict.get(ctx.getChild(0).getText().lower()).parse(ctx)


def main():
    xql = """load json.`/path` as temp1;"""
    my_lister = XQLExecListener()
    p = XQLExec()
    p.parse_xql(xql, my_lister)


if __name__ == '__main__':
    main()
