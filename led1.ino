#define led1 9
#define led2 3

void setup() {
    Serial.begin(9600);
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
}

void loop() {
   if (Serial.available()) {
        char signal = Serial.read();
        // Update the last signal
        char lastSignal = signal;
    

    // Handle the last received signal
    if (lastSignal == '2') {
        digitalWrite(led1, HIGH);
        digitalWrite(led2, LOW);
    } else if (lastSignal == '3') {
        digitalWrite(led2, HIGH);
        digitalWrite(led1, LOW);
    } else {
        digitalWrite(led1, LOW);
        digitalWrite(led2, LOW);
    }
   }
}
