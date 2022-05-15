#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

WiFiClient wifiClient;
const int GPIO_1 = 2;

void setup () {

  pinMode(GPIO_1, OUTPUT);
  digitalWrite(GPIO_1, 0);
  
  Serial.begin(115200);
  WiFi.begin("ADITII Radio", "47111999");
  
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
 
  }
  Serial.println("Connected to WiFi Network");
 
}
 
void loop() {
 
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    HTTPClient http;  //Declare an object of class HTTPClient
 
    //http.begin(wifiClient,"http://192.168.0.104:8080/esp"); //Specify request destination

    http.begin(wifiClient,"http://tiitc22-pa1tech.herokuapp.com/esp"); 
 
    int httpCode = http.GET(); //Send the request
 
    if (httpCode > 0) { //Check the returning code
 
      String payload = http.getString();   //Get the request response payload
      Serial.println(payload.charAt(0));             //Print the response payload
      
      if (payload.charAt(0) == '1'){
        digitalWrite(GPIO_1, 0);
      }else{
        digitalWrite(GPIO_1, 1);
      }
 
    }else Serial.println("Error");
 
    http.end();   //Close connection
 
  }
 
  delay(10000);    //Send a request every 10 seconds
 
}
