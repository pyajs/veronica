from common.params_util import ParamsUtil
from core.platform import PlatformManager


class VeronicaApp:

    @classmethod
    def run(cls, params):
        params = ParamsUtil(params)
        PlatformManager.run(params)


params_list = [
    "-xmatrix.master", "local[2]",
    "-xmatrix.name", "Monster",
    "-xmatrix.rest", "false",
    "-xmatrix.rest.ip", "127.0.0.1",
    "-xmatrix.rest.port", "8123",
    "-xmatrix.platform", "spark",
    "-xmatrix.xql", "/home/w4n9/Code/Github/veronica/xql/alg.xql",
]

VeronicaApp.run(params_list)
