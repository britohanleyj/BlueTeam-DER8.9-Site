from flask import Flask, session, render_template, g, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import time
import sqlite3
from markupsafe import escape

app = Flask(__name__)
DATABASE = 'identifier.sqlite'
app.config['STATIC_FOLDER'] = 'static'
app.config['SECRET_KEY'] = 'oooits secretz'

# creates connection to database
# to use database just run var = get_db().execute(You SQL code as str)
# example below in my opportunityDatabase page
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# closes the database; really never used but nice to have just in case
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/',methods =['GET', 'POST'])
def hello_world(): 
    return redirect(url_for('home'))


def getDataBaseFilters():
    pass


@app.route('/login', methods=['GET', 'POST'])
def getLogin():
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form

        # Check if the provided email and password exist in the database
        user = get_user_from_database(email, password)

        if user:
            session['user_id'] = user[0]  # Set the user's ID in the session
            session['user_e'] = user[1]  # Set the user's email in the session
            if session['user_id'] == 2:
                return redirect(url_for('admin'))
            else: 
                return redirect(url_for('home'))
        else:
            return render_template('login.html', login_error=True)

    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route("/Home") 
def home():
        return render_template('home.html')


@app.route("/About_Us") 
def aboutUs():
        return render_template('aboutUs.html')


@app.route("/DER_Data")
def dataDER():
    if loggedIn():
        if session['user_id'] == 2:
            return render_template('dataDER.html')
    return redirect(url_for('noData'))


@app.route("/Contact") 
def contact():
        return render_template('contact.html')


@app.route('/submit', methods=['POST'])
def submit():
    time.sleep(1)
    message = "Submitted Successfully, redirecting in 3 seconds..."

    return f"<h1>{message}</h1><script>setTimeout(function(){{window.location.href = '{url_for('home')}'}}, 3000);</script>"


@app.route('/admin')
def admin():
    if loggedIn():
        if session['user_id'] == 2:
            return render_template('admin.html')
        else:
            return redirect(url_for('home'))
    else:
        return render_template('not_logged_in.html')
    

@app.route('/dashboard')
def dashboard():
    if loggedIn():
        return "Dashboard Page"
    else:
        return render_template('not_logged_in.html')
@app.route('/contact_submissions')
def contact_submissions():
    if loggedIn():
        return "Contact Submissions Page"
    else:
        return render_template('not_logged_in.html')

@app.route('/registered_users')
def registered_users():
    if loggedIn():
        return "Registered Users Page"
    else:
        return render_template('not_logged_in.html')

    
def loggedIn():
    if 'user_id' in session:
        return True
    else:
        return False

# def add_user_to_database(password):
#     hashed_password = generate_password_hash(password)
#     print (hashed_password)



def get_user_from_database(email, password):
    db = get_db()
    cursor = db.cursor()

    # Select the user based on the provided email
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    print (user)

    if user:
        # Index 1 corresponds to the 'email' column, and Index 2 corresponds to the 'password' column
        db_id = user[0]
        db_email = user[1]
        db_password = user[2]
        print (user)
        # Verify the hashed password
        if db_email == email and check_password_hash(db_password, password):
            # Return the user tuple or just the user ID
            return user

    return None

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route("/noData")
def noData():
    return render_template('noData.html')
    
@app.route('/update_user_email')
def update_user_email_route():
    # Specify the old email and the new email
    old_email = 'admin@cfc.local'
    new_email = 'admin@cfc.com'

    # Get the database connection
    db = get_db()
    cursor = db.cursor()

    # Check if the user with the old email exists in the database
    cursor.execute("SELECT id FROM users WHERE email = ?", (old_email,))
    user_id = cursor.fetchone()

    if user_id:
        # Update the email for the user with the old email
        cursor.execute("UPDATE users SET email = ? WHERE email = ?", (new_email, old_email))
        db.commit()
        return f"Email updated successfully for user with ID {user_id[0]}."

    return "User not found with the old email."
if __name__ == '__main__':
    app.run(debug=True)
