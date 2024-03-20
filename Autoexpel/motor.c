// Adapted from Niall McIntyre 2023 (Adapted from Nick Brooks)


#include <ezButton.h>



const byte numChars = 32;
char receivedChars[numChars];

char messageFromPC = 0;
int integerFromPC = 0;
float floatFromPC1 = 0.0;
float floatFromPC2 = 0.0;
boolean newData = false;
 // create ezButton object that attaches to pin 12

const int dirPin1 = 2;
const int stepPin1 = 3;
const int dirPin2 = 5;
const int stepPin2 = 6;
const int dirPin3 = 8;
const int stepPin3 = 9;
const int motorSpeed = 1000;

const int ls1 = 4;
const int ls2= 7;
const int ls3= 11;


ezButton limitSwitch1(ls1);
ezButton limitSwitch2(ls2);




// Functions to run the motor

//Sets the direction and speed of motor
//Sets the direction and speed of motor
void setMotorHorzDirection (int value) {
  digitalWrite(dirPin1, value);
  Serial.println("Turnt1");

}


void setMotorVertDirection (int value) {
  digitalWrite(dirPin3, value);
  if (value == 0) {
    value = 1;
  }
  else {
    value = 0;
  }
  digitalWrite(dirPin2, value);
  Serial.println("Turnt2");
}




void setDistanceHorz (int distance){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(motorSpeed);

  }
  Serial.println("Moved1");

}


void setDistanceHorzLS (int distance, int speed){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(speed);

  }

}
void setDistanceVert (int distance){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(motorSpeed);
  }

  Serial.println("Moved2");

}

void setDistanceVertLS (int distance, int speed){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(speed);
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(speed);

  }

}

void setMotorHorzDirectionLS (int value) {
  digitalWrite(dirPin1, value);

}

void setMotorVertDirectionLS (int value) {
  digitalWrite(dirPin3, value);
  if (value == 0) {
    value = 1;
  }
  else {
    value = 0;
  }
  digitalWrite(dirPin2, value);
}

void setDistanceBoth(int distance1, int distance2) {
  int steps1 = abs(distance1); // Number of steps for horizontal (m1)
  int steps2 = abs(distance2); // Number of steps for motor (m2 and m3)
  Serial.println(steps1,steps2);

  // Loop through the maximum number of steps for both motors
  for (int x = 0; x < max(steps1, steps2); x++) {
    // Control motor 1 if there are remaining steps
    if (x < steps1) {
      digitalWrite(stepPin1, HIGH);
      delayMicroseconds(motorSpeed);
      digitalWrite(stepPin1, LOW);
      delayMicroseconds(motorSpeed);
    }

    // Control motor 2 if there are remaining steps
    if (x < steps2) {
      digitalWrite(stepPin2, HIGH);
      delayMicroseconds(motorSpeed);
      digitalWrite(stepPin2, LOW);
      delayMicroseconds(motorSpeed);
      digitalWrite(stepPin3, HIGH);
      delayMicroseconds(motorSpeed);
      digitalWrite(stepPin3, LOW);
      delayMicroseconds(motorSpeed);

    Serial.println(x);

    }
  }

  Serial.println("Moved Both");
}


void Homing() {
  bool isStopped1 = false;
  bool isStopped2 = false;
  bool isStopped3 = false;
  bool isStopped4 = false;



  while (!isStopped1) {
    limitSwitch1.loop();

    setMotorHorzDirectionLS(1);
    setMotorVertDirectionLS(1);
    

    setDistanceHorzLS(1, 1000);

    if (limitSwitch1.isPressed()) {
      isStopped1 = true;
    }
  }

  // Once Stepper1 has hit its limit switch and set its position, move Stepper2
  if (isStopped1) {
    delay(1000);
    setMotorHorzDirectionLS(0);
    setDistanceHorzLS(50, 1000);
    setMotorHorzDirectionLS(1);
    delay(1000);





    while (!isStopped2) {
      limitSwitch1.loop();
      
      setDistanceHorzLS(1, 1000);

      delay(100);


      if (!isStopped2) {
        if (limitSwitch1.isPressed()) {
          isStopped2 = true;

        }
      }
    }
  }



  if (isStopped2) {
    delay(1000);


    while (!isStopped3) {
      limitSwitch2.loop();
      
      setDistanceVertLS(1, 1000);


      if (!isStopped3) {
        if (limitSwitch2.isPressed()) {
          isStopped3 = true;
        }
      }
    }
  }

  if (isStopped3) {
    delay(1000);
    setMotorVertDirectionLS(0);
    setDistanceVertLS(50, 1000);
    setMotorVertDirectionLS(1);
    delay(1000);





    while (!isStopped4) {
      limitSwitch2.loop();
      
      setDistanceVertLS(1, 1000);
      delay(100);


      if (!isStopped4) {
        if (limitSwitch2.isPressed()) {
          isStopped4 = true;
          Serial.println("Done");
        }
      }
    }
  }




}


/****** Functions to handle serial communication with the computer*******/


void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}


void parseData() {      // split the data into its parts

  char* atofIndx;

  //First character represents command
  messageFromPC = receivedChars[0];

  //Remainder of received data converted to number
  atofIndx = strtok(receivedChars + 1, ",");
  floatFromPC1 = atof(atofIndx);

}

// Process commands received from the computer

void showParsedData() {
  /*
    Serial.print("Message ");
    Serial.println(messageFromPC);
    Serial.print("Float ");
    Serial.println(floatFromPC);
  */

  if (messageFromPC == 'M') {
    setMotorHorzDirection (floatFromPC1);
  }

  else if (messageFromPC == 'N') {
    setMotorVertDirection (floatFromPC1);
  }

  else if (messageFromPC == 'L'){
    setDistanceHorz (floatFromPC1);
  }
  
  else if (messageFromPC == 'P'){
    setDistanceVert (floatFromPC1);
  }

  else if (messageFromPC == 'B') {
    setDistanceBoth (floatFromPC1,floatFromPC2);
  }
  
  else if (messageFromPC == 'H'){
    Homing ();
  }
  else {
    Serial.println("?");
  }

}





void setup() {
  // put your setup code here, to run once:
	pinMode(stepPin1, OUTPUT);
	pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
	pinMode(dirPin2, OUTPUT);
  pinMode(stepPin3, OUTPUT);
	pinMode(dirPin3, OUTPUT);



  Serial.begin(115200);
  while (!Serial) {
  delay(1);}
  Serial.println("We are Connected");
  

}

void loop() {
  recvWithStartEndMarkers();
  if (newData == true) {
    parseData();
    showParsedData();
    newData = false;
  }
}
