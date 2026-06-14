# SwedeAccounting

A comprehensive cloud-based accounting software tool for small and medium-sized businesses. Built with Python backend and HTML/CSS/JavaScript frontend.

## Features

### Core Modules
- **Invoicing** - Create, send, and track invoices
- **Bookkeeping** - Automated ledger management and transaction tracking
- **Accounts Payable** - Manage supplier invoices and payments
- **Reporting** - Financial reports, dashboards, and analytics
- **Inventory Management** - Stock tracking and valuation
- **Payroll** - Employee salary and time tracking
- **Project Management** - Cost tracking and budgeting

## Project Structure

```
SwedeAccounting/
├── backend/              # Python backend (Flask/FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/       # Database models
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   └── utils/        # Helper functions
│   ├── migrations/       # Database migrations
│   ├── tests/            # Unit tests
│   ├── requirements.txt  # Python dependencies
│   └── config.py         # Configuration
├── frontend/             # HTML/CSS/JavaScript frontend
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── docs/                 # Documentation
└── .gitignore
```

## Getting Started

### Backend Setup
1. Navigate to `backend/` directory
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python app/main.py`

### Frontend Setup
1. Open `frontend/index.html` in your browser or serve with a local server

## Tech Stack
- **Backend**: Python (Flask/FastAPI)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: PostgreSQL (recommended)
- **API**: RESTful API

## License
MIT

## Author
Swede76
