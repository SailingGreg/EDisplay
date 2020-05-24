
# pla flow - redundant
import requests
from lxml import html

plaflow = ""
placfm = 'http://www.pla.co.uk/templates/widgets/trafficWidget.cfm'

class PFlow:
    def loadFlow(self):
        global plaflow, placfm

        page = requests.get(placfm)
        # check page.status_code

        tree = html.fromstring(page.content)
        pla = tree.xpath('//span[@class="warningTitle"]//text()')
        
        if (len(pla) > 0): # then we have a list
            return pla[0]
        else:
            return ""
# end loadFlow
