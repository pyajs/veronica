from pyspark.ml.feature import IDF, IDFModel, HashingTF
from pyspark.sql.types import IntegerType
from algs.functions import Functions
from pyspark.ml.linalg import Vectors


class SQLTfidf(Functions):

    def train(self, df, path, option):  # pyspark 没有 IntTF 只能尝试使用 HashingTF
        hashing_tf = HashingTF()
        self.configure_model_spark(hashing_tf, option)
        hashing_tf.setOutputCol("__rawFeatures__")
        featurized_data = hashing_tf.transform(df)
        print(featurized_data.collect())
        idf = IDF()
        self.configure_model_spark(idf, option)
        idf.setInputCol("__rawFeatures__")
        model = idf.fit(featurized_data)
        print(model.transform(featurized_data).select("ff").collect())
        model.write().overwrite().save(path)

    def load(self, spark_session, path, option):
        return IDFModel.load(path)

    def predict(self, spark_session, _model, fname, option):
        model = spark_session.sparkContext.broadcast(_model.idf)
        hashing_tf = HashingTF(numFeatures=model.value.size, binary=True)

        def f1(ss):
            return 1

        spark_session.udf.register(fname, f=f1, returnType=IntegerType())
