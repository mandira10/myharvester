from flask import Blueprint


myharvester = Blueprint(
    "myharvester", __name__)


def page():
    return "Hello, myharvester!"


myharvester.add_url_rule(
    "/myharvester/page", view_func=page)


def get_blueprints():
    return [myharvester]
