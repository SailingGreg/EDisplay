#
# demo code for the wordpress mec rest api
#
#

import requests
import datetime
import dateutil.relativedelta

#
# get the wordpress posts
#
class PPosts:
    def loadPosts (self):
        # The main access url for the wordpress post api
        postsurl = "https://ranelaghsc.co.uk/wp-json/wp/v2/posts"

        # note the current date & calc the date for the last month
        tnow = datetime.datetime.now()
        ptime = tnow - dateutil.relativedelta.relativedelta(months=1)
        tquery = ptime.isoformat()

        # do the request - limted to '5'
        reqstr = postsurl + "?per_page=5&order=desc&after=" + tquery
        req = requests.get(reqstr)

        #jdict = req.json()
        #noPost = len(req.json())

        return (req.json())
        # end

# end of file
