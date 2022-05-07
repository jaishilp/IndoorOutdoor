import flask
from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from werkzeug.utils import secure_filename
import os
import os.path
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = "Indoor Outdoor"


class UploadFileForm(FlaskForm):
    file = FileField("File", vailidators=InputRequired())
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
def index():
    flash("Enter Start Hour (24 Hour Format)", "startTime")
    flash("Enter End Hour (24 Hour Format)", "endTime")
    flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    return render_template("index.HTML")


@app.route("/start", methods=["POST", "GET"])
def start():
    start_time = request.form['start_time_input']
    try:
        int(start_time)
    except:
        flash("Enter Start Hour (24 Hour Format)\nPLEASE ENTER 24 HOUR TIME ONLY", "startTime")
        flash("Enter End Hour (24 Hour Format)", "endTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    else:
        if 0 <= int(start_time) <= 24:
            with open('Start_Time.txt', 'w') as f:
                f.write(start_time)
            if 13 <= int(start_time) <= 23:
                disp_time = int(start_time) - 12
                flash("Enter Start Hour (24 Hour Format)\n Time Saved: " + str(disp_time) + "PM", "startTime")
                flash("Enter End Hour (24 Hour Format)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(start_time) == 24 or int(start_time) == 0:
                flash("Enter Start Hour (24 Hour Format)\n Time Saved: " + "12AM", "startTime")
                flash("Enter End Hour (24 Hour Format)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(start_time) == 12:
                flash("Enter Start Hour (24 Hour Format)\n Time Saved: " + "12PM", "startTime")
                flash("Enter End Hour (24 Hour Format)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            else:
                flash("Enter Start Hour (24 Hour Format)\n Time Saved: " + start_time + "AM", "startTime")
                flash("Enter End Hour (24 Hour Format)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        else:
            flash("Enter Start Hour (24 Hour Format)\nPLEASE ENTER 24 HOUR TIME ONLY", "startTime")
            flash("Enter End Hour (24 Hour Format)", "endTime")
            flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    print(start_time)
    return render_template("index.HTML")


@app.route("/end", methods=["POST", "GET"])
def end():
    end_time = request.form['end_time_input']
    try:
        int(end_time)
    except:
        flash("Enter End Hour (24 Hour Format)\nPLEASE ENTER 24 HOUR TIME ONLY", "endTime")
        flash("Enter Start Hour (24 Hour Format)", "startTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    else:
        if 0 <= int(end_time) <= 24:
            with open('End_Time.txt', 'w') as f:
                f.write(end_time)
            if 13 <= int(end_time) <= 23:
                disp_time = int(end_time) - 12
                flash("Enter End Hour (24 Hour Format)\n Time Saved: " + str(disp_time) + "PM", "endTime")
                flash("Enter Start Hour (24 Hour Format)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(end_time) == 24 or int(end_time) == 0:
                flash("Enter End Hour (24 Hour Format)\n Time Saved: " + "12AM", "endTime")
                flash("Enter Start Hour (24 Hour Format)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockTy  pe")
            elif int(end_time) == 12:
                flash("Enter End Hour (24 Hour Format)\n Time Saved: " + "12PM", "endTime")
                flash("Enter Start Hour (24 Hour Format)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            else:
                flash("Enter End Hour (24 Hour Format)\n Time Saved: " + end_time + "AM", "endTime")
                flash("Enter Start Hour (24 Hour Format)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        else:
            flash("Enter End Hour (24 Hour Format)\nPLEASE ENTER 24 HOUR TIME ONLY", "endTime")
            flash("Enter Start Hour (24 Hour Format)", "startTime")
            flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    return render_template("index.HTML")


@app.route("/lock", methods=["POST", "GET"])
def lock():
    lock_type = request.form['lock_input'].lower()
    print(lock_type)
    if lock_type == "in" or lock_type == "out" or lock_type == "both" or lock_type == "locked":
        flash("Enter Lock Type: In, Out, Both, or Locked\n Lock Saved: " + lock_type.capitalize(), "lockType")
        flash("Enter Start Hour (24 Hour Format)", "startTime")
        flash("Enter End Hour (24 Hour Format)", "endTime")
        with open('Lock_Type.txt', 'w') as f:
            f.write(lock_type)
    else:
        flash("Please Enter ONLY: In, Out, Both, or Locked", "lockType")
        flash("Enter Start Hour (24 Hour Format)", "startTime")
        flash("Enter End Hour (24 Hour Format)", "endTime")
    return render_template("index.HTML")


@app.route("/data", methods=["POST", "GET"])
def data():
    flash("Enter Start Hour (24 Hour Format)", "startTime")
    flash("Enter End Hour (24 Hour Format)", "endTime")
    flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    if os.path.exists("Start_Time.txt"):
        with open('Start_Time.txt', 'r') as f:
            startTime = f.read()
    else:
        flash("No Start Time Found! Enter a Start Time.", "message")
    if os.path.exists("End_Time.txt"):
        with open('End_Time.txt', 'r') as x:
            endTime = x.read()
    else:
        flash("No End Time Found! Enter a End Time.", "message")
    if os.path.exists("Lock_Type.txt"):
        with open('Lock_Type.txt', 'r') as y:
            lockType = y.read()
    else:
        flash("No Lock Type Found! Enter a Lock Type.", "message")
    if os.path.exists("Start_Time.txt") and os.path.exists("End_Time.txt") and os.path.exists("Lock_Type.txt"):
        lockInfo = "The door's lock type is " + lockType + " from " + startTime + "00 Hours to " + endTime + "00 Hours."
        with open('Final.txt', 'w') as z:
            z.write(lockInfo)
        flash(lockInfo, "message")
    return render_template("index.HTML")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename("image.jpg"))
        flash("Enter Start Hour (24 Hour Format)", "startTime")
        flash("Enter End Hour (24 Hour Format)", "endTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        return render_template("index.HTML")


def get_minutes(minutes):
    if time

if 1 == 1:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
