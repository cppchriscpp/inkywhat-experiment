from inky import InkyWHAT as Ink
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import socket
import feedparser
import config

from geopy.geocoders import Nominatim
from darksky.api import DarkSky
from darksky.types import languages, units, weather

geolocator = Nominatim(user_agent='inkyWhat screen display toy')



feedUrl = config.rssFeedUrl

rssData = feedparser.parse(feedUrl)
panelWidth = 180
maxArticles = 6

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
titleW, titleH = font.getsize(feedTitle)
left = round((panelWidth - titleW) / 2)
if (left < 0):
    left = 0
draw.text((208 + left, 12), feedTitle, inkR.BLACK, font)
i = 32
totalArticles = 0
for post in rssData.entries:
    splutTitle = post['title'].split(' ')
    splutTitle.reverse()
    titleL1 = ''
    titleL2 = ''
    titleL3 = ''

    # TODO: Probably should make this a function or something..
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

    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titleL3
        titleL3 = titleL3 + ' ' + theWord
        w, h = titleFont.getsize(titleL3)
        if w > panelWidth:
            splutTitle.append(theWord)
            titleL3 = before
            break




    # TODO: If time+1h > now THEN red ELSE black
    draw.text((208, i), titleL1, inkR.BLACK, titleFont)
    i = i + 10
    draw.text((208, i), titleL2, inkR.BLACK, titleFont)
    i = i + 10
    draw.text((208, i), titleL3, inkR.BLACK, titleFont)
    i = i + 18

    totalArticles = totalArticles + 1
    if totalArticles >= maxArticles:
        break


# Left column, weather
darksky = DarkSky(config.darkskyApiKey)
location = geolocator.geocode(config.weatherLocation)

forecast = darksky.get_forecast(location.latitude, location.longitude)

wtitle = 'Weather'
titleW, titleH = font.getsize(wtitle)
left = round((panelWidth - titleW) / 2)

draw.text((12 + left, 12), wtitle, inkR.BLACK, font)

draw.text((12, 32), "Currently: " + forecast.currently.summary, inkR.BLACK, font)
draw.text((12, 44), 'Temperature: ' +  str(forecast.currently.temperature) + '°f', inkR.BLACK, font)
if len(forecast.alerts) > 0:
    draw.text((12, 56), forecast.alerts[0].title, inkR.RED, font)

try:
    # TODO: Icons look kind of bad/not visible... find better ones or figure out a better way to convert.
    icon = Image.open('DarkSky-icons/PNG/' + forecast.currently.icon + '.png').resize((64, 64)).convert('1')
    im.paste(icon, (48, 76))
except Exception as e:
    print('Unable to load icon... leaving blank. ' + str(e))

inkR.set_image(im)
inkR.show()
