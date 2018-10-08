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
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
            if type(_type) == DSLSQLParser.DbContext:
                globals()[_type.getText()] = option
        print(globals()["tables"])


class CreateAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class DropAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class InsertAdaptor(DslAdaptor):

    def __init__(self, xql_listener):
        self.xql_listener = xql_listener

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
                path = path.format(**self.xql_listener.get_env())
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
                option[self.clean_str(
                    _type.identifier().getText())] = self.clean_str(
                        _type.STRING().getText())
            if type(_type) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(_type.expression().identifier().
                                      getText())] = self.clean_str(
                                          _type.expression().STRING().getText())
        print(format_type, final_path, table_name, mode)
        print(option)
        old_df = self.xql_listener._sparkSession.table(table_name)
        old_df.show()
        writer = old_df.write.format(format_type).mode(mode)
        if option:
            writer.options(option)
        if partition_by_col:
            writer.partitionBy(partition_by_col)

        if format_type == "json":
            print("save")
            writer.save(final_path)


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
        df.show()


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
        print(set_key, set_value)

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
