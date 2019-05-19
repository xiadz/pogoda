/*

An Arduino controller for the weather station. Output is
shown on the LCD screen and written to the serial port
with SERIAL_BAUD speed, in the following form:
  - "Temperature: XX.X\n"
  - "Pressure: XXXX.X\n"

Units:
  - Humidity: percentage (relative humidity)
  - Temperature: degrees Celsius
  - Water level: raw analog pin reading
  - Pressure: hPa

Pin layout (for Arduino Nano):
  - A0: water level sensor analog output
  - D7: DHT11 humidity & temperature input/output pin
  - A4: SDA pin for LCD and pressure sensor
  - A5: SCL ping for LCD and pressure sensor

Required libraries:
  - Adafruit Unified Sensor, ver >= 1.0.3
  - DHT sensor library, ver >= 1.3.4
  - Adafruit BMP085 library >= 1.0.0

*/

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <Adafruit_BMP085.h>

// Output is written to serial.
#define SERIAL_BAUD 9600

// Temperature and humidity sensor.
#define DHTPIN 7
#define DHTTYPE AM2301
DHT dht(DHTPIN, DHTTYPE);

// Water level sensor.
#define WATER_SENSOR A0
#define WATER_ENABLED false

// Pressure sensor.
Adafruit_BMP085 bmp;

// Set the LCD address to 0x27 for a 16 chars and 2 line display.
LiquidCrystal_I2C lcd(0x27, 20, 4);

void setup() {
  // Initializes seral port.
  Serial.begin(SERIAL_BAUD);

  // Initializes LCD.
  lcd.init();
  lcd.backlight();
  lcd.clear();

  // Initializes DHT (temp & humidity) sensor.
  dht.begin();

  // Initializes pressure sensor.
  bmp.begin();
}

// For the LCD.
//   0: humidity and temperature
//   1: water level
int display_page = 0;

void loop() {
  // Need to wait 2 seconds for the first reading.
  delay(2000);

  // Read temperature and humidity.
  const float h = dht.readHumidity();
  const float t = dht.readTemperature();

  // Read water level.
  int water = 0;
  if (WATER_ENABLED) {
    water = analogRead(WATER_SENSOR);
  }

  // Read pressure.
  const float pressure = bmp.readPressure() / 100.0;

  // Print information to serial.
  Serial.print("Humidity: ");
  Serial.println(h);
  Serial.print("Temperature: ");
  Serial.println(t);
  if (WATER_ENABLED) {
    Serial.print("Water level: ");
    Serial.println(water);
  }
  Serial.print("Pressure: ");
  Serial.println(pressure);
  
  lcd.clear();
  if (display_page == 0) {
    // Print a message to the LCD.
    lcd.setCursor(0, 0);
    lcd.print("Hmdt: ");
    lcd.print(h);
    lcd.print(" %");
    
    lcd.setCursor(0, 1);
    lcd.print("Temp: ");
    lcd.print(t);
    lcd.print(" C");
  }

  if (display_page == 1) {
    if (WATER_ENABLED) {
      lcd.setCursor(0, 0);
      lcd.print("Water: ");
      lcd.print(water);
    }
    
    lcd.setCursor(0, 1);
    lcd.print("Pres: ");
    lcd.print(pressure);
    lcd.print("hPa");
  }

  display_page = display_page + 1;
  if (display_page == 2) {
    display_page = 0;
  }
}
