# Lab 3 — MVC Web Application

**SAP SuccessFactors — People Onboarding System**

A web application built using the **MVC (Model-View-Controller)** pattern for managing the employee onboarding process in an IT company. The domain is based on **SAP SuccessFactors** — a system that handles new hire onboarding, equipment provisioning, and account creation.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Web Framework | Flask 3.1 |
| ORM | SQLAlchemy 2.0 |
| Database | MySQL 8.x |
| DB Driver | PyMySQL |
| Templates | Jinja2 |
| Styling | Vanilla CSS (GlobalLogic-inspired design) |

---

## Project Structure

```
lab3/
├── app.py                          # Flask entry point — registers blueprints, starts server
├── config.py                       # Reads .env and provides DB connection URLs
├── db.py                           # SQLAlchemy engine, session management, DB init
├── seed.py                         # Populates the database with test data
├── requirements.txt                # Python dependencies
├── .env                            # Database credentials (not committed to git)
│
├── models/                         # MODEL layer — SQLAlchemy ORM models
│   ├── employee.py                 # Employee table (main entity)
│   ├── equipment.py                # Equipment table (FK → employees)
│   └── account.py                  # Account table (FK → employees)
│
├── services/                       # BUSINESS LOGIC layer — data operations
│   ├── employee_service.py         # CRUD + validation for employees
│   ├── equipment_service.py        # CRUD + validation for equipment
│   └── account_service.py          # CRUD + validation for accounts
│
├── controllers/                    # CONTROLLER layer — Flask Blueprints
│   ├── main_controller.py          # GET /              → Dashboard
│   ├── employee_controller.py      # GET/POST /employees → CRUD
│   ├── equipment_controller.py     # GET/POST /equipment → CRUD
│   └── account_controller.py       # GET/POST /accounts  → CRUD
│
├── templates/                      # VIEW layer — Jinja2 HTML templates
│   ├── base.html                   # Base layout (navbar, footer, flash messages)
│   ├── index.html                  # Dashboard with statistics
│   ├── employees/
│   │   ├── list.html               # Employee table
│   │   └── form.html               # Create/Edit employee form
│   ├── equipment/
│   │   ├── list.html               # Equipment table
│   │   └── form.html               # Create/Edit equipment form
│   └── accounts/
│       ├── list.html               # Accounts table
│       └── form.html               # Create/Edit account form
│
└── static/
    └── style.css                   # GlobalLogic-styled CSS
```

---

## Domain Model

The application is based on the **SAP SuccessFactors** onboarding domain from Lab 1.

**Main entity: Employee** — a new hire going through the onboarding process.

### Database Schema

```
┌─────────────────────┐
│      employees      │
├─────────────────────┤
│ id          PK      │
│ name        VARCHAR │
│ email       UNIQUE  │
│ position    VARCHAR │
│ start_date  DATE    │
│ status      VARCHAR │──── pending / in_progress / completed
└────────┬────────────┘
         │ 1
         │
    ┌────┴────┐
    │         │
    │ *       │ *
┌───┴─────────┴───┐   ┌──────────────────────┐
│    equipment    │   │       accounts       │
├─────────────────┤   ├──────────────────────┤
│ id          PK  │   │ id           PK      │
│ serial_number   │   │ username     VARCHAR │
│ equipment_type  │   │ system_name  VARCHAR │── email/jira/gitlab/slack/vpn
│ model           │   │ permissions  VARCHAR │── read/write/admin
│ employee_id FK ─┤   │ is_active    BOOL   │
└─────────────────┘   │ employee_id  FK ────┤
                      └──────────────────────┘
```

**Relationships:**
- One Employee → Many Equipment items (cascade delete)
- One Employee → Many Accounts (cascade delete)

---

## MVC Architecture

```
  Browser (HTTP Request)
       │
       ▼
  ┌─────────────────────────────────┐
  │  CONTROLLER (Flask Blueprint)   │  ← routes, request handling
  │  controllers/*_controller.py    │
  └──────────┬──────────────────────┘
             │ calls
             ▼
  ┌─────────────────────────────────┐
  │  SERVICE (Business Logic)       │  ← validation, CRUD operations
  │  services/*_service.py          │
  └──────────┬──────────────────────┘
             │ uses
             ▼
  ┌─────────────────────────────────┐
  │  MODEL (SQLAlchemy ORM)         │  ← maps to MySQL tables
  │  models/*.py                    │
  └──────────┬──────────────────────┘
             │ SQL queries
             ▼
  ┌─────────────────────────────────┐
  │  DATABASE (MySQL)               │
  │  lab3                           │
  └─────────────────────────────────┘

  Controller also calls:
  ┌─────────────────────────────────┐
  │  VIEW (Jinja2 Templates)        │  ← renders HTML pages
  │  templates/**/*.html            │
  └─────────────────────────────────┘
```

---

## Routes

### Dashboard
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Dashboard with stats and recent employees |

### Employees
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/employees/` | List all employees |
| GET | `/employees/create` | Show create form |
| POST | `/employees/create` | Create new employee |
| GET | `/employees/<id>/edit` | Show edit form |
| POST | `/employees/<id>/edit` | Update employee |
| POST | `/employees/<id>/delete` | Delete employee |

### Equipment
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/equipment/` | List all equipment |
| GET | `/equipment/create` | Show create form |
| POST | `/equipment/create` | Add new equipment |
| GET | `/equipment/<id>/edit` | Show edit form |
| POST | `/equipment/<id>/edit` | Update equipment |
| POST | `/equipment/<id>/delete` | Delete equipment |

### Accounts
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/accounts/` | List all accounts |
| GET | `/accounts/create` | Show create form |
| POST | `/accounts/create` | Create new account |
| GET | `/accounts/<id>/edit` | Show edit form |
| POST | `/accounts/<id>/edit` | Update account |
| POST | `/accounts/<id>/delete` | Delete account |

---

## How to Run

### Prerequisites

- **Python 3.11+** installed
- **MySQL 8.x** running on `localhost:3306`
- MySQL user `root` with password `12345678` (or edit `.env`)

### Step 1: Install Dependencies

```bash
cd lab3
pip install -r requirements.txt
```

If you get a `cryptography` error, also run:
```bash
pip install cryptography
```

### Step 2: Configure Database (optional)

Edit `.env` if your MySQL credentials differ:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=lab3
```

The database `lab3` will be **created automatically** on first run.

### Step 3: Seed Test Data

```bash
python seed.py
```

This creates **7 employees**, **10 equipment items**, and **12 accounts**.

### Step 4: Run the Application

```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## Test Data

### Employees (7)
| Name | Position | Status |
|------|----------|--------|
| Ivan Petrenko | Software Engineer | Completed |
| Olena Kovalenko | QA Engineer | Completed |
| Maksym Bondarenko | DevOps Engineer | In Progress |
| Sofiia Melnyk | Frontend Developer | In Progress |
| Taras Shevchenko | Backend Developer | Pending |
| Marta Kravets | Project Manager | Pending |
| Nazar Polishchuk | Data Analyst | Pending |

### Equipment Types
Laptop, Monitor, Keyboard, Mouse, Headset

### Account Systems
Email, Jira, GitLab, Slack, VPN

---

## Assignment Compliance

| # | Requirement | Implementation |
|---|------------|----------------|
| 1 | Define the main entity | **Employee** — new hire going through onboarding |
| 2 | Controllers with action methods | 4 Flask Blueprints with GET/POST handlers |
| 3 | Model + database + test data | SQLAlchemy ORM models + MySQL + `seed.py` |
| 4 | Add, edit, delete functionality | Full CRUD for all 3 entities |
| 5 | Data displayed as HTML pages | 8 Jinja2 templates rendering HTML |
| 6 | Business logic classes | `EmployeeService`, `EquipmentService`, `AccountService` |
