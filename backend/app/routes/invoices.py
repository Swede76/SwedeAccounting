from flask import request, jsonify
from app import db
from app.models.invoice import Invoice, InvoiceLine
from app.routes import invoice_bp

@invoice_bp.route('/', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([invoice.to_dict() for invoice in invoices]), 200

@invoice_bp.route('/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    return jsonify(invoice.to_dict()), 200

@invoice_bp.route('/', methods=['POST'])
def create_invoice():
    data = request.get_json()
    
    if not data or not data.get('invoice_number') or not data.get('customer_id'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    invoice = Invoice(
        invoice_number=data['invoice_number'],
        customer_id=data['customer_id'],
        user_id=data.get('user_id', 1),  # TODO: Get from auth
        notes=data.get('notes')
    )
    
    db.session.add(invoice)
    db.session.commit()
    
    return jsonify(invoice.to_dict()), 201
