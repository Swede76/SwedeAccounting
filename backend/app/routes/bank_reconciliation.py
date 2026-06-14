from flask import request, jsonify
from app import db
from app.models.bank_reconciliation import BankAccount, BankTransaction
from app.routes import invoice_bp
from datetime import datetime

@invoice_bp.route('/bank/accounts', methods=['GET'])
def get_bank_accounts():
    accounts = BankAccount.query.filter_by(is_active=True).all()
    return jsonify([acc.to_dict() for acc in accounts]), 200

@invoice_bp.route('/bank/accounts', methods=['POST'])
def create_bank_account():
    data = request.get_json()
    
    required = ['account_name', 'account_number', 'bank_name']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if BankAccount.query.filter_by(account_number=data['account_number']).first():
        return jsonify({'error': 'Account number already exists'}), 400
    
    bank_account = BankAccount(
        account_name=data['account_name'],
        account_number=data['account_number'],
        bank_name=data['bank_name'],
        currency=data.get('currency', 'USD'),
        balance=data.get('balance', 0.0)
    )
    
    db.session.add(bank_account)
    db.session.commit()
    
    return jsonify(bank_account.to_dict()), 201

@invoice_bp.route('/bank/transactions', methods=['POST'])
def record_bank_transaction():
    data = request.get_json()
    
    required = ['bank_account_id', 'transaction_date', 'transaction_type', 'amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    bank_account = BankAccount.query.get(data['bank_account_id'])
    if not bank_account:
        return jsonify({'error': 'Bank account not found'}), 404
    
    # Update bank balance
    if data['transaction_type'] == 'credit':
        bank_account.balance += data['amount']
    elif data['transaction_type'] == 'debit':
        bank_account.balance -= data['amount']
    
    transaction = BankTransaction(
        bank_account_id=data['bank_account_id'],
        transaction_date=datetime.fromisoformat(data['transaction_date']),
        transaction_type=data['transaction_type'],
        amount=data['amount'],
        description=data.get('description'),
        reference_number=data.get('reference_number')
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 201

@invoice_bp.route('/bank/reconcile/<int:transaction_id>', methods=['POST'])
def reconcile_transaction(transaction_id):
    transaction = BankTransaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    transaction.is_reconciled = True
    transaction.reconciled_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 200

@invoice_bp.route('/bank/accounts/<int:account_id>/unreconciled', methods=['GET'])
def get_unreconciled_transactions(account_id):
    transactions = BankTransaction.query.filter_by(
        bank_account_id=account_id,
        is_reconciled=False
    ).all()
    return jsonify([t.to_dict() for t in transactions]), 200
