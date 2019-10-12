## 数据源支持

### 1.json支持
1.1.json 文件支持
```sql
load json.`/json_file_path` as t1;
```

1.2.json 字符串支持
```sql
set rawJsonStr = '''
{"jack":1,"jack2":2}
{"jack":2,"jack2":3}
''';

load jsonStr.`{rawJsonStr}` as t1;
```


### 2.csv支持
1.1.csv 文件支持
```sql
load csv.`/csv_file_path` as t1;
```

1.2.csv 字符串支持
```sql
set rawCsvStr = '''
a b c
d e f
e d f
''';

load csvStr.`{rawCsvStr}` options header="false" as t2;
```

### 3.libsvm支持
```sql
load libsvm.`/libsvm_file_path` as t1;
```

### 4.parquet支持
```sql
load parquet.`/parquet_file_path` as t1;
```

### 5.其他数据源
理论上是可以支持很多其他数据源的, 比如通过jdbc访问mysql, 通过其他包来访问hbase, kudu, es, tidb等热门存储系统
后续会增加相关的支持
