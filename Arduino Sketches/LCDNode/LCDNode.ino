#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <LiquidCrystal_I2C.h>

const char* ssid = "NETGEAR18";
const char* password = "dizzypiano125";
LiquidCrystal_I2C lcd(0x3F, 16, 2);

ESP8266WebServer server(80);
IPAddress local_ip(192,168,1,10);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Temperature:");
  lcd.setCursor(0,1);
  Serial.begin(115200);
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
  server.on("/recieveTemp", HTTP_POST, []() {
    if(server.hasArg("temp")){
      int temp = server.arg("temp").toInt();
      lcd.setCursor(0,1);
      lcd.print(temp);
      server.send(200, "text/plain", "Temp was set");
    } 
    else {
      server.send(400, "text/plain", "Not a valid input");
    }
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
