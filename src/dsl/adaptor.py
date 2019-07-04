""" Adaptor """

import json
import importlib
import logging

from pyspark.sql import Row

from dsl.parser.DSLSQLParser import DSLSQLParser


class DslAdaptor:

    def clean_str(self, raw_str):
        if raw_str.startswith("`") or raw_str.startswith("\""):
            raw_str = raw_str.replace("`", "").replace("\"", "")
        if raw_str.startswith("'''"):
            raw_str = raw_str[3: len(raw_str) - 3]
        return raw_str

    def get_original_text(self, ctx):
        _input = ctx.start.getTokenSource()._input
        return _input.getText(ctx.start.start, ctx.stop.stop)


class ConnectAdaptor(DslAdaptor):
    # todo : 暂时不实现

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.Format_typeContext:
                option["format"] = _type.getText()
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
            if type(_type) == DSLSQLParser.DbContext:
                self.xql_listener.set_connect_options(_type.getText(), option)


class CreateAdaptor(DslAdaptor):
    # todo : 暂时不实现

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        # sparkSession.sql(sql).count()


class DropAdaptor(DslAdaptor):
    # todo : 暂时不实现

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # logging.info(original_text)
        # self.xql_listener._sparkSession.sql(original_text).count()
        # self.xql_listener.set_last_select_table(None)


class InsertAdaptor(DslAdaptor):
    # todo : 暂时不实现

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        # sparkSession.sql(sql).count()


class LoadAdaptor(DslAdaptor):
    # Load 语句: 用来加载各种数据源
    #   load    csv.`/file/path` options header="true" and delimiter="," as t1;
    # keyword   format   path    keyword             option              table_name

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        format_type, path, table_name = "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            # Format Get
            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()

            # Path Get
            if type(_type) == DSLSQLParser.PathContext:
                path = self.clean_str(_type.getText())
                path = path.format(**self.xql_listener.get_env())

            # TableName Get
            if type(_type) == DSLSQLParser.TableNameContext:
                table_name = _type.getText()

            # Options/Where key/value Get
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[_type.identifier().getText()] = self.clean_str(_type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[_type.expression().identifier().getText()] = self.clean_str(_type.expression().STRING().getText())

        table = None
        reader = self.xql_listener._sparkSession.read
        if option:
            reader.options(**option)

        if format_type in ["json", "csv", "parquet", "orc", "libsvm"]:  # Spark 默认支持的一些格式
            table = reader.format(format_type).load(path)

        if format_type == "jsonStr":
            json_items = list(map(lambda x: Row(**json.loads(x)), filter(lambda x: len(x) > 0, path.split("\n"))))
            table = self.xql_listener._sparkSession.createDataFrame(json_items)

        if format_type == "csvStr":

            def _csv_split(data, option):
                if "delimiter" not in option:
                    return [data]
                return data.split(option.get("delimiter", ","))

            index = 0
            csv_str_list = list(filter(lambda x: len(x) > 0,
                                       self.clean_str(path).split("\n")))
            key_list = ["_c{}".format(i) for i, _ in enumerate(_csv_split(csv_str_list[0], option))]
            if str(option.get("header", False)).lower() == "true":  # py3 居然不能通过 bool('false') 来转换
                key_list = _csv_split(csv_str_list[0], option)
                index = 1
            csv_items = [Row(**dict(zip(key_list, _csv_split(i, option)))) for i in csv_str_list[index:]]
            table = self.xql_listener._sparkSession.createDataFrame(csv_items)

        if format_type == "sqlite":
            reader.format("jdbc").load()

        if format_type == "mysql":
            pass

        table.createOrReplaceTempView(table_name)


class RegisterAdaptor(DslAdaptor):
    # Register 语句: 用来将Model加载为UDF
    # register word2vec.`/model/path` as w2v_predict;
    #  keyword   format      path         func_name

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        func_name, format_type, path = "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)

            if type(_type) == DSLSQLParser.FunctionNameContext:
                func_name = _type.getText()

            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()

            if type(_type) == DSLSQLParser.PathContext:
                path = self.clean_str(_type.getText())
                path = path.format(**self.xql_listener.get_env())

            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(_type.identifier().getText())] = self.clean_str(_type.STRING().getText())

            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().getText())] = self.clean_str(_type.expression().STRING().getText())

        ss = self.xql_listener._sparkSession

        xql_alg = MLMapping.find_alg(format_type, option)

        model = xql_alg.load(ss, path, option)
        xql_alg.predict(ss, model, func_name, option)

        self.xql_listener.set_last_select_table(None)


class SaveAdaptor(DslAdaptor):
    # Save语句: 用来持久化数据,将数据保存到各种数据源
    # save     overwrite   table1   as  json.`/data/`;
    # keyword     mode    table_name   format   path

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        mode, final_path, format_type, table_name = "", "", "", ""
        partition_by_col = []
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)

            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()

            if type(_type) == DSLSQLParser.PathContext:
                final_path = self.clean_str(_type.getText())
                final_path = final_path.format(**self.xql_listener.get_env())

            if type(_type) == DSLSQLParser.TableNameContext:
                table_name = _type.getText()

            if type(_type) == DSLSQLParser.OverwriteContext:
                mode = _type.getText()
            if type(_type) == DSLSQLParser.AppendContext:
                mode = _type.getText()
            if type(_type) == DSLSQLParser.ErrorIfExistsContext:
                mode = _type.getText()
            if type(_type) == DSLSQLParser.IgnoreContext:
                mode = _type.getText()

            if type(_type) == DSLSQLParser.ColContext:
                partition_by_col = _type.getText().split(",")

            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(_type.identifier().getText())] = self.clean_str(_type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().getText())] = self.clean_str(_type.expression().STRING().getText())

        old_df = self.xql_listener._sparkSession.table(table_name)
        if format_type == "console":
            old_df.show(5, False)
        else:
            # writer = old_df.write.format(format_type).mode(mode)
            if "FileNum" in option:
                old_df.repartition(int(option["FileNum"]))
            # if partition_by_col:
            #     writer.partitionBy(partition_by_col)

            if format_type in ["json", "csv", "parquet", "orc"]:
                old_df.write.format(format_type).mode(mode).save(final_path)


class SelectAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)

        chunks = original_text.split(" ")
        origin_table_name = chunks[-1].replace(";", "")
        xql = original_text.replace("as {}".format(origin_table_name), "")

        df = self.xql_listener._sparkSession.sql(xql)
        df.createOrReplaceTempView(origin_table_name)

        self.xql_listener.set_last_select_table(origin_table_name)


class SetAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        set_key, set_value = "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.SetKeyContext:
                set_key = _type.getText()
            if type(_type) == DSLSQLParser.SetValueContext:
                set_value = self.clean_str(_type.getText())
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())

        self.xql_listener._sparkSession.sql(f"set {set_key} = {set_value}")
        self.xql_listener.add_env(set_key, set_value)
        self.xql_listener.set_last_select_table(None)


class TrainAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        format_type, table_name, path = "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()
            if type(_type) == DSLSQLParser.PathContext:
                path = self.clean_str(_type.getText())
                path = path.format(**self.xql_listener.get_env())
            if type(_type) == DSLSQLParser.TableNameContext:
                table_name = _type.getText()
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
        df = self.xql_listener._sparkSession.table(table_name)
        xql_alg = MLMapping.find_alg(format_type, option)
        xql_alg.train(df, path, option)


class MLMapping:
    mapping = {"sparkmllib.word2vec": "algs.sparkmllib.word2vec",
               "sparkmllib.stringindex": "algs.sparkmllib.stringindex",
               "sparkmllib.tfidf": "algs.sparkmllib.tfidf"}

    @classmethod
    def find_alg(cls, format_type, option):
        alf_file = importlib.import_module(cls.mapping["{}.{}".format(format_type, option["alg"])])
        return getattr(alf_file, 'SQL{}'.format(option["alg"].capitalize()))()
