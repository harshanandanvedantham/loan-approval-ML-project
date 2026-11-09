
import os
import re
import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from mysql.connector import IntegrityError, Error

from database.database import get_db_connection
from explainability import explain_application, model


# ==========================================
# 1. FLASK APPLICATION CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "development-key-change-before-deployment"
)

# Use secure cookie settings when deploying over HTTPS.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("FLASK_HTTPS", "0") == "1"
)


# ==========================================
# 2. MODEL CONFIGURATION
# ==========================================

FEATURE_COLUMNS = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value"
]

print("LOANWISE ML model loaded successfully!")


# ==========================================
# 3. DATABASE CLEANUP HELPER
# ==========================================

def close_database(connection=None, cursor=None):

    if cursor is not None:
        try:
            cursor.close()
        except Error:
            app.logger.exception("Error closing database cursor")

    if connection is not None:
        try:
            if connection.is_connected():
                connection.close()
        except Error:
            app.logger.exception("Error closing database connection")


# ==========================================
# 4. HOME ROUTE
# ==========================================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("register"))


# ==========================================
# 5. USER REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Basic validation
        if not all([full_name, email, password, confirm_password]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if len(full_name) > 100:
            flash("Name must be 100 characters or fewer.", "error")
            return redirect(url_for("register"))

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("register"))

        if len(email) > 150:
            flash("Email address is too long.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        # Secure password hashing
        password_hash = generate_password_hash(password)

        connection = None
        cursor = None

        try:

            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO users
                (full_name, email, password_hash)
                VALUES (%s, %s, %s)
            """

            values = (
                full_name,
                email,
                password_hash
            )

            cursor.execute(query, values)
            connection.commit()

            flash(
                "Account created successfully! You can now log in.",
                "success"
            )

            return redirect(url_for("login"))

        except IntegrityError as error:

            if connection:
                connection.rollback()

            if error.errno == 1062:
                flash(
                    "An account with this email already exists.",
                    "error"
                )
            else:
                app.logger.exception("Registration integrity error")
                flash(
                    "Unable to create your account right now.",
                    "error"
                )

        except Error:

            if connection:
                connection.rollback()

            app.logger.exception("Database error during registration")
            flash("Database error. Please try again.", "error")

        except Exception:

            if connection:
                connection.rollback()

            app.logger.exception("Unexpected registration error")
            flash("Something went wrong. Please try again.", "error")

        finally:
            close_database(connection, cursor)

    return render_template("register.html")


# ==========================================
# 6. USER LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter your email and password.", "error")
            return redirect(url_for("login"))

        connection = None
        cursor = None

        try:

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    user_id,
                    full_name,
                    email,
                    password_hash
                FROM users
                WHERE email = %s
            """

            cursor.execute(query, (email,))
            user = cursor.fetchone()

            # Verify credentials
            if user and check_password_hash(
                user["password_hash"],
                password
            ):

                session.clear()

                session["user_id"] = user["user_id"]
                session["user_name"] = user["full_name"]
                session["user_email"] = user["email"]

                flash(
                    "Welcome back, " + user["full_name"] + "!",
                    "success"
                )

                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "error")

        except Error:

            app.logger.exception("Login database error")

            flash(
                "Unable to log in right now. Please try again.",
                "error"
            )

        except Exception:

            app.logger.exception("Unexpected login error")

            flash(
                "Something went wrong. Please try again.",
                "error"
            )

        finally:
            close_database(connection, cursor)

    return render_template("login.html")


# ==========================================
# 7. USER LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("login"))


# ==========================================
# 8. USER DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        user_id = session["user_id"]

        # Application statistics
        cursor.execute("""
            SELECT
                COUNT(*) AS total_applications,

                COALESCE(
                    SUM(
                        CASE
                            WHEN predicted_status = 'Approved'
                            THEN 1 ELSE 0
                        END
                    ), 0
                ) AS approved_applications,

                COALESCE(
                    SUM(
                        CASE
                            WHEN predicted_status = 'Rejected'
                            THEN 1 ELSE 0
                        END
                    ), 0
                ) AS rejected_applications

            FROM loan_applications
            WHERE user_id = %s
        """, (user_id,))

        stats = cursor.fetchone()

        # Recent applications
        cursor.execute("""
            SELECT
                application_id,
                predicted_status,
                predicted_probability,
                created_at

            FROM loan_applications

            WHERE user_id = %s

            ORDER BY created_at DESC

            LIMIT 5
        """, (user_id,))

        recent_applications = cursor.fetchall()

        return render_template(
            "dashboard.html",
            user_name=session["user_name"],
            stats=stats,
            recent_applications=recent_applications
        )

    except Error:

        app.logger.exception("Dashboard database error")

        flash("Unable to load dashboard data.", "error")

        return render_template(
            "dashboard.html",
            user_name=session.get("user_name", "User"),
            stats={
                "total_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0
            },
            recent_applications=[]
        )

    except Exception:

        app.logger.exception("Unexpected dashboard error")

        flash("Something went wrong while loading your dashboard.", "error")

        return render_template(
            "dashboard.html",
            user_name=session.get("user_name", "User"),
            stats={
                "total_applications": 0,
                "approved_applications": 0,
                "rejected_applications": 0
            },
            recent_applications=[]
        )

    finally:
        close_database(connection, cursor)


# ==========================================
# 9. NEW LOAN APPLICATION
# ==========================================

@app.route("/new-application", methods=["GET"])
def new_application():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))

    return render_template("application.html")


# ==========================================
# 10. LOAN PREDICTION AND EXPLAINABILITY
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        # --------------------------------------
        # COLLECT FORM DATA
        # --------------------------------------

        input_data = {
            "no_of_dependents": int(request.form["no_of_dependents"]),
            "education": request.form["education"],
            "self_employed": request.form["self_employed"],
            "income_annum": int(request.form["income_annum"]),
            "loan_amount": int(request.form["loan_amount"]),
            "loan_term": int(request.form["loan_term"]),
            "cibil_score": int(request.form["cibil_score"]),
            "residential_assets_value": int(
                request.form["residential_assets_value"]
            ),
            "commercial_assets_value": int(
                request.form["commercial_assets_value"]
            ),
            "luxury_assets_value": int(
                request.form["luxury_assets_value"]
            ),
            "bank_asset_value": int(
                request.form["bank_asset_value"]
            )
        }

        # --------------------------------------
        # VALIDATE CATEGORICAL INPUTS
        # --------------------------------------

        if input_data["education"] not in [
            "Graduate",
            "Not Graduate"
        ]:
            raise ValueError("Invalid education selection.")

        if input_data["self_employed"] not in [
            "Yes",
            "No"
        ]:
            raise ValueError("Invalid employment selection.")

        # --------------------------------------
        # VALIDATE NUMERIC INPUTS
        # --------------------------------------

        if not 0 <= input_data["no_of_dependents"] <= 10:
            raise ValueError("Dependents must be between 0 and 10.")

        if input_data["income_annum"] <= 0:
            raise ValueError("Annual income must be positive.")

        if input_data["loan_amount"] <= 0:
            raise ValueError("Loan amount must be positive.")

        if not 1 <= input_data["loan_term"] <= 50:
            raise ValueError("Loan term must be between 1 and 50 years.")

        if not 300 <= input_data["cibil_score"] <= 900:
            raise ValueError("CIBIL score must be between 300 and 900.")

        asset_fields = [
            "residential_assets_value",
            "commercial_assets_value",
            "luxury_assets_value",
            "bank_asset_value"
        ]

        if any(input_data[field] < 0 for field in asset_fields):
            raise ValueError("Asset values cannot be negative.")

        # --------------------------------------
        # GENERATE ML AND SHAP EXPLANATIONS
        # --------------------------------------

        explanation_result = explain_application(input_data)

        prediction = str(explanation_result["prediction"]).strip()

        predicted_probability = float(
            explanation_result["confidence"]
        )

        # --------------------------------------
        # CONVERT PREDICTION INTO DISPLAY STATUS
        # --------------------------------------

        prediction_text = prediction.lower()

        if prediction_text == "approved":

            predicted_status = "Approved"

        elif prediction_text == "rejected":

            predicted_status = "Rejected"

        else:

            raise ValueError(
                "Unexpected prediction label. Check your model classes."
            )

        if not 0 <= predicted_probability <= 100:
            raise ValueError("Invalid model-predicted probability.")

        # --------------------------------------
        # IDENTIFY MODEL
        # --------------------------------------

        model_name = (
            type(model.steps[-1][1]).__name__
            if hasattr(model, "steps")
            else type(model).__name__
        )

        # --------------------------------------
        # CONVERT EXPLANATION TO JSON
        # --------------------------------------

        explanation_json = json.dumps(explanation_result)

        # --------------------------------------
        # SAVE APPLICATION TO MYSQL
        # --------------------------------------

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO loan_applications (

                user_id,
                no_of_dependents,
                education,
                self_employed,
                income_annum,
                loan_amount,
                loan_term,
                cibil_score,
                residential_assets_value,
                commercial_assets_value,
                luxury_assets_value,
                bank_asset_value,
                predicted_status,
                predicted_probability,
                model_name,
                explanation

            )

            VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        values = (
            session["user_id"],
            input_data["no_of_dependents"],
            input_data["education"],
            input_data["self_employed"],
            input_data["income_annum"],
            input_data["loan_amount"],
            input_data["loan_term"],
            input_data["cibil_score"],
            input_data["residential_assets_value"],
            input_data["commercial_assets_value"],
            input_data["luxury_assets_value"],
            input_data["bank_asset_value"],
            predicted_status,
            predicted_probability,
            model_name,
            explanation_json
        )

        cursor.execute(query, values)

        connection.commit()

        application_id = cursor.lastrowid

        # --------------------------------------
        # DISPLAY RESULT
        # --------------------------------------

        return render_template(
            "result.html",
            status=predicted_status,
            probability=predicted_probability,
            application_id=application_id,
            explanation=explanation_result
        )

    except (ValueError, KeyError) as error:

        if connection:
            connection.rollback()

        flash(str(error), "error")

        return redirect(url_for("new_application"))

    except Error:

        if connection:
            connection.rollback()

        app.logger.exception("Database error during prediction")

        flash(
            "Unable to save your application. Please try again.",
            "error"
        )

        return redirect(url_for("new_application"))

    except Exception:

        if connection:
            connection.rollback()

        app.logger.exception("Prediction processing error")

        flash(
            "Something went wrong while processing your application.",
            "error"
        )

        return redirect(url_for("new_application"))

    finally:
        close_database(connection, cursor)

@app.route("/application-history")
def application_history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                application_id,
                loan_amount,
                cibil_score,
                predicted_status,
                predicted_probability,
                created_at
            FROM loan_applications
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (session["user_id"],))

        applications = cursor.fetchall()

        return render_template(
            "history.html",
            applications=applications
        )

    except Exception as error:
        app.logger.exception("Application history error")
        flash("Unable to load application history.", "error")
        return redirect(url_for("dashboard"))

    finally:
        close_database(connection, cursor)
        
@app.route("/my-profile")
def my_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                user_id,
                full_name,
                email,
                created_at
            FROM users
            WHERE user_id = %s
        """, (session["user_id"],))

        user = cursor.fetchone()

        if not user:
            session.clear()
            return redirect(url_for("login"))

        cursor.execute("""
            SELECT
                COUNT(*) AS total_applications,
                COALESCE(SUM(predicted_status = 'Approved'), 0)
                    AS approved_applications,
                COALESCE(SUM(predicted_status = 'Rejected'), 0)
                    AS rejected_applications
            FROM loan_applications
            WHERE user_id = %s
        """, (session["user_id"],))

        stats = cursor.fetchone()

        return render_template(
            "profile.html",
            user=user,
            stats=stats
        )

    except Exception:
        app.logger.exception("Profile loading error")
        flash("Unable to load your profile.", "error")
        return redirect(url_for("dashboard"))

    finally:
        close_database(connection, cursor)

# ==========================================
# 11. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
