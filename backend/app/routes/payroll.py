from flask import request, jsonify
from app import db
from app.models.payroll import Employee, TimeEntry, Payslip
from datetime import datetime, timedelta
from app.routes import invoice_bp

payroll_bp = None  # Will be created in init

@invoice_bp.route('/payroll/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.filter_by(is_active=True).all()
    return jsonify([emp.to_dict() for emp in employees]), 200

@invoice_bp.route('/payroll/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    
    required = ['first_name', 'last_name', 'salary', 'hire_date']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data.get('email'),
        phone=data.get('phone'),
        employment_type=data.get('employment_type', 'full_time'),
        salary=data['salary'],
        currency=data.get('currency', 'USD'),
        tax_id=data.get('tax_id'),
        bank_account=data.get('bank_account'),
        hire_date=datetime.fromisoformat(data['hire_date'])
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify(employee.to_dict()), 201

@invoice_bp.route('/payroll/time-entries', methods=['POST'])
def create_time_entry():
    data = request.get_json()
    
    required = ['employee_id', 'date', 'hours_worked']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    time_entry = TimeEntry(
        employee_id=data['employee_id'],
        date=datetime.fromisoformat(data['date']),
        hours_worked=data['hours_worked'],
        overtime_hours=data.get('overtime_hours', 0),
        description=data.get('description')
    )
    
    db.session.add(time_entry)
    db.session.commit()
    
    return jsonify(time_entry.to_dict()), 201

@invoice_bp.route('/payroll/payslips', methods=['POST'])
def generate_payslip():
    data = request.get_json()
    
    required = ['employee_id', 'pay_period_start', 'pay_period_end']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    employee = Employee.query.get(data['employee_id'])
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    pay_start = datetime.fromisoformat(data['pay_period_start'])
    pay_end = datetime.fromisoformat(data['pay_period_end'])
    
    # Calculate gross salary
    time_entries = TimeEntry.query.filter(
        TimeEntry.employee_id == employee.id,
        TimeEntry.date >= pay_start,
        TimeEntry.date <= pay_end
    ).all()
    
    total_hours = sum(t.hours_worked for t in time_entries)
    hourly_rate = employee.salary / (52 * 40)  # Annual salary / weekly hours
    gross_salary = total_hours * hourly_rate
    
    # Calculate deductions (simplified)
    tax_deduction = gross_salary * 0.20  # 20% tax
    social_security = gross_salary * 0.08  # 8% social security
    net_salary = gross_salary - tax_deduction - social_security
    
    payslip = Payslip(
        employee_id=employee.id,
        pay_period_start=pay_start,
        pay_period_end=pay_end,
        gross_salary=gross_salary,
        tax_deduction=tax_deduction,
        social_security=social_security,
        net_salary=net_salary,
        status='draft'
    )
    
    db.session.add(payslip)
    db.session.commit()
    
    return jsonify(payslip.to_dict()), 201

@invoice_bp.route('/payroll/payslips/<int:payslip_id>/approve', methods=['POST'])
def approve_payslip(payslip_id):
    payslip = Payslip.query.get(payslip_id)
    if not payslip:
        return jsonify({'error': 'Payslip not found'}), 404
    
    payslip.status = 'approved'
    db.session.commit()
    
    return jsonify(payslip.to_dict()), 200

@invoice_bp.route('/payroll/payslips/<int:payslip_id>/pay', methods=['POST'])
def pay_payslip(payslip_id):
    payslip = Payslip.query.get(payslip_id)
    if not payslip:
        return jsonify({'error': 'Payslip not found'}), 404
    
    if payslip.status != 'approved':
        return jsonify({'error': 'Payslip must be approved first'}), 400
    
    payslip.status = 'paid'
    payslip.payment_date = datetime.utcnow()
    db.session.commit()
    
    return jsonify(payslip.to_dict()), 200
