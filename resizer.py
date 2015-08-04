import PIL, configparser
from PIL import Image

config = configparser.ConfigParser()
config.read('config.cf')

img = Image.open(config["Resizer"]["path"])
height = int(config["Resizer"]["height"])
width = int(img.size[0] * (height / img.size[1]))
img = img.resize((width, height), PIL.Image.ANTIALIAS)
img.save(config["Resizer"]["path"])