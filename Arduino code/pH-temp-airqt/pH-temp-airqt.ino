#include <OneWire.h>
#include <DallasTemperature.h>
#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset 0.00            //deviation compensate
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
float voltage,phValue,temperature = 25;
const int SENSOR_PIN = 13;
const int airQualityPin = A1; // Connect the sensor to analog pin A1
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex=0;
OneWire oneWire(SENSOR_PIN);         // setup a oneWire instance
DallasTemperature tempSensor(&oneWire); // pass oneWire to DallasTemperature library
float tempCelsius;    // temperature in Celsius
float tempFahrenheit; // temperature in Fahrenheit

void setup(void)
{
  Serial.begin(9600);
  tempSensor.begin(); 
}
void loop(void)
{
  tempSensor.requestTemperatures();             // send the command to get temperatures
  int sensorValue = analogRead(airQualityPin);
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  if(millis() - printTime > printInterval)   //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
    
  
    Serial.print(voltage,2); //pH sensor Voltage
    Serial.print(",");
    Serial.print(pHValue,2); //pH sensor value
    Serial.print(",");
    Serial.print(tempFahrenheit,2); //temp value
    Serial.print(",");
    Serial.println(sensorValue); //Air Quality sensor Value
    printTime=millis();
  }
}
double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    //Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;

  tempCelsius = tempSensor.getTempCByIndex(0);  // read temperature in Celsius
  tempFahrenheit = tempCelsius * 9 / 5 + 32; // convert Celsius to Fahrenheit

  

}

  
