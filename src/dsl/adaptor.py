""" Adaptor """

from dsl.parser.DSLSQLParser import DSLSQLParser


class DslAdaptor:

    def clean_str(self, raw_str):
        if raw_str.startswith("`") or raw_str.startswith("\""):
            raw_str = raw_str.replace("`", "").replace("\"", "")
        return raw_str

    def get_original_text(self, ctx):
        _input = ctx.start.getTokenSource()._input
        return _input.getText(ctx.start.start, ctx.stop.stop)


class ConnectAdaptor(DslAdaptor):

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
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
            if type(_type) == DSLSQLParser.DbContext:
                globals()[_type.getText()] = option
        print(globals()["tables"])


class CreateAdaptor(DslAdaptor):

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class DropAdaptor(DslAdaptor):

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class InsertAdaptor(DslAdaptor):

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class LoadAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        option = dict()
        format_type, path, table_name = "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()
            if type(_type) == DSLSQLParser.PathContext:
                path = self.clean_str(_type.getText())
            if type(_type) == DSLSQLParser.TableNameContext:
                table_name = _type.getText()
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[_type.identifier().getText()] = _type.STRING().getText()
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[_type.expression().identifier().
                       getText()] = _type.expression().STRING().getText()
        print(format_type, path, table_name, option)
        table = None
        reader = self.xql_listener._sparkSession.read
        if option:
            reader.options(option)
        if format_type == "json":
            table = reader.format(format_type).load(path)
            table.show()
        table.createOrReplaceTempView(table_name)


class RegisterAdaptor(DslAdaptor):

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
                path = _type.getText()
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
        print(func_name, format_type, path)
        print(option)


class SaveAdaptor(DslAdaptor):

    def parse(self, ctx):
        option = dict()
        mode, final_path, format_type, table_name = "", "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()
            if type(_type) == DSLSQLParser.PathContext:
                final_path = _type.getText()
            if type(_type) == DSLSQLParser.TableNameContext:
                table_name = _type.getText()
            if type(_type) == DSLSQLParser.OverwriteContext:
                mode = _type.getText()
            if type(_type) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
        print(format_type, final_path, table_name, mode)
        print(option)


class SelectAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        print(original_text)
        chunks = original_text.split(" ")
        print(chunks)
        origin_table_name = chunks[-1].replace(";", "")
        print(origin_table_name)
        xql = original_text.replace("as {}".format(origin_table_name), "")
        print(xql)
        df = self.xql_listener._sparkSession.sql(xql)
        df.createOrReplaceTempView(origin_table_name)
        df.show()


class SetAdaptor(DslAdaptor):

    def parse(self, ctx):
        print("set adaptor", ctx)


class TrainAdaptor(DslAdaptor):

    def parse(self, ctx):
        option = dict()
        format_type, table_name, path = "", "", ""
        for i in range(ctx.getChildCount()):
            _type = ctx.getChild(i)
            if type(_type) == DSLSQLParser.Format_typeContext:
                format_type = _type.getText()
            if type(_type) == DSLSQLParser.PathContext:
                path = _type.getText()
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
        print(format_type, table_name, path)
        print(option)
