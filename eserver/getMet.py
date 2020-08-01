#
# code to parse the pla status page for the flow
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


from lxml import html
import requests
import initServer
#
# load predictions from the met office datahub
#
meturl = "https://api-metoffice.apiconnect.ibmcloud.com"
headers=""
#headers = {
    #}
metreq = "/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=false&latitude=51.469&longitude=-0.2199"
class PMet:

    oldrdict = []
    oldtimeseries = []

    def getMet (self):
        global headers

        # set the headers based on the inject keys
        if (headers == ""):
            headers = {
            'x-ibm-client-id': initServer.met_id,
            'x-ibm-client-secret': initServer.met_key,
            'accept': "application/json"
        }

        try:
            req = requests.get(meturl + metreq, headers=headers)
            #print (req.status_code)

            #rgeo = geojson(req.text)
            rdict = req.json()
            self.oldrdict = rdict
        except Exception as e:
            rdict = self.oldrdict

        # guard for truncated rdict
        try:
            for feature in rdict['features']:
                #print ("Loop: ", x)
                #print (feature['type'])
                #print (feature['geometry']['type'])
                #print (feature['geometry']['coordinates'])
                #print (feature['properties']['requestPointDistance'])
                #print (feature['properties']['modelRunDate'])
                timeseries = feature['properties']['timeSeries']
                self.oldtimeseries = timeseries
        except Exception as e:
            timeseries = self.oldtimeseries
            print (req.status_code)
            print (rdict)

        # return timeseries dict
        return (timeseries)
        #end
# end of file
