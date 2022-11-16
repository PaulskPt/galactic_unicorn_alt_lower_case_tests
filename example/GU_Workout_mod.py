# Pimoroni Galactic Unicorn Lower case character set and AHT20 sensing
# Tony Goodhew - 13th Nov 2022
# See: https://www.instructables.com/Galactic-Unicorn-Graphical-Workout/
# Needs ahtx0.py library and sensor for final part
# Full character set included - No size adjustments - single size - not enough height for enlargement
# To save space delete the extended characters not needed
# Notes @PaulskPt:
# a) See: https://github.com/targetblank/micropython_ahtx0/blob/master/ahtx0.py
# b) Added a kinda `hotplug` algorithm for the external sensor
# c) Added global brill variable and function adj_val() to reduce brilliance and adjust other of the r, g, b values accorindingly
#
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time, sys
from machine import Pin, I2C

# Added by @PaulskPt:
from GU_Workout_mod_ini import *

my_debug = False
use_sensor = True

if use_sensor:
    sensor_present = False
    ahtx0 = None
    sensor = None

# create a PicoGraphics framebuffer to draw into
gr = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)

# create our GalacticUnicorn object
gu = GalacticUnicorn()

brill = 100 # Using brill to make default brilliance less strong

def adj_val(v):
    global brill
    q = brill/255
    if my_debug:
        print(f"adj_val(): param= {v}, brill= {brill}, q= {q}")
    return int(float(v*q))

#Define some colours
BLACK = gr.create_pen(0, 0, 0)
RED =  gr.create_pen(brill, 0, 0)
YELLOW = gr.create_pen(brill, brill, 0)
GREEN = gr.create_pen(0, brill, 0)
CYAN =  gr.create_pen(0, brill, brill)
BLUE =  gr.create_pen(0, 0, brill)
MAGENTA =  gr.create_pen(brill, 0, brill)
p1 = adj_val(200) #int(float(200*q))  # adjust relative to global var brill value
p2 = adj_val(100) #int(float(100*q))  # same
p3 = adj_val(50) # int(float(50*q))   # same
WHITE =  gr.create_pen(p1, p1, p1)
GREY =  gr.create_pen(p2, p2, p2)
DRKGRY =  gr.create_pen(p3, p3, p3)
# Cleanup p1 ~ p3
q = None
p1 = None
p2 = None
p3 = None

def character(asc, xt, yt, r, g, b):  # Single character sz is size: 1 or 2
    colour = gr.create_pen(r, g, b)
    gr.set_pen(colour)
    code = asc * 5    # 5 bytes per character
    for ii in range(5):
        line = FONT[code + ii]
        for yy in range(8):
            if (line >> yy) & 0x1:
                gr.pixel(ii+xt, yy+yt) 
                                    
def prnt_st(asci, xx, yy, r, g, b):  # Text string
    move = 6
    for letter in(asci):
        asci = ord(letter)
        character(asci, xx, yy, r, g, b)
        xx = xx + move

def cntr_st(s, y, r, g, b): # Centres text on line y
    w = 6 
    gap = int((53 - len(s) * w)/2)
    prnt_st(s, gap, y, r, g, b)

def scroll(msg, yy, r, g, b):
    p =  53
    length = len(msg) * 6
    steps = length + 53
    for c in range(steps):
        gr.set_pen(BLACK)
        gr.clear()
        colour = gr.create_pen(r, g, b)
        gr.set_pen(colour)
        prnt_st(msg, p, yy, r ,g ,b)
        gu.update(gr)
        p = p - 1
        time.sleep(0.1)
# =========== End of font support routines ===========

def reconnect_sensor():
    global sensor_present, sensor, ahtx0

    if not sensor_present:
        if ahtx0 is None:
            import ahtx0
        try:
            i2c = I2C(id=0,scl=Pin(5), sda=Pin(4))
            sensor = ahtx0.AHT20(i2c)
        except ValueError as exc:  # ValueError occurs if the temperature sensor is not connected
            pass
        except OSError:
            pass

        if sensor is not None:
            sensor_present = True
    if sensor_present:
        return True
    return False
# =========== End of sensor support routine ===========

def scroll_p(msg, yy, r, g, b):  # Pimoroni font - no lower case
    p =  53
    length = gr.measure_text(msg, 1)
    steps = length + 53
    for c in range(steps):
        gr.set_pen(BLACK)
        gr.clear()
        colour = gr.create_pen(r, g, b)
        gr.set_pen(colour)
        gr.text(msg, p, yy, scale=1)
        gu.update(gr)
        p = p - 1
        time.sleep(0.18)
               
def rect_outline(x, y, w, h, c):
    gr.set_pen(c)    
    for xx in range(x, x+w-1):    
        gr.pixel(xx, y)
        gr.pixel(xx, y+h-1)
    for yy in range(y, y+h):
        gr.pixel(x, yy)
        gr.pixel(x+w-1, yy)
    gu.update(gr)

def clear():
    gr.set_pen(BLACK)
    gr.clear()
    gu.update(gr)

def ga_test():
    text = "Galactic Unicorn"
    print(f"{text} test...")
    scroll_p(text, 2, brill, adj_val(100), adj_val(30)) # Pimoroni font
    scroll(text, 2, 0, 0, brill)      # Extended character set lower case font
    gr.set_pen(RED)
    gu.update(gr)

def rect_test():
    print("rectangular test")
    rect_outline(0, 0, 53, 11, RED) # Fill the screen with colour rectangles
    gu.update(gr)
    time.sleep(1)
    rect_outline(1, 1, 51, 9, YELLOW)
    gu.update(gr)
    time.sleep(1)
    rect_outline(2, 2, 49, 7, GREEN)
    gu.update(gr)
    time.sleep(1)
    rect_outline(3, 3, 47, 5, CYAN)
    gu.update(gr)
    time.sleep(1)
    rect_outline(4, 4, 45, 3, BLUE)
    gu.update(gr)
    time.sleep(1)
    rect_outline(5, 5, 43, 1, MAGENTA)
    gu.update(gr)
    time.sleep(1)
    gr.set_pen(DRKGRY)  # Add a few circles
    gr.circle(25, 5, 5)
    gr.set_pen(GREY)
    gr.circle(25, 5, 4)
    gr.set_pen(BLACK)
    gr.circle(25, 5, 3)
    gr.set_pen(WHITE)
    gr.circle(25, 5, 2)
    gr.set_pen(BLACK)
    gr.pixel(25, 5)
    gu.update(gr)

    time.sleep(4)
    gr.set_pen(BLACK)
    gr.clear()
    gu.update(gr)

def tonygo2_test():
    print("TonyGo2 test")
    # prnt_st(asci, xx, yy, r, g, b):  # Text string
    prnt_st("TonyGo2", 6, 2, brill, 0, 0) # Text examples
    gu.update(gr)
    time.sleep(2)
    scroll("Lower case", 2, 0, 0, brill)
    gu.update(gr)
    clear()

def light_sensor_test():
    print("Light sensor test")
    #Light sensor bar graph
    q = adj_val(300)
    cntr_st("Cover",2, 0, q, 0)
    gu.update(gr)
    time.sleep(1.3)
    clear()
    cntr_st("and",2, 0, q, 0)
    gu.update(gr)
    time.sleep(1.3)
    clear()
    cntr_st("expose", 2, 0, q, 0)
    gu.update(gr)
    time.sleep(1.3)
    clear()
    cntr_st("light", 2, 0, q, 0)
    gu.update(gr)
    time.sleep(1.3)
    clear()
    cntr_st("sensor", 2, 0, q, 0)
    gr.set_pen(CYAN)
    gr.pixel(52, 4)
    gr.pixel(52, 3)
    gu.update(gr)
    gu.update(gr)
    time.sleep(1.3)

    clear()
    maxx = -999
    minn = 999999

    for i in range(53):         # Get max and min readings
        gr.set_pen(RED)
        l = gu.light()
        gr.pixel(i, 4)
        gr.pixel(i, 3)
        gu.update(gr)
        if l > maxx:
            maxx = l
            gr.set_pen(GREEN) # GREEN feedback flash
            gr.pixel(52, 0)
            gu.update(gr)
            time.sleep(0.2)
            gr.set_pen(BLACK)
            gr.pixel(52, 0)
            gu.update(gr)
            
        elif l < minn:
            minn = l
            gr.set_pen(BLUE) # BLUE feedback flash
            gr.pixel(50, 0)
            gu.update(gr)
            time.sleep(0.2)
            gr.set_pen(BLACK)
            gr.pixel(50, 0)
            gu.update(gr)
        time.sleep(0.1)
    #print(minn,maxx)
    print(f"Light sensor min,max values: {minn},{maxx}") # Mod by @Paulsk
    r = maxx -minn
    gr.set_pen(BLACK)
    gr.clear()
    gu.update(gr)

    for i in range(50):  # Draw the dynamic graph
        ww = int((gu.light() - minn) * 50 / r * 0.7) # Read the sensor and adjust range
        gr.set_pen(BLACK)
        gr.clear()
        gr.set_pen(GREEN)
        
        for i in range(ww): # Update bar graph
            gr.pixel(i, 4)
        gu.update(gr)
        time.sleep(0.15)
    clear()
        
gr.set_pen(BLACK)
gr.clear()        
# ===============================================================================
# AHT20 fitted to Stemma/QT socket = Comment out if not available
def temp_sensor_test():
    global sensor_present, sensor
    print("Temp & Hum test")
    while True:            
        if sensor_present:
            """
            i2c = I2C(id=0,scl=Pin(5), sda=Pin(4))
            # Create the sensor object using I2C
            sensor = ahtx0.AHT20(i2c)
            """
            cntr_st("AHT20", 2, 0, 300, 0)
            gu.update(gr)
            time.sleep(2)
            clear()
            cntr_st("Sensor", 2, 0, 300, 0)
            gu.update(gr)
            time.sleep(1.3)
            clear()

            t = int(sensor.temperature * 10 + 0.5) /10
            h = sensor.relative_humidity
            msg = str(t) + chr(248) + "C & Hum " + str(int(h + 0.5)) +" %" # degrees
            q = brill/255
            p1 = adj_val(100)  # adjust relative to global var brill value
            p2 = adj_val(20)   # same
            if my_debug:
                print(f"temp_sensor_test(): brill//255= {brill}//255= {q}, p1= {p1}, p2= {p2}")
            scroll(msg, 2, brill, p1, p2)
            break
        else:
            scroll("No sensor data. Check wiring...", 2, brill, 0, 0)
            gu.update(gr)
            time.sleep(2)
            if reconnect_sensor():
                if my_debug:
                    print("Temperature sensor has been (re)connected")
            else:
                print("Failed to reconnect temperature sensor")
                break

def doit(s):
    if s == "ga":
        ga_test()
    if s == "rect":
        rect_test()
    if s == "tonygo2":
        tonygo2_test()
    if s == "light":
        light_sensor_test()
    if s == "temp":
        temp_sensor_test()

stop = False
print("Starting tests...")
print("by Tony Goodhew (@tonygo2)")
print("modified by Paulus Schulinck (@PaulskPt)")
while True:
    try:
        # Run tests that are enabled in do_tests_dict
        for k,v in tests_dict.items():
            #print(f"v= {v}")
            if v[1]:
                doit(v[0])
        clear()
        prnt_st("Done", 15, 1, 0,brill-50, 0)
        print("Tests done")
        time.sleep(2)
        print()
        print("Going around...")
        clear()
    except KeyboardIntterupt:
        print("Interrupted by user. Exiting...")
        stop = True
 
if stop:
    #================================================================================
    # Tidy up
    gu.update(gr)
    time.sleep(1.5)
    gr.set_pen(BLACK)
    gr.clear()
    gu.update(gr)
    sys.exit()
