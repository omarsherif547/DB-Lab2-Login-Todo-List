
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from cachelib import FileSystemCache
import pymysql
import bcrypt
import os
from dotenv import load_dotenv
from datetime import date


# =====================================================
# 1. FLASK CONFIGURATION
# =====================================================

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "cachelib"
app.config["SESSION_CACHELIB"] = FileSystemCache(
    cache_dir="session_cache",
    threshold=500
)
app.config["SESSION_PERMANENT"] = False

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is missing from .env")

Session(app)


# =====================================================
# 2. MYSQL DATABASE CONNECTION
# =====================================================

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )


# =====================================================
# 3. HOME PAGE
# =====================================================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("todos"))

    return redirect(url_for("login"))


# =====================================================
# 4. USER REGISTRATION
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html", errors=[])

    # Get registration data
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    errors = []

    # Validate inputs
    if not name:
        errors.append("Name is required")

    if not email:
        errors.append("Email is required")

    if not password:
        errors.append("Password is required")

    if not confirm_password:
        errors.append("Confirm password is required")

    if password and confirm_password and password != confirm_password:
        errors.append("Passwords do not match")

    if errors:
        return render_template(
            "register.html",
            errors=errors
        )

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                INSERT INTO users (email, name, password_hash)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql,
                (email, name, hashed_password)
            )

            user_id = cursor.lastrowid

        connection.commit()

    except pymysql.err.IntegrityError as error:
        connection.rollback()

        if error.args[0] == 1062:
            return render_template(
                "register.html",
                errors=["Email Already Exists"]
            )

        raise

    finally:
        connection.close()

    # Automatically login after registration
    session.clear()
    session["user_id"] = user_id
    session["name"] = name

    return redirect(url_for("todos"))


# =====================================================
# 5. USER LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html", errors=[])

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    errors = []

    # Validate inputs
    if not email:
        errors.append("Email is required")

    if not password:
        errors.append("Password is required")

    if errors:
        return render_template(
            "login.html",
            errors=errors
        )

    # Find user in database
    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT user_id, name, password_hash
                FROM users
                WHERE email = %s
            """

            cursor.execute(sql, (email,))
            user = cursor.fetchone()

    finally:
        connection.close()

    # Check user existence
    if not user:
        return render_template(
            "login.html",
            errors=["Invalid email or password"]
        )

    # Verify password
    try:
        password_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        )
    except ValueError:
        password_correct = False

    if not password_correct:
        return render_template(
            "login.html",
            errors=["Invalid email or password"]
        )

    # Create login session
    session.clear()
    session["user_id"] = user["user_id"]
    session["name"] = user["name"]

    return redirect(url_for("todos"))


# =====================================================
# 6. USER LOGOUT
# =====================================================

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect(url_for("login"))


# =====================================================
# 7. DISPLAY AND ADD TO-DO TASKS
# =====================================================


# =====================================================
# 7. DISPLAY AND ADD TO-DO TASKS WITH DUE DATE
# =====================================================

@app.route("/todos", methods=["GET", "POST"])
def todos():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    errors = []
    input_title = ""
    input_due_date = ""

    # Handle adding a new task
    if request.method == "POST":

        input_title = request.form.get("title", "")
        title = input_title.strip()

        input_due_date = request.form.get("due_date", "").strip()
        parsed_due_date = None

        # Validate task title
        if not title:
            errors.append("Title is required")

        elif len(title) > 200:
            errors.append("Title is too long")

        # Validate due date (optional)
        if input_due_date:
            try:
                parsed_due_date = date.fromisoformat(input_due_date)

                if parsed_due_date.isoformat() != input_due_date:
                    raise ValueError("Invalid format")

            except ValueError:
                errors.append("Invalid due date")

        # Save task if input is valid
        if not errors:

            connection = get_db()

            try:
                with connection.cursor() as cursor:

                    sql = """
                        INSERT INTO todos (user_id, title, due_date)
                        VALUES (%s, %s, %s)
                    """

                    cursor.execute(
                        sql,
                        (user_id, title, parsed_due_date)
                    )

                connection.commit()

            except Exception:
                connection.rollback()
                raise

            finally:
                connection.close()

            return redirect(url_for("todos"))

    # Retrieve tasks from MySQL
    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT todo_id, title, is_done,
                       created_at, due_date
                FROM todos
                WHERE user_id = %s
                ORDER BY todo_id DESC
            """

            cursor.execute(sql, (user_id,))
            tasks = cursor.fetchall()

    finally:
        connection.close()

    return render_template(
        "todos.html",
        name=session["name"],
        tasks=tasks,
        errors=errors,
        input_title=input_title,
        input_due_date=input_due_date
    )



# =====================================================
# 8. EDIT EXISTING TO-DO TASK
# =====================================================


# =====================================================
# 8. EDIT TASK TITLE AND DUE DATE
# =====================================================

@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):

    # Check whether user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get updated information
    title = request.form.get("title", "").strip()
    due_date_input = request.form.get("due_date", "").strip()

    errors = []
    parsed_due_date = None

    # Validate task title
    if not title:
        errors.append("Title is required")

    elif len(title) > 200:
        errors.append("Title is too long")

    # Validate due date
    if due_date_input:
        try:
            parsed_due_date = date.fromisoformat(due_date_input)

            if parsed_due_date.isoformat() != due_date_input:
                raise ValueError("Invalid format")

        except ValueError:
            errors.append("Invalid due date")

    # Handle validation errors
    if errors:

        connection = get_db()

        try:
            with connection.cursor() as cursor:

                sql = """
                    SELECT todo_id, title, is_done,
                           created_at, due_date
                    FROM todos
                    WHERE user_id = %s
                    ORDER BY todo_id DESC
                """

                cursor.execute(sql, (session["user_id"],))
                tasks = cursor.fetchall()

        finally:
            connection.close()

        return render_template(
            "todos.html",
            name=session["name"],
            tasks=tasks,
            errors=[],
            input_title="",
            input_due_date="",
            edit_errors=errors,
            editing_todo_id=todo_id,
            edited_title=title,
            edited_due_date=due_date_input
        )

    # Update task in MySQL
    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                UPDATE todos
                SET title = %s, due_date = %s
                WHERE todo_id = %s AND user_id = %s
            """

            cursor.execute(
                sql,
                (
                    title,
                    parsed_due_date,
                    todo_id,
                    session["user_id"]
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("todos"))


# =====================================================
# 9. MARK TASK DONE / NOT DONE
# =====================================================

@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):

    # Check authentication
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get completion status
    is_done = request.form.get("is_done")

    # Validate completion status
    if is_done not in ("0", "1"):
        return "Invalid task status", 400

    # Connect to MySQL
    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                UPDATE todos
                SET is_done = %s
                WHERE todo_id = %s AND user_id = %s
            """

            cursor.execute(
                sql,
                (
                    int(is_done),
                    todo_id,
                    session["user_id"]
                )
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("todos"))


# =====================================================
# 10. DELETE A TO-DO TASK
# =====================================================

@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):

    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Connect to MySQL
    connection = get_db()

    try:
        with connection.cursor() as cursor:

            sql = """
                DELETE FROM todos
                WHERE todo_id = %s AND user_id = %s
            """

            cursor.execute(
                sql,
                (todo_id, session["user_id"])
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    return redirect(url_for("todos"))


if __name__ == "__main__":
    app.run(debug=True)
