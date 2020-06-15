# EDisplay
Epaper display supporting multiple display units

This is fork of the Epaper project that splits the code into a server element that creates images and a client that displays the images allowing the client to be both remote (and simplified). It also means that the clients cansupport different type of display units.

The server element pulls weather data, events, weather observations, weather predictions and tide information from a number of sources based on different schedules and creates the images for the different types of display classes.

![Screenshot](Club-display.jpg)

The intention is that this could evolve to support IoT displays that are battery powered using an ESP8266

Thanks to @nike199000 for her help in the architecture changes and restructuring the code base

