#include "Wire.h" // This library allows you to communicate with I2C devices.
#include <SoftwareSerial.h>


SoftwareSerial mySerial(2, 3); // RX, TX
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED}; // MAC address of your Arduino
IPAddress server_addr(127,0,0,1); // IP address of your MySQL server
char user[] = "alexcarola"; // MySQL username
char password[] = "123321"; // MySQL password

WiFiClient client;
MySQL_Connection conn((Client *)&client);

///////////////////////////////////

const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.

int16_t accelerometer_x, accelerometer_y, accelerometer_z; // variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z; // variables for gyro raw data
int16_t temperature; // variables for temperature data

char tmp_str[7]; // temporary variable used in convert function

char* convert_int16_to_str(int16_t i) { // converts int16 to string. Moreover, resulting strings will have the same length in the debug monitor.
  sprintf(tmp_str, "%6d", i);
  return tmp_str;
}

 int aX ;
 int aY ;
 int aZ ;
 int temp; 
 int gX ;
 int gY ;
 int gZ ;
 int dist; 

void setup() {
 Serial.begin(9600);
  Wire.begin();
  Wire.beginTransmission(MPU_ADDR); // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0); // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  pinMode(2, OUTPUT);//define arduino pin
  pinMode(4, INPUT);//define arduino pin
}

void loop() {
   Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
  Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
  Wire.requestFrom(MPU_ADDR, 7*2, true); // request a total of 7*2=14 registers
  
  // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
  accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
  accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
  accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
  temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
  gyro_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
  gyro_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
  gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)



  digitalWrite(2, LOW);
  delayMicroseconds(4);
  digitalWrite(2, HIGH);
  delayMicroseconds(10);
  digitalWrite(2, LOW);
  
  long t = pulseIn(4, HIGH);//input pulse and save it veriable
  long cm = t / 29 / 2; //time convert distance
  String CM = " cm";


  
  // print out data
  Serial.print("aX = "); Serial.print(convert_int16_to_str(accelerometer_x));
  Serial.print(" | aY = "); Serial.print(convert_int16_to_str(accelerometer_y));
  Serial.print(" | aZ = "); Serial.print(convert_int16_to_str(accelerometer_z));
  // the following equation was taken from the documentation [MPU-6000/MPU-6050 Register Map and Description, p.30]
  Serial.print(" | tmp = "); Serial.print(temperature/340.00+36.53);
  Serial.print(" | gX = "); Serial.print(convert_int16_to_str(gyro_x));
  Serial.print(" | gY = "); Serial.print(convert_int16_to_str(gyro_y));
  Serial.print(" | gZ = "); Serial.print(convert_int16_to_str(gyro_z));
  Serial.print(" | dist = "); Serial.print(cm + CM);
  Serial.println();//print space

  //////////////////////////////
    
 aX = accelerometer_x;
 aY = accelerometer_y;
 aZ = accelerometer_z;
 temp = temperature/340.00+36.53;
 gX = gyro_x;
 gY = gyro_y;
 gZ = gyro_z;
 dist = cm ;

  // Connect to MySQL server
  if (conn.connect(server_addr, 3306, user, password)) {
    Serial.println("Connected to MySQL server!");

    // Execute SQL query to insert data into table
    char drone[200];
    sprintf(drone, "INSERT INTO sensores (aX, aY, aZ, temp, gX, gY, gZ, dist) VALUES (%d, %d, %d, %d, %d, %d, %d, %d)", aX, aY, aZ, temp, gX, gY, gZ, dist);
    Serial.println(drone);
    MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);
   
  // delay
  delay(500);
}
}
