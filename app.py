import flask
from flask import Flask, render_template, request, flash, redirect
from wtforms import SubmitField, FileField
from werkzeug.utils import secure_filename
import os
import os.path
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import RPi.GPIO as GPIO
from time import sleep 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

app = Flask(__name__)
app.secret_key = "Indoor Outdoor"


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
    servo_run()
    return render_template("index.HTML")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if checkext(f.filename):
            f.save(secure_filename("image.png"))
            flash("File \"" + f.filename + "\" Successfully Uploaded", "upload")
        else:
            flash("Not a .png, .jpg, or .jpeg file!", "upload")
        flash("Enter Start Hour (24 Hour Format)", "startTime")
        flash("Enter End Hour (24 Hour Format)", "endTime")
        flash("Enter Lock Type: In, Out, Both, or Locked", "lockType")
        return render_template("index.HTML")


# placement button  
@app.route("/placement", methods=["POST", "GET"])
def placement():
    flash("Enter Start Hour (24 Hour Format)", "startTime")
    flash("Enter End Hour (24 Hour Format)", "endTime")
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


def checkext(filename):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return True
    else:
        return False
        
def servo_run():
    
    pwm=GPIO.PWM(17,50) 
    pwm.start(0)
    #NOTE: If 
    #creates the string and calls the serial address
    #ser= serial.Serial('/dev/ttyACM0', 9600, timeout=5)

    #read from the arduino
    #input_str= ser.readline()
    #print ( input_str.decode("utf-8").strip() )

    # Input a number between 1 to 4 for recieved and currentPosition

    with open ('Lock_Type.txt','r') as f:
        recieved_file= f.read() 
        
    with open('Start_Time.txt','r') as x:
        start_time = x.read()
        
    with open('End_Time.txt','r') as y:
        end_time = y.read()

    time_start = int(start_time)
    time_end = int(end_time)
    recieved = int(recieved_file)
    POSITION_UPDATE = 3
    currentPosition = POSITION_UPDATE	#to close the system, make currentPosition=POSITION_UPDATE.Input values for Demo Mode and make recieved a value inputted from website


    movement=recieved-currentPosition #Determine the number of lock spaces need to move

    # Website Lock Codes

    L_1 = 1 #Fully Locked Position
    R_1 = 1
    L_2 = 2 #Fully Opened Position
    R_2 = 2
    L_3 = 3 #One Way Out Position
    R_3 = 3
    L_4 = 4 #One Way In Position
    R_4 = 4

    direction = 0
    x = 0

    for x in range(1):
        
        #if movement == 0:
            #rint("PICK A DIFFERNT LOCK	TYPE")

        
        if movement <	0:
            pwm.ChangeDutyCycle(1.5) # (counter-clockwise) left (-90*)
            sleep(8* abs(movement))
    else:
        
         if movement >	0:	
             pwm.ChangeDutyCycle(12.5) # (clockwise) (90*) right
             sleep(8* abs(movement))
        
        
       #Clockwise = right movement (90*)
       #Counterclockwise = left Movement (-90*)
     

    pwm.ChangeDutyCycle(0) #stop

    pwm.stop 
    POSITION_UPDATE = recieved
    GPIO.cleanup             
        

if 1 == 1:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
