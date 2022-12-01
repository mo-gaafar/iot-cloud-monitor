#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

SoftwareSerial ard(0, 2);
String task[5]; // id,arg1,arg2,arg3,arg4

void setup()
{
  WiFi.mode(WIFI_STA); // start wifi as station
  Serial.begin(9600);
  ard.begin(9600); // start serial port
}

void loop()
{
  if (ard.available())
    task_read(); // check for msg
}

byte task_read()
{
  String buff = ard.readStringUntil('\n'); // read serial port until \n (new line)
  task[0] = buff.charAt(0);                // set up the id
  buff = buff.substring(1);
  task[1] = "";
  task[2] = ""; // remove the first char, and clear tasks
  int ind = 1;  // indexing value
  for (int l = 0; l < buff.length(); l++)
  {
    if (buff.charAt(l) == '\t')
      ind++;
    else
      task[ind] += buff.charAt(l); // write datas to task
  }
  byte id = byte(task[0].charAt(0)); // set up id
  byte invert = ~id;                 // create invert data
  Serial.print("id: ");
  Serial.print(id);
  Serial.print("\t"); // print incomeing datas
  Serial.print("Invert: ");
  Serial.println(invert);             // not necessary, just for debuging
  String resp = String(char(invert)); // add invert id to response
  switch (id)                         // check for command
  {
  case 1:
  {
    // WiFi client
    resp += wifi_connect(task[1], task[2]); // add the return datas to 'resp'
    Serial.print("Resp:\t");
    Serial.println(resp.substring(1));
    break;
  }
  case 2:
  {
    // WiFi AP
    break;
  }
  case 3:
  {
    // scan network
    resp += scan();
    Serial.print("Resp:\t");
    Serial.println(resp.substring(1));
    break;
  }
  case 4:
  {
    // is connected?
    if (WiFi.status() == WL_CONNECTED)
      resp += "connected";
    else
      resp += "disconnected";
    Serial.print("Resp:\t");
    Serial.println(resp.substring(1));
    break;
  }
  case 9:
  {
    WiFi.disconnect();
    resp += "ok";
    break;
  }
  case 21:
  {
    // http client
    resp += http_client(task[1]);
    Serial.print("Resp:\t");
    Serial.println(resp.substring(1));
    break;
  }
  }
  resp += String(char(244)); // Add the closing character
  ard.println(resp);         // send datas
}

String wifi_connect(String ssid, String password)
{
  Serial.println("Wifi connect to");
  Serial.print(ssid);
  Serial.print("\t");
  Serial.println(password);
  WiFi.mode(WIFI_STA);        // set up wifi as station
  WiFi.begin(ssid, password); // connect to network
  for (int tim = 0; tim < 30; tim++)
  {
    if (WiFi.status() == WL_CONNECTED)
      break;
    else
      delay(500);
  }
  // try for 15 seconds connect to network
  Serial.println(WiFi.localIP());
  if (WiFi.status() == WL_CONNECTED)
    return (String(WiFi.localIP()[0]) + "." + String(WiFi.localIP()[1]) + "." + String(WiFi.localIP()[2]) + "." + String(WiFi.localIP()[3]));
  else
    return "0";
  // if we succeed, we will return with the ip address, if we do not return with 0
}

String scan()
{

  int n = WiFi.scanNetworks();
  if (n == 0)
    return "0 networks availabele";
  else
  {
    String ret = "";
    for (int i = 0; i < n; ++i)
    {
      ret += WiFi.SSID(i);
      ret += "\t";
      ret += WiFi.RSSI(i);
      ret += "\t";
      ret += ((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? "Opened" : "Closed");
      ret += "\n";
    }
    return ret;
  }
}

String http_client(String URL)
{
  if ((WiFi.status() == WL_CONNECTED))
  {
    WiFiClient client;
    HTTPClient http;
    if (http.begin(client, URL))
    {
      int httpCode = http.GET();
      if (httpCode > 0)
      {
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
        {
          String payload = http.getString();
          http.end();
          return payload; // return with the source code
        }
      }
      else
        return "False request";
    }
  }
  else
  {
    return "Not connected";
  }
}