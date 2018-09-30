from pyspark import SparkConf
from pyspark.sql import SparkSession


class SparkRuntime:
    __instance = None

    def __init__(self, _params):
        self.params = _params

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def is_local_master(self):
        master = self.params.get("xmatrix.master", "")
        return master == "local" or master.startwith("local[")

    def create_runtime(self):
        conf = SparkConf()
        for k in self.params.keys():
            if k.startwith("spark.") or k.startwith("hive."):
                conf.set(k, self.params[k])

        if "xmatrix.master" in self.params:
            conf.setMaster(self.params["xmatrix.master"])

        conf.setAppName(self.params["xmatrix.name"])

        sparkSession = SparkSession.builder.config(conf)

        if bool(self.params.get("xmatrix.enableHiveSupport", "false")):
            sparkSession.enableHiveSupport()

        ss = sparkSession.getOrCreate()

        job_type = self.params.get("xmatrix.type", "script")

        if job_type == "stream" and "xmatrix.metrics.kafka" in self.params:
            ss.sparkContext.setLocalProperty(
                "kafkaAddr", self.params["xmatrix.metrics.kafka"])

        return ss

    def register_udf(self, clzz):
        pass
