from app import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    
    budgeted_amount = db.Column(db.Float, nullable=False)
    spent_amount = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='active')  # active, completed, on_hold
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project_costs = db.relationship('ProjectCost', backref='project', lazy=True, cascade='all, delete-orphan')
    project_invoices = db.relationship('ProjectInvoice', backref='project', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_name': self.project_name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'budgeted_amount': self.budgeted_amount,
            'spent_amount': self.spent_amount,
            'remaining_budget': self.budgeted_amount - self.spent_amount,
            'status': self.status,
        }

class ProjectCost(db.Model):
    __tablename__ = 'project_costs'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    cost_description = db.Column(db.String(255), nullable=False)
    cost_type = db.Column(db.String(50), nullable=False)  # labor, material, equipment, etc
    amount = db.Column(db.Float, nullable=False)
    
    date = db.Column(db.DateTime, default=datetime.utcnow)
    reference = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'cost_description': self.cost_description,
            'cost_type': self.cost_type,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'reference': self.reference,
        }

class ProjectInvoice(db.Model):
    __tablename__ = 'project_invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoice = db.relationship('Invoice', backref='project_invoices')
