#include <DHT.h>
#include <Servo.h>
//LEDS
#define LED_LR 2
#define LED_DR 3
#define LED_KT 4
#define LED_PS 5
#define LED_BR 6
#define LED_LP 7
#define LED_HL 8
#define LED_BH 9

//BLIND
#define N1 10
#define N2 11
#define N3 12
#define N4 13

//LDR
#define PIN_LDR A0

//PIR
#define PIN_PIR A1

#define DHT_TYPE DHT11
#define PIN_DHT A2

//VENTILACION
#define IN_1 A3
#define IN_2 A4
#define PWM A5

//RIEGO
#define IN_3 A6
#define IN_4 A7
#define PWM_P A8

//ALARMA
#define IN_5 A9
#define IN_6 A10
#define PIN_MQ A11

//LLAVE
#define F1 23
#define S1 39

DHT dht(PIN_DHT, DHT11);

Servo myServo;

void setup() {
  //LIGHTING SYSTEM 
  pinMode(PIN_PIR, INPUT);
  pinMode(LED_LR, OUTPUT);
  pinMode(LED_DR, OUTPUT);
  pinMode(LED_KT, OUTPUT);
  pinMode(LED_PS, OUTPUT);
  pinMode(LED_BR, OUTPUT);
  pinMode(LED_LP, OUTPUT);
  pinMode(LED_HL, OUTPUT);
  pinMode(LED_BH, OUTPUT);
  pinMode(N1, OUTPUT);
  pinMode(N2, OUTPUT);
  pinMode(N3, OUTPUT);
  pinMode(N4, OUTPUT);
  digitalWrite(LED_LR, 0);
  digitalWrite(LED_DR, 0);
  digitalWrite(LED_KT, 0);
  digitalWrite(LED_PS, 0);
  digitalWrite(LED_BR, 0);
  digitalWrite(LED_LP, 0);
  digitalWrite(LED_HL, 0);
  digitalWrite(LED_BH, 0);
  digitalWrite(N1, 0);
  digitalWrite(N2, 0);
  digitalWrite(N3, 0);
  digitalWrite(N4, 0);

  //VENTILACION

  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(PWM, OUTPUT);

  //RIEGO
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT);
  pinMode(PWM_P, OUTPUT);

  //TEMPERATURA Y HUMEDAD
  dht.begin();

  //ENVIO DE DATOS
  Serial.begin(2400);

  //ALARMA
  pinMode(IN_5, OUTPUT);
  pinMode(IN_6, OUTPUT);

  //LLAVE
  myServo.attach(39);
}

void lightSystem(int LDR_value, int ps_value, int &l1, int &l4, int &blind) {

  if (ps_value == HIGH) {
    digitalWrite(LED_PS, 1);
    l4 = 1;
  } else {
    digitalWrite(LED_PS, 0);
    l4 = 0;
  }
  if (LDR_value <= 100) {
    digitalWrite(LED_LR, 0);
    digitalWrite(LED_DR, 0);
    digitalWrite(LED_KT, 0);
    digitalWrite(LED_BR, 0);
    digitalWrite(LED_LP, 0);
    digitalWrite(LED_HL, 0);
    digitalWrite(LED_BH, 0);
    digitalWrite(N1, 1);
    digitalWrite(N2, 1);
    digitalWrite(N3, 1);
    digitalWrite(N4, 1);
    l1=0;
    blind=1;
    
  } else if (LDR_value > 100 && LDR_value <= 400) {
    analogWrite(LED_LR, 90);
    analogWrite(LED_DR, 90);
    analogWrite(LED_KT, 90);
    analogWrite(LED_BR, 90);
    analogWrite(LED_LP, 90);
    analogWrite(LED_HL, 90);
    analogWrite(LED_BH, 90);
    digitalWrite(N1, 0);
    digitalWrite(N2, 1);
    digitalWrite(N3, 1);
    digitalWrite(N4, 1);
    l1=1;
    blind=1;

  } else if (LDR_value > 400 && LDR_value <= 800) {
    analogWrite(LED_LR, 180);
    analogWrite(LED_KT, 180);
    analogWrite(LED_BR, 180);
    analogWrite(LED_LP, 180);
    analogWrite(LED_HL, 180);
    analogWrite(LED_BH, 180);
    digitalWrite(N1, 0);
    digitalWrite(N2, 0);
    digitalWrite(N3, 1);
    digitalWrite(N4, 1);
    l1=1;
    blind=1;

  } else {
    digitalWrite(LED_LR, 1);
    digitalWrite(LED_DR, 1);
    digitalWrite(LED_KT, 1);
    digitalWrite(LED_BR, 1);
    digitalWrite(LED_LP, 1);
    digitalWrite(LED_HL, 1);
    digitalWrite(LED_BH, 1);
    digitalWrite(N1, 0);
    digitalWrite(N2, 0);
    digitalWrite(N3, 0);
    digitalWrite(N4, 0);
    l1=1;
    blind=0;
  }
}

void loop() {
  float temperature = 0;
  float humidity = 0;
  int LDR_value = analogRead(PIN_LDR);
  int ps_value = digitalRead(PIN_PIR);
  int mq_value = digitalRead(PIN_MQ);
  int l1 = 0;
  int l4 = 0;
  int blind = 0;
  int fan = 0;
  int pump = 0;
  int fueguin = 0;
  int llave  = 0;
  lightSystem(LDR_value, ps_value, l1, l4, blind);
  readTemperatureAndHumidity(temperature, humidity);
  regulationFan(temperature, fan);
  regulationPump(humidity, pump);
  alarma(mq_value, fueguin);
  llaveSec(llave);
  sendDataOverSerial(temperature, humidity, l1, l4, blind, fan, pump, fueguin, llave);
  delay(500);
}


void readTemperatureAndHumidity(float &temperature, float &humidity) {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
}

void regulationFan(float temperature, int &fan){
  if (temperature >= 18 && temperature <= 21){
    digitalWrite(IN_1,1);
    digitalWrite(IN_2,0);
    digitalWrite(PWM,100);
    fan = 1;
  }
  else if (temperature > 21 && temperature <= 26){
    digitalWrite(IN_1,1);
    digitalWrite(IN_2,0);
    digitalWrite(PWM,180);
    fan = 1;
  }
  else if (temperature > 26 && temperature <= 40){
    digitalWrite(IN_1,1);
    digitalWrite(IN_2,0);
    digitalWrite(PWM,255);
    fan = 1;
  }
  else{
    digitalWrite(IN_1,0);
    digitalWrite(IN_2,0);
    digitalWrite(PWM,0);
    fan = 0;
  }
}

void regulationPump(float humidity, int &pump){
    digitalWrite(IN_3,1);
  if (humidity <= 20){
    digitalWrite(IN_4,0);
    digitalWrite(PWM_P,255);
    pump = 1;
  }
  else if (humidity > 20 && humidity <= 40){
    digitalWrite(IN_3,1);
    digitalWrite(IN_4,0);
    digitalWrite(PWM_P,180);
    pump = 1;
  }
  else if (humidity > 40 && humidity <= 60){
    digitalWrite(IN_3,1);
    digitalWrite(IN_4,0);
    digitalWrite(PWM_P,90);
    pump = 1;
  }
  else{
    digitalWrite(IN_1,0);
    digitalWrite(IN_2,0);
    digitalWrite(PWM_P,0);
    pump = 0;
  }
}

void alarma(int mq_value, int &fueguin){
  if (mq_value == 1){
    digitalWrite(IN_5,1);
    digitalWrite(IN_6,0);
    fueguin = 1;
  }
  else{
    digitalWrite(IN_5,0);
    digitalWrite(IN_6,0);
    fueguin = 0;
  }
}

void llaveSec(int &llave){
  int customKey = digitalRead(F1);

  if (customKey == 1){
    llave = 1;
    myServo.write(90);
    delay(300);
    myServo.write(0);
    delay(300);
  }
  else{
    llave = 0;
  }
}

void sendDataOverSerial(float temperature, float humidity ,int l1, int l4, int blind, int fan, int pump, int fueguin, int llave) {
  Serial.print(int(temperature));
  Serial.print(int(humidity));
  Serial.print(l1);
  Serial.print(l4);
  Serial.print(blind);
  Serial.print(fan);
  Serial.print(pump);
  Serial.print(fueguin);
  Serial.print(llave);
  Serial.print("\n");
}