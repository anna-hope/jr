int XPin = 0 ;   
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
  
  TransmitData(ButtonVal, Yval, Xval);
  delay(100);
}


void TransmitData( byte ButtonVal, byte Yval, byte Xval)
{
  Serial.print(0);
  Serial.print(" ");
  Serial.print(ButtonVal);
  Serial.print(" ");
  Serial.print(Yval);
  Serial.print(" ");
  Serial.println(Xval);
}
