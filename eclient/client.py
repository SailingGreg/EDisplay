#
# display.py - display information on an epaper display
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
picdir = "/home/pi/Cdisplay/Epaper-client/epaperws/pic"
#libdir = "./epaperws/lib"
libdir = "/home/pi/Cdisplay/Epaper-client/epaperws/lib"
#/home/pi/Cdisplay/Epaper-client
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image
from waveshare_epd import epd7in5_V2 # for the 800x600 V2

# definitions
#sdelay = 300
FIVE_MINS = 300
#url = "https://waveshare_epd.com/screen.bmp"
url = "http://piepaper/screen.bmp"


# used for pyowm install as it is a 'local' install
#locallib = "/usr/local/lib/python3.7/site-packages"
locallib = "/home/pi/.local/lib/python3.7/site-packages"
if os.path.exists(locallib):
    sys.path.append(locallib)
# retrieve the access keys from the environment
#owm_key = os.environ.get('OWM_KEY')
#met_id = os.environ.get('MET_ID')
#met_key = os.environ.get('MET_KEY')

#if (owm_key == "" or met_id == "" or met_key == ""):
    #print ("Please set OWM_KEY, MET_ID and MET_KEY")
    #exit(1)

#
# main()
#
try:
    # Initialise the interface
    epd = epd7in5_V2.EPD()

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
