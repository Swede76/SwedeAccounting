from flask import request, jsonify
from app import db
from app.models.transaction import Account
from app.routes import reporting_bp

@reporting_bp.route('/balance-sheet', methods=['GET'])
def balance_sheet():
    """Generate balance sheet report"""
    assets = Account.query.filter_by(account_type='Asset').all()
    liabilities = Account.query.filter_by(account_type='Liability').all()
    equity = Account.query.filter_by(account_type='Equity').all()
    
    total_assets = sum(a.balance for a in assets)
    total_liabilities = sum(l.balance for l in liabilities)
    total_equity = sum(e.balance for e in equity)
    
    return jsonify({
        'assets': [a.to_dict() for a in assets],
        'liabilities': [l.to_dict() for l in liabilities],
        'equity': [e.to_dict() for e in equity],
        'totals': {
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity
        }
    }), 200

@reporting_bp.route('/income-statement', methods=['GET'])
def income_statement():
    """Generate income statement report"""
    revenues = Account.query.filter_by(account_type='Revenue').all()
    expenses = Account.query.filter_by(account_type='Expense').all()
    
    total_revenue = sum(r.balance for r in revenues)
    total_expenses = sum(e.balance for e in expenses)
    net_income = total_revenue - total_expenses
    
    return jsonify({
        'revenues': [r.to_dict() for r in revenues],
        'expenses': [e.to_dict() for e in expenses],
        'totals': {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income
        }
    }), 200
