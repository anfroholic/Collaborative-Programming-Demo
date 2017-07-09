This is a demo program for collaborative programming for evezor robotic arm
    Copyright (C) 2017  Andrew Wingate

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import RPi.GPIO as GPIO
import smbus
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(15,GPIO.IN)  #Red Button
GPIO.setup(17,GPIO.IN)  #Green Button
GPIO.setup(18,GPIO.IN)  #Blue Button
GPIO.setup(23,GPIO.IN)  #Finished Button

bus = smbus.SMBus(1)

#Set Encoder Offsets
SHOULDER_ZERO = 176.2
ELBOW_ZERO = 182.24
HAND_ZERO = 119.1
FRTNBIT = 16384

DEGREE_CONVERSION = .0219726563

#Set encoder adresses
HAND_ENCODER = 0x43
SHOULDER_ENCODER = 0x40
ELBOW_ENCODER = 0x42
ANGLE_MSB = 0xFF
ANGLE_LSB = 0XFE

##############
#Prepare file for output
fo = open ('gcodeoutput.gcode','w')
fo.write(';RGB PICK AND DROP\nM302\nG92 X-54.1 Y143.2\nG28 Z0\n')


RED_BOX = """;RED BUTTON
G1 Z80
M400
M106 S255
G04 P500
G1 Z170
G1 X112 Y114
M400
M107
G04 P500
"""

GREEN_BOX = """;GREEN BUTTON
G1 Z80
M400
M106 S255
G04 P500
G1 Z170
G1 X166 Y35
M400
M107
G04 P500
"""

BLUE_BOX = """;BLUE BUTTON
G1 Z80
M400
M106 S255
G04 P500
G1 Z170
G1 X162 Y94
M400
M107
G04 P500
"""

GET_CANDY = """;GET CANDY
G1 X8 Y-49.9
G1 Z110
M400
M106 S255
G1 Z150
G1 X-2 Y-90
M400
M107
G04 P500
G1 Z130
G1 X8 Y-49.9
G1 Z70 ;GET HEIGHT FOR CANDY
M400
M106 S255
G04 P500
G1 Z100
G1 X43 Y90
G1 Z70 ;GET HEIGHT FOR CANDY
M400
M107
G04 P500
G1 X-50 Y135 Z200
M84
"""




#get angles
def ReadAngle (Address, Zero):
    MSB = bus.read_byte_data(Address,ANGLE_MSB)
    MSB = MSB << 6
    LSB = bus.read_byte_data(Address,ANGLE_LSB)
    ANGLE_RAW = MSB + LSB
    

    ANGLE_RAW = ANGLE_RAW * DEGREE_CONVERSION
    
    ANGLE_RAW = (ANGLE_RAW - Zero) 
    ANGLE_RAW = round(ANGLE_RAW,2)
    return ANGLE_RAW



while(True):
    #HAND = ReadAngle(HAND_ENCODER,HAND_ZERO)
    ELBOW = ReadAngle(ELBOW_ENCODER,ELBOW_ZERO)
    SHOULDER = ReadAngle(SHOULDER_ENCODER,SHOULDER_ZERO)

    if(GPIO.input(15) ==0):
        print("RED Button")
        fo.write('G1 X')
        fo.write(str(SHOULDER))
        fo.write(' Y')
        fo.write(str(ELBOW))
        fo.write('\n')
        fo.write(RED_BOX)
        time.sleep(1)
    if(GPIO.input(17) ==0):
        print("GREEN Button")
        fo.write('G1 X')
        fo.write(str(SHOULDER))
        fo.write(' Y')
        fo.write(str(ELBOW))
        fo.write('\n')
        fo.write(GREEN_BOX)
        time.sleep(1)
    if(GPIO.input(18) ==0):
        print("BLUE Button")
        fo.write('G1 X')
        fo.write(str(SHOULDER))
        fo.write(' Y')
        fo.write(str(ELBOW))
        fo.write('\n')
        fo.write(BLUE_BOX)
        time.sleep(1)
    if(GPIO.input(23) ==0):
        print("CLOSE PROGRAM")
        fo.write(GET_CANDY)
        fo.close()
        exit()
        time.sleep(1)


    time.sleep(.1)
    
    
