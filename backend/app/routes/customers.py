from flask import request, jsonify
from app import db
from app.models.customer import Customer
from app.routes import invoice_bp

@invoice_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.filter_by(is_active=True).all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@invoice_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Customer name required'}), 400
    
    if Customer.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    customer = Customer(
        name=data['name'],
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        city=data.get('city'),
        postal_code=data.get('postal_code'),
        country=data.get('country'),
        tax_id=data.get('tax_id'),
        company_name=data.get('company_name')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify(customer.to_dict()), 201

@invoice_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict()), 200

@invoice_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    
    for key in ['name', 'email', 'phone', 'address', 'city', 'postal_code', 'country', 'tax_id', 'company_name']:
        if key in data:
            setattr(customer, key, data[key])
    
    db.session.commit()
    return jsonify(customer.to_dict()), 200

@invoice_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    customer.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Customer deleted'}), 200
