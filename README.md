**Status:** 🚧 Prototype / Active Development

# 🧸 Mokers Keyring

A small portable IoT prototype built around an **ESP32 WROOM32** and **MicroPython**. Yeah !!! ( It's name is Mokers, because it just sounds silly ~ )

The project started as an experiment in combining networking, sensors, and embedded hardware into something small and tangible — essentially, a tiny keyring that can actually *do things*.

## ✨ Features

* 🖥️ **OLED Display** — Animated facial expressions and information screens
* 🌡️ **Temperature & Humidity** — DHT11 environmental sensor
* 🕐 **NTP Clock** — Synchronizes time over Wi-Fi
* 📶 **RSSI Monitoring** — Displays the current Wi-Fi signal strength
* 🔎 **Wi-Fi Scanner** — Scans and displays nearby wireless networks!
* 📡 **MQTT** — Experimental sensor telemetry support

## 🔧 Hardware

* ESP32 WROOM32
* 0.96" 128×64 OLED display
* DHT11 temperature & humidity sensor
* Breadboard / jumper wires
* USB power

## 💻 Software

* MicroPython
* Thonny
* SSD1306 OLED driver
* DHT sensor module
* Wi-Fi / NTP functionality
* MQTT (optional)

## 🛠️ Development

The project was developed incrmentally, starting with the OLED interface and gradually adding sensor readings, Wi-Fi functionality, NTP synchronization, and network monitoring features.

The project is currently a **prototype** running on a breadboard. A future version may move to a more compact custom/perfboard implementation with portable power.
