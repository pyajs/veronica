from pyspark import SparkConf
from pyspark.sql import SparkSession

from common.utils import singleton


@singleton
class SparkRuntime:

    def __init__(self, _params):
        self.params = _params
        self.sparkSession = self.create_runtime()

    def is_local_master(self):
        master = self.params.get("xmatrix.master", "")
        return master == "local" or master.startswith("local[")

    def create_runtime(self):
        conf = SparkConf()
        for k in self.params.keys():
            if k.startswith("spark.") or k.startswith("hive."):
                conf.set(k, self.params[k])

        if "xmatrix.master" in self.params:
            conf.setMaster(self.params["xmatrix.master"])

        conf.setAppName(self.params["xmatrix.name"])

        sparkSession = SparkSession.builder.config(conf=conf)

        if bool(self.params.get("xmatrix.enableHiveSupport", "false")):
            sparkSession.enableHiveSupport()

        ss = sparkSession.getOrCreate()

        job_type = self.params.get("xmatrix.type", "script")

        if job_type == "stream" and "xmatrix.metrics.kafka" in self.params:
            ss.sparkContext.setLocalProperty(
                "kafkaAddr", self.params["xmatrix.metrics.kafka"])
        print(ss)
        return ss

    def register_udf(self, clzz):
        pass
