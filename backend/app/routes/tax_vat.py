from flask import request, jsonify
from app import db
from app.models.tax_vat import VATRate, VATReturn
from app.routes import invoice_bp
from datetime import datetime

@invoice_bp.route('/tax/vat-rates', methods=['GET'])
def get_vat_rates():
    rates = VATRate.query.filter_by(is_active=True).all()
    return jsonify([r.to_dict() for r in rates]), 200

@invoice_bp.route('/tax/vat-rates', methods=['POST'])
def create_vat_rate():
    data = request.get_json()
    
    required = ['name', 'rate']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    vat_rate = VATRate(
        name=data['name'],
        rate=data['rate'],
        country=data.get('country')
    )
    
    db.session.add(vat_rate)
    db.session.commit()
    
    return jsonify(vat_rate.to_dict()), 201

@invoice_bp.route('/tax/vat-returns', methods=['POST'])
def create_vat_return():
    data = request.get_json()
    
    required = ['period_start', 'period_end']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    vat_return = VATReturn(
        period_start=datetime.fromisoformat(data['period_start']),
        period_end=datetime.fromisoformat(data['period_end']),
        total_sales=data.get('total_sales', 0),
        vat_on_sales=data.get('vat_on_sales', 0),
        total_purchases=data.get('total_purchases', 0),
        vat_on_purchases=data.get('vat_on_purchases', 0),
        net_vat=data.get('net_vat', 0),
        status='draft'
    )
    
    db.session.add(vat_return)
    db.session.commit()
    
    return jsonify(vat_return.to_dict()), 201

@invoice_bp.route('/tax/vat-returns', methods=['GET'])
def get_vat_returns():
    returns = VATReturn.query.all()
    return jsonify([r.to_dict() for r in returns]), 200

@invoice_bp.route('/tax/vat-returns/<int:return_id>/submit', methods=['POST'])
def submit_vat_return(return_id):
    vat_return = VATReturn.query.get(return_id)
    if not vat_return:
        return jsonify({'error': 'VAT return not found'}), 404
    
    vat_return.status = 'submitted'
    db.session.commit()
    
    return jsonify(vat_return.to_dict()), 200
