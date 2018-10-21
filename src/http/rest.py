""" http restful api """

import time
from bottle import route, run


@route("/api/v1/submit_xql")
def submit_xql():
    time.sleep(3)
    return {"status": 0}


@route("/api/v1/list_task")
def list_task():
    return {"status": 0}


@route("/api/v1/query_task")
def query_task():
    return {"status": 0}


def make_app(address="0.0.0.0", port=8123):
    run(host=address, port=int(port))


make_app()
