#
# test sample met office code - need to convert to request()
#
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

import os   # for environ()
import requests

import http.client  # redundant as using requests
import datetime
from datetime import date
import dateutil.relativedelta
from dateutil import parser
import logging

# The main access url for the wordpress post api
siteurl = "https://ranelaghsc.co.uk/"
eventsurl = "https://ranelaghsc.co.uk/wp-json/wp/v2/mec-events"
mecurl = siteurl + "wp-json/mecexternal/v1/calendar/922"
# the events list
events =["", "", ""]

#
# get the MEC events
#
class PEvents:
    def loadEvents (self):
        global events, eventsurl, mecurl

        # note the current date & calc yesterday
        tnow = datetime.datetime.now()
        yesterday = tnow - dateutil.relativedelta.relativedelta(hours=12)
        #tquery = ptime.isoformat()

        # do the request - limted to '3' - need to increase to 8
        # note we can sort by event date as it is not exposed!

        # following has been changed 15!
        #reqstr = eventsurl + "?per_page=15&order=desc"
        req = requests.get(mecurl)
        if (req.status_code != 200):
            logging.error("events return not 200")
            return 0

        jdict = req.json()
        lenjdict = len(req.json())

        #print(lenjdict)
        #print(jdict)

        # now query mec-event end point
        # the followig could be 0, 1, 2, or 3!
        eventCnt = 0

        mdict = jdict["content_json"] # this is actually the data
        for x in mdict:
            #print(x)

            #id = jdict[x]['id']
            for y in mdict[x]: # this at the date or individual level

                """
                tdate = mecdict['meta']['mec_date']['start']['date']
                thour = mecdict['meta']['mec_date']['start']['hour']
                tmins = mecdict['meta']['mec_date']['start']['minutes']
                tampm = mecdict['meta']['mec_date']['start']['ampm']

                # get a date object
                prdate = mectodate(tdate, int(thour), int(tmins), tampm)
                """

                if (eventCnt < 3): # then note the dict entry
                    events[eventCnt] = y["data"]
                    eventCnt = eventCnt + 1

            # end for
        # end for

        #print ("Found: ", eventCnt)
        return eventCnt # the no of events we've found

        return (req.json())
        # end
# end of function