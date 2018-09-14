""" Adaptor """

from parser.DSLSQLParser import DSLSQLParser


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
            ctype = ctx.getChild(i)
            if type(ctype) == DSLSQLParser.ExpressionContext:
                option[self.clean_str(
                    ctype.identifier().getText())] = self.clean_str(
                        ctype.STRING().getText())
            if type(ctype) == DSLSQLParser.BooleanExpressionContext:
                option[self.clean_str(ctype.expression().identifier().
                                      getText())] = self.clean_str(
                                          ctype.expression().STRING().getText())
            if type(ctype) == DSLSQLParser.DbContext:
                pass
        print(option)


class CreateAdaptor(DslAdaptor):

    def parse(self, ctx):
        original_text = self.get_original_text(ctx)
        # merge
        print(original_text)
        # sparkSession.sql(sql).count()


class DropAdaptor(DslAdaptor):

    def parse(self, ctx):
        original_text = original_text = self.get_original_text(ctx)
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

    def parse(self, ctx):
        option = dict()
        format_type, path, table_name = "", "", ""
        for i in range(ctx.getChildCount()):
            ctype = ctx.getChild(i)
            if type(ctype) == DSLSQLParser.Format_typeContext:
                format_type = ctype.getText()
            if type(ctype) == DSLSQLParser.PathContext:
                path = ctype.getText()
            if type(ctype) == DSLSQLParser.TableNameContext:
                table_name = ctype.getText()
            if type(ctype) == DSLSQLParser.ExpressionContext:
                option[ctype.identifier().getText()] = ctype.STRING().getText()
            if type(ctype) == DSLSQLParser.BooleanExpressionContext:
                option[ctype.expression().identifier().
                       getText()] = ctype.expression().STRING().getText()
        print(format_type, path, table_name)
        print(option)


class RegisterAdaptor(DslAdaptor):

    def parse(self, ctx):
        print("register adaptor", ctx)


class SaveAdaptor(DslAdaptor):

    def parse(self, ctx):
        print("save adaptor", ctx)


class SelectAdaptor(DslAdaptor):

    def parse(self, ctx):
        print("select adaptor", ctx)


class SetAdaptor(DslAdaptor):

    def parse(self, ctx):
        print("set adaptor", ctx)


class TrainAdaptor(DslAdaptor):

    def run(self, ctx):
        print("train adaptor", ctx)
