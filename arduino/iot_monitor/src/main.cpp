#include <Arduino.h>
#include <SPI.h>
#include <SD.h>


// Pin definitions
#define TEMP_SKIN A0 // read the thermistor readings from pin A0

#define SD_Module_CS 10
#define SD_Module_MOSI 11
#define SD_Module_MISO 12
#define SD_Module_SCK 13

#define TEMP_SKIN_sampling_rate 2000
#define TEMP_SKIN_period 20000

#define ECG_sampling_rate 1000
#define ECG_period 10000

#define SpO2_sampling_rate 1000
#define SpO2_period 20000

float temperature_degree(void)
{
  // intialize variables
  int thermistor_adc_value;
  float output_voltage, thermistor_resistance, thermistor_resistance_log, temperature;

  thermistor_adc_value = analogRead(TEMP_SKIN);
  output_voltage = ((thermistor_adc_value * 5.0) / 1023.0);
  thermistor_resistance = ((5 * (10.0 / output_voltage)) - 10); /* Resistance in kilo ohms */
  thermistor_resistance = thermistor_resistance * 1000;         /* Resistance in ohms   */
  thermistor_resistance_log = log(thermistor_resistance);
  temperature = (1 / (0.001129148 + (0.000234125 * thermistor_resistance_log) + (0.0000000876741 * thermistor_resistance_log * thermistor_resistance_log * thermistor_resistance_log))); /* Temperature in Kelvin */
  temperature = temperature - 273.15;                                                                                                                                                    /* Temperature in degree Celsius */

  return temperature;
}

File myFile;
void setup()
{
  pinMode(TEMP_SKIN, INPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(9600); // baud rate
  while (!Serial)
  {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("Initializing SD card...");
  if (!SD.begin(SD_Module_CS))
  {
    Serial.println("initialization failed!");
   
  }
  Serial.println("initialization done.");
  // open the file for reading:
  myFile = SD.open("test.txt");
  if (myFile)
  {
    Serial.println("test.txt:");
    // read from the file until there's nothing else in it:
    while (myFile.available())
    {
      Serial.write(myFile.read());
    }
    // close the file:
    myFile.close();
  }
  else
  {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
}

void loop()
{

  // Examples
  float ECG_array[100];
  int SpO2_array[100];
  // intialize buffers
  float TEMP_SKIN_buffer[TEMP_SKIN_period / TEMP_SKIN_sampling_rate];

  float ECG_buffer[ECG_period / ECG_sampling_rate];

  float SpO2_buffer[SpO2_period / SpO2_sampling_rate];

  // filling buffers using delay and size

  // for (int i = 0; i < 100; i++){
  //   TEMP_SKIN_buffer[i] = temperature_degree();
  //   delay(1000);
  // }

  // filling buffers using sampling rate and period and millies

  unsigned int start_time = millis();   // starting time of the period
  unsigned int current_time = millis(); // current time

  unsigned int previous_time_SkinTemp = 0; // previous time for the temperature
  unsigned int previous_time_ECG = 0;      // previous time for the ECG
  unsigned int previous_time_SpO2 = 0;     // previous time for the SpO2

  int i = 0;
  int k = 0;
  int z = 0;
  while (1)
  {
    //// SKIN TEMPERATURE
    if (current_time - start_time >= TEMP_SKIN_period || current_time - start_time >= ECG_period || current_time - start_time >= SpO2_period) // sending buffers
    {
      if (current_time - start_time >= TEMP_SKIN_period) // checking if the selected time period is over to send the buffer
      {
        // send the buffer to the api

        Serial.print(F("The period has finished--> send the buffer (Temperature)"));
        Serial.print("\n");

        int sizeOfArray = sizeof(TEMP_SKIN_buffer) / sizeof(TEMP_SKIN_buffer[0]); // getting the size

        Serial.print(sizeOfArray);
        Serial.print("\n");
        Serial.print("[");
        for (int j = 0; j < sizeOfArray; j++)
        {
          Serial.print(TEMP_SKIN_buffer[j]); // printing the buffer for testing
          if (j < sizeOfArray - 1)
            Serial.print(" ,");
        }
        Serial.print("]");
        Serial.print("\n");
        break;
      }
      ////// ECG
      if (current_time - start_time >= ECG_period) // checking if the selected time period is over to send the buffer
      {
        // send the buffer to the api

        Serial.print(F("The period has finished--> send the buffer (ECG)"));
        Serial.print("\n");

        int sizeOfArray = sizeof(ECG_buffer) / sizeof(ECG_buffer[0]); // getting the size

        Serial.print(sizeOfArray);
        Serial.print("\n");

        for (int j = 0; j < sizeOfArray; j++)
        {
          Serial.print(j + 1); // printing the buffer for testing
          Serial.print(" ");
          Serial.print(ECG_buffer[j]); // printing the buffer for testing
          Serial.print("\n");
        }
        break;
      }
      ////// spo2
      if (current_time - start_time >= SpO2_period) // checking if the selected time period is over to send the buffer
      {
        // send the buffer to the api

        Serial.print(F("The period has finished--> send the buffer (SpO2)"));
        Serial.print("\n");

        int sizeOfArray = sizeof(SpO2_buffer) / sizeof(SpO2_buffer[0]); // getting the size

        Serial.print(sizeOfArray);
        Serial.print("\n");

        for (int j = 0; j < sizeOfArray; j++)
        {
          Serial.print(j + 1); // printing the buffer for testing
          Serial.print(" ");
          Serial.print(SpO2_buffer[j]); // printing the buffer for testing
          Serial.print("\n");
        }
        break;
      }
    }
    else
    {
      if (current_time - previous_time_SkinTemp >= TEMP_SKIN_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print(F("Temperature = "));
        Serial.print(temperature_degree());
        Serial.print("\n");
        TEMP_SKIN_buffer[i] = temperature_degree(); // appeneding the buffer
        previous_time_SkinTemp = current_time;      // pervious time equals the current time
        i++;                                        // incrementing the index of the buffer
      }
      current_time = millis();
      if (current_time - previous_time_ECG >= ECG_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print(F("ECG = "));
        Serial.print("\n");
        ECG_buffer[k] = ECG_array[k];     // appeneding the buffer
        previous_time_ECG = current_time; // pervious time equals the current time
        k++;                              // incrementing the index of the buffer
      }
      current_time = millis();
      if (current_time - previous_time_SpO2 >= SpO2_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print(F("SpO2 = "));
        Serial.print("\n");
        SpO2_buffer[z] = SpO2_array[z];    // appeneding the buffer
        previous_time_SpO2 = current_time; // pervious time equals the current time
        z++;                               // incrementing the index of the buffer
      }
      current_time = millis();
    }
  }
}

// ////////////////////////////////////////////////////////// darft //////////////////////////////////////////////////////////

// // float TEMP_SKIN_buffer[TEMP_SKIN_period/TEMP_SKIN_sampling_rate] , send_TEMP_SKIN_buffer[TEMP_SKIN_period/TEMP_SKIN_sampling_rate] ;
// // float ECG_buffer[ECG_period/ECG_sampling_rate] , send_ECG_buffer[ECG_period/ECG_sampling_rate] ;
// // float SpO2_buffer[SpO2_period/SpO2_sampling_rate] , send_SpO2_buffer[SpO2_period/SpO2_sampling_rate];

// // printing the buffer

// //////////////////////////////////////////////////////////
//   // how to send the buffer to the api using http request ?
// Edit : rewritten for cURLpp 0.7.3
// Note : namespace changed, was cURLpp in 0.7.2 ...

// #include <curlpp/cURLpp.hpp>
// #include <curlpp/Options.hpp>
// // RAII cleanup

// curlpp::Cleanup myCleanup;

// // Send request and get a result.
// // Here I use a shortcut to get it in a string stream ...

// std::ostringstream os;
// os << curlpp::options::Url(std::string("http://example.com"));

// string asAskedInQuestion = os.str();

// // // Send request and get a result.


// how to send the buffer to the api using http request in arduino ?




// //////
