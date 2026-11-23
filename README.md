# FocusFlow – Take Control of Your Screen Time

FocusFlow is a web-based screen-time management system designed to help college students become more aware of their daily activities and manage their time effectively.

The system allows students to record their productive and distracting activities manually and manage their activity records through a simple dashboard.

## Core Features

### Account Management
- Student registration and login.
- User logout.
- Student and Admin role-based dashboards.
- User profile viewing and updating.

### Manual Activity Tracker
- Create activity records.
- View recorded activities.
- Update existing activity records.
- Delete activity records.
- Categorize activities as Productive or Distracting.
- Record activity name, duration, date and time, and optional notes.
- Validate required fields and activity duration.
- Restrict activity records to their respective owners.

## Technologies Used

- Python
- Django
- HTML and CSS
- PostgreSQL
- Supabase PostgreSQL
- psycopg
- python-dotenv

## Project Requirements

- Python 3.12 or compatible version
- PostgreSQL database
- Git

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ryaaanzi/FocusFlow-Acebedo-Ryan-G6.git
cd FocusFlow-Acebedo-Ryan-G6
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add the required Django secret key and PostgreSQL database connection settings. Use your own database credentials and keep this file private.

Do not commit or upload your `.env` file.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/accounts/login/

If port 8000 is unavailable, use another port:

```bash
python manage.py runserver 8001
```

Then open:

http://127.0.0.1:8001/accounts/login/

## Manual Activity Tracker Usage

1. Log in using a Student account.
2. Open the Student Dashboard.
3. Select **Open Activity Tracker**.
4. Add a productive or distracting activity.
5. View, edit, or delete your activity records.

Each student can only access their own activity records.

## Project Scope

FocusFlow currently uses manually entered activity records. Automatic device-wide screen-time tracking and automatic application blocking are outside the scope of this implementation.

## Repository

GitHub: https://github.com/ryaaanzi/FocusFlow-Acebedo-Ryan-G6