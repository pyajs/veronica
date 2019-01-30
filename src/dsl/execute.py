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
        self._last_select_table = None
        self._tmp_tables = set()
        self._connect_options = dict()
        self.AdaptorDict = {
            "load": LoadAdaptor(self),
            "connect": ConnectAdaptor(self),
            "select": SelectAdaptor(self),
            "save": SaveAdaptor(self),
            "create": CreateAdaptor(self),
            "insert": InsertAdaptor(self),
            "drop": DropAdaptor(self),
            "set": SetAdaptor(self),
            "train": TrainAdaptor(self),
            "register": RegisterAdaptor(self)
        }

    def set_last_select_table(self, table_name):
        self._last_select_table = table_name

    def get_last_select_table(self):
        return self._last_select_table

    def set_connect_options(self, k, v):
        self._connect_options[k] = v

    def get_connect_options(self):
        return self._connect_options

    def get_tmp_tables(self):
        return self._tmp_tables

    def add_tmp_tables(self, table_name):
        self._tmp_tables.add(table_name)

    def add_env(self, key, value):
        self._env[key] = value
        return self

    def get_env(self):
        return self._env

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
