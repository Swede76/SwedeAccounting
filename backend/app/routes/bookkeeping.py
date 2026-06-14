from flask import request, jsonify
from app import db
from app.models.transaction import Account, Transaction
from app.routes import bookkeeping_bp

@bookkeeping_bp.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([account.to_dict() for account in accounts]), 200

@bookkeeping_bp.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    
    if not data or not data.get('account_number') or not data.get('account_name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    account = Account(
        account_number=data['account_number'],
        account_name=data['account_name'],
        account_type=data.get('account_type', 'Asset')
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify(account.to_dict()), 201

@bookkeeping_bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200

@bookkeeping_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['debit_account_id', 'credit_account_id', 'amount']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    transaction = Transaction(
        debit_account_id=data['debit_account_id'],
        credit_account_id=data['credit_account_id'],
        amount=data['amount'],
        description=data.get('description'),
        reference=data.get('reference')
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify(transaction.to_dict()), 201
