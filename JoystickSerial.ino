
int XPin = 0;   
int YPin = 1;      
int ButtonPin = 6;  

void setup()
{
  pinMode(ButtonPin, INPUT);  
  digitalWrite(ButtonPin,HIGH);
  Serial.begin(9600);
}

void loop()
{
  byte Yval = analogRead(YPin) / 4.1 + 1;
  byte Xval = analogRead(XPin) / 4.1 + 1;  
  byte ButtonVal = digitalRead(ButtonPin) + 1;  
  
  Serial.write(0);
  Serial.write(ButtonVal);
  Serial.write(Yval);
  Serial.write(Xval);
  
  delay(100);
}
