#from flask_sqlalchemy import SQLAlchemy
#from extensions import db  # Instead of defining db again
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy
#db = SQLAlchemy()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student', 'admin', 'supervisor'

    student = db.relationship('Student', backref='user', uselist=False)
    admin = db.relationship('Admin', backref='user', uselist=False)
    supervisor = db.relationship('Supervisor', backref='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(200), nullable=False, unique=True)
    
    admins = db.relationship('Admin', backref='department', lazy=True)
    supervisors = db.relationship('Supervisor', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.dept_name}>'

class Student(db.Model):
    stud_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    complaints = db.relationship('Complaint', backref='student', lazy=True)
    appeal = db.relationship('Appeal', backref='student', uselist=False, lazy=True)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=False)
    superv_id = db.Column(db.Integer, db.ForeignKey('supervisor.superv_id'), nullable=True)

    complaints = db.relationship('Complaint', backref='admin', lazy=True)
    appeals = db.relationship('Appeal', backref='admin', lazy=True)

class Supervisor(db.Model):
    superv_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=False)
    
    complaints = db.relationship('Complaint', backref='supervisor', lazy=True)
    appeals = db.relationship('Appeal', backref='supervisor', lazy=True)

class Complaint(db.Model):
    comp_id = db.Column(db.Integer, primary_key=True)
    comp_datefiled = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    comp_descr = db.Column(db.String(500), nullable=False)
    comp_status = db.Column(db.String(100), default='Pending')
    comp_dept=db.Column(db.String(200), nullable=False)
    comp_anonymous = db.Column(db.Boolean, default=False)
    comp_dateresolved = db.Column(db.DateTime, nullable=True)
    comp_doc = db.Column(db.String(300), nullable=True)  # Stores filename of uploaded document
    
    stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=True)
    superv_id = db.Column(db.Integer, db.ForeignKey('supervisor.superv_id'), nullable=True)
    
    appeal = db.relationship('Appeal', backref='complaint', uselist=False, lazy=True)

class Appeal(db.Model):
    appeal_id = db.Column(db.Integer, primary_key=True)
    appeal_datefiled = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    appeal_reason = db.Column(db.String(500), nullable=False)
    appeal_status = db.Column(db.String(100), default='Pending')
    appeal_dateresolved = db.Column(db.DateTime, nullable=True)
    appeal_doc = db.Column(db.String(300), nullable=True)  # Stores filename of uploaded document
    
    comp_id = db.Column(db.Integer, db.ForeignKey('complaint.comp_id'), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=True)
    superv_id = db.Column(db.Integer, db.ForeignKey('supervisor.superv_id'), nullable=True)
    stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'), nullable=False)
