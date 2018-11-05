import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import csv
import sqlite3
import datetime
from datetime import datetime
import time
import random
from tkinter import filedialog
from collections import Counter
import math
from PIL import Image, ImageTk

import serial

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

from matplotlib import pyplot as plt
from scipy.integrate import simps
from scipy.integrate import trapz
import scipy.signal as signal
from scipy import *
import numpy as np
from matplotlib.pyplot import *
from scipy.signal import find_peaks
import plotly.plotly as py
import plotly.tools as tls

ArduinoSerial = serial.Serial('COM11', 115200, timeout = 0.1)
time.sleep(2)


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)
conn = sqlite3.connect('tutorial.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS DATASET(ID INTEGER PRIMARY KEY, Designation_text TEXT, Description TEXT)')
conn.commit()
c.execute('CREATE TABLE IF NOT EXISTS Data(ID INTEGER PRIMARY KEY, timestamp TIMESTAMP, XVALUE REAL, YVALUE REAL, ZVALUE REAL, DATASETID INTEGER)')
conn.commit()

c.execute('CREATE TABLE IF NOT EXISTS Sequence(ID INTEGER PRIMARY KEY, timestamp TIMESTAMP, EventID INTEGER)')
conn.commit()

mean = 1015.4993514915694

style.use("ggplot")

list1= []

f = Figure()
a = f.add_subplot(111)

exchange = "BTC-e"
DatCounter = 9000
programName = "btce"

#**********************************************************************
def set_rate():
    #global RateTime;
    #RateTime = tk.DoubleVar();
    
    if var.get()=='6.25':
     #   RateTime = 1/6.25
        ArduinoSerial.write(b'a') 

    if var.get()=='12.5':
      # RateTime = 1/12.5
       ArduinoSerial.write(b'b')

    if var.get()=='25':
       # RateTime = 1/25
        ArduinoSerial.write(b'c')

    if var.get()=='50':
        #RateTime = 1/50
        ArduinoSerial.write(b'd')

    if var.get()=='100':
       # RateTime = 1/100
        ArduinoSerial.write(b'e')

    if var.get()=='200':
        #RateTime = 1/200
        ArduinoSerial.write(b'f')

    if var.get()=='400':
      # RateTime = 1/400
       ArduinoSerial.write(b'g')

    if var.get()=='800':
       # RateTime = 1/800
        ArduinoSerial.write(b'h')

    if var.get()=='1600':
       # RateTime = 1/1600
        ArduinoSerial.write(b'i')

    if var.get()=='3200':
       # RateTime = 1/3200
        ArduinoSerial.write(b'j')
     

def set_range():
    if range1.get()=='0.5':        
        ArduinoSerial.write(b'k')
        #print(0.5)

    if range1.get()=='1':
       #print(1)
       ArduinoSerial.write(b'l')

    if range1.get()=='2':
        #print(2)
        ArduinoSerial.write(b'm')

    if range1.get()=='4':
        #print(4)
        ArduinoSerial.write(b'n')

def set_flag():
    
    if flag.get()=='Overwrite when buffer full':
        ArduinoSerial.write(b'o')

    if flag.get()=='Stop writing when buffer full':
        ArduinoSerial.write(b'p')    


#**********************************************************************
def downloadAll():
        
    ArduinoSerial.write(b'4')
    downloadFunction()
    time.sleep(1)
       

def downloadFunction():
    time1= []
    x1= []
    y1= []
    z1= []
    val = ""
    previousRead =""
    value = 0
    count= 0
    previous = 0
    while True:
          read = ArduinoSerial.readline().decode('utf-8')
          #print(read)
          val = val + str(read)
          if(read == "" and previous == "" ):
              count = count+1
              if(count ==4):
                  break
          else:
              count = 0          
          previous = read
    
    val = str(val)
    byteData = val.splitlines()
    if(byteData[0] == "Stop reading nothing left to read"):
        print("Stop reading nothing left to read")
    else:        
        for data_in in byteData:
            print(data_in)
            numCommas = data_in.count(',')
            if(numCommas == 3):
                time2, x2, y2, z2 = data_in.split(",")            
                numDash = time2.count('-')
                numSemis = time2.count(':')
                numSpace = time2.count(' ')
                if(numDash == 2 and numSemis==2 and numSpace==1):
                    time3 = str(time2)
                    if time3[0]=='1' and time3[1]=='8':
                        time1.append(time2)
                        x1.append(float(x2))
                        y1.append(float(y2))
                        z1.append(float(z2))
    
            
        designation = str(mystring4.get())
        descrip = str(mystring5.get())
        

        c.execute("INSERT INTO DATASET(Designation_text, Description) VALUES(?, ?)",(designation, descrip))
        conn.commit()
        iden = c.lastrowid
           
        for i in range(len(time1)):
            Timestamp = '20'+str(time1[i])
            Timestamp = datetime.fromisoformat(Timestamp)
            Xvalue = float(x1[i])
            Yvalue = float(y1[i])
            Zvalue = float(z1[i])
            DatasetID = iden
            c.execute("INSERT INTO Data(Timestamp, XVALUE, YVALUE, ZVALUE, DatasetID) VALUES (?, ?, ?, ?, ?)", (Timestamp, Xvalue, Yvalue, Zvalue, iden))       
            conn.commit()

'''seq = getSeq(iden)
        start, string, array1, peaks = whereStart(seq)
        time = getTimestamp(iden,peaks)'''
        
   
def downloadLatest():
    ArduinoSerial.write(b'3')
    downloadFunction()
    time.sleep(1)


#*********************************************************************
def start_sampling():
   ArduinoSerial.write(b'1')
   #print(ArduinoSerial.readline().decode('utf-8').strip())
   #time.sleep(1)
   
def stop_sampling():
   ArduinoSerial.write(b'2')
   #print(ArduinoSerial.readline().decode('utf-8').strip())
   #time.sleep(1)

   
#*********************************************************************
def led_on():
    ArduinoSerial.write(b'1') # set Arduino output pin 13 high
    
def led_off():
    ArduinoSerial.write(b'0') # set Arduino output pin 13 low
    while ArduinoSerial.in_waiting :
        print(ArduinoSerial.readline().decode('utf-8').strip())# get Arduino output pin 13 status
 

#*********************************************************************
def setDate_Time():
    now = datetime.datetime.now()
 
    print( "Current date and time using strftime:")
    print( now.strftime("%Y-%m-%d %H:%M"))    
    ArduinoSerial.write(b's')

#*********************************************************************


def donothing():
    print("do nothing")
    
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Download")

       
    popup.geometry("500x400")
    #popup.configure(background='white')
    popup.mainloop()
    
#=================================================
def Waiting():
    previous = 0
    count = 0
    while True:
          read = ArduinoSerial.readline().decode('utf-8')
          if(read != ""):
              print(read)
          if(read == "" and previous == "" ):
              count = count+1
              if(count ==4):
                  break
          else:
              count = 0          
          previous = read
def applySettings():
    set_rate();
    Waiting()
    #print(ArduinoSerial.readline().decode('utf-8').strip())# get Arduino output pin 13 status
def applySettings1():
    set_range();
    Waiting()
    #print(ArduinoSerial.readline().decode('utf-8').strip())# get Arduino output pin 13 status
def applySettings2():
    set_flag();
    Waiting()
    #print(ArduinoSerial.readline().decode('utf-8').strip()) 

#==============================================
def browseDraw():
    filename1 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    print(filename1)
    openFile = str(filename1)
    fileDraw.set(openFile)

def change_dropdown():
    file_open1 = str(axis.get())
    print(file_open1)
        
    if file_open1=='x-axis':
        DrawXGraph()
        
    elif file_open1=='y-axis':
        DrawYGraph()
        
    elif file_open1=='z-axis':
        DrawZGraph()
        
    elif file_open1=='xyz-axis':
        DrawXYZGraph()    
    

def DrawXYZGraph():
    
    time, x, y, z = np.loadtxt(fileDraw.get(), delimiter=',', unpack=True)
    plt.plot(time,x, label='x-axis')
    plt.plot(time,y, label='y-axis')
    plt.plot(time,z, label='z-axis')

    plt.xlabel('Time')
    plt.ylabel('Acceleration')
    plt.title('Comparison between the acceleration on each axis')
    plt.legend()
    plt.show()

def DrawXGraph():
    time, x, y, z = np.loadtxt(fileDraw.get(), delimiter=',', unpack=True)
    plt.plot(time,x)
    plt.xlabel('Time')
    plt.ylabel('Acceleration on x-axis')
    plt.title('Acceleration on x-axis vs Time')
    plt.legend()
    plt.show()

def DrawYGraph():
    time, x, y, z = np.loadtxt(fileDraw.get(), delimiter=',', unpack=True)
    plt.plot(time,y)
    plt.xlabel('Time')
    plt.ylabel('Acceleration on y-axis')
    plt.title('Acceleration on y-axis vs Time')
    plt.legend()
    plt.show()

def DrawZGraph():
    time, x, y, z = np.loadtxt(fileDraw.get(), delimiter=',', unpack=True)
    plt.plot(time,z)
    plt.xlabel('Time')
    plt.ylabel('Acceleration on z-axis')
    plt.title('Acceleration on z-axis vs Time')
    plt.legend()
    plt.show()


def change_dropdown1():

    i = str(listToDraw.get())
    dataSetId1, name = i.split(',')
    i = int(dataSetId1.strip('('))
    print(i)
    time  = [ ]
    x  = [ ]
    y  = [ ]
    z  = [ ]
    
    
    c.execute("SELECT TIMESTAMP, XVALUE, YVALUE, ZVALUE FROM DATA WHERE DATASETID = {}".format(i))
    rows1 = c.fetchall()
    
    
    for listTime,listX,listY,listZ in rows1:
        time.append(listTime)
        x.append(float(listX))
        y.append(float(listY))
        z.append(float(listZ))
        
    z[:] = [val - mean for val in z]
        
    if var1.get()==1 and var2.get()==1 and var3.get()==1:
        plt.plot(time,x, label='x-axis')
        plt.plot(time,y, label='y-axis')
        plt.plot(time,z, label='z-axis')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Comparison between the acceleration on each axis')
        plt.legend()
        plt.show()
    

    elif var1.get()==0 and var2.get()==1 and var3.get()==1:
        plt.plot(time,y, label='y-axis')
        plt.plot(time,z, label='z-axis')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Comparison between the acceleration on each axis')
        plt.legend()
        plt.show()

    elif var1.get()==1 and var2.get()==1 and var3.get()==0:
        plt.plot(time,x, label='x-axis')
        plt.plot(time,y, label='y-axis')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Comparison between the acceleration on each axis')
        plt.legend()
        plt.show()

    elif var1.get()==1 and var2.get()==0 and var3.get()==1:
        plt.plot(time,x, label='x-axis')
        plt.plot(time,z, label='z-axis')
        plt.xlabel('Time')
        plt.ylabel('Acceleration')
        plt.title('Comparison between the acceleration on each axis')
        plt.legend()
        plt.show()
            

    elif var1.get()==1 and var2.get()==0 and var3.get()==0:
        plt.plot(time,x)
        plt.xlabel('Time')
        plt.ylabel('Acceleration on x-axis')
        plt.title('Acceleration on x-axis vs Time')
        plt.legend()
        plt.show()

    elif var1.get()==0 and var2.get()==1 and var3.get()==0:
        plt.plot(time,y)
        plt.xlabel('Time')
        plt.ylabel('Acceleration on y-axis')
        plt.title('Acceleration on y-axis vs Time')
        plt.legend()
        plt.show()

    elif var1.get()==0 and var2.get()==0 and var3.get()==1:
        plt.plot(time,z)
        plt.xlabel('Time')
        plt.ylabel('Acceleration on z-axis')
        plt.title('Acceleration on z-axis vs Time')
        plt.legend()
        plt.show()  

    


#===========================================================

def browsing():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    #print(filename)
    mystring2.set(str(filename))
    

def create_table():
    time = []
    x = []
    y = []
    z = []
    designation = str(mystring.get())
    descrip = str(mystring1.get())
    file_open = str(mystring2.get())

    c.execute("INSERT INTO DATASET(Designation_text, Description) VALUES(?, ?)",(designation, descrip))
    conn.commit()
    iden = c.lastrowid
    with open(file_open) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        v = 0
        for row in csv_reader:
            for row1 in row:
                if(v%4 ==0):
                    time.append(row1)
                if(v%4 == 1):
                    x.append(row1)
                if(v%4 == 2):
                    y.append(row1)
                if(v%4 == 3):
                    z.append(row1)
                v = v+1       
   
    for i in range(len(x)):
        Timestamp = '20'+str(time[i])
        Timestamp = datetime.fromisoformat(Timestamp)
        Xvalue = x[i]
        Yvalue = y[i]
        Zvalue = z[i]
        DatasetID = iden
        c.execute("INSERT INTO Data(timestamp, XVALUE, YVALUE, ZVALUE, DatasetID) VALUES (?, ?, ?, ?, ?)", (Timestamp, Xvalue, Yvalue, Zvalue, DatasetID))       
        conn.commit()

    seq = getSeq(iden)
    start, string, array1, peaks = whereStart(seq)
    time = getTimestamp(iden, peaks)
    

def ExportToCSV():

    saveFile = open(str(mystring3.get()),'w+')
    
    i = str(listToDraw1.get())    
    c.execute('SELECT TIMESTAMP, XVALUE, YVALUE, ZVALUE FROM DATA WHERE DATASETID = {}'.format(i[1]))   
    data1 = c.fetchall()
              
    for time, xval, yval, zval in data1:
        saveFile.write(str(time) + ', '  + str(xval) + ', '  + str(yval) + ', '  + str(zval) + '\n')              
    saveFile.close()

    #w.pack()

#===========================================================

def Permutations():

    i = str(listToDraw2.get())
    dataSetId1, name = i.split(',')
    i = int(dataSetId1.strip('('))

    z = getSeq(i)

    start, string1, array1, peaks = whereStart(z)
    array2 = inBetween(start, array1)

    y = np.array(array2)
    array3 = np.array(y.shape)
    
    '''if(array3[0] != None):
        print(array2)
        for i in range(len(array2)):
            array3 = array2[i]
            #ax = ax.twinx()
            #df.array3.plot(kind='bar', color='red', ax=ax, position=i)
        plt.show()
        
        
    elif():'''
    bar1 = plt.bar(np.arange(len(array2)), height= np.array(array2))
    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
        
    plt.show()
            


#============================================================
#
def getTimestamp(i,peaks):
    time  = [ ]
    move = Search(i)
    c.execute("SELECT timestamp FROM Data WHERE DATASETID = {}".format(i))
    rows1 = c.fetchall()   
    for listTime in rows1:
        val = str(listTime).strip(')')
        val = val.strip('(')
        val = val.strip(',')
        val = val.replace("'", "")             
        time.append(val)
    
    time1 = []
    print(peaks)
    #print(time)
    for j in range(len(peaks)):
        if(j%2 == 0):
            print(peaks[j])
            time1.append(str(time[(peaks[j])])    )
    print(time1)
    
    print(move)
    for k in range(len(move)):
        Timestamp1 = time1[k]
        Timestamp1 = datetime.fromisoformat(Timestamp1)
        iden = int(move[k])
        c.execute("INSERT INTO Sequence(timestamp, EventID) VALUES (?, ?)", (Timestamp1, iden))       
        conn.commit()  
    return time1

def Search(i):
    seq1 = getSeq(i)
    start, string, array1, peaks = whereStart(seq1)
    movement = inBetween(start, array1)
    print(movement)
    move = []

    for i in range(1, len(movement),1):
        end1 = str(movement[i])
        start1 = str(movement[i-1])
        c.execute("SELECT ID FROM SeqDataset WHERE Start={} AND End={}".format(start1, end1))
        val = c.fetchall()
        val = str(val)
        val = val.strip('[')
        val = val.strip(']')
        val = val.strip(')')
        val = val.strip('(')
        val = val.strip(',')
        move.append(int(val))
    return move
#=========================================================

def getZ(i):
    z  = [ ]
    c.execute("SELECT ZVALUE FROM TemplateData WHERE DATASETID = {}".format(i))
    rows1 = c.fetchall()   
    for listZ in rows1:
        val = str(listZ).strip(')')
        val = val.strip('(')
        val = val.strip(',')
        z.append(float(val))    
    return z

def getSeq(i):
    z  = [ ]
    c.execute("SELECT ZVALUE FROM Data WHERE DATASETID = {}".format(i))
    rows1 = c.fetchall()   
    for listZ in rows1:
        val = str(listZ).strip(')')
        val = val.strip('(')
        val = val.strip(',')
        z.append(float(val))    
    z = filter1(z)
    z[:] = [x - mean for x in z]
    return z

def filter1(z):
    N  = 2    # Filter order
    Wn = 0.025 # Cutoff frequency
    B, A = signal.butter(N, Wn)
     
    # Second, apply the filter
    filtered1 = signal.filtfilt(B, A, z, method = 'gust')
    return filtered1

def getPeaks(signal):
    peaks, _ = find_peaks(signal, height=100000)
    
    signal1 = np.zeros(len(signal))
    for i in range(len(signal)):
        signal1[i] = -signal[i]
        
    peaks1, _ = find_peaks(signal1, height=100000)
    peaks = np.append(peaks, peaks1)
    peaks = sorted(peaks)
    return peaks

def plotPeaks(peaks, signal):
    plt.plot(signal)
    plot(peaks, signal[peaks], "x")
    plt.plot(np.zeros_like(signal), "--", color="gray")
    plt.show()

def getCode(peaks, signal):
    array1 = np.zeros(len(peaks))
    
    for i in range(0, len(array1)):
        if(signal[peaks[i]]>0):
            val = 1
        if(signal[peaks[i]]<0):
            val = -1            
        array1[i] = val
        
    return array1

def getDistance(signal):
    peaks = getPeaks(signal)
   #print(peaks)
    
    length = int(len(peaks)/2)
    array1 = np.zeros(length)
    for i in range(0, length):
        array1[i] = peaks[2*i +1]-peaks[2*i]            

    return array1

def getDirection(signal):
    
    length = int(len(signal)/2) 

    array1 = np.zeros(length)

    for i in range(0, length):

        if(signal[2*i +1]==4 and signal[2*i]==1):            
            array1[i] = 1    #up
        if(signal[2*i +1]==2 and signal[2*i]==3):            
            array1[i] = 2    #down

    return array1

def getAmountFloors(signal):
    
    length = int(len(signal))

    array1 = np.zeros(length)
    for i in range(0, length):
        if(signal[i]<300):            
            array1[i] = 1    #1 up or down
        elif(signal[i]<600):            
            array1[i] = 2    #2 up or down
        else:            
            array1[i] = 3    #3 up or down
        
    return array1

def AllinOne(seq1):
    arrayPos = [1, -1]  #AU or DD
    arrayNeg = [-1, 1]  #AD or DU
    U1 = [1, 1]
    U2 = [1, 2]
    U3 = [1, 3]
    D1 = [2, 1]
    D2 = [2, 2]
    D3 = [2, 3]
    POS = getZ(5)
    NEG = getZ(6)
    
    correlationPOS = np.correlate(seq1, POS)
    correlationNEG = np.correlate(seq1, NEG)

    peaks = getPeaks(correlationPOS)
    peaks1 = getPeaks(correlationNEG)
    print(peaks)
    #print(peaks1)
    
    array1 = getCode(peaks, correlationPOS)
    array2 = getCode(peaks1, correlationNEG)
    
    array = np.vstack((array1, array2))
    arrayCode = np.zeros(len(array[0]))

    for i in range(0, len(array[0])):
        array3 = array[:,i]
        if(np.array_equal(array3, arrayPos)):
            val = 1
        elif(np.array_equal(array3, arrayNeg)):
            val = 2
        arrayCode[i] = val

    #print(arrayCode)
    arrayFinal = np.zeros(len(arrayCode))

    for i in range(0, len(arrayCode)):
        if(arrayCode[i]==1 and (i%2)==0):
            val = 1
        if(arrayCode[i]==1 and (i%2)==1):
            val = 2
        if(arrayCode[i]==2 and (i%2)==0):
            val = 3
        if(arrayCode[i]==2 and (i%2)==1):
            val = 4
        arrayFinal[i] = val
    #print(arrayFinal)

    directionMoved = getDirection(arrayFinal)

    distanceBetween = getDistance(correlationPOS)
    amountFloors = getAmountFloors(distanceBetween)
    
    final = np.vstack((directionMoved, amountFloors))
    string1 = "Movement sequence was:\n"
    final1 = np.zeros(len(final[0]))
                      
    for i in range(0, len(final[0])):
        array3 = final[:,i]
        if(np.array_equal(array3, U1)):
            string1 += "1 up\n"
            final1[i] = 1
        elif(np.array_equal(array3, U2)):
            string1 += "2 up\n"
            final1[i] = 2
        elif(np.array_equal(array3, U3)):
            string1 += "3 up\n"
            final1[i] = 3
        elif(np.array_equal(array3, D1)):
            string1 += "1 down\n"
            final1[i] = -1
        elif(np.array_equal(array3, D2)):
            string1 += "2 down\n"
            final1[i] = -2
        elif(np.array_equal(array3, D3)):
            string1 += "3 down\n"
            final1[i] = -3
    return string1, final1, peaks

def whereEnd(start, seq1):
    array1 = AllinOne(seq1)
    end = start
    
    for i in range(0, len(array1)):
        end = end + array1[i]
    return end

def whereStart(seq1):
    string1, array1, peaks = AllinOne(seq1)
    no1 = 0
    no2 = 0
    no3 = 0

    if(array1[0] == 1):
        end = [1, 2, 3]
    elif(array1[0] == 2):
        end = [1, 2]
    elif(array1[0] == 3):
        end = [1]
    elif(array1[0] == -1):
        end = [2, 3, 4]
    elif(array1[0] == -2):
        end = [3, 4]
    elif(array1[0] == -3):
        end = [4]

    start= []
    if(len(end) == 2):
        val1 = end[0]
        val2 = end[1]
        
        for i in range(0, len(array1)):
            val1 = val1 + array1[i]
            val2 = val2 + array1[i]
            
            if(val1 <= 0 or val1>4):
                no1 = 1
            if(val2 <= 0 or val2>4):
                no2 = 1
                
        if(val1>0 and val1<5 and no1!=1):
            start.append(end[0])
            #ended = val1
        if(val2>0 and val2<5 and no2!=1):
            start.append(end[1])
            #ended = val2            
            
    elif(len(end) == 3):
        val1 = end[0]
        val2 = end[1]
        val3 = end[2]
        
        for i in range(0, len(array1)):
                val1 = val1 + array1[i]
                val2 = val2 + array1[i]
                val3 = val3 + array1[i]
                
                if(val1 <= 0 or val1>4):
                    no1 = 1
                if(val2 <= 0 or val2>4):
                    no2 = 1
                if(val3 <= 0 or val3>4):
                    no3 = 1
                    
        if(val1>0 and val1<5 and no1!=1):
            start.append(end[0])
            #ended = val1
        if(val2>0 and val2<5 and no2!=1):
            start.append(end[1])
            #ended = val2
        if(val3>0 and val3<5 and no3!=1):
            start.append(end[2])
            #ended = val3
            
        
    elif(len(end) == 1):
        val1 = end[0]
        start.append(end[0])
        
        for i in range(0, len(array1)):
            val1 = val1 + array1[i]
        #ended = val1    
        
    return start, string1, array1,peaks

def inBetween(start, seq):
    array1 = []

    if(len(start) ==1):
        start = str(start)
        start = start.strip("[")
        start = start.strip("]")
        start = int(start)
        val1 = start
        array1.append(val1)
        for i in range(0, len(seq)):
            val1 = val1 + seq[i]
            array1.append(int(val1))
        return array1 

    elif(len(start)>1):
        val1 = start
        array1.append(start) 
        for i in range(len(seq)):
            array1.append([])
            if(i!=0):
                seq[i] = seq[i-1]+seq[i]
            for j in range(len(start)):       
                array1[i+1].append(val1[j]+seq[i])
                  
        return array1 

#============================================================
def get_Plot_of_All():    
    c.execute("SELECT DISTINCT timestamp, EventID FROM Sequence ORDER BY timestamp ASC")
    rows1 = c.fetchall()
    listAll, amount, time, iden = getSequenceAll(rows1)
    return listAll, amount, time, iden
    
def getSequenceAll(rows1):
    time = []
    iden = []
    listAll = []
    v = 0
    
    for listZ in rows1:
        for listZ1 in listZ:
            if(v%2 ==0):
                time.append(listZ1)
                time.append("")
            if(v%2 ==1):
                iden.append(int(listZ1))
            v = v+1

    amount = []
    for i in range(1, 13, 1):
        amount.append(iden.count(i))
                   
    previous = 0
    for i in range(len(iden)):
        c.execute("SELECT Start, End FROM SeqDataset WHERE ID = {}".format(iden[i]) )
        rows1 = str(c.fetchall())
        rows1 =rows1.strip("[")
        rows1 =rows1.strip("]")
        rows1 =rows1.strip("(")
        rows1 =rows1.strip(")")
        rows1 =rows1.replace(" ", "")
        x,y = rows1.split(",")
        listAll.append(x)
        listAll.append(y)
        '''if(previous == x ):
            listAll.append(float(y))
        else:
            listAll.append(float(x))
            listAll.append(float(y))
        previous = y'''  

    return listAll, amount, time, iden
        
def get_Certain_Date():
    if(listToDraw6.get() == 'All Data'):
        listAll, amount, time, iden = get_Plot_of_All()
    else:
        now1 = str(listToDraw6.get())
        now1 = now1.strip("(")
        now1 = now1.strip(")")
        now1 = now1.strip(",")
        now1 = str(now1.replace("'",""))
        c.execute("SELECT DISTINCT timestamp,EventID FROM Sequence WHERE date(timestamp) = '%s' ORDER BY timestamp ASC" % now1)
        rows1 = c.fetchall()
        listAll, amount, time, iden = getSequenceAll(rows1)
    #print(amount)
    return listAll, amount, time, iden

def getAxis():
    ax0 = []
    now1 = str(listToDraw6.get())
    now1 = now1.strip("(")
    now1 = now1.strip(")")
    now1 = now1.strip(",")
    now1 = str(now1.replace("'",""))
    c.execute("SELECT DISTINCT time(timestamp) FROM Sequence WHERE date(timestamp) = '%s' ORDER BY timestamp ASC" % now1)
    rows1 = c.fetchall()
    for listZ in rows1:
        vals = str(listZ)
        vals = vals.strip("(")
        vals = vals.strip(")")
        vals = vals.strip(",")
        vals = vals.replace("'", "")
        ax0.append(vals)
        ax0.append("")
    return ax0

def plotAmount():
    listAll, array2, time, iden = get_Certain_Date()
    axis0 = ['1-2','1-3','1-4','2-1','2-3','2-4','3-1','3-2','3-4','4-1','4-2','4-3']
    plt.title('Amount of times each elevator ride occured for  %s' % listToDraw6.get(), fontsize=12)
    bar1 = plt.bar(axis0, height= np.array(array2))    
    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')        
    plt.show()

def plotTimeline():
    listAll, array2, time, iden = get_Certain_Date()
    listAll = list(map(int, listAll))    
    plt.title('Timeline for  %s' % listToDraw6.get(), fontsize=12)
    if(listToDraw6.get() == 'All Data'):
        x = np.arange(0,len(listAll),1)    
        bar2 = plt.bar(x, height = np.array(listAll))
        plt.xticks(x, time, rotation=90,fontsize=8)
        
        
            
    else:
       time = getAxis()
       x = np.arange(0,len(listAll),1)    
       bar2 = plt.bar(x, height = np.array(listAll))
       plt.xticks(x, time, rotation=90,fontsize=8)

    for rect in bar2:
            height = rect.get_height()
            #bar2[rect].set_color('r')
            plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')        
    plt.show()
            

#============================================================
    


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        self.geometry
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import from csv", command = lambda: self.show_frame(ImportCSV))
        filemenu.add_command(label="Export to csv", command = lambda: self.show_frame(ExportCSV))
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command = lambda: self.show_frame(SettingsPage))
        filemenu.add_separator()
        filemenu.add_command(label="Sample", command = lambda: self.show_frame(StartStopSample))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        Displaymenu = tk.Menu(menubar, tearoff=0)
        Displaymenu.add_command(label="Plot from csv", command = lambda: self.show_frame(PlotCSVPage) )
        Displaymenu.add_command(label="Plot from database", command = lambda: self.show_frame(PlotDataPage) )
        Displaymenu.add_separator()
        Displaymenu.add_command(label="List of all data in database", command = lambda: self.show_frame(LISTS) )
        menubar.add_cascade(label="Display", menu=Displaymenu)

        Capturemenu = tk.Menu(menubar, tearoff=1)
        Capturemenu.add_command(label="Download all data", command=lambda: self.show_frame(DownloadPage))
        #Capturemenu.add_command(label="Download latest data", command= popupmsg1(msg))
        menubar.add_cascade(label="Capture", menu=Capturemenu)

        Analysismenu = tk.Menu(menubar, tearoff=1)
        Analysismenu.add_command(label="Permutations", command = lambda: self.show_frame(PermutationPage))
        Analysismenu.add_command(label="Floors", command=lambda: changeExchange("BTC-e","btce"))
        menubar.add_cascade(label="Analysis", menu=Analysismenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, SettingsPage, StartStopSample, PlotCSVPage, ExportCSV, ImportCSV, PlotDataPage, LISTS, DownloadPage, PermutationPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
       

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class OptionMenu(tk.OptionMenu):
    def __init__(self, *args, **kw):
        self._command = kw.get("command")
        tk.OptionMenu.__init__(self, *args, **kw)
        

    def addOption(self):
        self['menu'].delete(0, 'end')
        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
               
        for row in rows1:
            label = str(row)
            self["menu"].add_command(label=label, command=tk._setit(listToDraw1, label, self._command))

    def addOption1(self):
        self['menu'].delete(0, 'end')
        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
               
        for row in rows1:
            label = str(row)
            self["menu"].add_command(label=label, command=tk._setit(listToDraw, label, self._command))

    def addOption1(self):
        self['menu'].delete(0, 'end')
        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
               
        for row in rows1:
            label = str(row)
            self["menu"].add_command(label=label, command=tk._setit(listToDraw2, label, self._command))

    def addOption3(self):
        self['menu'].delete(0, 'end')
        c.execute("SELECT DISTINCT date(timestamp) FROM Sequence")
        rows1 = c.fetchall()

        c.execute("SELECT DISTINCT date(timestamp) FROM Sequence")
        rows1 = c.fetchall()
               
        for row in rows1:
            label = str(row)
            self["menu"].add_command(label=label, command=tk._setit(listToDraw6, label, self._command))
                      
#========================================================================================        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        l12 = tk.Label(self, text="Home page", font= "Helvetica 16 bold italic").place(y=0, x=300)
        image = Image.open("Capture.gif")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo)
        label.image = photo # keep a reference!
        label.place(y=50, x=0)
        
            
class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)        
    
        global var
        var = tk.StringVar(self)

        global range1
        range1 = tk.StringVar(self)

        global flag
        flag = tk.StringVar(self)

        tk.Label(self, text="Configure the accelerometer", font=LARGE_FONT).place(y=0,x=10)
        
        tk.Label(self, text="Choose the output data rate (ODR)", font=NORM_FONT).place(y=50, x=10)

        optionList = ('6.25', '12.5', '25', '50', '100', '200', '400', '800', '1600', '3200')
        var.set(optionList[0])
        tk.OptionMenu(self, var, *optionList).place(y=80, x=20)
        tk.Button(self, text="Set ODR", command = applySettings).place(y=80, x=150)

        tk.Label(self, text="Choose the g-range", font=NORM_FONT).place(y=160, x=10)

        optionList1 = ('0.5', '1', '2', '4')
        range1.set(optionList1[0])
        tk.OptionMenu(self, range1, *optionList1).place(y=190, x=20)
        tk.Button(self, text="Set G-range", command = applySettings1).place(y=190, x=150)

        tk.Label(self, text="Choose the output data rate (ODR)", font=NORM_FONT).place(y=270, x=10)

        optionList2 = ('Overwrite when buffer full', 'Stop writing when buffer full')
        flag.set(optionList2[0])
        tk.OptionMenu(self, flag, *optionList2).place(y=300, x=20)
        tk.Button(self, text="Set flag", command = applySettings2).place(y=300, x=250)

        #tk.Label(self, text="Set date and time to current date and current time)", font=NORM_FONT).place(y=380, x=10)
        #tk.Button(self, text="Set date and time", command = setDate_Time).place(y=410, x=20)
      
        tk.Button(self, text="Done", command = lambda: controller.show_frame(StartPage)).place(y=450, x=550)

class StartStopSample(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        global var1
        var1 = tk.StringVar()
        var1.set('OFF')

        font1 = "-family {Courier New} -size 10 -weight bold -slant roman -underline 0 -overstrike 0"
        font2 = "-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0"
        font3 = "-family {@Arial Unicode MS} -size 12 -weight bold -slant roman -underline 1 -overstrike 0"
        font4 = "-family {Segoe UI} -size 10 -weight bold -slant roman -underline 0 -overstrike 0" 
        

        btn1 = tk.Button(self, text='Start sampling', font = font1, bg = 'light green', highlightbackground= 'black', borderwidth = 3, activebackground = 'light gray', relief='raised', command=start_sampling) # activate Arduino pin 13
        btn1.place(relx=0.34, rely=0.10, height=30, width=150)

        btn2 = tk.Button(self, text='Stop sampling', font = font1, bg = 'red2', fg = 'white', highlightbackground= 'black', borderwidth = 3, activebackground = 'light gray', relief='raised', command=stop_sampling) # deactivate Arduino pin 13
        btn2.place(relx=0.34, rely=0.30, height=30, width=150)

        #btn3 = tk.Button(self, text='Download all data', font = font1, bg = 'red2', fg = 'white', highlightbackground= 'black', borderwidth = 3, activebackground = 'light gray', relief='raised', command=downloadAll) # deactivate Arduino pin 13
        #btn3.place(relx=0.34, rely=0.50, height=30, width=150)

        #btn4 = tk.Button(self, text='Download latest data', font = font1, bg = 'red2', fg = 'white', highlightbackground= 'black', borderwidth = 3, activebackground = 'light gray', relief='raised', command=downloadLatest) # deactivate Arduino pin 13
        #btn4.place(relx=0.34, rely=0.70, height=30, width=300)

        tk.Button(self, text="Re-configure the device", command = lambda: controller.show_frame(StartPage)).place(y=10, x=550)



class PlotCSVPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global fileDraw
        fileDraw = tk.StringVar()
        global openFile
        openFile = tk.StringVar(self)
        global axis
        axis = tk.StringVar(self)
        
        tk.Label(self, text="Select file to plot as graph").place(y=60)
        tk.Entry(self, textvariable = fileDraw, width = 45).place(y=60, x=200)
        browsing_now = tk.Button(self, text="Browse", command = browseDraw).place(y=60, x=500)
        
        choices = {'x-axis','y-axis','z-axis','xyz-axis'}
        axis.set('z-axis') # set the default option
        
        popupMenu = tk.OptionMenu(self, axis, *choices)
        tk.Label(self, text="Select which axis to draw").place(y=90)
        popupMenu.place(y=90, x=200)    
        #axis.trace('w', change_dropdown)
        Plot = tk.Button(self, text="Plot", command = change_dropdown).place(y=150, x= 200)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)

class PlotDataPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global list2
        list2 = [None]
        
        global listToDraw 
        listToDraw = tk.StringVar(self)
        global axis1 
        axis1 = tk.StringVar(self)
        global var1         
        global var2 
        global var3  
        var1 = tk.IntVar()        
        var2 = tk.IntVar()
        var3 = tk.IntVar()

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
           
        for row in rows1:
            list2.append(str(row))
                
            
        tk.Label(self, text="Select which DATASETID to plot as a graph").place(y=60)
        tk.Label(self, text="Select which axis to plot").place(y=120)
        tk.Button(self, text="Update list of DATASETID", command=lambda: optionMenu.addOption1()).place(y=0, x=300)
        tk.Checkbutton(self, text="x-axis", variable=var1).place(y=120, x=300)
        tk.Checkbutton(self, text="y-axis", variable=var2).place(y=150, x=300)
        tk.Checkbutton(self, text="z-axis", variable=var3).place(y=180, x=300)       


        Plot = tk.Button(self, text="Plot", command = change_dropdown1).place(y=210, x= 300)

        optionMenu = OptionMenu(self, listToDraw, *list2)
        optionMenu.place(y=60, x=300)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)


class ImportCSV(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global mystring
        global mystring1
        global mystring2
        mystring = tk.StringVar()
        mystring1 = tk.StringVar()
        mystring2 = tk.StringVar()

        
        tk.Label(self, text="Enter the designation text for new table").place(y=30)
        tk.Label(self, text="Enter a description for the new table").place(y=60)#label
        tk.Label(self, text="Enter file name to create a table of").place(y=90)#label
        tk.Entry(self, textvariable = mystring).place(y=30, x=300) #entry textbox
        tk.Entry(self, textvariable = mystring1).place(y=60, x=300) #entry textbox
        tk.Entry(self, textvariable = mystring2, width = 45).place(y=90, x=300)
        browse = tk.Button(self, text="Browse", command = browsing).place(y=90, x=600)
        WSignUp = tk.Button(self, text="OK", command=create_table).place(y=120, x=300)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)

class ExportCSV(tk.Frame):
   
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global list1
        list1 = [None]
        
        global mystring3
        mystring3 = tk.StringVar()

        global listToDraw1
        listToDraw1 = tk.StringVar(self)

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
           
        for row in rows1:
            list1.append(str(row))

        tk.Label(self, text="Select the DATASETID to convert to a .csv", ).place(y=60)
        tk.Label(self, text="Filename(.csv):").place(y=100)        
        tk.Button(self, text="Update list of DATASETID", command=lambda: optionMenu.addOption()).place(y=0, x=300)
        tk.Entry(self, textvariable = mystring3, width = 40).place(y=100, x=300) 
        WSignUp1 = tk.Button(self, text="OK", command=ExportToCSV).place(y=120, x=300)

        optionMenu = OptionMenu(self, listToDraw1, *list1)
        optionMenu.place(y=60, x=300)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)

class LISTS(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text = "ID, TIMESTAMP, XVAL, YVAL, ZVAL, DATASETID").pack(side = tk.TOP)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
   #     tk.Button(self, text="Update list", command=lambda: ListBox.updateList()).place(y=0, x=600)
               

        c.execute("SELECT * FROM DATA")

        rows1 = c.fetchall()
           
        for row in rows1:        
            listbox.insert(row[0], str(row))
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)

class DownloadPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global mystring4
        global mystring5
        mystring4 = tk.StringVar()
        mystring5 = tk.StringVar()
        
            
        tk.Label(self, text="Enter the designation text for new data").place(y=30)
        tk.Label(self, text="Enter a description for the new data").place(y=60)#label
        
        tk.Entry(self, textvariable = mystring4).place(y=30, x=300) #entry textbox
        tk.Entry(self, textvariable = mystring5).place(y=60, x=300) #entry textbox

        tk.Label(self, text="Choose what data to download").place(y=120, x = 0)
        
        tk.Button(self, text="Download all data", command= downloadAll).place(y=150, x=0)
        tk.Button(self, text="Download latest data", command=downloadLatest).place(y=150, x=200)

        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)

class PermutationPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global list3
        list3 = [None]

        global list6
        list6 = [None]
        
        global mystring6
        mystring6 = tk.StringVar()

        global listToDraw2
        listToDraw2 = tk.StringVar(self)

        global listToDraw6
        listToDraw6 = tk.StringVar(self)

        c.execute("SELECT ID, Designation_text FROM DATASET")
        rows1 = c.fetchall()    
           
        for row in rows1:
            list3.append(str(row))

        c.execute("SELECT DISTINCT date(timestamp) FROM Sequence")
        rows1 = c.fetchall()      
           
        for row in rows1:
            list6.append(str(row))
        list6.append("All Data")

        tk.Label(self, text="Select which DATASETID to analyse").place(y=60)
        tk.Label(self, text="Select which Day to analyse").place(y=200)

        tk.Button(self, text="Update list of DATASETID", command=lambda: optionMenu.addOption1()).place(y=0, x=300)
        tk.Button(self, text="Update list of DAYS", command=lambda: optionMenu.addOption3()).place(y=0, x=500) 

        tk.Button(self, text="Determine sequence", command = Permutations).place(y=60, x= 500)
        tk.Button(self, text="Plot number of each permutation", command = plotAmount).place(y=200, x= 500)
        tk.Button(self, text="Plot Timeline", command = plotTimeline).place(y=200, x= 350)
        #tk.Button(self, text="Analyse all data", command = get_Plot_of_All).place(y=200, x= 500)

    
        
        optionMenu = OptionMenu(self, listToDraw2, *list3)
        optionMenu.place(y=60, x=300)

        optionMenu1 = OptionMenu(self, listToDraw6, *list6)
        optionMenu1.place(y=200, x=175)
        
        
        tk.Button(self, text="Back to home page", command=lambda: controller.show_frame(StartPage)).place(y = 0, x=635)      
        


app = SeaofBTCapp()
app.geometry("750x500")

app.mainloop()
conn.close()
