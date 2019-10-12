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
    set test1 = '''{"name": "wyz,a", "age": 20}
                   {"name": "wyz1,b", "age": 21}
                   {"name": "wyz1,c", "age": 22}
                   {"name": "wyz2,d", "age": 23}
                   {"name": "wyz2,e", "age": 24}
                   {"name": "wyz3,f,1", "age": 24}''';
    load jsonStr.`{test1}` as t1;
    select name, age as all from `t1` where name like "%" as t2;
    save overwrite t2 as console.``;
    """
]

VeronicaApp.run(params_list)