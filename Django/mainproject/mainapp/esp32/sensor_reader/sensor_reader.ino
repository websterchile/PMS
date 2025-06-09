#include <DHT.h>
#include <ArduinoJson.h>

// Sensor pins
#define DHT_PIN 4       // DHT11 data pin (GPIO 4)
#define VIBRATION_PIN 34 // SW-420 analog output pin (GPIO 34)
#define DHT_TYPE DHT11  // DHT11 sensor type

// Pump ID
const char* pumpId = "pump1";

// Initialize DHT sensor
DHT dht(DHT_PIN, DHT_TYPE);

// Function to get current timestamp (approximate, without NTP)
String getFormattedTimestamp() {
  unsigned long epochTime = millis() / 1000; // Simple epoch time in seconds
  // Convert to YYYY-MM-DD HH:MM:SS (approximate)
  char buf[20];
  snprintf(buf, sizeof(buf), "2025-06-03 %02d:%02d:%02d",
           (epochTime % 86400) / 3600, (epochTime % 3600) / 60, epochTime % 60);
  return String(buf);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Initialize DHT11
  dht.begin();

  // Initialize SW-420 (analog input, no setup needed)
  pinMode(VIBRATION_PIN, INPUT);
  Serial.println("Sensors initialized");
}

void loop() {
  // Read temperature from DHT11
  float temperature = dht.readTemperature();
  if (isnan(temperature)) {
    Serial.println("Error: Could not read temperature from DHT11");
    temperature = -999; // Error value
  }

  // Read vibration from SW-420 (analog, 0-1023)
  int vibrationRaw = analogRead(VIBRATION_PIN);
  // Scale to 0-100 (arbitrary units for vibration intensity)
  float vibration = map(vibrationRaw, 0, 1023, 0, 100);
  if (vibrationRaw < 0) {
    Serial.println("Error: Could not read vibration from SW-420");
    vibration = -999; // Error value
  }

  // Get timestamp
  String timestamp = getFormattedTimestamp();

  // Prepare JSON payload
  StaticJsonDocument<200> doc;
  doc["pump_id"] = pumpId;
  doc["timestamp"] = timestamp;
  doc["vibration"] = vibration;
  doc["temperature"] = temperature;
  String payload;
  serializeJson(doc, payload);

  // Send JSON over serial
  Serial.println(payload);

  // Wait 60 seconds before next reading
  delay(60000);
}