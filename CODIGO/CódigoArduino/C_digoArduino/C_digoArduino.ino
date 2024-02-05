#include <LiquidCrystal.h>
#include <DHT.h>
LiquidCrystal lcd(8,7,6,5,4,3,2);
DHT dht(9, DHT11);   

const int led = 13;
const int led1 = 12;
int valor_dato = 0;

void setup()
{
  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  digitalWrite (led, LOW);
  digitalWrite (led1, LOW);
  Serial.begin(2400);
  Serial.println("Conexión Establecida");
  delay(4000);
  dht.begin();        // INICIALIZAR EL DHT
  lcd.begin (16, 2);
}

void loop(){

  float TemC = dht.readTemperature();            // GRADOS CELCIUS
  float TemF = dht.readTemperature(true);        // GRADOS FAHRENHEIT
  float Humd = dht.readHumidity();
  String temp = String(TemC);             // HUMEDAD
  if(isnan(TemC) || isnan(TemF) || isnan(Humd)){ // SI LO QUE DEBUELVE NO ES UN NUMERO
      //Serial.println("Revisar conexion");        // IMPRIMIR MENSAJE DE HERRROR
      lcd.setCursor(0, 0); //COLOCAR EN POSICION
      lcd.print("Revisar conexion");
      lcd.setCursor(0, 1); //COLOCAR EN POSICION
      lcd.print("Revisar conexion");
    }
    else
    {
      lcd.setCursor(0, 0); //COLOCAR EN POSICION
      lcd.print("Tem:"+ String(TemC,1) + "C  " + String(TemF,1) +"F ");
      lcd.setCursor(0, 1); //COLOCAR EN POSICION
      lcd.print("Hum:"+ String(Humd,1) + "% ");
      Serial.println(temp);
    }
  delay(500);  

  while(Serial.available())
  {
    valor_dato = Serial.read();
  }
  
  if (valor_dato == '1')
  {
    digitalWrite (led, HIGH);
    digitalWrite (led1, HIGH);
  }
  else if (valor_dato == '0')
  {
    digitalWrite (led, LOW);
    digitalWrite (led1, LOW);
  }
}
