# import Libraries
import serial                    
import numpy                    
import matplotlib.pyplot as plt 
from drawnow import *
import atexit
import csv

 
serialData  = serial.Serial('com19', 9600) #Serial Object
Data1 = []
Data2 = []
Data3 = []
plt.ion()
cnt=0


fname = 'Serialdata.txt'          #file to save Serial data as well
fmode = 'ab'
open("data1.txt", "w").close()

        
fig, host = plt.subplots()
fig.subplots_adjust(right=0.85)


#Plot Realtime Values

def plotValues():
    #Create a second y axis  
    plt.ylim(0,4)                                      
    plt.title('Serial value')                              
    plt.grid(True)                                      
    plt.ylabel('ADC1')
    plt.xlabel('Last 50 Datas')
    plt.tick_params(axis='y', colors="red")
    plt.plot(Data1, 'ro-', label='ADC1')
    plt.legend(loc='upper left')

    #Create a second y axis
    plt2=plt.twinx()                                   
    plt2.set_ylim(0,12)                                
    plt2.plot(Data2, 'g^-', label='ADC2')              
    plt2.set_ylabel('ADC2')                         
    plt2.tick_params(axis='y', colors="green")
    plt2.ticklabel_format(useOffset=False)             
    plt2.legend(loc='upper right')              

    
def doAtExit():
    serialData .close()
    print("Close serial")
    print("serial.isOpen() = " + str(serialData .isOpen()))
    

# While loop                             
while True: 
    while (serialData .inWaiting()==0):          #Wait until data
        pass #do nothing
    
    serialString  = serialData .readline()       #Read Serial Datas
    serialString = serialString.decode('utf_8')
    print(serialString)
    
    dataArray = serialString.split(',')
    tempData1 = float( dataArray[0])            #Read first value and save in temporary variable
    tempData2 = float( dataArray[1])            #Read second value and save in temporary variable
    Data1.append(tempData1)                     #Data1 array 
    Data2.append(tempData2)                     #Data2 array

    drawnow(plotValues)                         #Call drawnow to update our live plot
    plt.pause(.000001)                         
    cnt=cnt+1

    saveFile = open('data1.txt', 'a')           #Save the received data to file
    saveFile.write(serialString)
    saveFile.close()
        
    if(cnt>50):                                 #If 50 or more points, delete the first one from the array
        Data1.pop(0)                           
        Data2.pop(0)
        
        
