
# extract flow from EA service - this is the source for PLA figures
# flow is measured in m3/sec

import requests
import logging

eauk = 'https://environment.data.gov.uk/flood-monitoring/id/stations/3400TH/readings?latest'
flowtext = ""
class PEaukFlow:

    def eaukFlow(self):
        global flowtext

        try:
            page = requests.get(eauk)
        except Exception as e:
            logging.error("eaukFlow(): requets()",  exc_info=True)
            return flowtext

        if (page.status_code != 200):
            logging.error("eauk return not 200")
            return flowtext

        # has content, meta and items
        tree = page.json()
        #print (len(tree))
        #print (tree)

        # items has level and flow
        level = tree["items"][0]
        flow = tree["items"][1]

        flowval = int(flow["value"])

        # removed > 0 so it covers the negative flow situation
        if (flowval <= 20):
            flowtext = "Low"
        elif (flowval > 20 and flowval <= 150):
            flowtext = "Average"
        elif (flowval > 150 and flowval <= 300):
            flowtext = "Strong"
        else:
            flowtext = "Very strong"

        flowtext = flowtext + " fluvial flows"

        return flowtext
# end eaukFlow
