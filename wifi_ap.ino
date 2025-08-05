#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define AP_SSID "YOUR_SSID"
#define AP_PASSWD "YOUR_PASSWORD"
#define UDP_PORT 1234
#define BUFFER_LEN 255

WiFiUDP udp;
char packetBuffer[BUFFER_LEN]; //buffer to hold incoming packet

void setup_ap() {
  Serial.begin(9600);

  boolean ready = WiFi.softAP(AP_SSID, AP_PASSWD);

  while(!ready) {
    Serial.println("Starting AP...");
    delay(1000);
  }
  Serial.println("AP is ready!");
  Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  udp.begin(UDP_PORT);
}

void receive_msg(int* valLeft, int* valRight) {
  if (udp.parsePacket() > 0) {
    // read the packet into packetBufffer
    int len = udp.read(packetBuffer, BUFFER_LEN);

    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.print("Got msg: ");
    Serial.println(packetBuffer);

    if (len == 4) {
      int dirLeft = packetBuffer[0] == '+' ? 1 : -1;
      *valLeft = dirLeft * (int) packetBuffer[1]; // range: -127 to +127

      int dirRight = packetBuffer[2] == '+' ? 1 : -1;
      *valRight = dirRight * (int) packetBuffer[3];
      Serial.print("Parsed value: ");
      Serial.print(*valLeft);
      Serial.print(", ");
      Serial.println(*valRight);
    }
  }
}