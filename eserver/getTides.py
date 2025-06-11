#
# demo code for the wordpress mec rest api
# this now works with the shortcode apis
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

import requests
from lxml import html
import initServer

# tide url & init tides
tideurl = 'https://thamestides.org.uk/dailytides2.php?statcode=PUT&startdate=0'
tides = []

class PTides:
    
    def loadTides(self):
        global tideurl, tides

        norows = 4
        nocols = 5

        #print (len(tides))
        if (len(tides) == 0): # then initialise
            for j in range(4, 4 + 4): # should be 4 - 8
                column = []
                for i in range(1, 1 + 5):
                    column.append("")
                tides.append(column)
        # now initialised
        #print (len(tides))

        # added to address latest failure
        try:
            tidepage = requests.get(tideurl)
            tree = html.fromstring(tidepage.content)
        except Exception as e:
            return tides


        # now parse the table into the array - note doesn't error
        for row in range (4, 4 + 4):
            for col in range(1, 1 + 5):
                # returns a list of text items
                tide = tree.xpath('//table[@class="first"]//tr['
                            + str(row) + ']//td[' + str(col) + ']//text()')
                if (len(tide) > 0):
                    tides[row-4][col-1] = initServer.PInitServer().removeNonAscii(tide[0])
                else:
                    tides[row-4][col-1] = ""
                #print ("tides ", str(row), str(col), tides[row-4][col-1])
            # end for
        # end for

        return (tides)
    # end loadTides()
