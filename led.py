


import time
from rpi_ws281x import *
import argparse

import requests
import json
from datetime import datetime

# LED strip configuration:
LED_COUNT = 64      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.

def leereAnzeige(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        # print(i) 0-63
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Gibt eine Farbe 1-8 von Lila bis Rot zurück
def getRegenbogenFarbe(wert, helligkeit):

    if wert == 1:
        farbe = Color(1, 0, 2)  # Lila
    elif wert == 2:
        farbe = Color(0, 0, 2)  # dunkel blau
    elif wert == 3:
        farbe = Color(0, 2, 3)  # hell blau
    elif wert == 4:
        farbe = Color(2, 3, 0)  # dunkel gelb
    elif wert == 5:
        farbe = Color(1, 2, 0)  # grün
    elif wert == 6:
        farbe = Color(1, 5, 0)  # dunkel gelb
    elif wert == 7:
        farbe = Color(2, 1, 0)  # dunkel gelb
    elif wert == 8:
        farbe = Color(2, 0, 0)  # rot
   
    debug = 'getRegenbogenFarbe - Debug 1: Wert: ' + str(wert) + ' Farbe: ' + str(farbe)
    print(debug)

    return farbe

# Gibt eine Farben in den Apelfarben (1-8) zurück
def getAmpelfarbe (wert, helligkeit):

    if wert < 1:
        print("Fehler der kleiner als 1")
        farbe = Color(3, 3, 3)  # weiss
    elif wert == 1:
        farbe = Color(0, 3, 0)  # Grün
    elif wert == 2:
        farbe = Color(1, 3, 0)  # Grün
    elif wert == 3:
        farbe = Color(1, 2, 0)  # Grün
    elif wert == 4:
       farbe = Color(3, 3, 0)  # Gelb
    elif wert == 5:
        farbe = Color(3, 2, 0)  # rot
    elif wert == 6:
        farbe = Color(3, 1, 0)  # rot
    elif wert == 7:
        farbe = Color(2, 0, 0)  # rot
    elif wert == 8:
        farbe = Color(3, 0, 0)  # rot
    elif wert > 8:
        print("Fehler der groesser als 8")
        farbe = Color(3, 3, 3)  # weiss

    if (helligkeit > 4):
        if wert < 1:
            print("Fehler der kleiner als 1")
            farbe = Color(30, 30, 30)  # weiss
        elif wert == 1:
            farbe = Color(0, 30, 0)  # Grün
        elif wert == 2:
            farbe = Color(10, 30, 0)  # Grün
        elif wert == 3:
            farbe = Color(10, 20, 0)  # Grün
        elif wert == 4:
            farbe = Color(30, 30, 0)  # Gelb
        elif wert == 5:
            farbe = Color(30, 20, 0)  # rot
        elif wert == 6:
            farbe = Color(30, 10, 0)  # rot
        elif wert == 7:
            farbe = Color(20, 0, 0)  # rot
        elif wert == 8:
            farbe = Color(30, 0, 0)  # rot
        elif wert > 8:
            print("Fehler der groesser als 8")
            farbe = Color(30, 30, 30)  # weiss

    if (helligkeit > 6):
        if wert < 1:
            print("Fehler der kleiner als 1")
            farbe = Color(90, 90, 90)  # weiss
        elif wert == 1:
            farbe = Color(0, 90, 0)  # Grün
        elif wert == 2:
            farbe = Color(30, 90, 0)  # Grün
        elif wert == 3:
            farbe = Color(30, 60, 0)  # Grün
        elif wert == 4:
            farbe = Color(90, 90, 0)  # Gelb
        elif wert == 5:
            farbe = Color(90, 60, 0)  # rot
        elif wert == 6:
            farbe = Color(90, 30, 0)  # rot
        elif wert == 7:
            farbe = Color(60, 0, 0)  # rot
        elif wert == 8:
            farbe = Color(90, 0, 0)  # rot
        elif wert > 8:
            print("Fehler der groesser als 8")
            farbe = Color(90, 90, 90)  # weiss

    debug = 'getAmpelfarbe - Debug 1: Wert: ' + str(wert) + ' Farbe: ' + str(farbe)
    print(debug)

    return farbe

# Gibt die für den Messbereich zurück (-3 | 1 | 5)
def getMessbereichfarbe (wert, helligkeit):

    if wert == -3:
        farbe = Color(3, 0, 0) # rot
    elif wert == -2:
        farbe = Color(3, 1, 0)  # Gelb   
    elif wert == -1:
        farbe = Color(1, 2, 0)   # gelb  
    elif wert == 1:
        farbe = Color(0, 3, 0)  # Grün # Mitte
    elif wert == 2:
        farbe = Color(1, 2, 0)  # gelb
    elif wert == 3:
        farbe = Color(3, 1, 0)  # org
    elif wert == 4:
        farbe = Color(3, 0, 0)  # rot
    elif wert == 5:
        farbe = Color(4, 0, 0)  # rot

    if (helligkeit > 4):
        if wert == -3:
            farbe = Color(30, 0, 0) # rot
        elif wert == -2:
            farbe = Color(30, 10, 0)  # Gelb   
        elif wert == -1:
            farbe = Color(10, 20, 0)   # gelb  
        elif wert == 1:
            farbe = Color(0, 30, 0)  # Grün # Mitte
        elif wert == 2:
            farbe = Color(10, 20, 0)  # gelb
        elif wert == 3:
            farbe = Color(30, 10, 0)  # org
        elif wert == 4:
            farbe = Color(30, 0, 0)  # rot
        elif wert == 5:
            farbe = Color(40, 0, 0)  # rot


    if (helligkeit > 6):
        if wert == -3:
            farbe = Color(90, 0, 0) # rot
        elif wert == -2:
            farbe = Color(90, 30, 0)  # Gelb   
        elif wert == -1:
            farbe = Color(90, 60, 0)   # gelb  
        elif wert == 1:
            farbe = Color(0, 90, 0)  # Grün # Mitte
        elif wert == 2:
            farbe = Color(20, 60, 0)  # gelb
        elif wert == 3:
            farbe = Color(90, 30, 0)  # org
        elif wert == 4:
            farbe = Color(90, 0, 0)  # rot
        elif wert == 5:
            farbe = Color(120, 0, 0)  # rot


    debug = 'getMessbereichfarbe - Debug 1: Wert: ' + str(wert) + ' Farbe: ' + str(farbe)
    print(debug)

    return farbe

# Gibt die Zahlen für Co2 zurück
def getCo2(messwert):
    
    if messwert > -10:
        ledWert = 1
    if messwert > 500:
        ledWert = 2
    if messwert > 700:
        ledWert = 3
    if messwert > 900:
        ledWert = 4
    if messwert > 1000:
        ledWert = 5
    if messwert > 1200:
        ledWert = 6
    if messwert > 1500:
        ledWert = 7
    if messwert > 1700:
        ledWert = 8
    debug = 'getCo2 - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert

# Gibt die Zahlen für Co2 zurück
def getTv(messwert):
    
    if messwert > -10:
        ledWert = 1
    if messwert > 100:
        ledWert = 2
    if messwert > 300:
        ledWert = 3
    if messwert > 500:
        ledWert = 4
    if messwert > 700:
        ledWert = 5
    if messwert > 1200:
        ledWert = 6
    if messwert > 1500:
        ledWert = 7
    if messwert > 1800:
        ledWert = 8
    debug = 'getTv - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert

# Gibt die Zahlen für Co2 zurück
def getFeuchtInnen(messwert):
    
    if messwert > -10:
        ledWert = -3
    if messwert > 40:
        ledWert = -2
    if messwert > 50:
        ledWert = -1
    if messwert > 60:
        ledWert = 1
    if messwert > 70:
        ledWert = 2
    if messwert > 80:
        ledWert = 3
    if messwert > 90:
        ledWert = 4
    if messwert > 95:
        ledWert = 5
    debug = 'getFeuchtInnen - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert


# Gibt die Zahlen für Co2 zurück
def getFeuchtAusssen(messwert):
    
    if messwert > -10:
        ledWert = -3
    if messwert > 50:
        ledWert = -2
    if messwert > 60:
        ledWert = -1
    if messwert > 70:
        ledWert = 1
    if messwert > 80:
        ledWert = 2
    if messwert > 85:
        ledWert = 3
    if messwert > 90:
        ledWert = 4
    if messwert > 95:
        ledWert = 5
    debug = 'getFeuchtAusssen - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert


# Gibt die Zahlen für Temp zurück
def getTempInnen(messwert):
    
    if messwert > -10:
        ledWert = -3
    if messwert > -10:
        ledWert = -2
    if messwert > -15:
        ledWert = -1
    if messwert > 19:
        ledWert = 1
    if messwert > 22:
        ledWert = 2
    if messwert > 23:
        ledWert = 3
    if messwert > 24:
        ledWert = 4
    if messwert > 25:
        ledWert = 5
    debug = 'getTempInnen - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert



# Gibt die Zahlen für Temp zurück
def getTempAussen(messwert):
    
    if messwert > -50:
        ledWert = -3
    if messwert > -7:
        ledWert = -2
    if messwert > -3:
        ledWert = -1
    if messwert > 0:
        ledWert = 1
    if messwert > 5:
        ledWert = 2
    if messwert > 10:
        ledWert = 3
    if messwert > 20:
        ledWert = 4
    if messwert > 30:
        ledWert = 5
    debug = 'getTemp - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert


# Gibt die Zahlen für Helligkeit zurück
def getHelligkeit(messwert):
    
    if messwert > -10:
        ledWert = 1
    if messwert > 5:
        ledWert = 2
    if messwert > 30:
        ledWert = 3
    if messwert > 100:
        ledWert = 4
    if messwert > 500:
        ledWert = 5
    if messwert > 800:
        ledWert = 6
    if messwert > 1400:
        ledWert = 7
    if messwert > 2000:
        ledWert = 8

    debug = 'getHelligkeit - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert

# Gibt die Zahlen für den Luftdruuck zurück
def getLuftdruck(messwert):
    
    if messwert > -10:
        ledWert = 1
    if messwert > 900:
        ledWert = 2
    if messwert > 950:
        ledWert = 3
    if messwert > 1010:
        ledWert = 4
    if messwert > 1030:
        ledWert = 5
    if messwert > 1040:
        ledWert = 6
    if messwert > 1050:
        ledWert = 7
    if messwert > 1060:
        ledWert = 8

    debug = 'getLuftdruck - Debug 1: messwert: ' + \
        str(messwert) + ' ledWert: ' + str(ledWert)
    print(debug)

    return ledWert    

# Setz eine Reihe von vor bis hinten
def setzePixelVorneHinten(strip, wert, reihe, helligkeit):

    debug = 'setzePixelVorneHinten - Debug 1: wert: ' +  str(wert) + ' Reihe: ' + str(reihe)
    print(debug)

    # Hole die Farbe
    farbe = getAmpelfarbe(wert, helligkeit)

    starthohe = (reihe * 8)
    sollwert = starthohe + (wert -1)

    # Aktive Farbe setzen
    tmpSollwert = sollwert
    while starthohe <= tmpSollwert:
        
        t = (tmpSollwert)
        debug = '> setze ' +  str(t)
        print(debug)

        strip.setPixelColor(t, farbe)
        tmpSollwert = tmpSollwert - 1

    # Alte Farben mit Schwarz überschreiben
    tmpStartOben = starthohe + 8 - 1
    while tmpStartOben > sollwert:

        t = (tmpStartOben)
        debug = '> loesche ' +  str(t)
        print(debug)

        strip.setPixelColor(t, Color(0, 0, 0))
        tmpStartOben = tmpStartOben - 1
        

    strip.show()

# Setz eine Reihe von vor bis hinten
def setzePixelMitte(strip, wert, reihe, helligkeit):

    starthohe = (reihe * 8)
    debug = 'setzePixelMitte - Debug 1: wert: ' + \
        str(wert) + ' Reihe: ' + str(reihe)  + ' starthohe: ' + str(starthohe)
    print(debug)

    starthohe = starthohe
    if wert == -3:
        strip.setPixelColor(starthohe + 0, getMessbereichfarbe(-3, helligkeit))
        strip.setPixelColor(starthohe + 1, getMessbereichfarbe(-2, helligkeit))
        strip.setPixelColor(starthohe + 2, getMessbereichfarbe(-1, helligkeit))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 5, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (0,1,2,3) ' +  str(starthohe)
        print(debug)

    if wert == -2:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, getMessbereichfarbe(-2, helligkeit))
        strip.setPixelColor(starthohe + 2, getMessbereichfarbe(-1, helligkeit))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 5, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (1,2,3) ' +  str(starthohe)
        print(debug)

    
    if wert == -1:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, getMessbereichfarbe(-1, helligkeit))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 5, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (2,3) ' +  str(starthohe)
        print(debug)

    if wert == 1:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 5, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (3) ' +  str(starthohe)
        print(debug)

    if wert == 2:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, getMessbereichfarbe(2, helligkeit))
        strip.setPixelColor(starthohe + 5, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (3,4) ' +  str(starthohe)
        print(debug)

    if wert == 3:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, getMessbereichfarbe(2, helligkeit))
        strip.setPixelColor(starthohe + 5, getMessbereichfarbe(3, helligkeit))
        strip.setPixelColor(starthohe + 6, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (3,4,5) ' +  str(starthohe)
        print(debug)

    if wert == 4:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, getMessbereichfarbe(2, helligkeit))
        strip.setPixelColor(starthohe + 5, getMessbereichfarbe(3, helligkeit))
        strip.setPixelColor(starthohe + 6, getMessbereichfarbe(4, helligkeit))
        strip.setPixelColor(starthohe + 7, Color(0, 0, 0))

        debug = '> setze (3,4,5,6) ' +  str(starthohe)
        print(debug)

    if wert == 5:
        strip.setPixelColor(starthohe + 0, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 1, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 2, Color(0, 0, 0))
        strip.setPixelColor(starthohe + 3, getMessbereichfarbe(1, helligkeit))
        strip.setPixelColor(starthohe + 4, getMessbereichfarbe(2, helligkeit))
        strip.setPixelColor(starthohe + 5, getMessbereichfarbe(3, helligkeit))
        strip.setPixelColor(starthohe + 6, getMessbereichfarbe(4, helligkeit))   
        strip.setPixelColor(starthohe + 7, getMessbereichfarbe(5, helligkeit)) 

        debug = '> setze (3,4,5,6,7) ' +  str(starthohe)
        print(debug)

    strip.show()

def beginne(strip):

    requestget = requests.get(url='http://192.168.2.102/apiFuerLed.php')
    response_data = requestget.json()
 
    co2 = response_data['co2']['Wert']
    co2 = getCo2(co2)
 
    tvoc = response_data['tvoc']['Wert']
    tvoc = getTv(tvoc)

    tempInnen = response_data['tempInnen']['Wert']
    tempInnen = getTempInnen(tempInnen)

    freutInnen = response_data['freutInnen']['Wert']
    freutInnen = getFeuchtInnen(freutInnen)

    tempAussen = response_data['tempAussen']['Wert']
    tempAussen = getTempAussen(tempAussen)

    freutAussen = response_data['freutAussen']['Wert']
    freutAussen = getFeuchtAusssen(freutAussen)

    licht = response_data['licht']['Wert'] 
    licht = getHelligkeit(licht)

    lichluftdruckt = response_data['luftdruck']['Wert']
    lichluftdruckt = getLuftdruck(lichluftdruckt)

    #co2 = 1
    #tvoc = 2
    #tempInnen = 3
    #freutInnen = 4
    #tempAussen = 5
    #freutAussen = 6
    #licht = 7
    #lichluftdruckt = 8

    #co2 = -3
    #tvoc = -2
    #tempInnen = -1
    #freutInnen = 1
    #tempAussen = 2
    #freutAussen = 3
    #licht = 4
    #lichluftdruckt = 5

    #co2 = 1
    #tvoc = 1
    #tempInnen = 1
    #freutInnen = 1
    #tempAussen = 1
    #freutAussen = 1
    #licht = 1
    #luftdruck = 1

    print('************')
    #leereAnzeige2(strip, Color(0,0,0))
    print('Licht ist')
    print(str(licht))
    print('************')

	# 
    print('\n\nCO2 -------')
    setzePixelVorneHinten(strip, co2, 0, licht)
    print('\n\nTV -------')
    setzePixelVorneHinten(strip, tvoc, 1, licht)
    print('\n\ntempInnen -------')
    setzePixelMitte(strip, tempInnen, 2, licht)
    print('\n\nfreutInnen -------')
    setzePixelMitte(strip, freutInnen, 3, licht)
    print('\n\ntempAussen -------')
    setzePixelMitte(strip, tempAussen, 4, licht)
    print('\n\nfreutAussen -------')
    setzePixelMitte(strip, freutAussen, 5, licht)
    print('\n\nlicht -------')
    setzePixelVorneHinten(strip, licht, 6, licht)
    print('\n\nlichluftdruckt -------')
    setzePixelVorneHinten(strip, lichluftdruckt, 7, licht)
    print('\n')

    print("Done...")


# Main program logic follows:
if __name__ == '__main__':

    # Process arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    #print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    while 1:
        try:
            #leereAnzeige(strip, Color(0,0,0), 1)
            #time.sleep(1)
            print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            beginne(strip)

            # break
            time.sleep(60)
            print('Ende...')
           # leereAnzeige(strip, Color(0,0,0), 1)

        except Exception as error:
            print(error.args)
            time.sleep(60)
