#include <Wire.h>
#include<WiFi.h>;
#include<HTTPClient.h>
#include<ArduinoJson.h>;

#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS    1000
#define REPORTING_PERIOD_MS_relay    3000
#define threshold 32
PulseOximeter max_sensor;
uint32_t lastReportTime = 0;
uint32_t lastReportTime_relay = 0;
int tog=0;
const char* ssid="7asn";
const char* password="barcelona";
char jsonOutput[128];




void onBeatDetected()
{
   Serial.println("Beat!");
}

#define BUZZER_PIN 25
#define relay 30

void setup() {
 // put your setup code here, to run once:
 pinMode(BUZZER_PIN, OUTPUT);
 pinMode(relay, OUTPUT);
 digitalWrite(relay, HIGH);


 Serial.begin(115200);
  WiFi.begin(ssid,password);
  Serial.print("connecting ti wifi");
  while(WiFi.status()!=WL_CONNECTED){
    Serial.print(".");
    delay(500);
  }
  
Serial.print("\nconnected to the wifi network");
Serial.print("ip address: ");
Serial.print(WiFi.localIP());



   Serial.print("Initializing pulse oximeter..");

//    Initialize the PulseOximeter instance
//    Failures are generally due to an improper I2C wiring, missing power supply
//    or wrong target chip
  if (!max_sensor.begin()) {
       Serial.println("FAILED");
       for(;;);
   } else {
       Serial.println("SUCCESS");
   }
       max_sensor.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
 // put your main code here, to run repeatedly:
// digitalWrite(BUZZER_PIN, HIGH);
// delay(1000);
// digitalWrite(BUZZER_PIN, LOW);
// delay(1000);
if((WiFi.status()==WL_CONNECTED)){

    HTTPClient client;
    client.begin("URL ");
    client.addHeader("Content Type","application/json");
    const size_t CAPACITY=JSON_OBJECT_SIZE(1);
    StaticJsonDocument<CAPACITY> doc;
    JsonObject object = doc.to<JsonObject>();
    object["title"]="ay 5araa";
    serializeJson(doc,jsonOutput);
    int httpCode=client.POST(String(jsonOutput));
    if(httpCode>0){
      String payload=client.getString();
      Serial.println("\nStatuscode: " + String(httpCode));
      Serial.println(payload);
      client.end();
      
    }
   else{
    
         Serial.println("Error on HTTP request");}
    
     

}
else
{
 Serial.println("connection lost");}
  delay(10000);


  unsigned long currentTime = millis();
  unsigned long currentTime_RELAY = millis();
 

  max_sensor.update();


   if (currentTime - lastReportTime > REPORTING_PERIOD_MS) {
       
       Serial.println(max_sensor.getHeartRate());
       lastReportTime=currentTime;
   }
   if(max_sensor.getHeartRate()<threshold){
     digitalWrite(relay, LOW);
     digitalWrite(BUZZER_PIN, HIGH);
     tog=1;
     
       
   }
   if(tog==1){
    if (currentTime_RELAY - lastReportTime_relay > REPORTING_PERIOD_MS_relay) {
        digitalWrite(relay, HIGH);
        digitalWrite(BUZZER_PIN, LOW);
        lastReportTime_relay=currentTime;
        tog=0;
    
    }
   }
    
   
   
   
}