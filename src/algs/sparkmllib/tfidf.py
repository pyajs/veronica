from pyspark.ml.feature import IDF, IDFModel
from algs.functions import Functions


class SQLTfidf(Functions):

    def train(self, df, path, option):
        idf = IDF()
        self.configure_model_spark(idf, option)
        model = idf.fit(df)
        model.write().overwrite().save(path)

    def load(self, spark_session, path, option):
        return IDFModel.load(path)

    def predict(self, spark_session, _model, fname, option):
        model = spark_session.sparkContext.broadcast(_model)
