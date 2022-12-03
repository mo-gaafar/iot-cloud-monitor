#include <Arduino.h>

// Pin definitions
#define TEMP_SKIN A0 // read the thermistor readings from pin A0

#define TEMP_SKIN_sampling_rate 1000
#define TEMP_SKIN_period 10000

#define ECG_sampling_rate 2331
#define ECG_period 29923

#define SpO2_sampling_rate 23
#define SpO2_period 23355

// intialize buffers
float TEMP_SKIN_buffer[TEMP_SKIN_period / TEMP_SKIN_sampling_rate];

float ECG_buffer[ECG_period / ECG_sampling_rate];

float SpO2_buffer[SpO2_period / SpO2_sampling_rate];

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

void setup()
{

  Serial.begin(9600); // baud rate
  pinMode(TEMP_SKIN, INPUT);
}

void loop()
{

  // Examples
  int ECG_array[1000];
  int SpO2_array[1000];

  // filling buffers using delay and size

  // for (int i = 0; i < 100; i++){
  //   TEMP_SKIN_buffer[i] = temperature_degree();
  //   delay(1000);
  // }

  // filling buffers using sampling rate and period and millies

  unsigned long start_time = millis();   // starting time of the period
  unsigned long current_time = millis(); // current time
  unsigned long previous_time = 0;
  int i = 0;
  while (1)
  {
    //// SKIN TEMPERATURE

    if (current_time - start_time >= TEMP_SKIN_period) // checking if the selected time period is over to send the buffer
    {
      // send the buffer to the api

      Serial.print("The period has finished--> send the buffer");
      Serial.print("\n");

      int sizeOfArray = sizeof(TEMP_SKIN_buffer) / sizeof(TEMP_SKIN_buffer[0]); // getting the size

      Serial.print(sizeOfArray);
      Serial.print("\n");

      for (int j = 0; j < sizeOfArray; j++)
      {
        Serial.print(j + 1); // printing the buffer for testing
        Serial.print(" ");
        Serial.print(TEMP_SKIN_buffer[j]); // printing the buffer for testing
        Serial.print("\n");
      }
      break;
    }
    else
    {
      if (current_time - previous_time >= TEMP_SKIN_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print("Temperature = ");
        Serial.print(temperature_degree());
        Serial.print("\n");
        TEMP_SKIN_buffer[i] = temperature_degree(); // appeneding the buffer
        previous_time = current_time;               // pervious time equals the current time
        i++;                                        // incrementing the index of the buffer
      }
      current_time = millis();
    }

    /////////////////////////// ECG /////////////////////////////

    start_time = millis();   // starting time of the period
    current_time = millis(); // current time
    previous_time = 0;
    i = 0;

    while (1)
    {

      if (current_time - start_time >= ECG_period) // checking if the selected time period is over to send the buffer
      {
        // send the buffer to the api

        Serial.print("The period has finished--> send the buffer");
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
      else
      {
        if (current_time - previous_time >= ECG_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
        {

          Serial.print("ECG = ");
          Serial.print("\n");
          ECG_buffer[i] = ECG_array[i]; // appeneding the buffer
          previous_time = current_time; // pervious time equals the current time
          i++;                          // incrementing the index of the buffer
        }
        current_time = millis();
      }
    }
  }
  /////////////////////////// SpO2 /////////////////////////////

  start_time = millis();   // starting time of the period
  current_time = millis(); // current time
  previous_time = 0;

  i = 0;

  while (1)
  {
    if (current_time - start_time >= SpO2_period) // checking if the selected time period is over to send the buffer
    {
      // send the buffer to the api

      Serial.print("The period has finished--> send the buffer");
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
    else
    {
      if (current_time - previous_time >= SpO2_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print("SpO2 = ");
        Serial.print("\n");
        SpO2_buffer[i] = SpO2_array[i]; // appeneding the buffer
        previous_time = current_time;   // pervious time equals the current time
        i++;                            // incrementing the index of the buffer
      }
      current_time = millis();
    }
  }
}

////////////////////////////////////////////////////////// darft //////////////////////////////////////////////////////////

// float TEMP_SKIN_buffer[TEMP_SKIN_period/TEMP_SKIN_sampling_rate] , send_TEMP_SKIN_buffer[TEMP_SKIN_period/TEMP_SKIN_sampling_rate] ;
// float ECG_buffer[ECG_period/ECG_sampling_rate] , send_ECG_buffer[ECG_period/ECG_sampling_rate] ;
// float SpO2_buffer[SpO2_period/SpO2_sampling_rate] , send_SpO2_buffer[SpO2_period/SpO2_sampling_rate];

// printing the buffer

//////////////////////////////////////////////////////////
//   // how to send the buffer to the api using http request ?
// // Edit : rewritten for cURLpp 0.7.3
// // Note : namespace changed, was cURLpp in 0.7.2 ...

// #include <curlpp/cURLpp.hpp>
// #include <curlpp/Options.hpp>
// // RAII cleanup

// curlpp::Cleanup myCleanup;

// // Send request and get a result.
// // Here I use a shortcut to get it in a string stream ...

// std::ostringstream os;
// os << curlpp::options::Url(std::string("http://example.com"));

// string asAskedInQuestion = os.str();

// // Send request and get a result.