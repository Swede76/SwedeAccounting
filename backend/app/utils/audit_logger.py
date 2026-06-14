from datetime import datetime
import json

def log_audit(user_id, action, resource_type, resource_id, old_values=None, new_values=None, ip_address=None, user_agent=None):
    """Log audit trail for changes"""
    from app import db
    from app.models.audit import AuditLog
    
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.session.add(audit_log)
    db.session.commit()
    
    return audit_log
