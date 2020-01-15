from inky import InkyWHAT as Ink
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import socket
import feedparser

# TODO: Make a config file, or use environment config, or something..
feedUrl = 'http://rss.slashdot.org/Slashdot/slashdotMain'

rssData = feedparser.parse(feedUrl)

inkR = Ink('red')

# im = Image.new('P', (inkR.WIDTH, inkR.HEIGHT))
im = Image.open('./layout.png')
draw = ImageDraw.Draw(im)

now = datetime.now()
prettyTime = now.strftime('%a, %b %d %I:%M %p')
font = ImageFont.load_default()
draw.text((262, 283), prettyTime, inkR.BLACK, font)

myIp = 'Unknown'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.1", 80))
    myIp = s.getsockname()[0]
    s.close()
except:
    myIp = 'Unknown'

draw.text((10, 283), myIp, inkR.BLACK, font)

# Right column
# Origin (208, 12) for right column
feedTitle = rssData['feed']['title']
draw.text((208, 12), feedTitle, inkR.BLACK, font)
i = 32
for post in rssData.entries:
    # TODO: If time+1h > now THEN red ELSE black
    draw.text((208, i,), entries[post]['title'], inkR.BLACK, font)
    i = i + 12



inkR.set_image(im)
inkR.show()
