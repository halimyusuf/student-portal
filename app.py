from flask import Flask, render_template, url_for, request, current_app
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import time
import os
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'studentportal'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

"""
***query to create table
CREATE TABLE studentportal.student(id int NOT NULL auto_increment, firstname varchar(255) NOT NULL, lastname varchar(255) NOT NULL, middlename varchar(255) NOT NULL, gender Varchar(10) check (gender in ('Female','Male')), address varchar(255) NOT NULL, state_of_origin varchar(255) NOT NULL, local_govt varchar(255) NOT NULL, status varchar(50) NOT NULL, next_of_kin varchar(255) NOT NULL, jamb_score int NOT NULL, email varchar(255) NOT NULL, dob varchar(30) NOT NULL, phone_number varchar(15) NOT NULL, image varchar(255), PRIMARY KEY (id));

***set default value for status
ALTER TABLE studentportal.student ALTER status SET DEFAULT 'undecided'

***query to insert in table
INSERT INTO studentportal.student(firstname, lastname, middlename, gender, address, state_of_origin, local_govt, status, next_of_kin, jamb_score, email, dob, phone_number) values('musty', 'becky', 'lander', 'Male', '4, decent Street', 'benin state', 'benin city', 'undecided', 'james bond', 300, 'palis@gmail.com', '12-03-2012', '09037739039');

"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students/portal')
def portal():
    return render_template('portal.html')

@app.route('/admin/dashboard')
def dashboard():
    # db conn
    conn = mysql.get_db()
    cur = conn.cursor()
    # fetch all students data
    cur.execute('SELECT * FROM student')
    res = cur.fetchall()
    return render_template('dashboard.html', students=res)

@app.route('/admin/students/<id>')
def get_student(id):
    # db conn
    conn = mysql.get_db()
    cur = conn.cursor()
    # fetch a student data
    cur.execute('SELECT * FROM student WHERE id=%s', id)
    res = cur.fetchall()
    if not res[0]['image']:
        res[0]['image'] = 'homepage.svg'
    return render_template('student.html', student=res[0])

@app.route('/students/new', methods=["POST"])
def new_student():
    data = dict(request.form)
    # save image file with current time in ms
    data['image'] = str(round(time.time() * 1000)) + '.' + data['image'].split('.')[-1]
    filepath = os.path.join(current_app.root_path, 'static/images/' + data['image'])
    image = request.files['file']
    if image:
        image.save(filepath)
    cols = ['firstname', 'lastname', 'middlename', 'gender', 'address', 'state_of_origin', 'local_govt', 'next_of_kin', 'jamb_score', 'email', 'dob', 'phone_number', 'image']
    vals = []
    for a in cols:
        vals.append(data[a])
    # db conn
    conn = mysql.get_db()
    cur = conn.cursor()
    # query to insert new data
    cur.execute("INSERT INTO studentportal.student(firstname, lastname, middlename, gender, address, state_of_origin, local_govt, next_of_kin, jamb_score, email, dob, phone_number, image) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
    conn.commit()
    cur.close()
    return json.dumps("SUCCESS")

@app.route('/student/status/<id>', methods=['POST'])
def update_status(id):
    status = request.get_json()['status']
    # db conn
    conn = mysql.get_db()
    cur = conn.cursor()
    # query to update student status
    cur.execute("UPDATE studentportal.student SET status=%s WHERE id=%s", (status, id))
    conn.commit()
    cur.close()
    return "Success"


if __name__ == '__main__':
    app.run(debug=True)