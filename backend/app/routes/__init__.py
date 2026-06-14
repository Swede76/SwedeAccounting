from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
invoice_bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')
bookkeeping_bp = Blueprint('bookkeeping', __name__, url_prefix='/api/bookkeeping')
reporting_bp = Blueprint('reporting', __name__, url_prefix='/api/reporting')

from app.routes import auth, invoices, bookkeeping, reporting
