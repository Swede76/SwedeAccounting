from app import db
from datetime import datetime

class VATRate(db.Model):
    __tablename__ = 'vat_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rate = db.Column(db.Float, nullable=False)  # e.g., 0.25 for 25%
    country = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rate': self.rate,
            'country': self.country,
            'is_active': self.is_active,
        }

class VATReturn(db.Model):
    __tablename__ = 'vat_returns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    total_sales = db.Column(db.Float, default=0.0)
    vat_on_sales = db.Column(db.Float, default=0.0)
    
    total_purchases = db.Column(db.Float, default=0.0)
    vat_on_purchases = db.Column(db.Float, default=0.0)
    
    net_vat = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # draft, submitted, approved
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'total_sales': self.total_sales,
            'vat_on_sales': self.vat_on_sales,
            'total_purchases': self.total_purchases,
            'vat_on_purchases': self.vat_on_purchases,
            'net_vat': self.net_vat,
            'status': self.status,
        }
