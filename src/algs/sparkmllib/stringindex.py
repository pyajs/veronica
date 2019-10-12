from pyspark.ml.feature import StringIndexer, StringIndexerModel
from pyspark.sql.types import ArrayType, StringType, IntegerType
from pyspark.sql.functions import explode
from algs.functions import Functions


class SQLStringindex(Functions):

    def train(self, df, path, option):
        new_df = df
        si = StringIndexer()
        self.configure_model_spark(si, option)
        for sf in df.schema:
            if sf.name == option["inputCol"]:
                if isinstance(sf.dataType, ArrayType):
                    new_df = df.select(explode(option["inputCol"]).alias(option["inputCol"]))
        model = si.fit(new_df)
        model.write().overwrite().save(path)

    def load(self, spark_session, path, option):
        return StringIndexerModel.load(path)

    def predict(self, spark_session, _model, fname, option):
        model = spark_session.sparkContext.broadcast(_model.labels)

        def f1(s):
            if s not in model.value:
                return -1
            return model.value.index(s)

        def f2(index):
            return model.value[index]

        def f3(sl):
            return [f1(i) for i in sl]

        spark_session.udf.register(fname, f=f1, returnType=IntegerType())
        spark_session.udf.register(fname + "_r", f=f2, returnType=StringType())
        spark_session.udf.register(fname + "_array", f=f3, returnType=ArrayType(IntegerType()))
