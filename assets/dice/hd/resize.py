from os import listdir
from os.path import isfile, join
from PIL import Image

a = [f for f in listdir("./") if isfile(join("./", f))]
a.remove("resize.py")

for file in a:
    img = Image.open(file)
    img.thumbnail([128,128], Image.ANTIALIAS)
    img.save(file)
