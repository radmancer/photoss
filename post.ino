#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte server[] = { 192, 168, 1, 126 }; //A server on the intranet.

byte servers[2][4] = { 
  { 192, 168, 1, 123 },
  { 192, 168, 1, 126 }
};

EthernetClient client;

void setup()
{
  Ethernet.begin(mac);
  Serial.begin(9600);

  delay(1000);

  Serial.println("Enter Photo Time (hh:mm): ");
  while (Serial.available() == 0) {}     //wait for data available
  String timestamp = Serial.readString();  //read until timeout
  timestamp.trim();

  Serial.println("connecting...");

  for(int i = 0; i < sizeof(servers) - 1; i++){
    if (client.connect(servers[i], 5000)) {
      String unitString = String((i + 1));//plus one because unit zero is down.
      String data = "unit=" + unitString + ";" + timestamp;
      Serial.println("connected");
      client.println("POST / HTTP/1.1");
      client.println("Host: 192.168.1.126");
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.print("Content-Length: ");
      client.println(data.length());
      client.println();
      client.print(data);
    } else {
      Serial.println("connection failed");
    } 
  }
}

void loop()
{
  
}
