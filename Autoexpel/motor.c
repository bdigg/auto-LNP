// Adapted from Niall McIntyre 2023 (Adapted from Nick Brooks)

#include <ezButton.h>



const byte numChars = 32;
char receivedChars[numChars];

char messageFromPC = 0;
int integerFromPC = 0;
float floatFromPC = 0.0;

boolean newData = false;
 // create ezButton object that attaches to pin 12

const int dirPin1 = 2;
const int stepPin1 = 3;
const int dirPin2 = 8;
const int stepPin2 = 9;
const int motorSpeed = 1000;

const int ls1 = 4;
const int ls2= 10;

ezButton limitSwitch1(ls1);
ezButton limitSwitch2(ls2);




// Functions to run the motor

//Sets the direction and speed of motor
//Sets the direction and speed of motor
void setMotor1Direction (int value) {
  digitalWrite(dirPin1, value);
  Serial.println("Turnt1");

}


void setMotor2Direction (int value) {
  digitalWrite(dirPin2, value);
  Serial.println("Turnt2");
}




void setDistance1 (int distance){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(motorSpeed);

  }
  Serial.println("Moved1");

}


void setDistance1LS (int distance, int speed){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(speed);

  }

}
void setDistance2 (int distance){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(motorSpeed);

  }
  Serial.println("Moved2");

}

void setDistance2LS (int distance, int speed){
  for (int x = 0; x < distance; x++)
  {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(speed);

  }

}

void setMotor1DirectionLS (int value) {
  digitalWrite(dirPin1, value);

}


void setMotor2DirectionLS (int value) {
  digitalWrite(dirPin2, value);
}


void Homing() {
  bool isStopped1 = false;
  bool isStopped2 = false;
  bool isStopped3 = false;
  bool isStopped4 = false;



  while (!isStopped1) {
    limitSwitch1.loop();

    setMotor1DirectionLS(1);
    setMotor2DirectionLS(1);
    

    setDistance1LS(1, 1000);

    if (limitSwitch1.isPressed()) {
      isStopped1 = true;
    }
  }

  // Once Stepper1 has hit its limit switch and set its position, move Stepper2
  if (isStopped1) {
    delay(1000);
    setMotor1DirectionLS(0);
    setDistance1LS(50, 1000);
    setMotor1DirectionLS(1);
    delay(1000);





    while (!isStopped2) {
      limitSwitch1.loop();
      
      setDistance1LS(1, 1000);

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
      
      setDistance2LS(1, 1000);


      if (!isStopped3) {
        if (limitSwitch2.isPressed()) {
          isStopped3 = true;
        }
      }
    }
  }

  if (isStopped3) {
    delay(1000);
    setMotor2DirectionLS(0);
    setDistance2LS(50, 1000);
    setMotor2DirectionLS(1);
    delay(1000);





    while (!isStopped4) {
      limitSwitch2.loop();
      
      setDistance2LS(1, 1000);
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




void HomingTest2() {
  bool isStopped1 = false;
  bool isStopped2 = false;
  int counter1 = 0;
  int counter2 = 0;


  while (!isStopped1) {
    limitSwitch1.loop();

    setMotor1DirectionLS(1);
    setMotor2DirectionLS(1);

    setDistance1LS(1, 1000);
    counter1++;  // Increment counter1

    if (limitSwitch1.isPressed()) {
      isStopped1 = true;
      Serial.println("Limit switch 1 pressed");
    }
  }
  Serial.print("Counter 1: ");
  Serial.println(counter1);

  // Once Stepper1 has hit its limit switch and set its position, move Stepper2
  if (isStopped1) {
    while (!isStopped2) {
      limitSwitch2.loop();
      setDistance2LS(1, 1000);
      counter2++;  // Increment counter2

      if (!isStopped2) {
        if (limitSwitch2.isPressed()) {
          isStopped2 = true;
          Serial.println("Stepper 2 stopped");
        }
      }
    }
  }
  Serial.print("Counter 2: ");
  Serial.println(counter2);
}

void HomingTRIAL2() {
  bool isStopped1 = false;
  bool isStopped2 = false;
  bool isStopped3 = false;
  bool isStopped4 = false;


  while (!isStopped1) {
    limitSwitch1.loop();

    setMotor1DirectionLS(1);
    setMotor2DirectionLS(1);
    

    setDistance1LS(1, 1000);

    if (limitSwitch1.isPressed()) {
      isStopped1 = true;
    }
  }

  // Once Stepper1 has hit its limit switch and set its position, move Stepper2
  if (isStopped1) {
    delay(1000);
    setMotor1DirectionLS(0);
    setDistance1LS(50, 1000);
    setMotor1DirectionLS(1);
    delay(1000);





    while (!isStopped2) {
      limitSwitch1.loop();
      
      setDistance1LS(1, 1000);
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
      
      setDistance2LS(1, 1000);


      if (!isStopped3) {
        if (limitSwitch2.isPressed()) {
          isStopped3 = true;
        }
      }
    }
  }

  if (isStopped3) {
    delay(1000);
    setMotor2DirectionLS(0);
    setDistance2LS(50, 1000);
    setMotor2DirectionLS(1);
    delay(1000);





    while (!isStopped4) {
      limitSwitch2.loop();
      
      setDistance2LS(1, 1000);
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
  atofIndx = receivedChars + 1;
  floatFromPC = atof(atofIndx);

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
    setMotor1Direction (floatFromPC);
  }

  else if (messageFromPC == 'N') {
    setMotor2Direction (floatFromPC);
  }

  else if (messageFromPC == 'L'){
    setDistance1 (floatFromPC);
  }
  
  else if (messageFromPC == 'P'){
    setDistance2 (floatFromPC);
  }
  else if (messageFromPC == 'Q'){
    HomingTest2 ();
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