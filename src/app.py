from common.params_util import ParamsUtil
from core.platform import PlatformManager


class VeronicaApp:

    @classmethod
    def run(cls, params):
        params = ParamsUtil(params)
        print(params)
        PlatformManager.run(params)


params_list = [
    "-xmatrix.master", "local[2]",
    "-xmatrix.name", "Monster",
    "-xmatrix.rest", "true",
    "-xmatrix.platform", "spark",
]

VeronicaApp.run(params_list)
