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
#define ECG_period 20000

#define SpO2_sampling_rate 1000
#define SpO2_period 10000

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
  float ECG_array[100]={  0.47444664743204257,
  0.5684811149268238,
  0.982826543775044,
  0.897627890630183,
  0.5816212273712149,
  0.7094513702534514,
  0.9426628428018541,
  0.17232692026912144,
  0.3292086918709255,
  0.5931145891950768,
  0.8662891827420619,
  0.40267043527342083,
  0.19861911687604328,
  0.4705386843188567,
  0.20694874362949267,
  0.655855808830471,
  0.8515546738709834,
  0.7174593164976019,
  0.054814911934406796,
  0.6398544163539558,
  0.9964824542722693,
  0.08117172979254728,
  0.9044060730120133,
  0.43152546677734815,
  0.6051422916973992,
  0.8651645906633971,
  0.021076281906214134,
  0.18129936999712104,
  0.22971290044563586,
  0.5257760584078173,
  0.8116303142333982,
  0.667250077381921,
  0.8490645499619786,
  0.4592529883509938,
  0.8440984434478556,
  0.7526680250568631,
  0.9959951001606158,
  0.1817387580759242,
  0.2561304277505555,
  0.4548044571930372,
  0.6267669953233599,
  0.3598196357669037,
  0.43121787217322594,
  0.06716592998173421,
  0.7910808985309932,
  0.22952362101963142,
  0.5116122528201448,
  0.32932128235069036,
  0.6651563285118817,
  0.4651856105671319,
  0.32163886221947524,
  0.19394943746256033,
  0.7381163275401474,
  0.3740479969480456,
  0.17442110197072136,
  0.3537268091684964,
  0.2858974709394754,
  0.8607441982592567,
  0.13026069925036354,
  0.5849212518660671,
  0.2859535200557415,
  0.38887571252042785,
  0.7555558629261543,
  0.4980107603605062,
  0.8029879929702669,
  0.6084577345420656,
  0.4054567929386107,
  0.08756979220484284,
  0.708229171525303,
  0.42512599501577386,
  0.3755472162851149,
  0.22961281098497666,
  0.20181675202570515,
  0.322262484883477,
  0.9306588571401287,
  0.028215245996978333,
  0.5914565492711185,
  0.22599939676591652,
  0.9984042347979794,
  0.3645893904238492,
  0.5525280137399204,
  0.5369849582648061,
  0.9818635239035262,
  0.04806826750559434,
  0.5486349334494821,
  0.2476141185241616,
  0.9310552113542268,
  0.3382365373776661,
  0.17763048323082553,
  0.4296514851973222,
  0.6698470645633974,
  0.512791601682767,
  0.6651438449696505,
  0.5389601165100086,
  0.9161138656818375,
  0.7683486282753793,
  0.3326600837173842,
  0.08636810589490451,
  0.4609496347887899};
  float SpO2_array[100]={0.12356980792838312,
  0.2814175002469502,
  0.979965179277593,
  0.727921688639059,
  0.6031974802469785,
  0.25672888486379475,
  0.0696285204147935,
  0.32236928803382014,
  0.9304430374521264,
  0.49544118451487107,
  0.5069903487628163,
  0.5494229583954404,
  0.18611319656038705,
  0.48155501941146794,
  0.7376064329716695,
  0.5933454975245722,
  0.6235231785429735,
  0.9728910736937819,
  0.5439257010162557,
  0.2791681836275701,
  0.8079215817581088,
  0.9005713962512424,
  0.6960402738764413,
  0.7802166412350129,
  0.27700276611213814,
  0.020960177759058674,
  0.644658256935785,
  0.069467628895862,
  0.5494077926365764,
  0.6163043287282786,
  0.8756392711139424,
  0.636831092241455,
  0.5844483526629459,
  0.5887311396695967,
  0.6718549981481012,
  0.13766898801526206,
  0.5070118454693542,
  0.1819733214320547,
  0.2638017268706322,
  0.24098351222566594,
  0.39478429498514556,
  0.9099006340994288,
  0.6690432947429706,
  0.9508813715097815,
  0.7620102041104039,
  0.402606427081976,
  0.3368029640058674,
  0.3412846504147864,
  0.7085651104400814,
  0.4135279940193437,
  0.7184705934159321,
  0.1970817140116775,
  0.6845381771007518,
  0.24775572882411212,
  0.6296366346846258,
  0.3748508675353007,
  0.6309438494274305,
  0.7906857319856145,
  0.9423822812960356,
  0.49625376830663415,
  0.8598813176683922,
  0.10881952112860382,
  0.7340987672765769,
  0.06395422110635118,
  0.46536806979934553,
  0.8523522083322348,
  0.9626892558684819,
  0.3111116989713142,
  0.44088134547664193,
  0.09594190413001136,
  0.489097462167025,
  0.2684144950208658,
  0.44645379002668517,
  0.5888346988413596,
  0.6709163337193128,
  0.5253052364558443,
  0.6943852960557746,
  0.9935127351837886,
  0.4049948038269944,
  0.6828269450593074,
  0.1013108079710936,
  0.06464534640659003,
  0.945724804526355,
  0.8971372402548293,
  0.23535602071305917,
  0.08474595917598193,
  0.40808106590981186,
  0.5460318986213315,
  0.8281730125700302,
  0.011535807894268446,
  0.021591036449976397,
  0.16012496551464495,
  0.6615792860008016,
  0.791097833733939,
  0.20248112763576842,
  0.9610577727011665,
  0.5510825257849887};
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
  //#TODO problem in the periods 
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
        Serial.print("[");
        for (int j = 0; j < sizeOfArray; j++)
        {
          Serial.print(ECG_buffer[j]); // printing the buffer for testing
          if (j < sizeOfArray - 1)
            Serial.print(" ,");
        }
        Serial.print("]");
        Serial.print("\n");
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
        Serial.print("[");
        for (int j = 0; j < sizeOfArray; j++)
        {
          Serial.print(SpO2_buffer[j]); // printing the buffer for testing
          if (j < sizeOfArray - 1)
            Serial.print(" ,");
        }
        Serial.print("]");
        Serial.print("\n");
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
        Serial.print(ECG_array[k]);
        Serial.print("\n");
        ECG_buffer[k] = ECG_array[k];     // appeneding the buffer
        previous_time_ECG = current_time; // pervious time equals the current time
        k++;                              // incrementing the index of the buffer
      }
      current_time = millis();
      if (current_time - previous_time_SpO2 >= SpO2_sampling_rate) // checking if the time is more than or equal the sampling rate to add in the buffer
      {

        Serial.print(F("SpO2 = "));
        Serial.print(SpO2_array[z]);
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
