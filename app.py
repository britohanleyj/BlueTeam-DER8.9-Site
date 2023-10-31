from flask import Flask, session, render_template, g, jsonify, request, redirect, url_for
from flask_wtf import FlaskForm
import time
from wtforms import IntegerField, StringField, SubmitField, DateTimeLocalField
import sqlite3
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)
DATABASE = 'identifier.sqlite'
app.config['STATIC_FOLDER'] = 'static'
app.config['SECRET_KEY'] = 'your_secret_key_here'

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

# class FilterForm(FlaskForm):
#     CompanyName = StringField('Company Name')
#     time = DateTimeLocalField('Time')
#     distance = IntegerField('Distance From Campus')
#     submit = SubmitField('Filter')

def getDataBaseFilters():
    pass




""" #student profile page
@app.route("/user-profile", methods=['GET'])
def accountPage():
    cur =  get_db()
    cursor = cur.cursor()
    cursor.execute("SELECT Name FROM student_users WHERE 1")
    username_result = cursor.fetchone()
    cursor.execute("SELECT XUID FROM student_users WHERE 1")
    banner_result = cursor.fetchone()

    # Extract tuple data
    username = username_result[0] if username_result else ''
    banner = banner_result[0] if banner_result else ''

    return render_template('student.html', username=username, banner=banner) """



@app.route('/login', methods=['GET','POST'])
def getLogin():
    if request.method == 'POST':
        user = request.form['username'] # Check the form for username
        if user == 'partner': # Two if statements for other attribute to be applied
            session['currentUser'] = user # The Users name
            return redirect(url_for('user'))
        else:
            return render_template('login.html') # Return login page if wrong
    else:
        if 'currentUser' in session:
            return redirect(url_for('getDatabase'))
        return render_template('login.html')

@app.route("/Home") #testing
def home():
        return render_template('home.html')

@app.route("/About_Us") #testing
def aboutUs():
        return render_template('aboutUs.html')

@app.route("/DER_Data") #testing
def dataDER():
        return render_template('dataDER.html')

@app.route("/Contact") #testing
def contact():
        return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    time.sleep(1)
    # Display a message within an h1 element
    message = "Submitted Successfully, redirecting in 3 seconds..."

    return f"<h1>{message}</h1><script>setTimeout(function(){{window.location.href = '{url_for('home')}'}}, 3000);</script>"
    
def loggedIn():
    if 'currentUser' in session:
        return True
    else:
        return False
    

@app.route("/logout")
def logout():
    session.pop('currentUser', None)
    return redirect(url_for('getLogin'))

if __name__ == '__main__':
    app.run(debug=True)
