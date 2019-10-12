import time
from datetime import datetime

from pyspark.sql.types import StringType
from pyspark.ml.linalg import Vectors, VectorUDT, SparseVector, DenseVector


def get_time_today():
    return datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d')


def vec_dense(l):
    return Vectors.dense(l)


def vec_dense2sparse(vec):
    return Vectors.sparse(vec)


def array_string_get(l, i):
    return l[i]


def register_udf(runtime):
    ss = runtime.sparkSession
    ss.udf.register('udf_day', f=get_time_today, returnType=StringType())
    ss.udf.register('vec_dense', f=vec_dense, returnType=VectorUDT())
    ss.udf.register('vec_dense2sparse', f=vec_dense2sparse, returnType=VectorUDT())
    ss.udf.register('array_string_get', f=array_string_get, returnType=StringType())
