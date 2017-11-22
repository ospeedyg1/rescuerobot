// HC-SR04 ultrasound sensor with 180 micro servo 
// Modified By: Jeovanny Reyes
// Modified to work on ROS
// Raytheon Radar Guided Rescue Robot

// Input: None
// Output: None

// Publisher: pub_range publishes to "HerculesUltrasound" topic
// Subscriber: None

#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>

#include <Servo.h> 

ros::NodeHandle nh;

sensor_msgs::Range range_msg; // This creates the message "Range"
ros::Publisher pub_range( "/HerculesUltrasound", &range_msg); // 
 
// Defines Trig and Echo pins of the Ultrasonic Sensor
const int trigPin = 10;
const int echoPin = 11;

// Variables for the duration and the distance
long duration;
int distance;
Servo myServo; // Creates a servo object for controlling the servo motor


void setup() {

  nh.initNode();
  nh.advertise(pub_range);

  range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg.header.frame_id = "/USH";
  range_msg.field_of_view = 0.523; // 30 degree field of vision
  range_msg.min_range = 0.020;  // 2 cm
  range_msg.max_range = 4.00;   // 4 m
  
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  //Serial.begin(9600);
  myServo.attach(12); // Defines on which pin is the servo motor attached
}

void loop() {
  
  // rotates the servo motor from 15 to 165 degrees
  for(int i=15;i<=165;i++){   
  myServo.write(i);
  delay(30);
  
  range_msg.range = calculateDistance();
  range_msg.header.stamp = nh.now();
  pub_range.publish( &range_msg);
  
  }
  // Repeats the previous lines from 165 to 15 degrees
  for(int i=165;i>15;i--){  
  myServo.write(i);
  delay(30);

  range_msg.range = calculateDistance();
  range_msg.header.stamp = nh.now();
  pub_range.publish( &range_msg);
  
  }

  nh.spinOnce();
}

// Function for calculating the distance measured by the Ultrasonic sensor
float calculateDistance(){ 
  
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH); // Reads the echoPin, returns the sound wave travel time in microseconds
  distance= duration*0.034/2;
  return distance / 100; // in meters
}
