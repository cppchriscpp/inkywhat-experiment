from inky import InkyWHAT as Ink
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from dateutil import parser
import socket
import feedparser
import config

from geopy.geocoders import Nominatim
from darksky.api import DarkSky
from darksky.types import languages, units, weather

geolocator = Nominatim(user_agent='inkyWhat screen display toy')



feedUrl = config.rssFeedUrl
feed2Url = config.rssFeed2Url

rssData = feedparser.parse(feedUrl)
rssData2 = feedparser.parse(feed2Url)
panelWidth = 180
maxArticles = 6

inkR = Ink('red')

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
feed2Title = config.rssFeed2Name
titleW, titleH = font.getsize(feedTitle)
left = round((panelWidth - titleW) / 2)
if (left < 0):
    left = 0
draw.text((208 + left, 12), feedTitle, inkR.BLACK, font)
i = 32
totalArticles = 0
titleW, titleH = font.getsize(feed2Title)
left = round((panelWidth - titleW) / 2)
if (left < 0):
    left = 0
draw.text((12 + left, 120), feed2Title, inkR.BLACK, font)
for post in rssData.entries:
    splutTitle = post['title'].split(' ')
    splutTitle.reverse()
    titlebL1 = ''
    titlebL2 = ''
    titlebL3 = ''

    thisDate = parser.parse(post['date'])
    thisColor = inkR.BLACK
    if (datetime.now(thisDate.tzinfo)-timedelta(hours=1) <= thisDate):
        thisColor = inkR.RED

    # TODO: Probably should make this a function or something..
    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titlebL1
        titlebL1 = titlebL1 + ' ' + theWord
        w, h = titleFont.getsize(titlebL1)
        if w > panelWidth:
            splutTitle.append(theWord)
            titlebL1 = before
            break
    
    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titlebL2
        titlebL2 = titlebL2 + ' ' + theWord
        w, h = titleFont.getsize(titlebL2)
        if w > panelWidth:
            splutTitle.append(theWord)
            titlebL2 = before
            break

    while len(splutTitle) > 0:
        theWord = splutTitle.pop()
        before = titlebL3
        titlebL3 = titlebL3 + ' ' + theWord
        w, h = titleFont.getsize(titlebL3)
        if w > panelWidth:
            splutTitle.append(theWord)
            titlebL3 = before
            break




    draw.text((208, i), titlebL1, thisColor, titleFont)
    i = i + 10
    draw.text((208, i), titlebL2, thisColor, titleFont)
    i = i + 10
    draw.text((208, i), titlebL3, thisColor, titleFont)
    i = i + 18

    totalArticles = totalArticles + 1
    if totalArticles >= maxArticles:
        break

j = 134
totalArticles = 0
for post in rssData2.entries:
    print('got here ' + str(i))
    print(post['title'])

    splutTitle = post['title'].split(' ')
    splutTitle.reverse()
    titleL1 = ''
    titleL2 = ''
    titleL3 = ''

    thisDate = parser.parse(post['date'])
    thisColor = inkR.BLACK
    if (datetime.now(thisDate.tzinfo)-timedelta(hours=12) <= thisDate):
        thisColor = inkR.RED

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




    draw.text((12, j), titleL1, thisColor, titleFont)
    j = j + 10
    draw.text((12, j), titleL2, thisColor, titleFont)
    j = j + 10
    draw.text((12, j), titleL3, thisColor, titleFont)
    j = j + 18

    totalArticles = totalArticles + 1
    if totalArticles >= maxArticles:
        break

iconDict = {
    'clear-day': 'Tempestacons-master/converted/day.png', 
    'clear-night': 'Tempestacons-master/converted/day.png', 
    'rain': 'Tempestacons-master/converted/rain.png', 
    'snow': 'Tempestacons-master/converted/snow.png', 
    'sleet': 'Tempestacons-master/converted/mixed-rain-snow.png', 
    'wind': 'Tempestacons-master/converted/wind.png', 
    'fog': 'Tempestacons-master/converted/fog.png', 
    'cloudy': 'Tempestacons-master/converted/cloudy.png', 
    'partly-cloudy-day': 'Tempestacons-master/converted/partly-cloudy.png', 
    'partly-cloudy-night': 'Tempestacons-master/converted/partly-cloudy.png',
    'hail': 'Tempestacons-master/converted/hail.png', 
    'thunderstorm': 'Tempestacons-master/converted/thunderstorms.png',
    'tornado': 'Tempestacons-master/converted/tornado.png'
}


# Left column, weather
darksky = DarkSky(config.darkskyApiKey)
location = geolocator.geocode(config.weatherLocation)

forecast = darksky.get_forecast(location.latitude, location.longitude)

wtitle = 'Weather'
titleW, titleH = font.getsize(wtitle)
left = round((panelWidth - titleW) / 2)

draw.text((12 + left, 12), wtitle, inkR.BLACK, font)

if len(forecast.alerts) > 0:
    draw.text((12, 98), ' ' + forecast.alerts[0].title, inkR.RED, font)

try:
    icon = Image.open(iconDict[forecast.currently.icon])
    im.paste(icon, (164, 8))
except Exception as e:
    print('Unable to load icon... leaving blank. ' + str(e))


forecastTxt = forecast.daily.summary
forecastL1 = ''
forecastL2 = ''
forecastL3 = ''
splutForecast = forecastTxt.split(' ')
splutForecast.reverse()

# TODO: Probably should make this a function or something.. (ESPECIALLY now that I'm doing this two places...)
while len(splutForecast) > 0:
    theWord = splutForecast.pop()
    before = forecastL1
    forecastL1 = forecastL1 + ' ' + theWord
    w, h = titleFont.getsize(forecastL1)
    if w > panelWidth:
        splutForecast.append(theWord)
        forecastL1 = before
        break

while len(splutForecast) > 0:
    theWord = splutForecast.pop()
    before = forecastL2
    forecastL2 = forecastL2 + ' ' + theWord
    w, h = titleFont.getsize(forecastL2)
    if w > panelWidth:
        splutForecast.append(theWord)
        forecastL2 = before
        break

while len(splutForecast) > 0:
    theWord = splutForecast.pop()
    before = forecastL3
    forecastL3 = forecastL3 + ' ' + theWord
    w, h = titleFont.getsize(forecastL3)
    if w > panelWidth:
        splutForecast.append(theWord)
        forecastL3 = before
        break

draw.text((12, 38), forecastL1, inkR.BLACK, font)
draw.text((12, 50), forecastL2, inkR.BLACK, font)
draw.text((12, 62), forecastL3, inkR.BLACK, font)
draw.text((12, 74), ' Temperature: ' +  str(forecast.currently.temperature) + '°f', inkR.BLACK, font)
draw.text((12, 86), ' High: ' + str(forecast.daily.data[0].temperature_high) + '°f  Low: ' + str(forecast.daily.data[0].temperature_low) + '°f', inkR.BLACK, font)

inkR.set_image(im)
inkR.show()
