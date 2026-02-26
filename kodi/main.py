from machine import Pin, SoftI2C
import neopixel
import time
import random
import math
from I2C_LCD import I2cLcd
from buzzer_music import music


#lag
song = '0 B3 1 55;4 B4 1 55;4 F#4 1 55;4 D#5 1 55;12 B4 1 55;12 F#4 1 55;12 D#5 1 55;20 B4 1 55;20 F#4 1 55;20 D#5 1 55;28 B4 1 55;28 F#4 1 55;28 D#5 1 55;32 A#3 1 55;36 A#4 1 55;36 F4 1 55;36 C#5 1 55;44 A#4 1 55;44 F4 1 55;44 C#5 1 55;52 A#4 1 55;52 F4 1 55;52 C#5 1 55;60 A#4 1 55;60 F4 1 55;60 C#5 1 55;64 D#4 1 55;68 D#5 1 55;68 A#4 1 55;68 F#5 1 55;76 D#5 1 55;76 A#4 1 55;76 F#5 1 55;84 D#5 1 55;84 A#4 1 55;84 F#5 1 55;92 D#5 1 55;92 A#4 1 55;92 F#5 1 55;96 D#4 1 55;100 C#5 1 55;100 A#4 1 55;100 F#5 1 55;108 C#5 1 55;108 A#4 1 55;108 F#5 1 55;116 C#5 1 55;116 A#4 1 55;116 F#5 1 55;124 C#5 1 55;124 A#4 1 55;124 F#5 1 55;0 D#6 2 10055;2 C#6 2 10055;4 B5 2 10055;6 C#6 2 10055;8 D#6 2 10055;10 B5 1 10055;11 A#5 1 10055;12 C#6 2 10055;14 G#5 1 10055;15 F#5 1 10055;24 A#4 2 10055;26 C#5 6 10055;44 C#5 4 10055;42 D#5 2 10055;40 F5 2 10055;36 C#5 4 10055;34 F#5 2 10055;32 C#5 2 10055;48 D#5 2 10055;50 F5 2 10055;52 G#5 2 10055;54 D#5 2 10055;62 D#5 2 10055;60 F5 2 10055;56 F5 2 10055;58 A#5 2 10055;64 F5 4 10055;72 G#5 4 10055;76 B5 8 10055;92 G#5 4 10055;88 F#5 4 10055;84 F5 4 10055;68 G#5 4 10055;96 C#5 10 10055;106 F5 4 10055;110 D#5 6 10055;116 F5 4 10055;120 F#5 4 10055;124 G#5 4 10055;128 B3 1 55;132 B4 1 55;132 F#4 1 55;132 D#5 1 55;140 B4 1 55;140 F#4 1 55;140 D#5 1 55;148 B4 1 55;148 F#4 1 55;148 D#5 1 55;156 B4 1 55;156 F#4 1 55;156 D#5 1 55;160 A#3 1 55;164 A#4 1 55;164 F4 1 55;164 C#5 1 55;172 A#4 1 55;172 F4 1 55;172 C#5 1 55;180 A#4 1 55;180 F4 1 55;180 C#5 1 55;188 A#4 1 55;188 F4 1 55;188 C#5 1 55;192 D#4 1 55;196 D#5 1 55;196 A#4 1 55;196 F#5 1 55;204 D#5 1 55;204 A#4 1 55;204 F#5 1 55;128 D#6 2 10055;130 C#6 2 10055;132 B5 2 10055;134 C#6 2 10055;136 D#6 2 10055;138 B5 1 10055;139 A#5 1 10055;140 C#6 2 10055;142 G#5 1 10055;143 F#5 1 10055;152 A#4 2 10055;154 C#5 6 10055;172 C#5 4 10055;170 D#5 2 10055;168 F5 2 10055;164 C#5 4 10055;162 F#5 2 10055;160 C#5 2 10055;176 D#5 2 10055;178 F5 2 10055;180 G#5 2 10055;182 D#5 2 10055;190 D#5 2 10055;188 F5 2 10055;184 F5 2 10055;186 A#5 2 10055;192 F5 4 10055;200 G#5 4 10055;196 G#5 4 10055;160 C#7 4 20055;128 F#5 4 20055;132 D#7 4 20055;160 F#5 4 20055;176 F6 4 20055;184 G#6 4 20055;192 B6 4 20055;184 F6 4 20055;176 C#6 4 20055;192 F#6 4 20055;192 G#5 4 20055;0 B7 1 55 0'

# Happy sound for hit
happy_song = '0 C5 1 55;2 E5 1 55;4 G5 1 55;6 C6 2 55'

# Sad sound for miss
sad_song = '0 A4 2 55;2 F4 2 55;4 D4 2 55'

# I2C LCD setup
i2c = SoftI2C(scl=Pin(13), sda=Pin(3), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

ledAmount = 35

# NeoPixel setup
pin = Pin(10, Pin.OUT)
np = neopixel.NeoPixel(pin, ledAmount)

# NeoPixel Eldur
pinNpAmb = Pin(12, Pin.OUT)
npAmb = neopixel.NeoPixel(pinNpAmb, 16)

# Buttons
button1 = Pin(11, Pin.IN, Pin.PULL_UP)
button2 = Pin(9, Pin.IN, Pin.PULL_UP)

# takka led
btnLed = Pin(14, Pin.OUT)

# litir
brightness = 125
red   = (brightness, 0, 0)
green = (0, brightness, 0)
blue  = (0, 0, brightness)
off   = (0, 0, 0)

# leik var
target_index = random.randint(0, ledAmount - 1)
speed_delay = 80
min_speed = 10
speed_step = 10

current_player = 1
player1_pos = 0
player2_pos = 0

btnLed.value(1)

fire_phase = 0.0
fire_speed = 0.08
fire_min = 40
fire_max = 125


def fire_breathe():
    global fire_phase

    fire_phase += fire_speed
    breath = (math.sin(fire_phase) + 1) / 2  # 0–1 smooth breathing

    base = int(fire_min + (fire_max - fire_min) * breath)

    for i in range(16):
        flicker = random.randint(-30, 15)

        r = max(0, min(255, base + flicker))

        # Much less green (true orange tone)
        g = max(0, min(255, int(r * 0.18) + random.randint(-5, 5)))

        b = 0

        npAmb[i] = (r, g, b)

    npAmb.write()
# leik func
def clear_strip():
    for i in range(ledAmount):
        np[i] = off


def show_target():
    np[target_index] = green


def circular_distance(a, b):
    forward = abs(a - b)
    wrap = ledAmount - forward
    return min(forward, wrap)


def flash_color(color, times=2, delay=80):
    for _ in range(times):
        clear_strip()
        np.write()
        time.sleep_ms(delay)

        for i in range(ledAmount):
            np[i] = color
        np.write()
        time.sleep_ms(delay)


def wait_release(button):
    while button.value() == 0:
        fire_breathe()  # keep fire alive while waiting


def switch_player():
    global current_player
    current_player = 2 if current_player == 1 else 1


def check_loser():
    global player1_pos, player2_pos

    if player1_pos >= 12:
        lcd.clear()
        lcd.putstr("P1 TAPAR!")
        lcd.move_to(0, 1)
        lcd.putstr("P2 VINNUR!")
        flash_color(red, 5, 100)
        reset_game()


    if player2_pos >= 12:
        lcd.clear()
        lcd.putstr("P2 TAPAR!")
        lcd.move_to(0, 1)
        lcd.putstr("P1 VINNUR!")
        flash_color(red, 5, 100)
        reset_game()

        


def reset_game():
    global player1_pos, player2_pos, speed_delay
    player1_pos = 0
    player2_pos = 0
    speed_delay = 80
    time.sleep(2)
    lcd.clear()
    
def intro():
    lcd.clear()
    lcd.putstr("  LED DUEL  ")
    lcd.move_to(0, 1)
    lcd.putstr("  Tilbuin...")

    # Led Intro
    for i in range(ledAmount):
        np[i] = (0, 0, 50)
        np.write()
        time.sleep_ms(20)

    # Play the intro song ONCE
    introSong = music(song, looping=False, pins=[Pin(21)])
    while introSong.tick():  
        fire_breathe()       
        time.sleep_ms(5)

    # clear led
    clear_strip()
    np.write()

    lcd.clear()
    lcd.putstr("LEIKUR HEFST!")
    time.sleep(2)
    lcd.clear()

intro()

# ts loop
while True:

    fire_breathe()  # eldur

    print("Pos P1 =", player1_pos, "Pos P2 =", player2_pos)

    for current_index in range(ledAmount):

        fire_breathe()  # update eld

        clear_strip()
        show_target()
        np[current_index] = red
        np.write()
        time.sleep_ms(speed_delay)

        active_button = button1 if current_player == 1 else button2

        if active_button.value() == 0:

            distance = circular_distance(current_index, target_index)

            if distance == 0:
                # HIT
                flash_color(green)
                
                
                if speed_delay > min_speed:
                    speed_delay -= speed_step

                #LCD Stuff
                lcd.clear()
                lcd.putstr("P" + str(current_player) + " HITTIR!")

                # Play happy sound
                happyTone = music(happy_song, looping=False, pins=[Pin(21)])
                while happyTone.tick():
                    fire_breathe()
                    time.sleep_ms(5)

            else:
                # MISS
                flash_color(red)

                # Play sad sound
                sadTone = music(sad_song, looping=False, pins=[Pin(21)])
                while sadTone.tick():
                    fire_breathe()
                    time.sleep_ms(5)
                    
                    
                #CALC reiti
                squaresAhead = distance / 4
                spacestoGo = int(math.ceil(squaresAhead))
                
                
                #update pos
                if current_player == 1:
                    player1_pos += spacestoGo
                    if player1_pos > 12:
                        player1_pos = 12
                    new_pos = player1_pos
                else:
                    player2_pos += spacestoGo
                    if player2_pos > 12:
                        player2_pos = 12
                    new_pos = player2_pos



                # LCD Stuff
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("P" + str(current_player) + " fara " + str(spacestoGo) + " áfram")
                lcd.move_to(0, 1)
                lcd.putstr("Nuna á reit: " + str(new_pos))

            wait_release(active_button)

            target_index = random.randint(0, ledAmount - 1)

            check_loser()
            switch_player()

            break
