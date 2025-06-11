#
# getCowes.py - parse cowes.co.uk for tidal height
#

import requests
#from datetime import datetime
from lxml import html
import time

# the CHC sister website cowes.co.uk
tideurl = "https://www.cowes.co.uk/harbour-information/weather-tide-information/"

oheight = 0.0 # cache
odatestr = ""

def getCowes():
    global oheight

    # Need to check DST as times in GMT/UTC
    dtime = time.localtime()
    #print(dtime, dtime.tm_isdst) # (2010, 5, 21, 21, 48, 51, 4, 141, 0)
    BST = (dtime.tm_isdst == 1) 

    try:
        tidepage = requests.get(tideurl)
        #print(tidepage)
        tree = html.fromstring(tidepage.content)
    except Exception as e:
        print(e)
        return(odatestr, oheight)


    # dateTime related to the cols
    datestr = tree.xpath('//span[@class="dateTime"]/text()')[1]
    #print(datestr) # 04/06/25 13:31
    if (BST): # deal with DST
        hr = datestr[10:12]
        val = int(hr)
        #print(hr, val)
        val += 1
        if val > 24: val = 0
    datestr = datestr[0:10] + f"{val:02d}:" + datestr[13:]

    # and Observed!
    hval = tree.xpath('//span[text()="Observed:"]/following-sibling::text()')[0]
    #print(hval, float(hval[:-1]))

    odatestr = datestr
    oheight = float(hval[:-1])

    return(datestr, float(hval[:-1]))

# end getCowes()

if __name__ == "__main__":
    dstr, hval = getCowes()
    print (dstr, hval)
