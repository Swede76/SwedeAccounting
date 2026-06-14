from flask import request, jsonify
from app import db
from app.models.invoice import Invoice
from app.models.transaction import Account, Transaction
from app.models.payroll import Payslip
from app.models.bank_reconciliation import BankAccount, BankTransaction
from app.routes import reporting_bp
from datetime import datetime, timedelta
from sqlalchemy import func

@reporting_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get comprehensive dashboard with all key metrics"""
    
    # Get time period (default last 30 days)
    days = request.args.get('days', default=30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total Revenue (from paid invoices)
    revenue = db.session.query(func.sum(Invoice.total_amount)).filter(
        Invoice.status == 'paid',
        Invoice.created_at >= start_date
    ).scalar() or 0.0
    
    # Total Costs (from expenses accounts)
    expenses = db.session.query(func.sum(Account.balance)).filter(
        Account.account_type == 'Expense'
    ).scalar() or 0.0
    
    # Total Payroll Costs
    payroll_costs = db.session.query(func.sum(Payslip.gross_salary)).filter(
        Payslip.status == 'paid',
        Payslip.payment_date >= start_date
    ).scalar() or 0.0
    
    # Outstanding Invoices
    outstanding = db.session.query(func.sum(Invoice.total_amount)).filter(
        Invoice.status.in_(['sent', 'overdue']),
        Invoice.created_at >= start_date
    ).scalar() or 0.0
    
    # Pending Bills
    pending_bills = db.session.query(func.sum(BankTransaction.amount)).filter(
        BankTransaction.transaction_type == 'debit',
        BankTransaction.is_reconciled == False,
        BankTransaction.created_at >= start_date
    ).scalar() or 0.0
    
    # Account Balance (from all asset accounts)
    account_balance = db.session.query(func.sum(Account.balance)).filter(
        Account.account_type == 'Asset'
    ).scalar() or 0.0
    
    # Bank Balance
    bank_balance = db.session.query(func.sum(BankAccount.balance)).scalar() or 0.0
    
    # Net Income
    net_income = revenue - expenses - payroll_costs
    
    return jsonify({
        'summary': {
            'total_revenue': round(revenue, 2),
            'total_expenses': round(expenses, 2),
            'payroll_costs': round(payroll_costs, 2),
            'net_income': round(net_income, 2),
            'outstanding_invoices': round(outstanding, 2),
            'pending_bills': round(pending_bills, 2),
            'account_balance': round(account_balance, 2),
            'bank_balance': round(bank_balance, 2),
        }
    }), 200

@reporting_bp.route('/dashboard/income-expense', methods=['GET'])
def get_income_expense_chart():
    """Get income vs expense data for chart (monthly breakdown)"""
    
    # Get last 12 months
    months = request.args.get('months', default=12, type=int)
    
    data = []
    
    for i in range(months, 0, -1):
        # Calculate month range
        current_date = datetime.utcnow()
        month_start = current_date.replace(day=1) - timedelta(days=current_date.day - 1)
        month_end = month_start + timedelta(days=32)
        month_end = month_end.replace(day=1) - timedelta(days=1)
        
        # Adjust for i months back
        month_start = month_start - timedelta(days=30 * (i - 1))
        month_end = month_end - timedelta(days=30 * (i - 1))
        
        # Get income
        income = db.session.query(func.sum(Invoice.total_amount)).filter(
            Invoice.status == 'paid',
            Invoice.created_at >= month_start,
            Invoice.created_at <= month_end
        ).scalar() or 0.0
        
        # Get expenses
        expenses = db.session.query(func.sum(Account.balance)).filter(
            Account.account_type == 'Expense'
        ).scalar() or 0.0
        
        data.append({
            'month': month_start.strftime('%B %Y'),
            'month_short': month_start.strftime('%b %y'),
            'income': round(income, 2),
            'expenses': round(expenses, 2),
            'net': round(income - expenses, 2)
        })
    
    return jsonify({'data': data}), 200

@reporting_bp.route('/dashboard/account-balances', methods=['GET'])
def get_account_balances():
    """Get current balance for all accounts by type"""
    
    account_types = ['Asset', 'Liability', 'Equity']
    balances = {}
    
    for acc_type in account_types:
        accounts = Account.query.filter_by(account_type=acc_type).all()
        total_balance = sum(a.balance for a in accounts)
        balances[acc_type] = {
            'total': round(total_balance, 2),
            'accounts': [{
                'name': a.account_name,
                'number': a.account_number,
                'balance': round(a.balance, 2)
            } for a in accounts]
        }
    
    return jsonify(balances), 200

@reporting_bp.route('/dashboard/bank-accounts', methods=['GET'])
def get_bank_accounts_summary():
    """Get summary of all bank accounts"""
    
    accounts = BankAccount.query.filter_by(is_active=True).all()
    
    return jsonify({
        'accounts': [{
            'name': a.account_name,
            'bank': a.bank_name,
            'currency': a.currency,
            'balance': round(a.balance, 2)
        } for a in accounts],
        'total_balance': round(sum(a.balance for a in accounts), 2)
    }), 200

@reporting_bp.route('/dashboard/recent-transactions', methods=['GET'])
def get_recent_transactions():
    """Get recent transactions for dashboard"""
    
    limit = request.args.get('limit', default=10, type=int)
    
    # Get recent invoices
    invoices = db.session.query(Invoice).order_by(Invoice.created_at.desc()).limit(limit).all()
    
    transactions = [{
        'type': 'invoice',
        'id': inv.id,
        'description': f"Invoice {inv.invoice_number}",
        'amount': inv.total_amount,
        'status': inv.status,
        'date': inv.created_at.isoformat()
    } for inv in invoices]
    
    return jsonify({'transactions': transactions}), 200

@reporting_bp.route('/dashboard/quick-stats', methods=['GET'])
def get_quick_stats():
    """Get quick statistics for dashboard widgets"""
    
    # Total Customers
    from app.models.customer import Customer
    total_customers = Customer.query.filter_by(is_active=True).count()
    
    # Total Employees
    from app.models.payroll import Employee
    total_employees = Employee.query.filter_by(is_active=True).count()
    
    # Total Projects
    from app.models.project import Project
    total_projects = Project.query.filter_by(status='active').count()
    
    # Total Products
    from app.models.product import Product
    total_products = Product.query.count()
    
    # Overdue Invoices
    overdue_count = Invoice.query.filter_by(status='overdue').count()
    overdue_amount = db.session.query(func.sum(Invoice.total_amount)).filter(
        Invoice.status == 'overdue'
    ).scalar() or 0.0
    
    return jsonify({
        'total_customers': total_customers,
        'total_employees': total_employees,
        'total_projects': total_projects,
        'total_products': total_products,
        'overdue_invoices': overdue_count,
        'overdue_amount': round(overdue_amount, 2)
    }), 200
