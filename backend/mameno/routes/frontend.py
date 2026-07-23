from flask import Blueprint,send_from_directory
import os

frontend_bp = Blueprint('frontend', __name__,static_folder="../dist")

@frontend_bp.route('/version')
def version():
    return "0.0.1",200

@frontend_bp.route("/", defaults={"path": ""})
@frontend_bp.route("/<path:path>")
def index(path):
    static_folder = frontend_bp.static_folder

    if path and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)

    return send_from_directory(static_folder, "index.html")