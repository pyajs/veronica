from itertools import zip_longest


class ParamsUtil:

    def __init__(self, params):
        self.params = params
        self.pd = self.parse_param()

    def parse_param(self):
        if (len(self.params) % 2 != 0):
            raise Exception("params num error")

        def p(x):
            if x.startswith("-"):
                return x[1:]
            return x

        return dict(zip_longest(*[iter(map(p, self.params))] * 2, fillvalue=""))
