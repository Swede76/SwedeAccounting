from app import db
from datetime import datetime
from enum import Enum

class EmploymentType(Enum):
    FULL_TIME = 'full_time'
    PART_TIME = 'part_time'
    CONTRACT = 'contract'
    TEMPORARY = 'temporary'

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    
    employment_type = db.Column(db.String(20), default=EmploymentType.FULL_TIME.value)
    salary = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    tax_id = db.Column(db.String(50))
    bank_account = db.Column(db.String(100))
    
    hire_date = db.Column(db.DateTime, nullable=False)
    termination_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    payslips = db.relationship('Payslip', backref='employee', lazy=True)
    time_entries = db.relationship('TimeEntry', backref='employee', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'employment_type': self.employment_type,
            'salary': self.salary,
            'currency': self.currency,
            'hire_date': self.hire_date.isoformat(),
            'termination_date': self.termination_date.isoformat() if self.termination_date else None,
            'is_active': self.is_active,
        }

class TimeEntry(db.Model):
    __tablename__ = 'time_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    date = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    overtime_hours = db.Column(db.Float, default=0.0)
    description = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat(),
            'hours_worked': self.hours_worked,
            'overtime_hours': self.overtime_hours,
            'description': self.description,
        }

class Payslip(db.Model):
    __tablename__ = 'payslips'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    pay_period_start = db.Column(db.DateTime, nullable=False)
    pay_period_end = db.Column(db.DateTime, nullable=False)
    
    gross_salary = db.Column(db.Float, nullable=False)
    tax_deduction = db.Column(db.Float, default=0.0)
    social_security = db.Column(db.Float, default=0.0)
    other_deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    
    payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, approved, paid
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'pay_period_start': self.pay_period_start.isoformat(),
            'pay_period_end': self.pay_period_end.isoformat(),
            'gross_salary': self.gross_salary,
            'tax_deduction': self.tax_deduction,
            'social_security': self.social_security,
            'other_deductions': self.other_deductions,
            'net_salary': self.net_salary,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'status': self.status,
        }
