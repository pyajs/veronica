from app import VeronicaApp


params_list = [
    "-xmatrix.master", "local[2]",
    "-xmatrix.name", "Monster",
    "-xmatrix.rest", "false",
    "-xmatrix.rest.ip", "127.0.0.1",
    "-xmatrix.rest.port", "8123",
    "-xmatrix.platform", "spark",
    "-xmatrix.xql",
    """
    set test = '''{"name": "wyz", "age": "20"}\n{"name": "wyz", "age": "21"}''';
    load jsonStr.`{test}` as t1;
    select * from t1 as t2;
    save overwrite t2 as console.``;
    """
]

VeronicaApp.run(params_list)