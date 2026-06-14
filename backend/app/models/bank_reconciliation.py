from app import db
from datetime import datetime
from enum import Enum

class BankTransactionType(Enum):
    DEBIT = 'debit'
    CREDIT = 'credit'

class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(120), nullable=False)
    account_number = db.Column(db.String(50), unique=True, nullable=False)
    bank_name = db.Column(db.String(120), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    balance = db.Column(db.Float, default=0.0)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    transactions = db.relationship('BankTransaction', backref='bank_account', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_name': self.account_name,
            'account_number': self.account_number,
            'bank_name': self.bank_name,
            'currency': self.currency,
            'balance': self.balance,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }

class BankTransaction(db.Model):
    __tablename__ = 'bank_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable=False)
    
    transaction_date = db.Column(db.DateTime, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # debit, credit
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    reference_number = db.Column(db.String(50))
    
    is_reconciled = db.Column(db.Boolean, default=False)
    reconciled_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'bank_account_id': self.bank_account_id,
            'transaction_date': self.transaction_date.isoformat(),
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'reference_number': self.reference_number,
            'is_reconciled': self.is_reconciled,
            'reconciled_at': self.reconciled_at.isoformat() if self.reconciled_at else None,
        }
