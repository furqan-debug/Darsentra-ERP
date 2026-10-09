# Darsentra ERP

> **Modern, Multi-Tenant School Management SaaS Platform for Pakistani Schools**

Darsentra ERP is an enterprise-grade School Management SaaS engineered from the ground up for K-12 schools, colleges, and higher secondary systems across Pakistan (Matric/FSc, Cambridge O/A Levels, Federal Board, and provincial curricula).

---

## Architecture Highlights

- **Backend**: Python 3.12+ / Django 5.1 / Django REST Framework
- **Frontend**: React 18 / TypeScript / Vite / Tailwind CSS / shadcn/ui
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose
- **Tenant Isolation**: Row-level logical isolation anchored on `School` and `SchoolMembership` with custom RBAC permissions
- **API Boundary**: RESTful API under `/api/v1/` with consistent JSON error envelopes and health telemetry

---

## Directory Layout

```text
Darsentra/
├── docker-compose.yml              # Multi-container orchestration (DB, Backend, Frontend)
├── docker-compose.override.yml.example
├── .env.example                    # Global environment variables template
├── .editorconfig                   # Cross-platform indentation and line endings
├── .gitignore                      # Multi-tier gitignore (Python, Node, Docker)
├── docs/                           # Architectural and operational specifications
│   └── architecture/
│       ├── overview.md             # System architecture overview
│       └── tenant_isolation.md     # Multi-tenant isolation strategy & RBAC
├── backend/                        # Django REST Framework backend monolith
│   ├── Dockerfile                  # Production container definition
│   ├── Dockerfile.dev              # Hot-reloading development container
│   ├── manage.py                   # Django management entrypoint
│   ├── pyproject.toml              # Ruff and pytest configurations
│   ├── requirements.txt            # Production dependencies
│   ├── requirements-dev.txt        # Testing and linting dependencies
│   ├── config/                     # Project configuration & split settings
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   ├── urls.py                 # Namespaced API routing (/api/v1/...)
│   │   └── settings/
│   │       ├── base.py             # Shared settings & security baseline
│   │       ├── development.py      # Dev settings with flexible DB options
│   │       └── production.py       # Hardened production settings
│   └── apps/                       # Modular applications
│       ├── core/                   # Base models, health check (/api/v1/health/), exceptions
│       ├── accounts/               # Custom User model (UUID, email-based auth)
│       ├── schools/                # Multi-tenant School & SchoolMembership models
│       ├── academics/              # Classes, sections, subjects (Phase 2 skeleton)
│       ├── students/               # Student profiles and admissions (Phase 2 skeleton)
│       ├── attendance/             # Daily student & staff attendance (Phase 2 skeleton)
│       ├── examinations/           # Exams, mark sheets, grade scales (Phase 2 skeleton)
│       ├── fees/                   # Fee structures, challans, payments (Phase 2 skeleton)
│       ├── staff/                  # Teachers & staff management (Phase 2 skeleton)
│       └── reports/                # Analytics and reporting (Phase 2 skeleton)
└── frontend/                       # React TypeScript Single Page Application
    ├── Dockerfile                  # Production multi-stage Nginx container
    ├── Dockerfile.dev              # Development container with hot reloading
    ├── nginx.conf                  # Nginx production configuration
    ├── package.json                # React, Vite, Tailwind, Lucide dependencies
    ├── tsconfig.json               # TypeScript strict configuration & paths
    ├── vite.config.ts              # Vite dev server and proxy configuration
    ├── tailwind.config.js          # Tailwind CSS with shadcn/ui design tokens
    └── src/
        ├── App.tsx                 # Foundation dashboard with live health monitor
        ├── main.tsx                # React Router & DOM mount
        ├── index.css               # Global theme variables & styles
        ├── components/ui/          # Reusable UI primitives (Button, Card, Badge)
        ├── layouts/                # Responsive enterprise layouts
        ├── hooks/                  # Custom hooks (useHealthCheck)
        ├── services/               # Centralized Axios client & services
        ├── types/                  # TypeScript interface definitions
        └── features/               # Modular feature directories (Phase 2 ready)
```

---

## Quickstart Guide

### Option A: Running with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/furqan-debug/Darsentra-ERP.git
   cd Darsentra
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. **Start the environment**:
   ```bash
   docker compose up --build
   ```

4. **Verify running services**:
   - Frontend UI: [http://localhost:5173](http://localhost:5173)
   - Backend API Health: [http://localhost:8000/api/v1/health/](http://localhost:8000/api/v1/health/)
   - Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### Option B: Running Locally (Windows / WSL2 / Linux / macOS)

#### 1. Backend Setup

```bash
cd backend

# Create and activate Python virtual environment
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux / macOS / WSL2:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Create initial environment file
cp .env.example .env

# Run database migrations (uses SQLite fallback if PostgreSQL is not running locally)
python manage.py migrate

# Run Django system checks
python manage.py check

# Run automated test suite
python manage.py test

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
```

#### 2. Frontend Setup

In a separate terminal:

```bash
cd frontend

# Install node dependencies
npm install

# Run type check and production build
npm run build

# Start Vite development server
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) to see the Darsentra ERP dashboard communicating live with the backend.

---

## Operational Commands Reference

### Database Migrations

```bash
# Generate new migration files for models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Running Automated Tests

```bash
# Run all tests
python manage.py test

# Run tenant isolation tests specifically
python manage.py test apps.schools.tests.test_tenant_isolation

# Run health check tests
python manage.py test apps.core.tests.test_health

# Run user model tests
python manage.py test apps.accounts.tests.test_user
```

### Code Formatting & Linting

```bash
# Lint backend with Ruff
ruff check backend/

# Format backend with Ruff
ruff format backend/

# Build frontend production bundle
cd frontend && npm run build
```

### Stopping Docker Services

```bash
# Stop containers
docker compose down

# Stop containers and remove persistent volumes
docker compose down -v
```

---

## Multi-Tenant Security & Isolation Model

Darsentra ERP enforces strict row-level tenant isolation:

1. **Untrusted Client Claims**: Client-provided school IDs in parameters or headers are treated as untrusted claims and never accepted blindly.
2. **Membership Verification**: Every request to a tenant resource verifies that `request.user` has an active `SchoolMembership` in the school.
3. **Tenant QuerySet Scoping**: DRF views filter querysets by the requesting user's verified active school.
4. **Cross-Tenant Prevention**: Automated integration tests confirm that any cross-tenant request immediately returns `403 Forbidden`.

For detailed architecture documentation, see [`docs/architecture/tenant_isolation.md`](docs/architecture/tenant_isolation.md).
