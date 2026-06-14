# SwedeAccounting - Full Accounting Suite
## Deployed & Production Ready 🚀

### Live Demo
- **Frontend**: [Access Dashboard](#) (deploy URL will be here)
- **API**: [API Documentation](#) (deploy URL will be here)

## Features ✨

### Core Modules
- ✅ **Invoicing** - Create, send, and track invoices
- ✅ **Bookkeeping** - Automated ledger management and transactions
- ✅ **Accounts Payable** - Manage supplier invoices
- ✅ **Reporting** - Financial reports and dashboards
- ✅ **Inventory Management** - Stock tracking
- ✅ **Payroll** - Employee salary management
- ✅ **Project Management** - Cost tracking and budgeting
- ✅ **Tax & VAT** - VAT management and returns
- ✅ **Bank Reconciliation** - Bank account reconciliation
- ✅ **Audit Logging** - Complete audit trail

### Dashboard Features
- 📊 Real-time income vs expense charts
- 💰 Account balance visualization
- 🏦 Bank account summary
- 📈 Financial metrics and KPIs
- 🎨 Professional gradient design
- ⚡ Smooth animations
- 📱 Fully responsive

## Tech Stack

**Backend:**
- Python 3.11
- Flask 2.3
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- Flask-CORS

**Frontend:**
- HTML5
- CSS3 (with gradients & animations)
- JavaScript (Vanilla)
- Chart.js for visualizations

## Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/Swede76/SwedeAccounting.git
cd SwedeAccounting

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your database credentials

# Run migrations and start server
python app/main.py
```

The backend will be available at `http://localhost:5000`

### Frontend

```bash
# Open in browser
open frontend/dashboard.html
# Or serve with a local server
python -m http.server 8000
```

Access at `http://localhost:8000/frontend/dashboard.html`

## Deployment

### Heroku (Recommended - Free Tier)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create swedeaccounting-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# Open app
heroku open
```

### Railway.app (Free Tier)

1. Sign up at [railway.app](https://railway.app)
2. Connect GitHub repository
3. Add PostgreSQL database
4. Set environment variables
5. Deploy automatically on push

### PythonAnywhere (Free)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload code
3. Configure virtual environment
4. Set up web app
5. Configure database

### Docker Deployment

```bash
# Build image
docker build -t swedeaccounting .

# Run container
docker run -p 5000:5000 -e DATABASE_URL=postgresql://... swedeaccounting
```

## Environment Variables

Create `.env` file:

```env
# Flask
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=postgresql://user:password@host:5432/swedeaccounting

# Server
PORT=5000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - User login

### Invoices
- `GET /api/invoices/` - List invoices
- `POST /api/invoices/` - Create invoice
- `GET /api/invoices/{id}` - Get invoice
- `GET /api/invoices/customers` - List customers
- `POST /api/invoices/customers` - Create customer

### Bookkeeping
- `GET /api/bookkeeping/accounts` - List accounts
- `POST /api/bookkeeping/accounts` - Create account
- `GET /api/bookkeeping/transactions` - List transactions
- `POST /api/bookkeeping/transactions` - Create transaction

### Payroll
- `GET /api/invoices/payroll/employees` - List employees
- `POST /api/invoices/payroll/employees` - Create employee
- `POST /api/invoices/payroll/payslips` - Generate payslip

### Bank Reconciliation
- `GET /api/invoices/bank/accounts` - List bank accounts
- `POST /api/invoices/bank/transactions` - Record transaction
- `POST /api/invoices/bank/reconcile/{id}` - Mark reconciled

### Reporting & Dashboard
- `GET /api/reporting/dashboard` - Dashboard summary
- `GET /api/reporting/dashboard/income-expense` - Income vs expense data
- `GET /api/reporting/dashboard/account-balances` - Account balances
- `GET /api/reporting/balance-sheet` - Balance sheet report
- `GET /api/reporting/income-statement` - Income statement

## Project Structure

```
SwedeAccounting/
├── backend/
│   ├── app/
│   │   ├── models/           # Database models
│   │   ├── routes/           # API routes
│   │   ├── utils/            # Helper functions
│   │   ├── __init__.py
│   │   └── main.py
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Python dependencies
│   └── .env.example
├── frontend/
│   ├── dashboard.html        # Main dashboard
│   ├── index.html            # Alternative view
│   ├── css/
│   │   └── style.css         # Styles
│   └── js/
│       ├── dashboard.js      # Dashboard logic
│       ├── main.js           # Utilities
│       └── chart-config.js   # Chart configuration
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── FEATURES_UPDATE.md
│   ├── DASHBOARD_FEATURES.md
│   └── DESIGN_HIGHLIGHTS.md
├── Procfile                  # Heroku config
├── runtime.txt               # Python version
├── .gitignore
├── README.md
└── LICENSE
```

## Database Schema

### Core Tables
- `users` - User accounts
- `customers` - Customer information
- `invoices` - Invoice records
- `invoice_lines` - Invoice items
- `suppliers` - Supplier information
- `supplier_invoices` - Supplier invoices
- `accounts` - Chart of accounts
- `transactions` - Ledger transactions
- `employees` - Employee data
- `payslips` - Payroll records
- `bank_accounts` - Bank account details
- `bank_transactions` - Bank transactions
- `projects` - Project information
- `products` - Product catalog
- `inventory` - Stock levels
- `vat_rates` - VAT configuration
- `audit_logs` - Audit trail

## Design System

### Colors
- Primary: #007bff (Blue)
- Success: #28a745 (Green)
- Danger: #dc3545 (Red)
- Warning: #ffc107 (Yellow)

### Features
- Gradient backgrounds
- Smooth animations (250ms)
- Advanced shadows
- Responsive layout
- Glassmorphism effects
- Accessibility compliant

## Performance

- 60fps animations
- Optimized database queries
- Efficient API responses
- Responsive design
- Mobile-optimized
- Fast load times

## Security

- JWT authentication
- Password hashing (Werkzeug)
- SQL injection prevention (SQLAlchemy ORM)
- CORS protection
- Input validation
- Audit logging

## Contributing

Feel free to fork and contribute! This is an open-source project.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check documentation in `/docs`
2. Review API endpoints
3. Check GitHub Issues

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] PDF report exports
- [ ] Multi-currency support
- [ ] Advanced analytics
- [ ] API webhooks
- [ ] Third-party integrations
- [ ] Dark mode
- [ ] Advanced user permissions
- [ ] Real-time notifications

## Credits

Built with ❤️ by Swede76

---

**Ready to use! 🎉** Start deploying today!
