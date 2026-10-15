# Darsentra ERP - System Architecture Overview

## 1. System Vision

Darsentra ERP is a modern, cloud-native School Management SaaS platform engineered specifically for schools in Pakistan. It replaces fragmented legacy software and manual paper registers with an enterprise-grade, high-performance web platform.

## 2. Technology Stack

- **Backend**: Python 3.12+ / Django 5.1 / Django REST Framework 3.15+
- **Frontend**: React 19 / TypeScript / Vite 6+ / Tailwind CSS / shadcn/ui
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose
- **Security**: Django Authentication Infrastructure, Argon2/PBKDF2 Password Hashing, CSRF/CORS Guards
- **Architecture**: Modular Monolith with RESTful API Boundaries

## 3. Directory Layout

```text
Darsentra/
├── backend/                       # Django REST Framework Monolith
│   ├── config/                    # WSGI/ASGI and split environments
│   │   └── settings/              # base, development, production
│   └── apps/                      # Domain applications
│       ├── core/                  # Base models, exceptions, health check
│       ├── accounts/              # Custom user model & auth foundation
│       ├── schools/               # Tenants and memberships
│       ├── academics/             # Classes, sections, subjects (Phase 2)
│       ├── students/              # Student profiles & enrollments (Phase 2)
│       ├── attendance/            # Attendance marking (Phase 2)
│       ├── examinations/          # Exams, grade scales & marks (Phase 2)
│       ├── fees/                  # Fee structures & challans (Phase 2)
│       ├── staff/                 # Teachers and staff profiles (Phase 2)
│       └── reports/               # Analytics and reporting (Phase 2)
├── frontend/                      # React TypeScript Vite Single Page App
│   ├── src/
│   │   ├── components/ui/         # shadcn/ui design primitives
│   │   ├── layouts/               # Shared responsive layouts
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── services/              # Centralized Axios API client
│   │   └── types/                 # TypeScript interfaces
├── docs/                          # Architectural and operational documentation
├── docker-compose.yml             # Container orchestration
└── README.md                      # Developer onboarding and setup
```
