import flask
from flask import Flask, render_template, request, flash, redirect
from wtforms import SubmitField, FileField
from werkzeug.utils import secure_filename
import os
import os.path
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = "Indoor Outdoor"


@app.route('/', methods=['GET', "POST"])
def index():
    flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
    flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
    flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    return render_template("index.HTML")


@app.route("/start", methods=["POST", "GET"])
def start():
    start_time = request.form['start_time_input']
    start_hour = get_hour(start_time)
    start_minutes = get_minutes(start_time)
    try:
        int(start_hour)
        int(start_minutes)
    except:
        flash("Enter Start Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "startTime")
        flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    else:
        if 0 <= int(start_hour) <= 24:
            with open('Start_Time_Hour.txt', 'w') as f:
                f.write(start_hour)
            if 0 <= int(start_minutes) <= 59:
                with open('Start_Time_Minute.txt', 'w') as x:
                    x.write(start_minutes)
            else:
                flash("Enter Start Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "startTime")
                flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            if 13 <= int(start_hour) <= 23:
                disp_time = str(int(start_hour) - 12) + ":" + start_minutes
                flash("Enter Start Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "PM", "startTime")
                flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(start_hour) == 24 or int(start_hour) == 0:
                disp_time = start_hour + ":" + start_minutes
                flash("Enter Start Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "AM", "startTime")
                flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(start_hour) == 12:
                disp_time = start_hour + ":" + start_minutes
                flash("Enter Start Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "PM", "startTime")
                flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            else:
                disp_time = start_hour + ":" + start_minutes
                flash("Enter Start Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "AM", "startTime")
                flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        else:
            flash("Enter Start Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "startTime")
            flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
            flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    print(start_hour)
    return render_template("index.HTML")


@app.route("/end", methods=["POST", "GET"])
def end():
    end_time = request.form['end_time_input']
    end_hour = get_hour(end_time)
    end_minutes = get_minutes(end_time)
    try:
        int(end_hour)
        int(end_minutes)
    except:
        flash("Enter End Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "endTime")
        flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    else:
        if 0 <= int(end_hour) <= 24:
            with open('End_Time_Hour.txt', 'w') as f:
                f.write(end_hour)
            if 0 <= int(end_minutes) <= 59:
                with open('End_Time_Minute.txt', 'w') as x:
                    x.write(end_minutes)
            else:
                flash("Enter End Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "endTime")
                flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            if 13 <= int(end_hour) <= 23:
                disp_time = str(int(end_hour) - 12) + ":" + end_minutes
                flash("Enter End Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "PM", "endTime")
                flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            elif int(end_hour) == 24 or int(end_hour) == 0:
                disp_time = "12:" + end_minutes
                flash("Enter End Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "AM", "endTime")
                flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockTy  pe")
            elif int(end_hour) == 12:
                disp_time = end_hour + ":" + end_minutes
                flash("Enter End Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "PM", "endTime")
                flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
            else:
                disp_time = end_hour + ":" + end_minutes
                flash("Enter End Hour (24 Hour Format HH:MM)\n Time Saved: " + disp_time + "AM", "endTime")
                flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
                flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        else:
            flash("Enter End Hour (24 Hour Format HH:MM)\nPLEASE ENTER 24 HOUR TIME ONLY", "endTime")
            flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
            flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    return render_template("index.HTML")


@app.route("/lock", methods=["POST", "GET"])
def lock():
    lock_type = request.form['lock_input'].lower()
    print(lock_type)
    if lock_type == "in" or lock_type == "out" or lock_type == "both" or lock_type == "locked":
        flash("Enter Lock Type: In, Out, Both, or Locked\n Lock Saved: " + lock_type.capitalize(), "lockType")
        flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
        flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
        if lock_type == "in":
            lock_number = 4
            with open('Lock_Type.txt', 'w') as f:
                f.write('4')
        elif lock_type == "out":
            lock_number = 3
            with open('Lock_Type.txt', 'w') as f:
                f.write('3')
        elif lock_type == "both":
            lock_number = 2
            with open('Lock_Type.txt', 'w') as f:
                f.write('2')
        elif lock_type == "locked":
            lock_number = 1
            with open('Lock_Type.txt', 'w') as f:
                f.write('1')
    else:
        flash("Please Enter ONLY: In, Out, Both, or Locked", "lockType")
        flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
        flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
    return render_template("index.HTML")


@app.route("/data", methods=["POST", "GET"])
def data():
    flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
    flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
    flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    if os.path.exists("Start_Time_Hour.txt") and os.path.exists("Start_Time_Minute.txt"):
        with open('Start_Time_Hour.txt', 'r') as f1:
            starthour = f1.read()
        with open('Start_Time_Minute.txt', 'r') as f2:
            startminute = f2.read()
        startTime = starthour + ':' + startminute
    else:
        flash("No Start Time Found! Enter a Start Time.", "message")
    if os.path.exists("End_Time_Hour.txt") and os.path.exists("End_Time_Minute.txt"):
        with open('End_Time_Hour.txt', 'r') as x1:
            endhour = x1.read()
        with open('End_Time_Minute.txt', 'r') as x2:
            endminute = x2.read()
        endTime = endhour + ':' + endminute
    else:
        flash("No End Time Found! Enter a End Time.", "message")
    if os.path.exists("Lock_Type.txt"):
        lockType = lock_name()
    else:
        flash("No Lock Type Found! Enter a Lock Type.", "message")
    if os.path.exists("Start_Time_Hour.txt") and os.path.exists("Start_Time_Minute.txt") and os.path.exists("End_Time_Hour.txt") and os.path.exists("End_Time_Minute.txt") and os.path.exists("Lock_Type.txt"):
        lockInfo = "The door's lock type is " + lockType + " from " + startTime + " Hours to " + endTime + " Hours."
        with open('Final.txt', 'w') as z:
            z.write(lockInfo)
        flash(lockInfo, "message")
    return render_template("index.HTML")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if check_extension(f.filename):
            f.save(secure_filename("image.png"))
            flash("File \"" + f.filename + "\" Successfully Uploaded", "upload")
        else:
            flash("Not a .png, .jpg, or .jpeg file!", "upload")
        flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
        flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        return render_template("index.HTML")


# placement button  
@app.route("/placement", methods=["POST", "GET"])
def placement():
    flash("Enter Start Hour (24 Hour Format HH:MM)", "startTime")
    flash("Enter End Hour (24 Hour Format HH:MM)", "endTime")
    flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
    if os.path.exists("Placement.txt"):
        with open('Placement.txt', 'r') as f:
            Placement = f.read()
        if Placement == "in":
            flash("Pet is inside", "placement")
        else:
            flash("Pet is outside", "placement")
    else:
        flash("Error Reading", "placement")
    return render_template("index.HTML")


def check_extension(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return True
    else:
        return False


def get_hour(time_in):
    return time_in[:-3]


def get_minutes(time_in):
    return time_in[-2:]


def lock_name():
    with open('Lock_Type.txt', 'r') as y:
        lockType = y.read()
    if int(lockType) == 1:
        return "Completely Locked"
    elif int(lockType) == 2:
        return "Open Both Ways"
    elif int(lockType) == 3:
        return "Out Only"
    else:
        return "In Only"


if 1 == 1:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
