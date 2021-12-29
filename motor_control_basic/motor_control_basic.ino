
#define RPWM 3 // define pin 3 for RPWM pin (output)
#define R_EN 4 // define pin 4 for R_EN pin (input)
#define R_IS 5 // define pin 5 for R_IS pin (output)

#define LPWM 6 // define pin 6 for LPWM pin (output)
#define L_EN 7 // define pin 7 for L_EN pin (input)
#define L_IS 8 // define pin 8 for L_IS pin (output)
#define CW 1 //do not change
#define CCW 0 //do not change
#define debug 1 //change to 0 to hide serial monitor debugging infornmation or set to 1 to view

#include <Servo.h>
#include <RobojaxBTS7960.h>
Servo myservo;
int pos = 90;
int actionValue =0; // For incoming signal
RobojaxBTS7960 motor(R_EN,RPWM,R_IS, L_EN,LPWM,L_IS,debug);

void setup() {
    myservo.attach(9); 
    Serial.begin(115200);// setup Serial Monitor to display information
   
    motor.begin();
    
}

void loop() 
{
  if(Serial.available()>0)
    {
    actionValue = Serial.read();
      if (actionValue == 0)
        {
          pos = 95;                       // No steer
          myservo.write(pos);
          motor.rotate(10,CCW);          // run motor with 10% speed in forward direction with no steer
          delay(500);
          motor.stop();                  // stop the motor
          
          Serial.print("No Steering");
        }
      else if (actionValue == 2)
        {          
           pos = 60;                    // steer right
           
           myservo.write(pos);
           motor.rotate(10,CCW);        // run motor with 10% speed in forward direction with left steer
           delay(500);
           motor.stop();                // stop the motor 
           
           Serial.print("Steering Left");
        }
      else
        {               
          pos = 140;                     // steer left
          myservo.write(pos);
          motor.rotate(10,CCW);          // run motor at 10% speed in forward direction with right steer
          delay(500);
          motor.stop();                 // stop the motor
          
          Serial.print("Steering Right");
        }
    }
  pos = 95; 
  myservo.write(pos);
  //delay(500);
}// loop ends 
/*
   pos = 55;
   myservo.write(pos);
   motor.rotate(10,CCW);// run motor with 10% speed in CW direction
   delay(3000);//run for 5 seconds
    motor.stop();// stop the motor    
    delay(2000);// stop for 3 seconds
    pos = 155;
    myservo.write(pos);
    motor.rotate(15,CW);// run motor at 10% speed in CCW direction
    delay(3000);// run for 5 seconds
    motor.stop();// stop the motor
    delay(2000);  // stop for 3 seconds
    pos = 90;
    myservo.write(pos);
    motor.rotate(10,CCW);// run motor with 10% speed in CW direction
    delay(3000);//run for 5 seconds
    motor.stop();// stop the motor
     delay(3000);
/*
	// slowly speed up the motor from 0 to 100% speed
    for(int i=0; i<=100; i++){ 
        motor.rotate(i,CCW);
        delay(50);
    } 
	
   // slow down the motor from 100% to 0 with 
    for(int i=100; i>0; i--){ 
        motor.rotate(i,CCW);
        delay(50);
    } 
    motor.stop();// stop motor
    delay(3000); // stop for 3 seconds        
 
 */
 
