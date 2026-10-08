# Darsentra ERP 🏫

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](LICENSE)
[![GitHub Repository](https://img.shields.io/badge/GitHub-furqan--debug%2FDarsentra--ERP-181717.svg?logo=github)](https://github.com/furqan-debug/Darsentra-ERP)
[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-purple.svg)](https://www.odoo.com/)

**Darsentra ERP** is a modern, enterprise-grade **School Management System (SMS)** built on Odoo 19, specifically tailored and localized for Pakistani schools (Pre-School, Primary, Middle, Secondary/Matric, O-Levels).

Repository: **[https://github.com/furqan-debug/Darsentra-ERP](https://github.com/furqan-debug/Darsentra-ERP)**

---

## 🌟 Core Pakistani School Features

### 1. 🪪 Student Profile & NADRA Localization (`darsentra_school_core`)
- **NADRA B-Form / CRC Validation**: Automated formatting (`XXXXX-XXXXXXX-X`) and 13-digit validation for minor students.
- **Family Particulars**: Father & Mother CNIC, profession, and primary WhatsApp / Mobile contact for fee alerts and announcements.
- **School Houses**: Pre-configured historical houses (*Jinnah House, Iqbal House, Liaquat House, Sir Syed House*).
- **Pick & Drop / Transport**: School Van, Private Contractor, and Parent Pick & Drop logistics tracking with vehicle numbers and driver contacts.
- **Official Certificates**: Built-in generators with printable QWeb PDF templates for:
  - **School Leaving Certificate (SLC)**
  - **Character & Conduct Certificate**
  - **Bonafide Student Certificate**

### 2. 🧾 Monthly Fee Challan & Banking Engine (`darsentra_school_fees`)
- **Bulk Monthly Fee Generator**: One-click fee generator wizard by Class and Section.
- **Automated Sibling Discounts**: Automatic 10% discount for 2nd child and 20% for 3rd+ child matched by Father's CNIC / Mobile.
- **1Link / Kuickpay Integration**: Auto-generated 12-digit Consumer ID per challan for ATM, Mobile Banking, and OTC payments.
- **3-Part Bank Challan**: Standard printable slip containing Bank Copy, School Accounts Copy, and Parent Copy.
- **Arrears & Late Fee Fines**: Carry-forward of unpaid balances and grace period late fee calculations.

### 3. 🏆 Examination & Term Progress Report Cards (`darsentra_school_exam`)
- **Subject Marks System**: Maximum Marks, Passing Marks, and Marks Obtained.
- **Class Ranking**: Automated calculation of class ranks (`1st Position 🏆`, `2nd Position 🥈`, `3rd Position 🥉`).
- **Pakistani BISE Grade Scale**: Standard percentage-to-grade mapping (`A+ Outstanding`, `A Excellent`, `B Very Good`, `C Good`, `D Fair`, `E Pass`, `F Fail`).
- **Term Progress Report Card**: Official printable result card featuring attendance %, class teacher remarks, and subject breakdown.

---

## 🚀 Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/furqan-debug/Darsentra-ERP.git
cd Darsentra-ERP

# Start Odoo 19 and PostgreSQL containers
docker compose up -d

# Access the ERP
http://localhost:8069
```

---

## 📁 Architecture & Module Structure

```text
├── darsentra_school_core/     # NADRA B-Form, Parents, Houses, SLC & Character Certs
├── darsentra_school_fees/     # Monthly Fee Generator, 3-Part Challan, Sibling Discounts
├── darsentra_school_exam/     # Subject Marks, Class Positions (1st/2nd/3rd), Report Cards
├── openeducat_core/           # Base academic framework (Classes, Sections, Teachers)
├── openeducat_admission/      # Online and counter admissions workflow
├── openeducat_attendance/     # Daily student attendance tracking
├── openeducat_timetable/      # School timetable & bell schedule
└── docker-compose.yml         # Containerized local development stack
```

---

## 📄 License

Darsentra ERP is licensed under the [GNU Lesser General Public License v3.0 (LGPL-3.0)](LICENSE).
