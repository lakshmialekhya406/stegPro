from PIL import Image
import sys

image = Image.open(sys.argv[1])
path = "C:\\Users\\dell\\Downloads" + "-enc.png"

image.save(path)