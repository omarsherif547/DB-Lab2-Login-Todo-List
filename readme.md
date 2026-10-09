# DB Lab 2 — Login & To-Do Application

## 1. Project Information

**University:** Alexandria National University  
**Faculty:** Faculty of Engineering  
**Course:** Introduction to Database Systems  
**Assignment:** Lab 2 — Login & To-Do Application

**Student Name:** Omar Sherif Mahmoud  
**Student ID:** 2304021  

## 2. Project Description

A web-based To-Do List application developed using Python Flask and MySQL.

The application allows users to register, log in securely, and manage their personal tasks. Each user can access only their own tasks.

## 3. Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Database:** MySQL
- **Database Connector:** PyMySQL
- **Password Security:** bcrypt
- **Session Management:** Flask-Session
- **Version Control:** Git and GitHub

## 4. Application Features

- User registration with duplicate-email detection
- Secure login and logout
- Password hashing using bcrypt
- Private task lists for each user
- Add new tasks
- Edit existing tasks
- Mark tasks as completed or pending
- Delete tasks with confirmation
- Optional task due dates (bonus)
- Client-side and server-side validation
- Responsive user interface
- Parameterized SQL queries

## 5. Installation and Setup

**Step 1 — Requirements**

Install Python, MySQL Server, and Git.

**Step 2 — Clone the Repository**

Clone this GitHub repository and open the project folder.

**Step 3 — Create a Virtual Environment**

Run `python -m venv .venv`.

**Step 4 — Install Dependencies**

Run `.venv\Scripts\python.exe -m pip install -r requirements.txt` on Windows.

**Step 5 — Create the Database**

Open MySQL Workbench, connect to MySQL, and execute the file `database/schema.sql`.

Warning: This script recreates the database and deletes any existing data in `registration`.

**Step 6 — Configure Environment Variables**

Copy `.env.example` to `.env` and set the MySQL connection values and a securely generated `SECRET_KEY`.

**Step 7 — Start the Server**

Run `.venv\Scripts\python.exe app.py` on Windows.

**Step 8 — Open the Website**

Open `http://127.0.0.1:5000` in your browser.

## 6. Database Structure

**users**

Stores user accounts with the following fields:

- user_id — Primary key
- email — Unique
- name
- password_hash
- registration_date

**todos**

Stores tasks belonging to registered users:

- todo_id — Primary key
- user_id — Foreign key referencing users
- title
- is_done
- created_at
- due_date — Optional bonus field

**Relationship:** One user can have many tasks, but each task belongs to one user.



## 7. Database Theory Questions

**Q1: Why do UPDATE and DELETE queries contain AND user_id = ? What happens if it is removed?**

The condition ensures that only the owner of a task can modify or delete it. Without this condition, an authenticated user could potentially change or delete another user's task by supplying its todo_id.

**Q2: What happens if you insert a task with a user_id that doesn't exist? Which constraint is involved?**

MySQL rejects the insertion because the user_id must reference an existing user in the users table. This is enforced by the foreign key constraint, which maintains referential integrity.

**Q3: Why store a password hash instead of the actual password?**

A password hash protects user credentials if the database is compromised. bcrypt creates a salted, computationally expensive hash. During login, the entered password is verified against the stored hash rather than decrypting it.

**Q4: If the name column is NOT NULL, why do we still need to validate an empty name?**

NOT NULL prevents SQL NULL values, but an empty string is not NULL. Therefore, application-level validation is necessary to reject empty or whitespace-only names.

## 8. Security Features

- Passwords hashed using bcrypt
- Parameterized SQL queries
- Server-side sessions
- Protected routes for authenticated users
- Task ownership enforcement
- Input validation on both frontend and backend
- Sensitive credentials stored outside version control

## 9. Bonus Feature

Users can assign an optional due date to tasks, view it, and change or remove it later.
