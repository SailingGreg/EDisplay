#
# 
#

from dateutil import parser
from PIL import Image, ImageFont
import sys
import os

from ecreds import *

# need the name of root of the pic and lib directories
# they also have fonts under fonts under picdir

LOC = "/home/pi/EDisplay/eserver/"
picdir = LOC + "./epaperws/pic"
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = LOC + "./epaperws/lib"
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# used for pyowm install as it is a 'local' install
#locallib = "/usr/local/lib/python3.7/site-packages"
locallib = "/home/pi/.local/lib/python3.7/site-packages"
if os.path.exists(locallib):
    sys.path.append(locallib)

# definitions
#sdelay = 300
FIVE_MINS = 300
#ranelaghlogo = LOC + "./tmp/ranelagh-253x47"
ranelaghlogo = LOC + "./tmp/ccyc-image-207x"
#ranelaghlogo = "./tmp/RSC-180x33"

# mapping to images
weather_icon_dict = {200:"6", 201:"6", 202:"6", 210:"6", 211:"6", 212 : "6", 
                     221:"6", 230:"6", 231:"6", 232:"6", 
                     300:"7", 301:"7", 302:"8", 310:"7", 311:"8", 312 : "8",
                     313:"8", 314:"8", 321:"8", 
                     500:"7", 501:"7", 502:"8", 503:"8", 504:"8", 511 : "8", 
                     520:"7", 521:"7", 522:"8", 531:"8",
                     600:"V", 601:"V", 602:"W", 611:"X", 612:"X", 613 : "X",
                     615:"V", 616:"V", 620:"V", 621:"W", 622:"W", 
                     701:"M", 711:"M", 721:"M", 731:"M", 741:"M", 751 : "M",
                     761:"M", 762:"M", 771:"M", 781:"M",
                     800:"1", 801:"H", 802:"N", 803:"N", 804:"Y",
                     "few clouds":"1", "scattered clouds":"H", "broken clouds":"N", "overcast clouds":"Y" }

# the fonts
# font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
# font36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36)
# font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
# font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
# font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
# font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)

font40 = ImageFont.truetype(LOC + './pic/Font.ttc', 40)
font36 = ImageFont.truetype(LOC + './pic/Font.ttc', 36)
font32 = ImageFont.truetype(LOC + './pic/Font.ttc', 32)
font24 = ImageFont.truetype(LOC + './pic/Font.ttc', 24)
font18 = ImageFont.truetype(LOC + './pic/Font.ttc', 18)
font14 = ImageFont.truetype(LOC + './pic/Font.ttc', 14)
font16 = ImageFont.truetype(LOC + './pic/Font.ttc', 16)
font28 = ImageFont.truetype(LOC + './pic/Font.ttc', 28)

# font36 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 36)
# font28 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 28)
# font24 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 24)
# font20 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 20)
# font16 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 16)
# # overwrite the 14 font
# font14 = ImageFont.truetype(LOC+ './epaperws/fonts/arial.ttf', 14)
fontweather = ImageFont.truetype(LOC+ './epaperws/fonts/meteocons-webfont.ttf', 30)
fontweatherbig = ImageFont.truetype(LOC+ './epaperws/fonts/meteocons-webfont.ttf', 60)
#fontweather = ImageFont.truetype(LOC+ './pic/Font.ttc', 30)
#fontweatherbig = ImageFont.truetype(LOC+ './pic/Font.ttc', 60)


#
# credentials are in the ecreds.py file
#owm_key="xxx"
#met_id = "xxx-xxx-xxx-xxx-xxx"
#met_key = "xxx"

class PInitServer:
    # function to convert logo
    def ranelaghLogo(self):

        file_in = ranelaghlogo
        img = Image.open(file_in + ".png")
        img2 = img.convert("1")
        img2.save(file_in + ".bmp")
        #end
    def removeNonAscii(self, s):
        return "".join(i for i in s if (ord(i)<128 and ord(i)>31))

    # convert MEC attritubutes to ISO and parse to a date object.
    def mectodate(self, date, hour, mins, ampm):

        if (ampm == "PM" and hour < 12):
            hour = hour + 12

        # now format the iso string
        estart = "{}T{:02d}:{:02d}".format(date, int(hour), int(mins))
        # and then parse to date for return
        tdate = parser.isoparse (estart)

        return tdate
    # end mectodate()
