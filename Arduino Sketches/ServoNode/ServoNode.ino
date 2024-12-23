#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

Servo servo;

const char* ssid = "NETGEAR18";
const char* password = "dizzypiano125";

ESP8266WebServer server(80);
IPAddress local_ip(192,168,1,12);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

void setup() {
    servo.attach(D4);
    Serial.begin(115200);
    WiFi.config(local_ip, gateway, subnet);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    server.on("/Open_Door", []() {
        // Code to turn on LED
        servo.write(180);
        server.send(200, "text/plain", "Door is Opened");
    });

    server.on("/Close_Door", []() {
        // Code to turn off LED
        servo.write(0);
        server.send(200, "text/plain", "Door is Closed");
    });

    server.begin();
}

void loop() {
    server.handleClient();
}