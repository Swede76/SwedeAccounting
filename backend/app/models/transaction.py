from app import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(10), unique=True, nullable=False)
    account_name = db.Column(db.String(120), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    balance = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'balance': self.balance,
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    debit_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    credit_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    reference = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'debit_account_id': self.debit_account_id,
            'credit_account_id': self.credit_account_id,
            'amount': self.amount,
            'description': self.description,
            'transaction_date': self.transaction_date.isoformat(),
            'reference': self.reference,
        }
