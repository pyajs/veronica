import time
from datetime import datetime

from pyspark.sql.types import StringType


def get_time_today():
    return datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d')


def register_udf(runtime):
    ss = runtime.sparkSession
    ss.udf.register('udf_day', f=get_time_today, returnType=StringType())
