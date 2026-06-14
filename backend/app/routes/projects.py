from flask import request, jsonify
from app import db
from app.models.project import Project, ProjectCost, ProjectInvoice
from app.routes import invoice_bp
from datetime import datetime

@invoice_bp.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects]), 200

@invoice_bp.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    
    required = ['project_name', 'start_date', 'budgeted_amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    project = Project(
        project_name=data['project_name'],
        description=data.get('description'),
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        budgeted_amount=data['budgeted_amount'],
        status=data.get('status', 'active')
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@invoice_bp.route('/projects/<int:project_id>/costs', methods=['POST'])
def add_project_cost(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    data = request.get_json()
    
    required = ['cost_description', 'cost_type', 'amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    project_cost = ProjectCost(
        project_id=project_id,
        cost_description=data['cost_description'],
        cost_type=data['cost_type'],
        amount=data['amount'],
        reference=data.get('reference')
    )
    
    project.spent_amount += data['amount']
    
    db.session.add(project_cost)
    db.session.commit()
    
    return jsonify(project_cost.to_dict()), 201

@invoice_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project_dict = project.to_dict()
    project_dict['costs'] = [c.to_dict() for c in project.project_costs]
    
    return jsonify(project_dict), 200

@invoice_bp.route('/projects/<int:project_id>/attach-invoice/<int:invoice_id>', methods=['POST'])
def attach_invoice_to_project(project_id, invoice_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    project_invoice = ProjectInvoice(
        project_id=project_id,
        invoice_id=invoice_id
    )
    
    db.session.add(project_invoice)
    db.session.commit()
    
    return jsonify({'message': 'Invoice attached to project'}), 201
