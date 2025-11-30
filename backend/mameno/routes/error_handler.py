from flask import Blueprint,redirect
import os


error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def page_not_found(e):
    frontend_url = os.getenv("FRONTEND_URL")
    return redirect(frontend_url)  