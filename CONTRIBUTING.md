# SwedeAccounting - Contributing Guide

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Git
- Node.js (optional, for frontend tooling)

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/Swede76/SwedeAccounting.git
cd SwedeAccounting

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup environment
cp ../.env.example .env
# Edit .env with your local database URL

# Run backend
python app/main.py
```

Backend runs on `http://localhost:5000`

### Frontend Development

```bash
# Serve frontend files
cd frontend
python -m http.server 8000
```

Access at `http://localhost:8000/dashboard.html`

## Code Style

### Python (Backend)

```python
# Follow PEP 8
# Use type hints where possible
def get_invoice(invoice_id: int) -> Invoice:
    """Get invoice by ID."""
    return Invoice.query.get(invoice_id)

# Use docstrings
class Invoice(db.Model):
    """Invoice model for storing customer invoices."""
    pass
```

### JavaScript (Frontend)

```javascript
// Use camelCase for functions and variables
function updateDashboard() {
    // Implementation
}

// Use const by default
const API_BASE_URL = 'http://localhost:5000/api';

// Add comments for complex logic
// Calculate net income after deductions
const netIncome = revenue - expenses;
```

### CSS

```css
/* Use CSS variables */
:root {
    --primary-color: #007bff;
}

/* Use meaningful class names */
.stat-card {
    /* styles */
}

/* Mobile-first responsive design */
@media (max-width: 768px) {
    /* styles */
}
```

## Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Examples:
- `feat(dashboard): add income vs expense chart`
- `fix(auth): resolve JWT token validation issue`
- `docs(api): update endpoint documentation`

## Testing

### Run Tests

```bash
# Backend tests
cd backend
python -m pytest tests/

# With coverage
python -m pytest --cov=app tests/
```

### Write Tests

```python
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_invoice(app):
    client = app.test_client()
    response = client.post('/api/invoices/', json={
        'invoice_number': 'INV-001',
        'customer_id': 1
    })
    assert response.status_code == 201
```

## Documentation

### Update Docs When:
- Adding new features
- Changing API endpoints
- Modifying database schema
- Adding configuration options

### Documentation Files:
- `README.md` - Overview and quick start
- `docs/API_DOCUMENTATION.md` - API endpoints
- `docs/DEPLOYMENT_GUIDE.md` - Deployment instructions
- `docs/DESIGN_HIGHLIGHTS.md` - Design system

## Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
How to test these changes

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
```

## Project Structure

```
backend/
├── app/
│   ├── models/       # Database models
│   ├── routes/       # API routes
│   ├── utils/        # Helper functions
│   └── __init__.py
├── tests/            # Unit tests
├── requirements.txt
└── config.py

frontend/
├── css/              # Stylesheets
├── js/               # JavaScript files
├── dashboard.html    # Main dashboard
└── index.html        # Alternative view

docs/                 # Documentation
```

## Adding New Features

### Backend Feature

1. Create model in `backend/app/models/`
2. Add routes in `backend/app/routes/`
3. Update `backend/app/__init__.py` imports
4. Write tests in `backend/tests/`
5. Update `docs/API_DOCUMENTATION.md`

### Frontend Feature

1. Add HTML in `frontend/dashboard.html`
2. Add CSS in `frontend/css/style.css`
3. Add JavaScript in `frontend/js/`
4. Test responsiveness
5. Update documentation

## Reporting Issues

### Bug Report Template

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots/Logs
If applicable

## Environment
- OS: 
- Browser: 
- Python Version: 
```

## Feature Requests

Use GitHub Issues with clear description of:
- Use case
- Expected behavior
- Priority
- Acceptance criteria

## Questions?

Join our discussions or open an issue!

---

**Thank you for contributing! 🙏**
