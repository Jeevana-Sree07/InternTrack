# InternTrack

## Internship Application Tracking System

InternTrack is a web-based internship application tracking system developed using **Python, Flask, MySQL, HTML, and CSS**.

The system allows students to explore internship opportunities, search internships by required skills, submit applications, track application status, and manage interview rounds.

---

## Features

- 📊 Dashboard with internship and application statistics
- 🔎 Browse available internships
- 🛠️ Search internships by technical skill
- 📝 Apply for internships
- 📋 View and track internship applications
- 🔄 Update application status
- 🎤 Add and manage interview rounds
- 📅 Record interview dates
- ✅ Track interview results
- 💬 Store interview feedback
- 🔗 Relational MySQL database
- ⚙️ SQL views, trigger, stored procedure, and transaction

---

## Technologies Used

### Frontend

- HTML5
- CSS3

### Backend

- Python
- Flask

### Database

- MySQL

### Development Tools

- Visual Studio Code
- MySQL Workbench
- Git
- GitHub

---

## System Architecture

```text
User
  │
  ▼
HTML / CSS
  │
  ▼
Flask Web Application
  │
  ▼
MySQL Database
```

---

## Database Design

The system contains the following tables:

1. **Student** – Stores student information.
2. **Company** – Stores company details.
3. **Internship** – Stores internship opportunities.
4. **Application** – Stores student internship applications.
5. **Interview** – Stores interview rounds, results, and feedback.
6. **Skill** – Stores technical skills.
7. **Internship_Skill** – Connects internships with required skills.

### Database Relationships

```text
Student
   │
   ▼
Application ─────────► Internship ─────────► Company
   │                       │
   │                       ▼
   │                 Internship_Skill
   │                       │
   ▼                       ▼
Interview                 Skill
```

---

## DBMS Concepts Demonstrated

This project demonstrates important DBMS concepts including:

- Primary Keys
- Foreign Keys
- Unique Constraints
- NOT NULL Constraints
- ENUM Data Types
- One-to-Many Relationships
- Many-to-Many Relationships
- SQL JOIN Operations
- Views
- Triggers
- Stored Procedures
- Transactions
- Referential Integrity

---

## Project Structure

```text
InternTrack/
│
├── app.py
├── database.py
├── database.sql
├── requirements.txt
├── .env
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── internships.html
│   ├── apply.html
│   ├── applications.html
│   ├── interviews.html
│   └── add_interview.html
│
├── static/
│   └── css/
│       └── style.css
│
└── venv/
```

> The `venv/` directory is ignored by Git and is used only for the local Python environment.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Jeevana-Sree07/InternTrack.git
```

Move into the project directory:

```bash
cd InternTrack
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set Up the MySQL Database

Make sure **MySQL Server** is installed and running.

Open **MySQL Workbench** and run the `database.sql` script included in this repository.

The script creates:

- `interntrack` database
- Seven relational tables
- Sample companies
- Sample students
- Sample internships
- Technical skills
- Internship-skill relationships
- Sample applications
- Sample interviews
- Database views
- Deadline trigger
- Stored procedure

---

### 5. Configure Database Connection

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=interntrack
DB_PORT=3306
```

Replace `your_mysql_password` with your own MySQL password.

> **Do not upload the `.env` file to GitHub.**

---

### 6. Run the Application

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run the Flask application:

```bash
python app.py
```

The application will start at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## Application Pages

### Dashboard

The dashboard displays:

- Total internships
- Total applications
- Number of interviews
- Number of selected applications

### Internships

Users can:

- Browse available internships
- Search internships by skill
- View company information
- View stipend and deadline
- Apply for an internship

### Applications

Users can:

- View internship applications
- View application dates
- View application status
- Update application status

Available statuses:

- Applied
- Shortlisted
- Interview
- Selected
- Rejected

### Interviews

Users can:

- View interview rounds
- Add new interviews
- Record interview dates
- Record interview results
- Store interview feedback

Available interview results:

- Pending
- Passed
- Failed

---

## SQL Features

### Views

The project contains two database views.

#### ApplicationDetails

Provides application information by combining:

- Student
- Application
- Internship
- Company

#### InternshipSkills

Provides internship and required skill information using multiple table joins.

---

### Trigger

The project contains a trigger named:

```text
prevent_late_application
```

This trigger prevents an internship application from being inserted after the internship deadline.

---

### Stored Procedure

The project contains the stored procedure:

```text
ApplyForInternship
```

It allows an internship application to be created using a stored procedure.

---

### Transaction

Interview creation and application status updates are handled as related database operations and committed together.

---

## Future Improvements

Possible future enhancements include:

- Student login and authentication
- Admin dashboard
- Add internships through the website
- Resume upload
- Email notifications
- Application analytics
- Skill-based internship recommendations
- Cloud deployment
- Responsive mobile interface

---

## Author

**Maloth Jeevana Sree**

B.Tech – Computer Science and Engineering (Data Science)

**VNR VJIET**

GitHub: [Jeevana-Sree07](https://github.com/Jeevana-Sree07)

---

## License

This project was developed for educational and academic purposes.