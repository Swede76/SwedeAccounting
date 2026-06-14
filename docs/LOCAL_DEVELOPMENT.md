# SwedeAccounting - Local Development Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Git
- Code editor (VS Code, PyCharm, etc.)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/Swede76/SwedeAccounting.git
cd SwedeAccounting
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE swedeaccounting_dev;
\q

# Copy environment file
cp ../.env.example .env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://postgres:password@localhost:5432/swedeaccounting_dev
```

### 4. Run Backend

```bash
# From backend directory
python app/main.py
```

Backend runs on `http://localhost:5000`

Test it:
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", "service": "SwedeAccounting API"}
```

### 5. Setup Frontend

```bash
# From root directory
cd frontend

# Option 1: Use Python server
python -m http.server 8000

# Option 2: Use Node.js http-server
npm install -g http-server
http-server

# Option 3: Use Live Server (VS Code extension)
```

Access at `http://localhost:8000/dashboard.html`

## Development Workflow

### Backend Development

```bash
# Create new model
cat > backend/app/models/new_model.py << 'EOF'
from app import db
from datetime import datetime

class NewModel(db.Model):
    __tablename__ = 'new_models'
    id = db.Column(db.Integer, primary_key=True)
    # Add columns
EOF

# Create new route
cat > backend/app/routes/new_route.py << 'EOF'
from flask import Blueprint

new_bp = Blueprint('new', __name__, url_prefix='/api/new')

@new_bp.route('/', methods=['GET'])
def get_all():
    return {'data': []}, 200
EOF

# Update imports in backend/app/__init__.py
```

### Frontend Development

```bash
# Add new section to dashboard.html
<section id="new-section" class="section">
    <h2>New Feature</h2>
    <div id="content"></div>
</section>

# Add styles to frontend/css/style.css
#new-section {
    /* styles */
}

# Add JavaScript to frontend/js/main.js
function loadNewFeature() {
    // implementation
}
```

## Testing

### Test Backend

```bash
# Test API endpoint
curl -X GET http://localhost:5000/api/bookkeeping/accounts

# Test with data
curl -X POST http://localhost:5000/api/bookkeeping/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1000",
    "account_name": "Cash",
    "account_type": "Asset"
  }'
```

### Test Frontend

1. Open browser console (F12)
2. Check Network tab for API calls
3. Test dashboard responsiveness
4. Verify chart rendering

## Useful Commands

### Database

```bash
# Connect to PostgreSQL
psql -U postgres -d swedeaccounting_dev

# List tables
\dt

# View table schema
\d users

# Exit
\q
```

### Git

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "feat: add new feature"

# Push to GitHub
git push origin main

# Create new branch
git checkout -b feature/new-feature
```

### Virtual Environment

```bash
# Deactivate virtual environment
deactivate

# Reactivate
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Freeze requirements
pip freeze > requirements.txt
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
FLASK_APP=app/main.py FLASK_ENV=development python -m flask run --port 5001
```

### Database Connection Error

```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
echo $DATABASE_URL

# Test connection
psql -h localhost -U postgres -d swedeaccounting_dev
```

### Module Not Found

```bash
# Verify virtual environment is activated
which python  # Should show path to venv

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Issues

Update `.env`:
```
CORS_ORIGINS=http://localhost:8000,http://localhost:3000
```

## IDE Setup

### VS Code

1. Install extensions:
   - Python
   - Pylance
   - Thunder Client (for API testing)
   - Live Server

2. Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

### PyCharm

1. Open project
2. Set Python interpreter: Preferences → Project → Python Interpreter
3. Select `backend/venv/bin/python`
4. Mark `frontend` as Resource Root

## Next Steps

1. Explore codebase
2. Make a change
3. Test locally
4. Commit and push
5. Deploy to production

Happy coding! 🚀
