from PIL import Image

IMG = "hub/static/img/ben.jpg"
SCALE = 1.5

foo = Image.open(IMG)

WIDTH_SCALED = foo.width / int(SCALE)
HEIGHT_SCALED = foo.height / int(SCALE)

foo = foo.resize((int(WIDTH_SCALED), int(HEIGHT_SCALED)), Image.ANTIALIAS)
foo.save("hub/static/img/optimized/ben_scaled.jpg", quality=95)

foo.save("hub/static/img/optimized/ben_optimized.jpg", optimize=True, quality=95)
