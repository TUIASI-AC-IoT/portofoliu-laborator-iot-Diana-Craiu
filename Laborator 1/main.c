#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define GPIO_OUTPUT_IO 4
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)

void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    int cnt = 0;
    while(1) {
        // Ton1 = 1 sec (LED ON)
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        printf("LED ON for 1 sec\n");
        vTaskDelay(1000 / portTICK_PERIOD_MS);  //asteapta 1 sec

        // Toff1 = 0.5 sec (LED OFF)
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        printf("LED OFF for 0.5 sec\n");
        vTaskDelay(500 / portTICK_PERIOD_MS);  //asteapta 0.5 sec

        // Ton2 = 0.25 sec (LED ON)
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        printf("LED ON for 0.25 sec\n");
        vTaskDelay(250 / portTICK_PERIOD_MS);  //asteapta 0.25 sec

        // Toff2 = 0.75 sec (LED OFF)
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        printf("LED OFF for 0.75 sec\n");
        vTaskDelay(750 / portTICK_PERIOD_MS);  //asteapta 0.75 sec 
    }
}


// I: Ce rol are functia gpio config?
// R: "Configure GPIO's Mode,pull-up,PullDown,IntrType" = este utilizat pentru a configura modul I/O , rezistentele interne  pulldown, pull-up pentru pini


// I: In codul exemplu, pinul GPIO4 este configurat ca iesire. Care sunt celelalte moduri ın care poate fi configurat un pin GPIO? 
// R: GPIO_MODE_INPUT, GPIO_MODE_DISABLE, GPIO_MODE_INPUT_OUTPUT, GPIO_MODE_INPUT_OUTPUT_OD, etc -> un pin poate fi configurat ca intrare, iesire, poate citi semnale, etc.

// I: Explicati apelul vTaskDelay.
// R: Aceasta este utilizata pentru a introduce o intarziere intr-o sarcina (task), permitand astfel altor sarcini sa fie executate in timpul respectiv

// I: De ce funcia principala se numeste app main?
// R: 