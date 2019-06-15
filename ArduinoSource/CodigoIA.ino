#include <SoftwareSerial.h>
int rxPin = 2;
int txPin = 3; 
SoftwareSerial BT(rxPin, txPin);

int EnableA = 10; 
int InA1 = 8;
int InA2 = 9;
int EnableB = 11;
int InB1 = 12;
int InB2 = 13;
int potencia = 64;
char comando = 'x';

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  BT.begin(9600);
  Serial.begin(9600);

  //pinMode(EnableA, OUTPUT); // sets the pin as output
  pinMode(InA1, OUTPUT); // sets the pin as output
  pinMode(InA2, OUTPUT); // sets the pin as output
  //pinMode(EnableB, OUTPUT); // sets the pin as output
  pinMode(InB1, OUTPUT); // sets the pin as output
  pinMode(InB2, OUTPUT); // sets the pin as output
 
  digitalWrite(EnableA, LOW);
  digitalWrite(InA1, LOW);
  digitalWrite(InA2, LOW);
  digitalWrite(EnableB, LOW);
  digitalWrite(InB1, LOW);
  digitalWrite(InB2, LOW);

}
int percentFlux(int number, int flux){
  int x = random(100 - flux, 100 + flux);
  return (number * x) / 100;
}
void loop() {
  // Ir adelante
  if(comando== 'u')
  {
    potencia = percentFlux(140, 5);
    BT.println("Avanzando");
    adelante();
  }
  // Ir atrás
  else if(comando=='d')
  {
    potencia = percentFlux(75, 5);
    BT.println("Retrocediendo");
    atras();
  }
  //Ir a la derecha
  else if(comando == 'r')
  {
    potencia = percentFlux(90, 5);
    BT.println("Derecha");
    derecha();
  }
  //Ir hacia la izquierda
  else if(comando == 'l')
  {
    potencia = percentFlux(90, 5);
    BT.println("Izquierda");
    izquierda();
  }
  //Frenar
  else if(comando == 'b')
  {
    BT.println("Freno");
    analogWrite(EnableB, 0);
    analogWrite(EnableA, 0);
  }
  if(BT.available()){
    Serial.println("Recibido");
    char simbolo = BT.read();
    /*Cuando reciba una nueva línea (al pulsar enter en la app) 
    entra en la función*/
    Serial.println(simbolo);/*Visualizamos el comando recibido en el 
    Monitor Serial*/

    
    //Maxima potencia
    if(simbolo == 'f')
    {
      BT.println("Rápido");
      potencia = 80;
    }
    //Potencia media
    else if(simbolo == 'm')
    {
      BT.println("Paso normal");
      potencia = 80;
    }
    //Potencia alta
    else if(simbolo == 's')
    {
      BT.println("Lento");
      potencia = 48;
    }
    else{
      comando = simbolo;
    }
  } else{
    Serial.println("BT no disponible");
  }
  //derecha();
  //izquierda();
//atras();
//adelante();
//derecha();
}
void motor_izquierda(int dir){
  analogWrite(EnableB, potencia);
  if(dir==1){
    //adelante
      Serial.println("Motor Derecho adelante");
      digitalWrite(InB1, HIGH);
      digitalWrite(InB2, LOW);
  }else if(dir==-1){
    //atrás
      Serial.println("Motor Derecho atrás");
      digitalWrite(InB1, LOW);
      digitalWrite(InB2, HIGH);
  }
}
void motor_derecha(int dir){
  //notar que dir está invertido con respecto a la llanta derecha
  analogWrite(EnableA, potencia);
  if(dir==-1){
    //adelante
      Serial.println("Motor Izquierdo adelante");
      digitalWrite(InA1, HIGH);
      digitalWrite(InA2, LOW);
  }else if(dir==1){
    //atrás
      Serial.println("Motor Izquierdo atrás");
      digitalWrite(InA1, LOW);
      digitalWrite(InA2, HIGH);
  }
}

void adelante(){
  motor_derecha(1);
  motor_izquierda(1);
}
void atras(){
  motor_derecha(-1);
  motor_izquierda(-1);
}
void derecha(){
  motor_derecha(-1);
  motor_izquierda(1);
}
void izquierda(){
  motor_izquierda(-1);
  motor_derecha(1);
}
