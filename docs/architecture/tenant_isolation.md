# Darsentra ERP - Multi-Tenant Isolation Strategy

## Overview

Darsentra ERP is architected as a high-integrity, multi-tenant SaaS School Management platform designed specifically for the Pakistani education sector (Matric/FSc, Cambridge O/A Levels, FBISE, and provincial boards).

In an enterprise education SaaS platform, strict tenant isolation is a non-negotiable security requirement. School records, student personal information, disciplinary notes, fee receipts, and examination marks belonging to one institution must be completely inaccessible to any unauthorized party from another institution.

---

## 1. Tenant Architecture Model

### Pooled Database with Logical Isolation
Darsentra ERP employs a **shared database, shared schema with row-level logical isolation**:
- **Tenant Root**: The `School` model in `apps.schools.models.School`.
- **Tenant Key**: Each school is uniquely identified by a UUID primary key (`id`) and a canonical school slug/code.
- **Tenant Association**: The `SchoolMembership` model connects `User` records with `School` records and defines their role (Owner, Principal, Admin, Teacher, Accountant, Student, Parent, Staff).

---

## 2. The 5 Core Isolation Rules

### Rule 1: Never Trust Client-Provided Tenant Identifiers
Clients never directly specify which tenant data they can access without verification. An incoming school identifier (whether in URL parameters, query strings, headers, or request bodies) is treated as an **untrusted claim**.

### Rule 2: Membership-Gated Access Verification
Before any query or mutation is executed against tenant-scoped data, the backend executes membership verification:
```python
membership = SchoolMembership.objects.filter(
    user=request.user,
    school_id=target_school_id,
    is_active=True,
    school__is_active=True,
).first()

if not membership:
    raise PermissionDenied("Access denied: You do not have an active membership in this school.")
```
If a user is inactive, or the school tenant itself is marked inactive (e.g. suspended account), access is immediately denied with HTTP 403.

### Rule 3: Universal Base Inheritance (`TenantScopedModel`)
Every database table representing school-specific data inherits from `TenantScopedModel` in `apps.core.models`:
```python
class TenantScopedModel(TimeStampedModel):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_records",
        db_index=True,
    )
    class Meta:
        abstract = True
```
This guarantees:
1. Every record has a mandatory non-null foreign key to a valid `School`.
2. Cascading deletes cleanly remove all tenant data when a school is purged.
3. Database index on `school_id` optimizes query filtering.

### Rule 4: Mandatory QuerySet Tenant Scoping
In Django REST Framework views, `get_queryset()` must always scope its results to the verified tenant:
```python
def get_queryset(self):
    active_school = self.get_active_school()
    return super().get_queryset().filter(school=active_school)
```
Defaulting to `Model.objects.all()` without tenant filtering is prohibited across all domain modules (students, academics, fees, examinations, etc.).

### Rule 5: Tenant Context Resolution for Multi-Campus Users
In Pakistani education systems, certain users (such as visiting teachers, regional directors, or parents with children in multiple schools) may possess memberships in multiple independent schools:
1. When requesting tenant-specific data, the client passes an `X-School-ID` header.
2. The `TenantSecurityService` validates that `request.user` holds an active membership for that specific school.
3. If valid, the school is bound to `request.tenant_school`.
4. If invalid, the request is immediately halted with HTTP 403 Forbidden.
5. If no header is provided and the user belongs to exactly one active school, the system defaults to that school.

---

## 3. Role-Based Access Control (RBAC) Hierarchy

Within each school tenant, permissions are partitioned by roles:

| Role | Scope & Permissions |
|---|---|
| **OWNER** | Full administrative and legal control; subscription billing; school profile configuration. |
| **PRINCIPAL** | Full operational control across all academic, staff, student, and reporting functions. |
| **ADMIN** | Institutional administration: student admissions, fee structures, timetables, and staff onboarding. |
| **TEACHER** | Attendance marking, homework/assignments, marks entry for assigned classes and sections. |
| **ACCOUNTANT** | Fee challan generation, fee collection reconciliation, financial reporting. |
| **STUDENT** | Read-only access to own class timetable, attendance, homework, and term exam marks. |
| **PARENT** | Read-only access to enrolled children's attendance, academic progress, and fee challan history. |
| **STAFF** | Non-teaching administrative and operational functions. |

---

## 4. Verification and Automated Testing

All multi-tenant isolation rules are covered by automated integration tests in:
- `backend/apps/schools/tests/test_tenant_isolation.py`

These tests verify:
- Complete prevention of cross-tenant data leakage.
- Automatic filtering of school listings to the authenticated user's active memberships.
- Rejection of spoofed school IDs with HTTP 403 Forbidden.
- Immediate revocation of access upon membership deactivation.
