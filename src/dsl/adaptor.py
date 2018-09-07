""" Adaptor """


class DslAdaptor:
    def __init__(self):
        pass


class ConnectAdaptor:
    def parse(self, ctx):
        print("connect adaptor", ctx)


class CreateAdaptor:
    def parse(self, ctx):
        print("create adaptor", ctx)


class DropAdaptor:
    def parse(self, ctx):
        print("drop adaptor", ctx)


class InsertAdaptor:
    def parse(self, ctx):
        print("insert adaptor", ctx)


class LoadAdaptor:
    def parse(self, ctx):
        print("load adaptor", ctx)


class RegisterAdaptor:
    def parse(self, ctx):
        print("register adaptor", ctx)


class SaveAdaptor:
    def parse(self, ctx):
        print("save adaptor", ctx)


class SelectAdaptor:
    def parse(self, ctx):
        print("select adaptor", ctx)


class SetAdaptor:
    def parse(self, ctx):
        print("set adaptor", ctx)


class TrainAdaptor:
    def run(self):
        print("train adaptor", ctx)
