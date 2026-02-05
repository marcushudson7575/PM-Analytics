# PM Analytics

A full-stack private markets data platform built with React (frontend) and Python/FastAPI (backend).

## 🎯 Project Overview

PM Analytics solves the private markets industry's data opacity problem by capturing, synthesizing, and storing private markets data to create actionable insights for General Partners (GPs) and Limited Partners (LPs).

### Key Features (MVP)
- 📊 Dashboard with KPIs and analytics charts
- 🔍 Search and filter funds by strategy, vintage year, geography
- 📈 Performance metrics (IRR, MOIC, DPI, RVPI, TVPI)
- 📥 Data ingestion (manual entry + CSV upload)
- 🧹 Automated data cleaning with confidence scoring
- ✅ Only displays 100% confidence data

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic

### Frontend
- **Framework**: Next.js 14 + React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Custom SVG visualizations
- **Export**: Static HTML/CSS/JS

### Deployment
- **Frontend**: GitHub Pages (static hosting via GitHub Actions)
- **Backend**: Railway.app (free tier) - for future API integration
- **Database**: Railway PostgreSQL - for future API integration

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+**
   ```bash
   python3 --version
   ```

2. **Node.js 18+**
   ```bash
   node --version
   ```

3. **Docker Desktop** (for local PostgreSQL)
   - Download from: https://www.docker.com/products/docker-desktop
   - Or use a cloud PostgreSQL database (see Alternative Setup below)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default values work for local dev)
   ```

5. **Start PostgreSQL database**

   **Option A: Using Docker (Recommended)**
   ```bash
   cd ..  # Back to project root
   docker-compose up -d
   ```

   **Option B: Using Railway.app (Cloud)**
   - Go to https://railway.app
   - Sign in with GitHub
   - Create new project → Add PostgreSQL
   - Copy the DATABASE_URL
   - Update `backend/.env` with your DATABASE_URL

6. **Run database migrations**
   ```bash
   cd backend
   source venv/bin/activate
   alembic upgrade head
   ```

7. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

   API will be available at: http://localhost:8000
   API docs: http://localhost:8000/api/v1/docs

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

4. **Build for production (static export)**
   ```bash
   npm run build
   ```

   Static files will be generated in the `out` directory

## 📁 Project Structure

```
pm-analytics/
├── backend/                   # Python FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration settings
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── api/v1/           # API routes
│   │   ├── services/         # Business logic
│   │   └── db/               # Database setup
│   ├── alembic/              # Database migrations
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── .env                  # Environment variables
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API clients
│   │   ├── hooks/           # Custom hooks
│   │   ├── store/           # State management
│   │   └── utils/           # Utilities
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
│
├── scripts/                  # Utility scripts
│   └── seed_data.py         # Generate sample data
│
├── docker-compose.yml       # Local PostgreSQL
└── README.md                # This file
```

## 🗄️ Database Schema

### Core Tables
- **funds** - Main fund entity with performance data
- **investments** - Portfolio companies
- **fund_performance** - Time series performance metrics
- **data_sources** - Track scraping sources
- **ingestion_logs** - Data ingestion audit trail
- **data_quality_issues** - Quality monitoring

### Key Features
- UUID primary keys
- Confidence scoring (0.0 to 1.0)
- Audit timestamps (created_at, updated_at)
- Foreign key relationships

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Deploy Backend to Railway

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your pm-analytics repository

3. **Add PostgreSQL**
   - In your project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will auto-generate DATABASE_URL

4. **Configure environment variables**
   - In your backend service settings
   - Add `CORS_ORIGINS=https://yourusername.github.io`

5. **Deploy**
   - Railway will automatically deploy on git push
   - Your API URL: `https://your-project.up.railway.app`

### Deploy Frontend to GitHub Pages

**Automatic Deployment (Recommended)**

The project is configured for automatic deployment via GitHub Actions:

1. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Select "GitHub Actions"

2. **Push to main branch**
   ```bash
   git add .
   git commit -m "Deploy PM Analytics to GitHub Pages"
   git push origin main
   ```

3. **Monitor deployment**
   - Go to the "Actions" tab in your repository
   - Watch the "Deploy PM Analytics to GitHub Pages" workflow
   - Once complete, your site will be live at: `https://yourusername.github.io/PM-Analytics/`

**Manual Deployment (Alternative)**

If you prefer to build and deploy manually:

1. **Build the frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy the `out` directory**
   - The static files in `frontend/out` can be deployed to any static hosting service
   - For GitHub Pages, use the GitHub Actions workflow (recommended)

**Configuration Notes**
- The `next.config.js` is pre-configured with `basePath: '/PM-Analytics'` for GitHub Pages
- The `.github/workflows/deploy.yml` handles automatic builds and deployments
- A `.nojekyll` file is included to ensure proper asset loading on GitHub Pages

## 🛠️ Development

### Running Locally

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Terminal 3 (Database):
```bash
docker-compose up
```

### Creating Database Migrations

After modifying models:
```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Generating Seed Data

```bash
cd backend
source venv/bin/activate
python ../scripts/seed_data.py
```

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### Key Endpoints

- `GET /api/v1/funds` - List funds with filters
- `GET /api/v1/funds/{id}` - Get fund details
- `GET /api/v1/search?q={query}` - Search funds
- `GET /api/v1/analytics/dashboard` - Get dashboard KPIs
- `POST /api/v1/ingest/manual` - Manual data entry (admin)
- `POST /api/v1/ingest/csv` - Bulk CSV upload (admin)

## 🐛 Troubleshooting

### Database Connection Issues

**Error**: `Connection refused` to localhost:5432

**Solutions**:
1. Install Docker Desktop and run `docker-compose up`
2. Or use Railway cloud PostgreSQL (see Backend Setup above)
3. Check if PostgreSQL is running: `docker ps`

### Port Already in Use

**Backend (8000)**:
```bash
lsof -ti:8000 | xargs kill -9
```

**Frontend (5173)**:
```bash
lsof -ti:5173 | xargs kill -9
```

### CORS Errors

Make sure `CORS_ORIGINS` in `backend/.env` includes your frontend URL:
```
CORS_ORIGINS=http://localhost:5173,https://yourusername.github.io
```

## 📚 Next Steps

1. ✅ Set up local development environment
2. ⬜ Create seed data for testing
3. ⬜ Build frontend dashboard components
4. ⬜ Implement search functionality
5. ⬜ Add data ingestion endpoints
6. ⬜ Deploy to Railway + GitHub Pages
7. ⬜ Add web scraping for SEC filings
8. ⬜ Implement PDF export

## 🤝 Contributing

This is a private project. For questions or issues, please contact the project maintainer.

## 📄 License

Private - All Rights Reserved

## 🙋 Support

For setup help:
1. Check the Troubleshooting section above
2. Review the plan document: `.claude/plans/peppy-twirling-marble.md`
3. Check API docs at http://localhost:8000/api/v1/docs

## 💡 Tips

- Use the `/health` endpoint to check if backend is running
- Frontend hot-reloads automatically during development
- Database schema changes require new migrations
- Only 100% confidence data is displayed (critical rule!)

---

**Built with** ❤️ **using FastAPI, React, and PostgreSQL**
