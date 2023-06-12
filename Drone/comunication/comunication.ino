String axis0_1;
String axis1_1;
String axis0_2;
String axis1_2;
String lt;
String rt;
String a_button;
String b_button;
String x_button;
String y_button;
String lb_button;
String rb_button;
String back_button;
String start_button;

unsigned long previousMillis = 0;  // Variable to store the previous update time
const unsigned long updateInterval = 100;  // Update interval in milliseconds

void setup() {
  Serial.begin(9600);
  Serial.println();  // Print an empty line to clear the initial line
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    Serial.print('\r');          // Move the cursor to the beginning of the line
    
    // Parse the input string into individual variables
    axis0_1 = getValue(input, "axis0_1:");
    axis1_1 = getValue(input, "axis1_1:");
    axis0_2 = getValue(input, "axis0_2:");
    axis1_2 = getValue(input, "axis1_2:");
    lt = getValue(input, "lt:");
    rt = getValue(input, "rt:");
    a_button = getValue(input, "a_button:");
    b_button = getValue(input, "b_button:");
    x_button = getValue(input, "x_button:");
    y_button = getValue(input, "y_button:");
    lb_button = getValue(input, "lb_button:");
    rb_button = getValue(input, "rb_button:");
    back_button = getValue(input, "back_button:");
    start_button = getValue(input, "start_button:");
  }
  
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= updateInterval) {
    previousMillis = currentMillis;
    
    // Print the individual variables
    Serial.print("axis0_1: ");
    Serial.println(axis0_1);
    Serial.print("axis1_1: ");
    Serial.println(axis1_1);
    // Repeat for other variables...
  }
}

// Function to extract the value associated with a specific key from a string
String getValue(String data, String key) {
  int keyIndex = data.indexOf(key);
  if (keyIndex >= 0) {
    int valueIndex = keyIndex + key.length();
    int endIndex = data.indexOf(" ", valueIndex);
    if (endIndex < 0) {
      endIndex = data.length();
    }
    return data.substring(valueIndex, endIndex);
  }
  return "";
}
