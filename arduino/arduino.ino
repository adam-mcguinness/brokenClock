#include <Wire.h>
#include <SPI.h>
#include <avr/pgmspace.h>
#include <RTClib.h>

#define RTC_ADDRESS 0x68 // I2C address of the RTC
#define NUM_LEDS 720
#define WIDTH_IN_TILES 10
#define HEIGHT_IN_TILES 8

#define HOUR_BUTTON_PIN A4
#define MINUTE_BUTTON_PIN A5
#define SECOND_BUTTON_PIN A6

enum TimeUnit { HOURS, MINUTES, SECONDS };

const unsigned long timeoutDuration = 10000; // 10 seconds timeout

RTC_DS1307 rtc; // Create an RTC object. Adjust based on your library.

bool lastHourButtonState = LOW;
bool lastMinuteButtonState = LOW;
bool lastSecondButtonState = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

unsigned long lastModeSwitchTime = 0;
bool displayMode = false; // false for single LED progress, true for displaying time

const uint16_t totalRows = 24;
const uint16_t totalColumns = 30;

const uint16_t ledMap[720] PROGMEM = {
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24,
  25,
  26,
  27,
  28,
  29,
  30,
  31,
  32,
  33,
  34,
  35,
  36,
  37,
  38,
  39,
  40,
  41,
  42,
  43,
  44,
  45,
  46,
  47,
  48,
  49,
  50,
  51,
  52,
  53,
  54,
  55,
  56,
  57,
  58,
  59,
  60,
  61,
  62,
  63,
  64,
  65,
  66,
  67,
  68,
  69,
  70,
  71,
  72,
  73,
  74,
  75,
  76,
  77,
  78,
  79,
  80,
  81,
  82,
  83,
  84,
  85,
  86,
  87,
  88,
  89,
  90,
  91,
  92,
  93,
  94,
  95,
  96,
  97,
  98,
  99,
  100,
  101,
  102,
  103,
  104,
  105,
  106,
  107,
  108,
  109,
  110,
  111,
  112,
  113,
  114,
  115,
  116,
  117,
  118,
  119,
  120,
  121,
  122,
  123,
  124,
  125,
  126,
  127,
  128,
  129,
  130,
  131,
  132,
  133,
  134,
  135,
  136,
  137,
  138,
  139,
  140,
  141,
  142,
  143,
  144,
  145,
  146,
  147,
  148,
  149,
  150,
  151,
  152,
  153,
  154,
  155,
  156,
  157,
  158,
  159,
  160,
  161,
  162,
  163,
  164,
  165,
  166,
  167,
  168,
  169,
  170,
  171,
  172,
  173,
  174,
  175,
  176,
  177,
  178,
  179,
  180,
  181,
  182,
  183,
  184,
  185,
  186,
  187,
  188,
  189,
  190,
  191,
  192,
  193,
  194,
  195,
  196,
  197,
  198,
  199,
  200,
  201,
  202,
  203,
  204,
  205,
  206,
  207,
  208,
  209,
  210,
  211,
  212,
  213,
  214,
  215,
  216,
  217,
  218,
  219,
  220,
  221,
  222,
  223,
  224,
  225,
  226,
  227,
  228,
  229,
  230,
  231,
  232,
  233,
  234,
  235,
  236,
  237,
  238,
  239,
  240,
  241,
  242,
  243,
  244,
  245,
  246,
  247,
  248,
  249,
  250,
  251,
  252,
  253,
  254,
  255,
  256,
  257,
  258,
  259,
  260,
  261,
  262,
  263,
  264,
  265,
  266,
  267,
  268,
  269,
  270,
  271,
  272,
  273,
  274,
  275,
  276,
  277,
  278,
  279,
  280,
  281,
  282,
  283,
  284,
  285,
  286,
  287,
  288,
  289,
  290,
  291,
  292,
  293,
  294,
  295,
  296,
  297,
  298,
  299,
  300,
  301,
  302,
  303,
  304,
  305,
  306,
  307,
  308,
  309,
  310,
  311,
  312,
  313,
  314,
  315,
  316,
  317,
  318,
  319,
  320,
  321,
  322,
  323,
  324,
  325,
  326,
  327,
  328,
  329,
  330,
  331,
  332,
  333,
  334,
  335,
  336,
  337,
  338,
  339,
  340,
  341,
  342,
  343,
  344,
  345,
  346,
  347,
  348,
  349,
  350,
  351,
  352,
  353,
  354,
  355,
  356,
  357,
  358,
  359,
  360,
  361,
  362,
  363,
  364,
  365,
  366,
  367,
  368,
  369,
  370,
  371,
  372,
  373,
  374,
  375,
  376,
  377,
  378,
  379,
  380,
  381,
  382,
  383,
  384,
  385,
  386,
  387,
  388,
  389,
  390,
  391,
  392,
  393,
  394,
  395,
  396,
  397,
  398,
  399,
  400,
  401,
  402,
  403,
  404,
  405,
  406,
  407,
  408,
  409,
  410,
  411,
  412,
  413,
  414,
  415,
  416,
  417,
  418,
  419,
  420,
  421,
  422,
  423,
  424,
  425,
  426,
  427,
  428,
  429,
  430,
  431,
  432,
  433,
  434,
  435,
  436,
  437,
  438,
  439,
  440,
  441,
  442,
  443,
  444,
  445,
  446,
  447,
  448,
  449,
  450,
  451,
  452,
  453,
  454,
  455,
  456,
  457,
  458,
  459,
  460,
  461,
  462,
  463,
  464,
  465,
  466,
  467,
  468,
  469,
  470,
  471,
  472,
  473,
  474,
  475,
  476,
  477,
  478,
  479,
  480,
  481,
  482,
  483,
  484,
  485,
  486,
  487,
  488,
  489,
  490,
  491,
  492,
  493,
  494,
  495,
  496,
  497,
  498,
  499,
  500,
  501,
  502,
  503,
  504,
  505,
  506,
  507,
  508,
  509,
  510,
  511,
  512,
  513,
  514,
  515,
  516,
  517,
  518,
  519,
  520,
  521,
  522,
  523,
  524,
  525,
  526,
  527,
  528,
  529,
  530,
  531,
  532,
  533,
  534,
  535,
  536,
  537,
  538,
  539,
  540,
  541,
  542,
  543,
  544,
  545,
  546,
  547,
  548,
  549,
  550,
  551,
  552,
  553,
  554,
  555,
  556,
  557,
  558,
  559,
  560,
  561,
  562,
  563,
  564,
  565,
  566,
  567,
  568,
  569,
  570,
  571,
  572,
  573,
  574,
  575,
  576,
  577,
  578,
  579,
  580,
  581,
  582,
  583,
  584,
  585,
  586,
  587,
  588,
  589,
  590,
  591,
  592,
  593,
  594,
  595,
  596,
  597,
  598,
  599,
  600,
  601,
  602,
  603,
  604,
  605,
  606,
  607,
  608,
  609,
  610,
  611,
  612,
  613,
  614,
  615,
  616,
  617,
  618,
  619,
  620,
  621,
  622,
  623,
  624,
  625,
  626,
  627,
  628,
  629,
  630,
  631,
  632,
  633,
  634,
  635,
  636,
  637,
  638,
  639,
  640,
  641,
  642,
  643,
  644,
  645,
  646,
  647,
  648,
  649,
  650,
  651,
  652,
  653,
  654,
  655,
  656,
  657,
  658,
  659,
  660,
  661,
  662,
  663,
  664,
  665,
  666,
  667,
  668,
  669,
  670,
  671,
  672,
  673,
  674,
  675,
  676,
  677,
  678,
  679,
  680,
  681,
  682,
  683,
  684,
  685,
  686,
  687,
  688,
  689,
  690,
  691,
  692,
  693,
  694,
  695,
  696,
  697,
  698,
  699,
  700,
  701,
  702,
  703,
  704,
  705,
  706,
  707,
  708,
  709,
  710,
  711,
  712,
  713,
  714,
  715,
  716,
  717,
  718,
  719,
};


const bool digitSegmentMap[10][7] = {
    {1, 1, 1, 1, 1, 1, 0}, // 0
    {0, 1, 1, 0, 0, 0, 0}, // 1
    {1, 1, 0, 1, 1, 0, 1}, // 2
    {1, 1, 1, 1, 0, 0, 1}, // 3
    {0, 1, 1, 0, 0, 1, 1}, // 4
    {1, 0, 1, 1, 0, 1, 1}, // 5
    {1, 0, 1, 1, 1, 1, 1}, // 6
    {1, 1, 1, 0, 0, 0, 0}, // 7
    {1, 1, 1, 1, 1, 1, 1}, // 8
    {1, 1, 1, 1, 0, 1, 1}  // 9
};

const uint16_t segmentIndexes[7][5] = {
    {0,1,2, 0xFFFF},       // A
    {2,32, 0xFFFF},        // B
    {62,92,122, 0xFFFF},   // C
    {120,121,122, 0xFFFF}, // D
    {60,90, 0xFFFF},       // E
    {0,30,0xFFFF},         // F (no LEDs for the digit "0", placeholder)
    {60,61,62, 0xFFFF}     // G
};


void setup() {

  SPI.begin(); // Initialize SPI communication

  pinMode(HOUR_BUTTON_PIN, INPUT_PULLUP);
  pinMode(MINUTE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(SECOND_BUTTON_PIN, INPUT_PULLUP);

  Serial.begin(9600); // Start hardware serial at 9600 bps

  if (!rtc.begin()) {
    Serial.println("RTC failed");
  }
}

void loop() {
    unsigned long currentMillis = millis();

    // Handle button presses for mode switching and time adjustments
    if (digitalRead(HOUR_BUTTON_PIN) == LOW || digitalRead(MINUTE_BUTTON_PIN) == LOW || digitalRead(SECOND_BUTTON_PIN) == LOW) {
        if (currentMillis - lastDebounceTime > debounceDelay) {
            lastDebounceTime = currentMillis;
            lastModeSwitchTime = currentMillis; // Reset timeout timer
            displayMode = true; // Switch to display time mode
            
            // Adjust time based on which button was pressed
            if (digitalRead(HOUR_BUTTON_PIN) == LOW) AdjustTime(HOURS);
            else if (digitalRead(MINUTE_BUTTON_PIN) == LOW) AdjustTime(MINUTES);
            else if (digitalRead(SECOND_BUTTON_PIN) == LOW) AdjustTime(SECONDS);
        }
    }

    // Display logic based on mode
    if (displayMode) {
        DisplayTime();
        if (currentMillis - lastModeSwitchTime > timeoutDuration) {
            displayMode = false; // Timeout reached, switch back to showing progress mode
        }
    } else {
        DateTime now = rtc.now();
        // Normalize the hour for a 12-hour format (0-11)
        uint8_t hour = now.hour() % 12;

        // Calculate total minutes into the 12-hour cycle
        uint16_t minutesIntoCycle = hour * 60 + now.minute();

        // Ensure index wraps around correctly for a 12-hour cycle represented by 720 LEDs
        minutesIntoCycle = minutesIntoCycle % 720; // Ensures wrapping at the end of 12-hour cycle

        if (minutesIntoCycle < NUM_LEDS) {
            int ledIndex = getLedIndex(minutesIntoCycle);
            lightUpLED(ledIndex);
        } else {
            Serial.println("Error: Calculated LED index is out of range.");
        }
    }

    delay(100); // Slight delay for loop
}


void lightUpLED(uint16_t index) {
  // Start Frame
  for (int i = 0; i < 4; i++) {
    SPI.transfer(0x00);
  }

  // LED Frames
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    if (i == index) {
      SPI.transfer(0xE0 | 0x1F); // Brightness + Full brightness value
      SPI.transfer(0xFF); // Blue
      SPI.transfer(0xFF); // Green
      SPI.transfer(0xFF); // Red
    } else {
      SPI.transfer(0xE0 | 0x00); // LED off
      SPI.transfer(0x00);
      SPI.transfer(0x00);
      SPI.transfer(0x00);
    }
  }

    // End Frame
  for (int i = 0; i < 4; i++) {
    SPI.transfer(0xFF);
  }
}

void DisplayTime() {
    DateTime now = rtc.now(); // Get current time
    
    int hour = now.hour();
    if (hour > 12) hour -= 12;
    else if (hour == 0) hour = 12;
    
    int hourTens = hour / 10;
    int hourOnes = hour % 10;
    int minuteTens = now.minute() / 10;
    int minuteOnes = now.minute() % 10;
    int secondTens = now.second() / 10;
    int secondOnes = now.second() % 10;
    
    // Starting indices calculation remains the same
    int digitsAndIndices[][2] = {
        {hourTens, 0},       // Hour tens
        {hourOnes, 4},       // Hour ones
        {minuteTens, 9},     // Minute tens
        {minuteOnes, 13},    // Minute ones
        {secondTens, 18},    // Second tens
        {secondOnes, 22}     // Second ones
    };

    LightUpDigits(digitsAndIndices, 6);
}

void LightUpDigits(const int digits[][2], int numDigits) {
    // Start Frame
    for (int i = 0; i < 4; i++) {
        SPI.transfer(0x00);
    }
    
    // LED Frames
    for (uint16_t i = 0; i < NUM_LEDS; i++) {
        bool lightUp = false;
        for (int d = 0; d < numDigits; d++) {
            int digit = digits[d][0];
            uint16_t startIndex = digits[d][1];
            // Check each segment for the current digit
            for (int segment = 0; segment < 7; segment++) {
                if (digitSegmentMap[digit][segment]) {
                    // If this segment should be lit, check if current LED is part of it, considering the startIndex
                    for (int j = 0; segmentIndexes[segment][j] != 0xFFFF; j++) {
                        // Adjust each segment index through the getLedIndex function
                        uint16_t originalIndex = segmentIndexes[segment][j];
                        uint16_t adjustedIndex = getLedIndex(startIndex + originalIndex);
                        if (i == adjustedIndex) {
                            lightUp = true;
                            break;
                        }
                    }
                }
                if (lightUp) break;
            }
            if (lightUp) break;
        }
        
        if (lightUp) {
            SPI.transfer(0XE0 | 0x1F); // Brightness + Full brightness value
            SPI.transfer(0x80); // Blue
            SPI.transfer(0x80); // Green
            SPI.transfer(0x80); // Red
        } else {
            SPI.transfer(0xE0 | 0x00); // LED off
            SPI.transfer(0x00);
            SPI.transfer(0x00);
            SPI.transfer(0x00);
        }
    }

    // End Frame
    for (int i = 0; i < 4; i++) {
        SPI.transfer(0xFF);
    }
}


void AdjustTime(TimeUnit unit) {
    DateTime now = rtc.now();
    int year = now.year();
    int month = now.month();
    int day = now.day();
    int hour = now.hour();
    int minute = now.minute();
    int second = now.second();
    
    switch (unit) {
        case HOURS:
            hour = (hour + 1) % 24;
            break;
        case MINUTES:
            minute = (minute + 1) % 60;
            break;
        case SECONDS:
            second = 0; // Reset seconds to 0
            break;
    }
    
    // Set the new time
    rtc.adjust(DateTime(year, month, day, hour, minute, second));
}

int getLedIndex(int n) {
    int totalWidth = WIDTH_IN_TILES * 3;
    
    int r = n / totalWidth;
    int c = n % totalWidth;
    
    int tileRow = r / 3;
    int tileColumn = c / 3;
    
    int withinTileRow = r % 3;
    int withinTileColumn = c % 3;
    
    int indexInTile = withinTileRow * 3 + withinTileColumn;
    
    int tileLinearIndex = tileRow * WIDTH_IN_TILES + tileColumn;
    
    int overallIndex = tileLinearIndex * 9 + indexInTile;
    return overallIndex;
}
