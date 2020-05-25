#
# display.py - display club and race information on an epaper display
#
# It sources the wind from the cub systems
# The upcoming events from the clubs website (via mec api)
# Adds the weather observation and the forecast for the next 6 hours
# and the tide from thamestides plus flow from the EA
#
# Distributed under MIT License
# 
# Copyright (c) 2020 Greg Brougham
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# pip install epd-library

#!/usr/bin/python3
#
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

# needed for html requests
import requests
import json
import datetime
from datetime import date
import dateutil.relativedelta
from dateutil import parser
import pyowm # wraps open weather apis
from lxml import html
from bs4 import BeautifulSoup

EPD7in5WIDTH = 800
EPD7in5HEIGHT = 480
EPD4in2WIDTH = 400
EPD4in2HEIGHT = 300

import initServer
import getEaukFlow, getEvents, getFlow, getMet, getObs, getopt, getPosts, getTides, getWind
# changed from DEBUG to INFO
logging.basicConfig(level=logging.INFO)
logging.info("server and nginx")


# added to directory absolute for systemd
LOC = "/home/pi/EDisplay/eserver/"

#if (initServer.owm_key == "" or initServer.met_id == "" or initServer.met_key == ""):
    #print ("Please set OWM_KEY, MET_ID and MET_KEY")
    #exit(1)

#
# main()
#
try:
    # initialise the owm library
    owm = pyowm.OWM(initServer.owm_key)
    # for one run
    oneRun = 1

    # prime the loop to last 5mins
    next_call = time.time() + initServer.FIVE_MINS

    # for test purposed this should be at least 3 or 15mins
    loop = 0
    while (True):

        logging.info("init and Clear")
        # load wind on every iteration
        logging.info("loadWind ...")
        getWind.PWind().loadWind()

        # get the weather
        if ((loop % 3) == 0):
            logging.info("getObs ...")
            obs1 = getObs.PObs().getObs(owm, 'London,GB')

        # break out
        weather = obs1.get_weather()
        temperature = weather.get_temperature(unit='celsius')
        sunrise = weather.get_sunrise_time()
        sunset = weather.get_sunset_time()
        #print (obs1)

        # load tides every 6 times through the loop
        if ((loop % 6) == 0):
            logging.info("loadTides ...")
            prtides = getTides.PTides().loadTides()

        # load eauk flows - updated every 15 mins so mode 3
        if ((loop % 3) == 0):
            logging.info("eaukFlow ...")
            rflow = getEaukFlow.PEaukFlow().eaukFlow() # string

        if ((loop % 3) == 0):
            logging.info("loadEvents ...")
            noEvents = getEvents.PEvents().loadEvents() # return list
            mecevents = getEvents.events # the global

        if ((loop % 3) == 0):
            logging.info("getMet ...")
            timeseries = getMet.PMet().getMet() # return list
            noTimeseries = len(timeseries)

        #Column1 = 10
        logging.info("4.read bmp file on window")
        # Note changing width/height changes the orientation
        # 255: clear the frame
        #Himage2 = Image.new('1', (epd.width, epd.height), 255)
        # corrected to reflect the v2 dimensions in landscape
        Himage2 = Image.new('1', (EPD7in5WIDTH, EPD7in5HEIGHT), 255)
        # image for the 4in2 display in portrait
        smallImage = Image.new('1', (EPD4in2WIDTH, EPD4in2HEIGHT), 255)
        #Himage2 = Image.new('1', (800, 600), 255)

        # draw is just shorthand to make the code more readable
        draw = ImageDraw.Draw(Himage2)
        smalldraw = ImageDraw.Draw(smallImage)
        draw.text((10, 0), 'Club Wind', font = initServer.font36, fill = 0)

        # load the wind and ranelagh images
        bmp = Image.open(LOC + "./tmp/daywind.png")
        bmp2 = Image.open(LOC + "./tmp/daywinddir.png")
        bmp3 = Image.open(initServer.ranelaghlogo + ".bmp")

        # for now this is just to the right
        Column1 = 10
        Column2 = 320 # the horizontal offset

        # these image are 300 x 180 by default - gap 10 pixels
        Himage2.paste(bmp, (Column1, 46))
        Himage2.paste(bmp2, (Column1, 180 + 10 + 46)) # 236
        Himage2.paste(bmp3, (Column1 - 30, 2*180 + 20 + 46)) # 236
        # use a negative offset to 'trim' the image
        smallImage.paste(bmp3, (Column1 - 30, EPD4in2HEIGHT - 50)) # 236
        #smallImage.paste(bmp3, (Column1, EPD4in2HEIGHT - 50)) # 236

        # add date & time - top right
        tnow = datetime.datetime.now()
        imgtext = tnow.strftime('%d %b %Y %H:%M')
        dw, h = draw.textsize(imgtext, font=initServer.font24)
        sdw, sh = draw.textsize(imgtext, font=initServer.font16)
        draw.text((EPD7in5WIDTH-dw-10, 0), imgtext, \
                                font = initServer.font24, fill = 0)

        smalldraw.text((EPD4in2WIDTH-sdw-10, 0), imgtext, \
                                font = initServer.font16, fill = 0)


        draw = ImageDraw.Draw(Himage2)
        draw.text((Column2, 0), 'Club Events', font = initServer.font36,\
                                                                    fill = 0)
        smalldraw.text((Column1, 0), 'Club Events', font = initServer.font32, \
                                                                    fill = 0)

        mecendpoint = 'https://ranelaghsc.co.uk/wp-json/mecexternal/v1/event/'

        for x in range(noEvents):

            # which has id, data and date
            etitle = BeautifulSoup(mecevents[x]["title"], "lxml").text
            econtent = mecevents[x]["content"]
            cleantext = BeautifulSoup(econtent, "lxml").text
            estart_date = mecevents[x]["meta"]["mec_start_date"]
            estart_hour = mecevents[x]["meta"]["mec_start_time_hour"]
            estart_mins = mecevents[x]["meta"]["mec_start_time_minutes"]
            estart_ampm = mecevents[x]["meta"]["mec_start_time_ampm"]

            # denormalise and parse to python date
            prdate = initServer.PInitServer().mectodate(estart_date, int(estart_hour), int(estart_mins), estart_ampm)
            imgtext = prdate.strftime('%a %d %b %Y %H:%M') + " - " + etitle

            txt = " > " + cleantext[0:65]
            # the following is rendered twice to effect 'bold'
            draw.text((Column2, 2*x* 20 + 40), imgtext, font = initServer.font16, fill = 0)
            draw.text((Column2, 2*x* 20 + 41), imgtext, font = initServer.font16, fill = 0)
            draw.text((Column2, (2*x+1) * 20 + 40), txt, font = initServer.font16, fill = 0)

            # just add the title for small displays
            smalldraw.text((Column1, x * 20 + 40), imgtext, \
                                        font = initServer.font16, fill = 0)
        # end while

        # now the weather forecast and observations
        # first row is 236
        draw.text((Column2, 236), "Weather", font = initServer.font36, fill = 0)

        # add 100 to vert offset
        draw.text((Column2 + 150, 236 - 25), initServer.weather_icon_dict[weather.get_weather_code()], font = initServer.fontweatherbig, fill = 0)
        tempstr = str("{0}{1}C".format(int(round(temperature['temp'])), u'\u00b0'))
        draw.text((Column2 + 225, 236 + 12), tempstr, font = initServer.font24, fill = 0)


        # forecast at 236 + 36 + 2266 -> 274 and lists the next 6 hours
        tstr =  "Time:"
        twind = "Wind:"
        #twind = "Wind (knots):"
        tgust = "Gust:"
        tdir =  "Dir:"
        ttemp = "Temp:"
        draw.text((Column2, 274 + 0 * 18), tstr, font = initServer.font16, fill = 0)
        draw.text((Column2, 274 + 1 * 18), twind, font = initServer.font16, fill = 0)
        draw.text((Column2, 274 + 2 * 18), tgust, font = initServer.font16, fill = 0)
        draw.text((Column2, 274 + 3 * 18), tdir, font = initServer.font16, fill = 0)
        draw.text((Column2, 274 + 4 * 18), ttemp, font = initServer.font16, fill = 0)

        # convert m/s -> knots
        for x in range(6):
            ftime = timeseries[x]['time']
            wspeed = timeseries[x]['windSpeed10m']
            wspeed = wspeed * 1.943844
            gspeed = timeseries[x]['windGustSpeed10m']
            gspeed = gspeed * 1.943844
            wdir = timeseries[x]['windDirectionFrom10m']
            wtemp = timeseries[x]['screenTemperature']

            idate = parser.isoparse (ftime)
            itime = str("{:%H:%M}".format(idate))
            iwind = str("{:>2d}".format(int(round(wspeed))))
            igust = str("{:>2d}".format(int(round(gspeed))))
            idir = str("{:03d}".format(int(round(wdir))))
            itemp = str("{:>2d}".format(int(round(wtemp))))

            # note the 'width' for column calc
            dw, h = draw.textsize(itime, font=initServer.font16)
            ww, h = draw.textsize(iwind, font=initServer.font16)
            wg, h = draw.textsize(igust, font=initServer.font16)
            wd, h = draw.textsize(idir, font=initServer.font16)
            wt, h = draw.textsize(itemp, font=initServer.font16)

            draw.text((Column2 + 95 + x*48-dw, 274 + 0*18), itime, font = initServer.font16, fill = 0)
            draw.text((Column2 + 95 + x*48-ww, 274 + 1*18), iwind, font = initServer.font16, fill = 0)
            draw.text((Column2 + 95 + x*48-wg, 274 + 2*18), igust, font = initServer.font16, fill = 0)
            draw.text((Column2 + 95 + x*48-wd, 274 + 3*18), idir, font = initServer.font16, fill = 0)
            draw.text((Column2 + 95 + x*48-wt, 274 + 4*18), itemp, font = initServer.font16, fill = 0)
            # end of for timeseries

        # and finally the tides!
        tiderow = 236 + 36 + 6 * 18
        stiderow = 150
        draw.text((Column2, tiderow), "Tides", font = initServer.font28, fill = 0)
        smalldraw.text((Column1, stiderow), "Tides", font = initServer.font28, fill = 0)
        dw, h = draw.textsize("Tides", font=initServer.font28)
        draw.text((Column2 + dw + 14, tiderow + 28 - 14), \
                    "(via thamestides.org)", font = initServer.font14, fill = 0)
        smalldraw.text((Column1 + dw + 14, stiderow + 28 - 14), \
                    "(via thamestides.org)", font = initServer.font14, fill = 0)
        tidestr1 = ""
        tidestr2 = ""
        for row in range (0, 4):
            if (row == 0 or row == 1):
                if (len(prtides[row][1]) > 0):
                    tidestr1 = tidestr1 + prtides[row][0] + ": " \
                        + prtides[row][1] + " " + prtides[row][2] + "m"
                    if (row == 0):
                        tidestr1 = tidestr1 + ", "
            if (row == 2 or row == 3):
                if (len(prtides[row][1]) > 0):
                    tidestr2 = tidestr2 + prtides[row][0] + ": " \
                        + prtides[row][1] + " " + prtides[row][2] + "m"
                    if (row == 2):
                        tidestr2 = tidestr2 + ", "

        # end for
        draw.text((Column2, tiderow + 32), tidestr1, font = initServer.font16, fill = 0)
        smalldraw.text((Column1, stiderow + 32), tidestr1, font = initServer.font16, fill = 0)
        draw.text((Column2, tiderow + 32 + 18), tidestr2, font = initServer.font16, fill = 0)
        smalldraw.text((Column1, stiderow + 32 + 18), tidestr2, font = initServer.font16, fill = 0)

        # Add the river flow
        draw.text((Column2, tiderow + 32 + 2 * 18), rflow, font = initServer.font16, fill = 0)
        smalldraw.text((Column1, stiderow + 32 + 2 * 18), rflow, font = initServer.font16, fill = 0)

        # save a copy of the image
        if (oneRun == 1):
            Himage2.save(LOC + "./static/screen.bmp")
            #Himage2.save(LOC + "./static/7in5image.bmp")
            smallImage.save(LOC + "./static/4in2image.bmp")
            #Himage2.save("./tmp/screen.bmp")

        #sleep
        time.sleep(5)

        # should put the display to sleep & then delay 5 mins -> 300 seconds
        logging.info("sleeping ...")

        # sleep until 5mins is up
        if ((next_call - time.time()) > 0.0):
            time.sleep(next_call - time.time())

        next_call = time.time() + initServer.FIVE_MINS

        loop = loop + 1
        if (loop == 100): # reset so it nevers exceeds 'int'
            loop = 0

    # end processing loop

    logging.info("Clear...")
    logging.info("Goto Sleep...")
    
except IOError as e:
    print ('traceback.format_exc():\n%s', traceback.format_exc())
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()

# end file
