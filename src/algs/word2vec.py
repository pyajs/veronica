from pyspark.ml.feature import Word2Vec, Word2VecModel
from pyspark.sql.types import ArrayType, DoubleType, StringType, StructType, StructField, IntegerType
from algs.functions import Functions
from numpy.core.multiarray import array


class XQLWord2Vec(Functions):

    def train(self, df, path, option):
        w2v = Word2Vec()
        self.configure_model_spark(w2v, option)
        model = w2v.fit(df)
        model.write().overwrite().save(path)

    def load(self, spark_session, path, option):
        return Word2VecModel.load(path)

    def predict(self, spark_session, _model, fname, option):
        model = spark_session.sparkContext.broadcast(
            _model.getVectors().collect())
        model_predict = {r.word: r.vector.toArray() for r in model.value}
        model_find = {w: _model.findSynonymsArray(w, 5) for w in model_predict}

        def f1(w):
            return model_predict.get(w, array([0.0])).tolist()

        def f2(wl):
            return list(map(f1, wl))

        def f3(w, n):
            return model_find.get(w, [("", 0.0)])[0:int(n)]

        spark_session.udf.register(
            fname + "_array",
            f=f2,
            returnType=ArrayType(ArrayType(DoubleType())))
        spark_session.udf.register(
            fname + "_find",
            f=f3,
            returnType=ArrayType(
                StructType([
                    StructField("word", StringType(), False),
                    StructField("find", DoubleType(), False)
                ])))
        spark_session.udf.register(
            fname, f=f1, returnType=ArrayType(DoubleType()))
