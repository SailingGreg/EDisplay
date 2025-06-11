
#
# getCCYC - get calender entries for current month
#

import re
import requests
#from datetime import datetime
from lxml import html
import time

# the fixed url for the club calendar
CCYC="https://www.ccyc.org.uk/calendar"

months = ["January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December" ]

# list of months to added to
# entry will be {"day": day, "event": event}
ientries = {
        "January": [],
        "February": [],
        "March": [],
        "April": [],
        "May": [],
        "June": [],
        "July": [],
        "August": [],
        "September": [],
        "October": [],
        "November": [],
        "December": []
        }

def getCCYC():
    # DST?
    dtime = time.localtime()
    #print(dtime, dtime.tm_isdst) # (2010, 5, 21, 21, 48, 51, 4, 141, 0)
    BST = (dtime.tm_isdst == 1) 

    curmnth = dtime[1]
    curday = dtime[2]
    #print (curmnth, curday, months)

    try:
        ccycpage = requests.get(CCYC)
        print(ccycpage)
        tree = html.fromstring(ccycpage.content)
    except Exception as e:
        print(e)


    # dateTime related to the cols
    tstr = tree.xpath('//span[@class="wixui-rich-text__text"]/text()')
    #print (tstr)
    #datestr = tree.xpath('//span[@class="dateTime"]/text()')[1]
    #print(datestr) # 04/06/25 13:31

    mnth = 0
    pmnth = 0
    res = ""
    entries = []
    # iterate over the entries looking for 'month' sections
    for ent in tstr:
        if (ent == "January"):
            mnth = 1
        if (ent == "February"):
            mnth = 2
        if (ent == "March"):
            mnth = 3
        if (ent == "April"):
            mnth = 4
        if (ent == "May"):
            mnth = 5
        if (ent == "June"):
            mnth = 6
        if (ent == "July"):
            mnth = 7
        if (ent == "August"):
            mnth = 8;
        if (ent == "September"):
            mnth = 9;
        if (ent == "October"):
            mnth = 10;
        if (ent == "November"):
            mnth = 11;
        if (ent == "December"):
            mnth = 12;

        if (mnth != 0): # calendar entry?

            if (pmnth != mnth): # new section
                pmnth = mnth
            res = re.sub(r'[^\x00-\x7f]',r'', ent)

            if (len(res) > 0 and res not in months): # not 'month' then entry

                #day = re.sub(r'[^\x00-\x7f]',r'', res)

                #ientries[mnth - 1].append(int(day))
                dstr = re.search('^[0-9]*', res).group(0)
                #print (day, int(dstr))
                #dent = {'day': int(dstr), 'event': res}
                dent = {'mnth': mnth, 'event': res}
                #print (dent)
                ientries[months[mnth -1]].append(dent)
                entries.append(dent)
                #entries.append(f'[{mnth}: {res}]')
                #print (mnth, res)
            if (len(res) == 0): # end of section
                mnth  = 0
            #print (mnth, res)
        
    '''
    jdict = {"mnth": []}
    for ient in ientries[months[mnth - 1]]:
        # copy
        for tmp in ient:
            print ("ient", tmp)
            jdict["mnth"].append(ient)
    '''

    #print (ientries[months[5]])
    #entries.sort#()
    #print (entries)

    ment = []

    # crude sort
    for day in range(1, 31):
        for ent in entries:
            if (ent['mnth'] == curmnth): # this month
                # extract the day
                str = ent['event']
                dstr = re.search('^[0-9]*', str).group(0)
                # past event?
                if (int(dstr) >= curday and int(dstr) == day):
                    ment.append(ent['event']) # add to list of events
    #print (entries)
    return(ment)

# end getCowes()

if __name__ == "__main__":
    dstr = getCCYC()
    print (dstr)
