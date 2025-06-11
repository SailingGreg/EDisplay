#
# getTidal.py - get tidal data from UKMO via Tidal API
#

import requests
from datetime import datetime
import time

# key needs to be removed to secrets
#ukho_key = "xxxxxxxxxxxxxxxx"
import initServer # has creds

# Constants
LOCATION = "0060"
baseurl =  "https://admiraltyapi.azure-api.net/uktidalapi"
discovery = "/api/V1/Stations"
tidalurl = baseurl + discovery + "/" + LOCATION
tidaldata = tidalurl + "/TidalEvents?1"

# Globals
today = "" # blank to start with
dayhour = "" # blank to start with
otides = [] # cache of tidal data

header={"Ocp-Apim-Subscription-Key": initServer.ukho_key}

def getTidal ():
    global today, dayhour, otides

    # get the current date/time
    dstr = datetime.now().replace(microsecond=0).isoformat()
    cstr = dstr[0:10] # the current data
    hstr = dstr[11:13] # and the hour
    #print (dstr, cstr, hstr)

    # DST?
    dtime = time.localtime()
    #print(dtime, dtime.tm_isdst) # (2010, 5, 21, 21, 48, 51, 4, 141, 0)
    BST = (dtime.tm_isdst == 1) 
    #print ("BST", BST)

    # do this if only a new day or first run
    if (today != cstr): 
        today = cstr # note date

        # get station information
        print (f"fetching {tidalurl}")
        req = requests.get(tidalurl, headers=header)

        print (req)
        jdict = req.json()
        #print (jdict)
        #for ent in jdict:
            #print(ent, type (ent))
        print (jdict["properties"]['Id'], jdict["properties"]['Name'])
    
    # and the tidal information every hour which allows for DST changes
    if (dayhour != hstr):
        dayhour = hstr # note hour

        # get the tides for the station
        print (f"fetching {tidaldata}")
        try:
            req = requests.get(tidaldata, headers=header)
        except e:
            print(req)

        print (req)
        jdict = req.json()
        #print (jdict)

        ret = [] # tidal entries
        cnt = 0
        # iterate over the tidal entries and note today's
        pent = ""
        for ent in jdict:
            cnt += 1
            if (ent['DateTime'].startswith(cstr)): # today?
                #print (f"match {ent}")

                val = f"{round(ent['Height'],1):0.1f}" # also rounds
                #val = str(round(ent['Height'],1))
                if (ent['EventType'] == 'HighWater'):
                    etype = "HW"
                else:
                    etype = "LW"

                # deal with DST
                if BST: # incr hour
                    stime = ent['DateTime'][11:]
                    #print (stime, stime[0:1])
                    hour = int(stime[0:2])
                    hour += 1

                    if (hour >= 24): # not today
                        hour = 0
                    # rebuild the DateTime entry
                    ent['DateTime'] = cstr + f"T{hour:02}:" + stime [3:]
                    #print (ent['DateTime'])

                # we need to filter out the 'double' stands
                if (pent != etype):
                    pent = etype

                    # need to adjust for BST if appropriate
                    estr = ent['DateTime'][11:] + " " + etype + " " + val
                    ret.append(estr)
                else:
                    estr = "duplicate"
                #print ("Entry ", estr)
            #print (ent, ent['EventType'], ent['DateTime'], type (ent))
        otides = ret

    #print(cnt, ret)
    return (otides)

# end of getTidal()

# support testing in isolation
if __name__ == "__main__":
    res = getTidal()
    print (res)
