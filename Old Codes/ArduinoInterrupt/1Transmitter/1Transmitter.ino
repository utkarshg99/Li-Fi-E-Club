#define PULSE_TIME 150
#define PULSE2_TIME 300
int start = 785 ;
int ends  = 423 ;
//String data = "H" ;
String data="Li-Fi internal presentation submission. delay is 50 us";
int output_pin = 6 ;
int temp = 10 ;

void setup() {
  pinMode(output_pin, OUTPUT) ;
  //Serial.begin(230400) ;
}

int enc_backend(int in) {
  switch(in) {
    case  0 : return 30 ; break ;
    case  1 : return  9 ; break ;
    case  2 : return 20 ; break ;
    case  3 : return 21 ; break ;
    case  4 : return 10 ; break ;
    case  5 : return 11 ; break ;
    case  6 : return 14 ; break ;
    case  7 : return 15 ; break ;
    case  8 : return 18 ; break ;
    case  9 : return 19 ; break ;
    case 10 : return 22 ; break ;
    case 11 : return 23 ; break ;
    case 12 : return 26 ; break ;
    case 13 : return 27 ; break ;
    case 14 : return 28 ; break ;
    case 15 : return 29 ; break ;
    default : return 00 ;
  }
}

void sendbit(int bit) {
  if(bit == 1) {
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(PULSE_TIME) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(PULSE_TIME) ;
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(PULSE_TIME) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(PULSE_TIME) ;
    digitalWrite(output_pin, LOW) ;
  }
  else {
    digitalWrite(output_pin, LOW) ;
    delayMicroseconds(PULSE2_TIME) ;
    digitalWrite(output_pin, HIGH);
    delayMicroseconds(PULSE2_TIME) ;
    digitalWrite(output_pin, LOW) ;
  }
}
void sendnum(int num) {
  for(int div = 512 ; div >= 1 ; div = div >> 1) {
    if(num >= div) {
      sendbit(1) ;
      num -= div ;
    }
    else {
      sendbit(0) ;
    }
  }
}

int enc(int num) {
  int half1 ;
  int half2 ;
  half1 = num >> 4 ;
  half2 = num & 15 ;
  half1 = enc_backend(half1) ;
  half2 = enc_backend(half2) ;
  return (half1 << 5) + (half2) ;
}

void loop() {
    sendnum(start) ;
    
    for (int i=0; i<data.length(); i++)
    {
      char f=data.charAt(i);
      sendnum(enc((int)f));
    }
    sendnum(enc(10))  ;
    sendnum(ends) ;
    
 }
