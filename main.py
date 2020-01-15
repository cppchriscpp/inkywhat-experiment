from inky import InkyWHAT as Ink
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import socket
import feedparser

# TODO: Make a config file, or use environment config, or something..
feedUrl = 'http://rss.slashdot.org/Slashdot/slashdotMain'

rssData = feedparser.parse(feedUrl)
panelWidth = 180

inkR = Ink('red')

# im = Image.new('P', (inkR.WIDTH, inkR.HEIGHT))
im = Image.open('./layout.png')
draw = ImageDraw.Draw(im)

now = datetime.now()
prettyTime = now.strftime('%a, %b %d %I:%M %p')
font = ImageFont.load_default()
titleFont = font
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
totalArticles = 0
for post in rssData.entries:
    splutTitle = post['title'].split(' ').reverse()
    titleL1 = ''
    titleL2 = ''
    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titleL1
        titleL1 = titleL1 + ' ' + theWord
        w, h = titleFont.getsize(titleL1)
        if w > panelWidth:
            splutTitle.append(theWord)
            titleL1 = before
            break
    
    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titleL2
        titleL2 = titleL2 + ' ' + theWord
        w, h = titleFont.getsize(titleL2)
        if w > panelWidth:
            splutTitle.append(theWord)
            titleL2 = before
            break


    # TODO: If time+1h > now THEN red ELSE black
    draw.text((208, i), titleL1, inkR.BLACK, titleFont)
    i = i + 10
    draw.text((208, i), titleL2, inkR.BLACK, titleFont)
    i = i + 18

    totalArticles = totalArticles + 1
    if totalArticles > 6:
        break



inkR.set_image(im)
inkR.show()
