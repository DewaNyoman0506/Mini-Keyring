from machine import Pin, I2C
import dht
import time
import ssd1306
import random
import ntptime
import network
from umqtt.robust import MQTTClient
from json import dumps

# Sync NTP =====

def get_time():
    t = time.localtime()
    
    hour = ( t[3] + 7 ) % 24
    minute = t[4]
    
    return "{:02d}:{:02d}".format(hour, minute)

# Buat OLED =====
i2c = I2C( 0, scl=Pin(22), sda=Pin(21) )
oled = ssd1306.SSD1306_I2C( 128, 64, i2c, addr=0x3C )

# Buat DHT11 =====
sensor = dht.DHT11(Pin(4))

# MQTT stuff =====
MQTTserver_addr = "127.0.0.1" # Broker IP disini
MQTTserver_port = 1887 # Port number disini

mqtt = None

# Koneksi Wifi && Time =====

known_net = [
    ("TupleOfWifiSSIDDisini", "Passwordnya")
     ]
     

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

def connect_wifi():
    print( "Memindai..." )
    
    available = wifi.scan()
    
    # Ambil yang available
    available_ssids = [net[0].decode() for net in available]
    
    for ssid, password in known_net:
        if ssid in available_ssids:
            print( "Mencoba : ", ssid )
            
            wifi.connect( ssid, password )
            
            start = time.ticks_ms() # Tunggu max 15 detik :
            
            while not wifi.isconnected():
                if time.ticks_diff(
                    time.ticks_ms(), start
                ) > 15000:
                    print( "Gagal", ssid )
                    wifi.disconnect()
                    time.sleep(1)
                    break
                
                time.sleep(0.5)
                
            if wifi.isconnected():
                print( "Terhubung ke : ", ssid )
                print( wifi.ifconfig())
                return True
            
    print( "Tidak ada jaringan yang dikenal..." )
    return False
    
while not connect_wifi():
    print( "Mencoba kembali dalam 5 detik...!" )
    time.sleep(5)

# Sinkronisasi Network Time P ==
ntptime.settime()

print( "Jam sudah tersinkronisasi!" )
print( time.localtime() )

# MQTT Detection

if MQTTserver_addr:
    try:
        mqtt = MQTTClient(
            b"Mokers Keyring",
            MQTTserver_addr,
            MQTTserver_port
            )
        
        mqtt.connect()
        print( "MQTT terhubung ! ! !" )
        
    except Exception as e:
        print( "Broker tidak terdeteksi" )
        mqtt = None

# Smiley!! =====

def draw_face(blink=False):
    oled.fill(0)
    
    if blink:
        # Closed
        oled.hline( 30, 18, 18, 1 )
        oled.hline( 80, 18, 18, 1 )
        
    else:
        # Buka
        oled.fill_rect( 30, 15, 18, 12, 1 )
        oled.fill_rect( 80, 15, 18, 12, 1 )
        
    # Nyengir
    oled.hline( 54, 37, 20, 1 )
    oled.pixel( 53, 36, 1 )
    oled.pixel( 75, 36, 1 )
    oled.pixel( 55, 38, 1 )
    oled.pixel( 72, 38, 1 )
    
    oled.text(get_time(), 44, 52) # NTP
    
    oled.show()
    
# Yippee ======

def draw_happy_face():
    oled.fill(0)

    # Kiri eye
    oled.hline(32, 18, 14, 1)
    oled.pixel(31, 19, 1)
    oled.pixel(30, 20, 1)
    oled.pixel(46, 19, 1)
    oled.pixel(47, 20, 1)
    
    # Kanan eye
    oled.hline(82, 18, 14, 1)
    oled.pixel(81, 19, 1)
    oled.pixel(80, 20, 1)
    oled.pixel(96, 19, 1)
    oled.pixel(97, 20, 1)

    # Mulut
    oled.hline(52, 35, 24, 1)      # Top line of open mouth
    oled.vline(52, 35, 10, 1)      # Left side edge
    oled.vline(75, 35, 10, 1)      # Right side edge
    oled.hline(53, 45, 22, 1)      # Bottom line curve
    
    oled.text(get_time(), 44, 52) # NTP

    oled.show()
    
# MQTT Publishing =====

def publishByMQTT():
    if mqtt is None:
        return()
    
    sensor.measure()
    
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    
    data = {
        "device": "Mokers Keyring",
        "payload": {
            "temperature": temperature,
            "humidity": humidity,
            }
        }
    
    try:
        mqtt.publish(
            b"mokers/sensors",
            dumps( data )
            )
        
        print( "Data terkirim!!!" )
        
    except Exception as e:
        print( "Publishing gagal...", e )
    
# Screen Sensor =====

def show_data():
    sensor.measure()
    
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    rssi = wifi.status("rssi")
    
    oled.fill(0)
    
    oled.text("Sensor Mokers", 15, 0)
    
    oled.text( "Temp", 0, 16 )
    oled.text( str(temperature) + " C", 55, 16 )
    
    oled.text( "Humd", 0, 32 )
    oled.text( str(humidity) + " %", 55, 32 )
    
    oled.text( "rssi", 0, 48 )
    oled.text( str(wifi.status("rssi")) + " dBm", 55, 48 )
    
    oled.show()
    
    print( "Temperature: ", temperature, "C" )
    print( "Humidity: ", humidity, "%")
    
    publishByMQTT()
    
# Wifi Scanner =====

def wifi_scanner():
    networks = wifi.scan()
    
    oled.fill(0)
    oled.text( "Wifi Scan", 0, 0 )
    
    for i, network in enumerate(networks[:3]):
        ssid = network[0].decode()
        channel = network[2]
        rssi = network[3]
        
        ssid = ssid[:8]
        
        y = 16 + ( i* 16 )
        
        oled.text( ssid, 0, y )
        oled.text( "CH" + str(channel), 72, y )
        oled.text( str(rssi), 96, y + 8 )
        
        oled.show()
    
while True:
    
    start = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start) < 15000:
        if random.random() < 0.2:
            draw_happy_face()
            time.sleep(2)
        else:
            draw_face(False)
            time.sleep(random.uniform(2, 4))
            
            draw_face(True)
            time.sleep(0.15)
    
    # Sensor screen
    show_data()
    time.sleep(3)
    
    # WiFi screen
    wifi_scanner()
    time.sleep(5)