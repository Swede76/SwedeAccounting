# SwedeAccounting Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Heroku (Recommended - Easiest)

**Step 1: Prepare**
```bash
# Make sure you have Heroku CLI installed
# Download from: https://devcenter.heroku.com/articles/heroku-cli

heroku login
```

**Step 2: Create & Configure**
```bash
# Create new Heroku app
heroku create swedeaccounting-your-name

# Add PostgreSQL database (free hobby tier)
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32)
heroku config:set FLASK_ENV=production
```

**Step 3: Deploy**
```bash
# Deploy code
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

### Option 2: Railway.app (Free Tier)

1. Sign up at https://railway.app (free tier available)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add PostgreSQL database service
5. Set environment variables in Railway dashboard:
   - `DATABASE_URL` - Auto-generated when you add PostgreSQL
   - `SECRET_KEY` - Generate with: `openssl rand -hex 32`
   - `JWT_SECRET_KEY` - Generate with: `openssl rand -hex 32`
   - `FLASK_ENV=production`
6. Deploy automatically on every push!

### Option 3: PythonAnywhere (Free)

1. Sign up at https://www.pythonanywhere.com
2. Upload your code via Git
3. Create virtual environment
4. Install requirements
5. Create web app pointing to Flask app
6. Configure database connection
7. Reload web app

### Option 4: Docker + Deploy Anywhere

```bash
# Build Docker image
docker build -t swedeaccounting .

# Run locally
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  swedeaccounting

# Push to Docker Hub
docker tag swedeaccounting yourusername/swedeaccounting
docker push yourusername/swedeaccounting

# Deploy on services like:
# - AWS EC2
# - Google Cloud Run
# - Azure Container Instances
# - DigitalOcean App Platform
```

## 📋 Pre-Deployment Checklist

- [ ] All code committed to Git
- [ ] `.env` configured with production values
- [ ] Database URL configured
- [ ] Secret keys generated (min 32 chars)
- [ ] Backend requirements updated
- [ ] Frontend built/optimized
- [ ] No hardcoded secrets in code
- [ ] Error handling configured
- [ ] Logging configured
- [ ] CORS configured for your domain

## 🔒 Security Best Practices

### Generate Secure Keys

```bash
# On Mac/Linux:
openssl rand -hex 32

# On Windows (PowerShell):
[System.Convert]::ToBase64String((1..32|ForEach-Object{Get-Random -Max 256}))
```

### Environment Variables (Never commit these!)

1. Keep `.env` in `.gitignore`
2. Set in deployment platform:
   - Heroku: `heroku config:set KEY=value`
   - Railway: Dashboard UI
   - Docker: `docker run -e KEY=value`

### Database Security

- Use strong PostgreSQL password
- Use SSL connection if available
- Regular backups
- Monitor access logs

## 🗄️ Database Setup

### Automatic (Recommended)

Database tables created automatically on first run via `db.create_all()`

### Manual Migration

```bash
# Connect to your database
psql -h host -U user -d database

# Tables are auto-created on application start
```

## 🔍 Monitoring & Logs

### Heroku
```bash
# View logs
heroku logs --tail

# View specific error
heroku logs --tail --filter error
```

### Railway
- Logs visible in dashboard
- Real-time monitoring
- Error tracking

### Docker
```bash
docker logs -f container_id
```

## 🚨 Troubleshooting

### Database Connection Failed
```bash
# Check DATABASE_URL format
# Should be: postgresql://user:password@host:port/database

# Verify credentials
psql -h host -U user -d database
```

### Port Already in Use
```bash
# On Linux/Mac:
lsof -i :5000
kill -9 PID

# On Windows:
netstat -ano | findstr :5000
taskkill /PID process_id /F
```

### Module Not Found
```bash
# Reinstall requirements
pip install -r backend/requirements.txt
```

### CORS Issues
```bash
# Update CORS_ORIGINS in .env
# Include your deployed frontend URL
CORS_ORIGINS=https://yourdomain.com
```

## 📊 Performance Tips

1. **Enable compression**: Heroku does this automatically
2. **Optimize database queries**: Add indexes
3. **Cache responses**: Consider Redis for caching
4. **CDN for static files**: Use CloudFlare
5. **Monitor performance**: Use Heroku dashboard

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "swedeaccounting-your-name"
          heroku_email: "your-email@gmail.com"
```

## 📈 Scaling

### Heroku Scaling
```bash
# View current dynos
heroku ps

# Scale web dynos
heroku ps:scale web=2

# Scale worker dynos
heroku ps:scale worker=1
```

## 🆘 Support

- **Heroku Docs**: https://devcenter.heroku.com
- **Railway Docs**: https://docs.railway.app
- **Flask Docs**: https://flask.palletsprojects.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs

## ✅ Deployment Complete!

Your SwedeAccounting application is now live! 🎉

- Access at: `https://swedeaccounting-your-name.herokuapp.com`
- API at: `https://swedeaccounting-your-name.herokuapp.com/api`
- Dashboard at: `https://swedeaccounting-your-name.herokuapp.com/static/dashboard.html`

### Next Steps:

1. Test all features
2. Set up custom domain
3. Enable HTTPS
4. Configure monitoring
5. Set up automated backups
6. Document for team
