from dsl.parser.DSLSQLLexer import DSLSQLLexer
from dsl.parser.DSLSQLListener import DSLSQLListener
from dsl.parser.DSLSQLParser import DSLSQLParser

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from dsl.adaptor import LoadAdaptor, ConnectAdaptor, SelectAdaptor, SaveAdaptor, \
                    CreateAdaptor, InsertAdaptor, DropAdaptor, SetAdaptor, \
                    TrainAdaptor, RegisterAdaptor

from common.utils import singleton


class XQLExec:

    @classmethod
    def parse_xql(cls, input_xql, listener):
        lexer = DSLSQLLexer(InputStream(input_xql))
        tokens = CommonTokenStream(lexer)
        parse = DSLSQLParser(tokens)
        tree = parse.statement()
        ParseTreeWalker().walk(listener, tree)


@singleton
class XQLExecListener(DSLSQLListener):

    def __init__(self, sparkSession, group_id):
        self._env = dict()
        self._sparkSession = sparkSession
        self.last_select_table = None
        self.AdaptorDict = {
            "load": LoadAdaptor(self),
            "connect": ConnectAdaptor(),
            "select": SelectAdaptor(),
            "save": SaveAdaptor(),
            "create": CreateAdaptor(),
            "insert": InsertAdaptor(),
            "drop": DropAdaptor(),
            "set": SetAdaptor(),
            "train": TrainAdaptor(),
            "register": RegisterAdaptor()
        }

    def exitSql(self, ctx):
        self.AdaptorDict.get(ctx.getChild(0).getText().lower()).parse(ctx)


def main():
    # load_xql = """load json.`/path` where `xxxx`="aaaa" and yyyy="bbbbb" and zzzz="ccc" as temp1;"""
    # connect_xql = """ connect es where `es.nodes`="192.168.200.152" and `es.port`="9200" as tables; """
    # create_xql = """ create table test; """
    # drop_xql = """ drop table if exists test; """
    # reg_xql = """ register DCT.`/path` as predict_func; """
    # save_xql = """ save overwrite table as parquet.`/tmp/table`; """
    # select_xql = """ select * from table2 as table3; """
    train_xql = """ train temp1 as SKLearn.`/path` where `aaaa`="123" and `bbb`="222"; """
    my_lister = XQLExecListener()
    p = XQLExec()
    p.parse_xql(train_xql, my_lister)


if __name__ == '__main__':
    main()
