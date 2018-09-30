from core.spark_runtime import 


class PlatformManager:
    config = None
    listeners = []

    def __init__(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass

    def start_http_server(self, ip, port):
        print(ip, port)

    def start_thrift_server(self):
        pass

    def get_runtime(self):
        pass

    def clear(self):
        pass

    @classmethod
    def run(cls, _params, re_run=False):
        print(_params.pp)
        params = cls.config = _params.pp

        temp_params = {i: params[i] for i in params.keys() if i.startswith("xmatrix")}
        print(temp_params)
        runtime = cls.get_runtime()

        if bool(params.get("xmatrix.rest", "false")):
            ip = params.get("xmatrix.rest.ip", "127.0.0.1")
            port = int(params.get("xmatrix.rest.port", "8080"))
            cls.start_http_server(cls, ip, port)

        if bool(params.get("xmatrix.thrift", "false")):
            cls.start_thrift_server(cls)

        if bool(params.get("xmatrix.unitest.startRuntime", "true")):
            runtime.start_runtime()

        if params.get("xmatrix.udfClassPath", "") != "":
            pass

        if params.get("xmatrix.xql", "") != "":
            job_file_path = params.get("xmatrix.xql")
            xql = ""
            if job_file_path.startswith("classpath://"):
                pass
            else:
                xql = ""

            ss = runtime.sparkSession()
            job_type = params.get("xmatrix.type", "script")
            groupId = ss.sparkContext.appName