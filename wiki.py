import wikipedia
import matplotlib.pyplot as plt
import cv2 as cv


wikipedia.set_lang("ru")
page = wikipedia.page("КНДР")
url = page.images[0]

from urllib.request import urlopen
from PIL import Image

img = Image.open(urlopen(url))
plt.imshow(img)
plt.show()