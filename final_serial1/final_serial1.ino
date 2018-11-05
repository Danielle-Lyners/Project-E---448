/*  ********************************************* 
 *  SparkFun_ADXL345_Example
 *  Triple Axis Accelerometer Breakout - ADXL345 
 *  Hook Up Guide Example 
 *  
 *  Utilizing Sparkfun's ADXL345 Library
 *  Bildr ADXL345 source file modified to support 
 *  both I2C and SPI Communication
 *  
 *  E.Robert @ SparkFun Electronics
 *  Created: Jul 13, 2016
 *  Updated: Sep 06, 2016
 *  
 *  Development Environment Specifics:
 *  Arduino 1.6.11
 *  
 *  Hardware Specifications:
 *  SparkFun ADXL345
 *  Arduino Uno
 *  *********************************************/

#include <ADXL313.h>         // SparkFun ADXL345 Library
#include <SD.h>
#include <RTCZero.h>

/*********** COMMUNICATION SELECTION ***********/
/*    Comment Out The One You Are Not Using    */
ADXL313 adxl;           // USE FOR SPI COMMUNICATION, ADXL345(CS_PIN);
int data;
int sample = 1;
const int chipSelect = SDCARD_SS_PIN;
int timeStamp = 1;
int alwaystimestamp = 0;

unsigned long lastWritePos = 0;
unsigned long lastReadPos = 0;
int overwriting = 0;
String save = "w";
int stopState = 0;
int amountReadreachEnd = 0;
int amountWritereachEnd = 0;
int readNum = 0;
int writeNum = 0;
int overWrote = 0;
int MemorySize = 2147483647;
int previousStopState = 0;
String memorymap;

unsigned long previousTime;
unsigned long currentTime;

RTCZero rtc;

/* Change these values to set the current initial time */
const byte seconds = 50;
const byte minutes = 3;
const byte hours = 18;

/* Change these values to set the current initial date */
const byte day = 13;
const byte month = 9;
const byte year = 18;
String myString;

//int setRange = 0;
//float setRange1 = 0;
float setRate1;
//int setRate = 0;
int setFlag = 0;

const int buttonPin = A1;    // the number of the pushbutton pin
const int ledPin = 5;      // the number of the LED pin

// Variables will change:
int ledState = HIGH;         // the current state of the output pin
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

/****************** INTERRUPT ******************/
/*      Uncomment If Attaching Interrupt       */
//int interruptPin = 2;                 // Setup pin 2 to be the interrupt pin (for most Arduino Boards)


/******************** SETUP ********************/
/*          Configure ADXL345 Settings         */
void setup(){

  Serial1.begin(115200); //initialize Serial1 COM at 9600 baudrate
  
  //while (!Serial1) {
  //  ; // wait for Serial1 port to connect. Needed for native USB port only
  //}
  
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(ledPin, OUTPUT);

  // initialize the LED as an output:
  pinMode(2, OUTPUT);
  digitalWrite(2,LOW);

  pinMode(3, OUTPUT);
  digitalWrite(3,LOW);

  adxl = ADXL313(1);
  adxl.powerOn();                     // Power on the ADXL345

  adxl.setRangeSetting(2);           // Give the range settings
                                      // Accepted values are 2g, 4g, 8g or 16g
                                      // Higher Values = Wider Measurement Range
                                      // Lower Values = Greater Sensitivity

  adxl.setSpiBit(0);                  // Configure the device to be in 4 wire SPI mode when set to '0' or 3 wire SPI mode when set to 1
                                      // Default: Set to 1
                                      // SPI pins on the ATMega328: 11, 12 and 13 as reference in SPI Library 

  adxl.setFullResBit(1);

/***********************************************************/

  //Serial1.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) 
  {
    Serial1.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  //Serial1.println("card initialized.");

/***********************************************************/

rtc.begin();
rtc.setTime(hours, minutes, seconds);
rtc.setDate(day, month, year);

/***********************************************************/
File dataFile = SD.open("datalog.txt");  
dataFile.seek(0);
if(dataFile)
{
  if(dataFile.available()>=MemorySize)
  {
    overwriting = 1;
    //Serial1.println(overwriting);
  }
}
dataFile.close();

}

/****************** MAIN CODE ******************/
/*     Accelerometer Readings and Interrupt    */
void loop(){
  
  int reading = digitalRead(buttonPin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
        ledState = !ledState;
        if(ledState == HIGH){    
          //Serial1.begin(115200); 
          timeStamp = 0;
          sample = 0;
          
        }
        if(ledState == LOW){ 
              
          sample = 1;
          if(overWrote == 1 && setFlag == 1)
          {
            lastReadPos = lastWritePos;
            //overWrote = 0;  //do not clear; clear only if read                 
          }
          //Serial1.end();
        }       
      }
    }
  }

  // set the LED:
  digitalWrite(ledPin, ledState);

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;

  if (Serial1.available()> 0)
 {
    data = Serial1.read();

    if (data == 'a')
    {
      adxl.setRate(6.25);    
      Serial1.println("rate = 6.25");
      data = '9';
      //setRate = 1;
      setRate1 = 6.25;
    }
    if (data == 'b')
    {
      adxl.setRate(12.5);  
      Serial1.println("rate = 12.5");    
      data = '9';
      //setRate = 1; 
      setRate1 = 12.5;   
    }
    if (data == 'c')
    {
      adxl.setRate(25); 
      Serial1.println("rate = 25");  
      data = '9'; 
      //setRate = 1;   
      setRate1 = 25;   
    }
    if (data == 'd')
    {
      adxl.setRate(50);
      Serial1.println("rate = 50");   
      data = '9';      
      //setRate = 1;
      setRate1 = 50;
    }
  
    if (data == 'e')
    {
      adxl.setRate(100);  
      Serial1.println("rate = 100");  
      data = '9';    
      //setRate = 1;  
      setRate1 = 100;
    }
    if (data == 'f')
    {
      adxl.setRate(200);    
      Serial1.println("rate = 200"); 
      data = '92'; 
      //setRate = 1;  
      setRate1 = 200;
    }
    if (data == 'g')
    {
      adxl.setRate(400);  
      Serial1.println("rate = 400");
      data = '9'; 
     // setRate = 1;
      setRate1 = 400;       
    }
    if (data == 'h')
    {
      adxl.setRate(800); 
      Serial1.println("rate = 800");    
      data = '9'; 
     // setRate = 1;  
      setRate1 = 800;  
    }
     
    if (data == 'i')
    {
      adxl.setRate(1600);          
      Serial1.println("rate = 1600");
      data = '9';
     // setRate = 1;
      setRate1 = 1600;
    }
    if (data == 'j')
    {
      adxl.setRate(3200); 
      Serial1.println("rate = 3200");         
      data = '9';
     // setRate = 1;
      setRate1 = 3200;
    }
  
  //******************************
   
    if (data == 'k')
    {
      adxl.setRangeSetting(0.5); 
      //setRange1 = 0.5;
      Serial1.println("range = 0.5");         
      data = '9';
      //setRange = 1;
    }
    if (data == 'l')
    {
      adxl.setRangeSetting(1);  
      //setRange1 = 1;  
      Serial1.println("range = 1");      
      data = '9';
      //setRange = 1;
    }
  
    if (data == 'm')
    {
      adxl.setRangeSetting(2);
      //setRange1 = 2; 
      Serial1.println("range = 2"); 
      data = '9';  
      //setRange = 1;      
    }
    if (data == 'n')
    {
      adxl.setRangeSetting(4);   
      //setRange1 = 4;       
      Serial1.println("range = 4");
      data = '9';
      //setRange = 1;
    }
  //***************************************
    if (data == 'o')
    {
      Serial1.println("Overwrite"); 
      data = '9';  
      alwaystimestamp = 1;   
      stopState = 0;
      digitalWrite(2, LOW);
      previousStopState = 0;   
      setFlag = 1;
    }
    if (data == 'p')
    {  
      Serial1.println("Stop writing"); 
      stopState=0; 
      alwaystimestamp = 1;
      data = '9';  
      setFlag = 0;    
    }
  //***************************************
    if (data == 's')
    {  
      Serial1.println("Set time"); 
      previousTime = millis(); 
      data = '9';      
    }

  //***************************************

    //if(setRange == 1 && setRate ==1 && setFlag ==1)
    //{
      
      if (data == '1')
       {
        sample = 0;   
        timeStamp = 0;     
        data = '9';    
       }
  
       if (data == '2')
       {     
         sample = 1;
         if(overWrote == 1 && setFlag == 1)
          {
            lastReadPos = lastWritePos;
            //overWrote = 0;  //do not clear; clear only if read       
          }
         data = '9';
       }    
    
     if (data == '3')
     { 
      readLatestData();
      if(stopState == 1)
      {
        stopState = 0;
        digitalWrite(2, LOW);
        previousStopState = 1;
        //Serial1.println("can sample again because read"); 
      }
      else if(stopState == 0)
      { 
        previousStopState = 0; 
      }
      data = '9';  
     }

     if (data == '4')
     {    
      readAllData();
      data = '9'; 
      if(stopState == 1)
      { 
        stopState = 0;
        digitalWrite(2, LOW);
        previousStopState = 1;
        //Serial1.println("can sample again because read"); 
      }
     else if(stopState == 0)
     { 
        previousStopState = 0; 
     }
     }
    
 }

 if(stopState == 0)
 {   //digitalWrite(5,LOW); 
    if(sample == 0)
    { 
        WriteToCertainPos();
    }
 }
 else if(stopState ==1)
 {
  //digitalWrite(5,HIGH);
 }
 
 
}

/********************* functions *********************/

void readLatestData()
{
  File dataFile = SD.open("datalog.txt");
  //Serial1.println("In function readLatestData");
  
 
  if (dataFile) 
  {   
      //where write pointer more than read pointer and not overwritten  
      if(amountReadreachEnd==amountWritereachEnd && lastReadPos==lastWritePos)   //amount of 
      {            
            Serial1.println("Stop reading nothing left to read");            
      }
      else
      {
        if(overwriting == 0)
        {  
          //Serial1.println("In overwriting = 0");
                    
            dataFile.seek(lastReadPos);
            while (dataFile.available())
            {
              //Serial1.print(String(lastReadPos)+"|");
              Serial1.write(dataFile.read());
              lastReadPos = dataFile.position();
              readNum++;
  
              if(lastReadPos == MemorySize)
             {
              lastReadPos = 0;
              //Serial1.println("read till end");
              amountReadreachEnd++;
              //Serial1.println("amountReadreachEnd is" + String(amountReadreachEnd));
             }               
            }                 
        }
        //where read pointer more than write pointer  and overwritten    
        if(overwriting ==1)
        {    
          //Serial1.println("In overwriting == 1"); 
          if(overWrote == 1)
          {
            overWrote = 0; //clear overwrote flag
            digitalWrite(3, LOW);
            
            dataFile.seek(lastReadPos);
            while (dataFile.available())
            {
              //Serial1.print(String(lastReadPos)+"|");
              Serial1.write(dataFile.read());
              lastReadPos = dataFile.position();
              readNum++;
          
              if(lastReadPos == MemorySize)
              {
                lastReadPos = 0;
                //Serial1.println("read till end");
                amountReadreachEnd++;
                //Serial1.println("amountReadreachEnd is" + String(amountReadreachEnd));
              }   
            }
            
            while(lastReadPos != lastWritePos)
            {
              dataFile.seek(lastReadPos);
              readNum++;
              //Serial1.print(String(lastReadPos)+"|");
              Serial1.write(dataFile.read());
              lastReadPos = dataFile.position();
            }
          amountReadreachEnd = 0;
          amountWritereachEnd = 0;  
          }  
          else{
          if(amountReadreachEnd<amountWritereachEnd)    //have overwritten but can read latest data
          {         
            if(lastReadPos>=lastWritePos)
            {    
                /*if(stopState == 1 && lastReadPos == lastWritePos)
                {
                  stopState = 0;
                  //Serial1.println("will read data so can write again; stopState is 0" );     //////////////////////////////////////////////////////////////////////////////////////////////
                }*/              
                dataFile.seek(lastReadPos);
                while (dataFile.available())
                {
                  readNum++;
                  //Serial1.print(String(lastReadPos)+"|");
                  Serial1.write(dataFile.read());
                  lastReadPos = dataFile.position();
                }
                lastReadPos = 0;
                amountReadreachEnd++;       
                //Serial1.println("amountReadreachEnd is" + String(amountReadreachEnd));
                //amountReadreachEnd(lastReadPos);     
            }
          }
          if(amountReadreachEnd==amountWritereachEnd)   //amount of 
          { 
              //where read pointer less than write pointer and overwritten
            if(lastReadPos<lastWritePos)
            {
              dataFile.seek(lastReadPos);
              while (lastReadPos<lastWritePos)
              {
                readNum++;
                //Serial1.print(String(lastReadPos)+"|");
                Serial1.write(dataFile.read());
                lastReadPos = dataFile.position();                             
              }
            }
            if(lastReadPos==lastWritePos)
            {
              Serial1.println();           
            }  
          }  
            dataFile.close();        
        }
      }
  } 
}
else 
{
  Serial1.println("error opening test.txt");
}
//Serial1.println("end of read");
}

void WriteToCertainPos()
{
  String datastring;
  int lengths;
  int index;
  int x,y,z;   
  adxl.readAccel(&x, &y, &z);         // Read the accelerometer values and store them in variables declared above x,y,z
  //Returns the number of milliseconds since the Arduino board began running the current program. 
  currentTime = millis() - previousTime;
  String w = getTime();
  //String m = String(setRate1);
  //String range0 = String(setRange1);
  
  if(timeStamp==0 || (setFlag == 0 && previousStopState == 1))
  {  
    //datastring += String(w) + ",";
    timeStamp = 1;
    
    if(setFlag == 0 && previousStopState == 1)
    {
      save = 'w';
      previousStopState = 0;    //wrote so previous it was not stopped
    }
  } 
  else if(alwaystimestamp == 1)
  {  
    ///datastring +=String(w) + ",";
    //alwaystimestamp = 0;
  } 
  // Output Results to Serial1
  datastring += String(w) + ","+ String(x) + "," + String(y) + "," + String(z) + "\n";

  if(overwriting == 0)
  { 
    File dataFile = SD.open("datalog.txt", FILE_WRITE);
    
    if(dataFile)
    {
      //datastring = "a,b,c,d/n"; 
      lengths = int(datastring.length());
      index = 0;       
              
      while(index!=lengths)
      {
        writeNum++;
        dataFile.seek(lastWritePos); 
        //Serial1.print(String(lastWritePos)+"|");
        //Serial1.print("time is " + String(millis()));
        dataFile.print(datastring.charAt(index));
        //Serial1.print(datastring.charAt(index));
        index++;             
        lastWritePos = dataFile.position();
  
        if(lastWritePos == MemorySize)
        {
        lastWritePos = 0;
        //Serial1.println("reached MemorySize");        
        amountWritereachEnd++;
        //Serial1.println("amountWritereachEnd is " +String(amountWritereachEnd));
        save = datastring.substring(index); 
        //Serial1.println("index is " +String(index));
        //Serial1.println(save);
        index = lengths;          
        overwriting = 1;
        //Serial1.println("overwriting is " + String(overwriting));             
        }
  
        if(lastWritePos == lastReadPos)
        {
          //Serial1.println("lastWritePos == lastReadPos");
          overwriting = 1; 
          //Serial1.println("overwriting is" + String(overwriting));         
          
          //Overwriting
         if(setFlag == 1)
         {
          if(lastWritePos == 0)
          {
          //Serial1.println("overwriting because reached read pointer");
          overwriting = 1;
          //Serial1.println("overwrite is " + String(overwriting));
          overWrote = 1;
          digitalWrite(3, HIGH);
          //Serial1.println("overWrote is " + String(overWrote));                             
          //Serial1.println("sample is" + String(sample));
          }
         }       
          //Stop writing
         if(setFlag == 0)
         {//stop overwriting but has overwritten
          //Serial1.println("stop writing when reach data");                             
          sample = 1;
          //Serial1.println("sample is" + String(sample));
          overwriting = 1;
          //Serial1.println("overwriting is" + String(overwriting));
          stopState = 1;
          digitalWrite(2, HIGH);
         }        
        }
      }
    }
    else
    {
      Serial1.println("error opening test.txt");
    }
  dataFile.close();
  }
  

if(overwriting == 1 && stopState==0)
{ 
  File datafile = SD.open("datalog.txt", O_WRITE | O_CREAT | O_SYNC);
  
  if(datafile)
  {
    if(save != "w" )
    { 
      datastring = save;
      save = "w";    
    }
    //get new string
    else
    {
      //datastring = "a,b,c,d/n";     //datastring same as original
    }
    lengths = datastring.length();
    index = 0;
                  
    while(index!=lengths)
    { 
      writeNum++;
      datafile.seek(lastWritePos);
      //Serial1.print(String(lastWritePos)+"|");
      datafile.print(datastring.charAt(index));
      //Serial1.print(datastring.charAt(index));
      index++; 
          
      lastWritePos = datafile.position();      

      if(lastWritePos == MemorySize)
      {
      //Serial1.println("reached MemorySize");
      lastWritePos = 0;      
      amountWritereachEnd++; 
      //Serial1.println("amountWritereachEnd is " +String(amountWritereachEnd));                         
      }

      if(lastWritePos == lastReadPos)
      {
        //Serial1.println("lastWritePos == lastReadPos");
      //Overwriting
      if(setFlag == 1)
      {
        //Serial1.println("overwrite when reach lastWritePos == lastReadPos");
        //continue writing

        overWrote = 1;
        digitalWrite(3, HIGH);
      }
     
        //Stop writing
       if(setFlag == 0)
       {//stop overwriting but has overwritten
        //Serial1.println("stop writing when lastWritePos == lastReadPos");
        save = datastring.substring(index); 
        //Serial1.println(save);
        index = lengths;                         
        sample = 1;
        //Serial1.println("sample is" + String(sample));
        stopState = 1;
        digitalWrite(2, HIGH);
        //Serial1.println("stop writing when lastWritePos == lastReadPos");        
        overwriting = 1;
       }        
      }
    }
   datafile.close();
  }
  else
  {
    Serial1.println("error opening test.txt");
  } 
  
}
}

void readAllData() 
{
File dataFile = SD.open("datalog.txt");

  if(overwriting == 0)
  {
  // if the file is available, write to it:
    if (dataFile) 
    {
      dataFile.seek(0);
      lastReadPos = 0; // need so that first value read is 0
      while (dataFile.available()) 
      {
        readNum++;
        //Serial1.print(String(lastReadPos)+"|");
        Serial1.write(dataFile.read());
        lastReadPos = dataFile.position();
      }
      dataFile.close();
    }
  // if the file isn't open, pop up an error:
    else 
    {
      Serial1.println("error opening datalog.txt");
    }
  }
  if(overwriting == 1)
  {  
    if (dataFile) 
    { 
      if(stopState == 0)
      {
      lastReadPos = lastWritePos;   //because have to read old data first and then new data
      }
      int lastReadPos1 = lastReadPos;      
      dataFile.seek(lastReadPos);      
      while (dataFile.available())
      {
        readNum++;
        //Serial1.print(String(lastReadPos)+"|");
        Serial1.write(dataFile.read());
        lastReadPos = dataFile.position();
        if(lastReadPos == MemorySize)
        {
          lastReadPos = 0;
          if(amountReadreachEnd<amountWritereachEnd)
          {
          amountReadreachEnd++; 
          //Serial1.println("amountReadreachEnd is " + String(amountReadreachEnd));
          }
        }                    
      }      
      while(lastReadPos1 != lastReadPos)
      {
        dataFile.seek(lastReadPos);
        //Serial1.print(String(lastReadPos)+"|");
        Serial1.write(dataFile.read());
        readNum++;
        lastReadPos = dataFile.position();    
      }
      if(stopState ==1)
      {
      lastReadPos = lastWritePos;   //because read all data now only have to read latest
      }
      dataFile.close() ; 
    }
    else 
    {
    Serial1.println("error opening datalog.txt");
    } 
    if(overWrote==1)
    {
      overWrote = 0;
      digitalWrite(3, LOW);
      amountReadreachEnd = 0;
      amountWritereachEnd = 0;       
    }
  }
  Serial1.println();
}

void test()
{
  File dataFile = SD.open("datalog.txt");

  // if the file is available, write to it:
  if (dataFile) {
    while (dataFile.available()) {
      Serial1.write(dataFile.read());
    }
    dataFile.close();
  }
  // if the file isn't open, pop up an error:
  else {
    Serial1.println("error opening datalog.txt");
  }
}


/****************************************************/



String getTime(void) {
  String returnString = "";

  returnString += String(rtc.getYear());

  returnString += "-";

  if (rtc.getMonth() < 10)
    returnString += "0" + String(rtc.getMonth());
  else
    returnString += String(rtc.getMonth());

  returnString += "-";

  if (rtc.getDay() < 10)
    returnString += "0" + String(rtc.getDay());
  else
    returnString += String(rtc.getDay());
    
  returnString += " ";    

  if (rtc.getHours() < 10)
    returnString += "0" + String(rtc.getHours());
  else
    returnString += String(rtc.getHours());

  returnString += ":";

  if (rtc.getMinutes() < 10)
    returnString += "0" + String(rtc.getMinutes());
  else
    returnString += String(rtc.getMinutes());

  returnString += ":";

  if (rtc.getSeconds() < 10)
    returnString += "0" + String(rtc.getSeconds());
  else
    returnString += String(rtc.getSeconds());

  return returnString;
}

  


