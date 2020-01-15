from inky import InkyWHAT as Ink
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import socket

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
    hostname = socket.getfqdn()
    myIp = socket.gethostbyname(hostname)
except:
    myIp = 'Unknown'

draw.text((10, 283), myIp, inkR.BLACK, font)



inkR.set_image(im)
inkR.show()
