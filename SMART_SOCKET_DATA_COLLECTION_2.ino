#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <PZEM004Tv30.h>
#include <math.h>

#define PZEM_RX_PIN D5
#define PZEM_TX_PIN D6

SoftwareSerial pzemSWSerial(PZEM_RX_PIN, PZEM_TX_PIN);
PZEM004Tv30 pzem(pzemSWSerial);

const char* ssid = "ADMIN";
const char* password = "Smartsocket@114";
const char* host = "script.google.com";
const int httpsPort = 443;

WiFiClientSecure client;

String GAS_ID = "AKfycbxTEpVXfEWTAnAXQWdAUZuKY0pEMnSMgzW9q_n_G7UEqtcRdiWegRXagnvLaVTr8TMR";

unsigned long previousMillis = 0;
const unsigned long interval = 600000; // 10 minutes in milliseconds

void setup() {
  Serial.begin(115200);
  delay(500);
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("");
  Serial.print("Successfully connected to: ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  client.setInsecure();
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (!client.connect(host, httpsPort)) {
      Serial.println("Connection failed");
      return;
    }

    float v = pzem.voltage();
    float c = pzem.current();
    float p = pzem.power();
    float e = pzem.energy();
    float f = pzem.frequency();
    float pf = pzem.pf();

     if (isnan(v) || isnan(c) || isnan(p) || isnan(e) || isnan(f) || isnan(pf)) {
   
    delay(1000);
    return;
  }

    String string_voltage = String(v);
    String string_current = String(c);
    String string_pf = String(pf);
    String string_energy = String(e);
    String string_power = String(p);
    String string_frequency = String(f);

    String url = "/macros/s/" + GAS_ID + "/exec?Voltage=" + string_voltage + "&Current=" + string_current + "&pf=" + string_pf + "&Energy=" + string_energy + "&Power=" + string_power + "&frequency=" + string_frequency;
    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "User-Agent: BuildFailureDetectorESP8266\r\n" +
                 "Connection: close\r\n\r\n");

    Serial.print("Requesting URL: ");
    Serial.println(url);

    while (client.connected()) {
      String line = client.readStringUntil('\n');
      if (line == "\r") {
        Serial.println("Headers received");
        break;
      }
    }

    String line = client.readStringUntil('\n');
    if (line.startsWith("{\"state\":\"success\"")) {
      Serial.println("Data sent successfully!");
    } else {
      Serial.println("Data transmission failed");
    }

    Serial.print("Reply was: ");
    Serial.println(line);
    Serial.println("Closing connection");
    Serial.println("==========");
    Serial.println();

    client.stop();
    pzem.resetEnergy();
  }

}
