from flask import Flask
from flask import Response
from flask import Blueprint

webpack_bp = Blueprint("webpack",__name__)

@webpack_bp.route("/")
def webpack_index():
    return open("static/website/dist/index.html","r",encoding="utf-8").read()

@webpack_bp.route("/css/<file>")
def webpack_css(file):
    return Response(open("static/website/dist/css/" + file,"r",encoding="utf-8").read(),content_type="text/css")

@webpack_bp.route("/js/<file>")
def webpack_js(file):
    return Response(open("static/website/dist/js/" + file,"r",encoding="utf-8").read(),content_type="application/javascript")