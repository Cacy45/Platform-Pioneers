"""from flask import render_template, request
from models import Complaint

def register_routes(app,db):
    @app.route('/')
    def index():
        complaint = Complaint.query.all()
        return str(complaint)
"""