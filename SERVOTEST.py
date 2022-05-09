import RPi.GPIO as GPIO
from time import sleep 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
import os
import os.path

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
    
with open('End_Time.txt','r') as y
    end_time = y.read()

time_start = int(start_time)
time_end = int(end_time)
recieved = int(recieved_file)
currentPosition =1 #POSITION_UPDATE	#to close the system, make currentPosition=POSITION_UPDATE.Input values for Demo Mode and make recieved a value inputted from website


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
POSITION_UPDATE=recieved
GPIO.cleanup
