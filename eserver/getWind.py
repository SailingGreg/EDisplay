import requests
import logging
from PIL import Image

LOC = "/home/pi/EDisplay/eserver/"

winddomain = "https://wind.ranelaghsc.co.uk/"
windurl = winddomain + "daywind.png"
winddirurl = winddomain + "daywinddir.png"
#
# loadWind from website - ignore if connectivity error
class PWind:

    def loadWind (self):
        try:
            rs = requests.get(windurl, allow_redirects=True)
            open(LOC + './tmp/daywind-copy.png', 'wb').write(rs.content)
        except Exception as e:
            logging.error("loadWind(): daywind",  exc_info=True)
            return

        try:
            rs2 = requests.get(winddirurl, allow_redirects=True)
            open(LOC + './tmp/daywinddir-copy.png', 'wb').write(rs2.content)
        except Exception as e:
            logging.error("loadWind(): daywinddir",  exc_info=True)
            return

        try:
            file_in = LOC + "./tmp/daywind"
            img = Image.open(file_in + "-copy.png")
            #img2 = img.convert("1")
            img2 = img.convert("LA")
            img2.save(file_in + ".png")
        except Exception as e:
            logging.error("loadWind(): convert daywind",  exc_info=True)
            return

        try:
            file_in = LOC + "./tmp/daywinddir"
            img = Image.open(file_in + "-copy.png")
            img2 = img.convert("1")
            img2.save(file_in + ".png")
        except Exception as e:
            logging.error("loadWind(): convert daywinddir",  exc_info=True)
            return

    # end loadWind()
