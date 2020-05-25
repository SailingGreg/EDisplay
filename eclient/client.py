#
# eclient.py - display information on an epaper display
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


#!/usr/bin/python3
#
# -*- coding:utf-8 -*-

import os
import sys
import requests
import traceback
import time

# need the name of root of the pic and lib directories
#picdir = "./epaperws/pic"
picdir = "/home/pi/EDisplay/eclient/epaperws/pic"
#libdir = "./epaperws/lib"
libdir = "/home/pi/EDisplay/eclient/epaperws/lib"
#/home/pi/EDisplay/eclient
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image
import platform

#if (platform.node() == "piepaper"):
    #display = "epd7in5_V2"
#else:
    #display = "epd4in2"
#from waveshare_epd import display # for the 400x300

if (platform.node() == "piepaper"):
    from waveshare_epd import epd7in5_V2 # for the 800x480 V2
else:
    from waveshare_epd import epd4in2 # for the 400x300


# definitions
#sdelay = 300
FIVE_MINS = 300
#url = "https://waveshare_epd.com/screen.bmp"
if (platform.node() == "piepaper"):
    url = "http://piepaper/screen.bmp"
else:
    url = "http://piepaper/4in2image.bmp"


#
# main()
#
try:
    # Initialise the interface
    if (platform.node() == "piepaper"):
        epd = epd7in5_V2.EPD()
    else:
        epd = epd4in2.EPD()
        #display = epd4in2
        #epd = display.EPD()

    # for one run
    oneRun = 1

    # prime the loop to last 5mins
    next_call = time.time() + FIVE_MINS

    # for test purposed this should be at least 3 or 15mins
    loop = 0
    #while (loop < 2):
    while (True):

        print("init and Clear")
        epd.init()
        
        # request a copy of the image
        r = requests.get(url, allow_redirects=True)        
        open('display.bmp', 'wb').write(r.content)
        #§img = Image.open("display.png")
        img = Image.open("display.bmp")

        # display and then sleep
        epd.display(epd.getbuffer(img))
        time.sleep(5)
        #loop = loop + 1

        # should put the display to sleep & then delay 5 mins -> 300 seconds
        print("sleeping ...")
        epd.sleep()

        # sleep until 5mins is up
        if ((next_call - time.time()) > 0.0):
            time.sleep(next_call - time.time())

        #time.sleep(300)
        next_call = time.time() + FIVE_MINS

        #time.sleep(180) # minimum refresh interval

        loop = loop + 1
        if (loop == 100): # reset so it nevers exceeds 'int'
            loop = 0

    # end processing loop

    # clear display
    print("Clear...")
    epd.init()
    epd.Clear()

    print("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    print ('traceback.format_exc():\n%s', traceback.format_exc())
    print(e)
    epd7in5_V2.epdconfig.module_exit()
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()

# end file
