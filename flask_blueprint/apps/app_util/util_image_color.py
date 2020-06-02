import os.path
from PIL import Image


def get_img_dir() -> str:
    '''
    Return the full path to the image directory

    :return: string
    '''
    pkg_dir = os.path.dirname(__file__)
    img_dir = os.path.join(pkg_dir, '..', 'static/images')
    return img_dir


def open_img(img_name: str) -> Image:
    '''
    Open the given file form the image directory

    :param img_name: Name including extension of the image
    :return: Image object
    '''
    img_dir = get_img_dir()
    full_img_path = os.path.join(img_dir, img_name)
    return Image.open(full_img_path)


def save_img(img: Image, img_name: str):
    '''
    Save the given image to the image directory

    :param img: Image object
    :param img_name: Name including the extension of the image
    '''
    img_dir = get_img_dir()
    full_img_path = os.path.join(img_dir, img_name)
    img.save(full_img_path)


def overlay(img: Image, overlay_color: tuple):
    '''
    Place an overlay over an existing image

    :param img: Image opened with PIL.Image
    :param overlay_color: four-tuple with color to add to your image
    '''
    assert len(overlay_color) == 4, 'Overlay color shall be a 4-tuple'

    img_overlay = Image.new(size=img.size, color=overlay_color, mode='RGBA')
    img.paste(img_overlay, None, mask=img_overlay)

    color_string = '_'.join([str(c) for c in overlay_color])
    filename = 'amsterdam_{color}.png'.format(color=color_string)
    save_img(img, filename)
rgb(196, 199, 203)

if __name__ == '__main__':
    i = open_img('chart_threed_liel_0.png')
    rgba = (196, 199, 203, 128)   #, 128)  rgb(196, 199, 203)
    overlay(i, rgba)

    overlay(open_img('chart_threed_liel_0.png'), (196, 199, 203, 128))


"""

To create an image from a file...
image = Image.open(filepath)


To create an image from scratch...
width = 400
height = 300
Image.new('RGBA', (width, height))


For easy and direct pixel editing...
Images have different palette modes. If the image has a palette, setting arbitrary RGBA values becomes a bit tricky. It's best to just convert it to an RGB or RGBA image...
if image.mode != 'RGBA':
    image = image.convert('RGBA')

Change 'RGBA' to 'RGB' if you don't care about alpha.

To get the color of a pixel...
pixels = image.load()
color = pixels[4, 5] # x = 4, y = 5 (0-indexed, of course)

This will return a tuple containing 3 numbers for RGB images and 4 for RGBA images.
For example, this would be non-translucent red: (255, 0, 0, 255)
As the palette mode name implies, the order is R, G, B, A.

To set the color of a pixel...
The pixels array mentioned above is also writable:
pixels[4, 5] = (128, 0, 128, 255) # purple


To get the width/height of an image...
width = image.size[0]
height = image.size[1]


To save an image to file...
image.save(filepath)








PIL.ImageColor.getrgb(color)


im = Image.open('freljord2.png')
#one_pixel = im.getpixel((0, 0))
#one_pixel[1] = 0;
#im.save('freljord3.png')


(0, 0, 0, 0)
for x in range(0):
for y in range(0):
    im.putpixel((x, y), (210, 210, 210))
for x in range(560):
    for y in range(557):
    print("hi")
    hello = ImageColor.get(00B200)
    im.putpixel((x, y), )
im.getpixel((0, 0))
(210, 210, 210, 255)
im.getpixel((0, 50))
(169, 169, 169, 255)
im.save('freljord2.png')




import Image
import numpy as np

im = Image.open('snapshot.jpg')

# In this case, it's a 3-band (red, green, blue) image
# so we'll unpack the bands into 3 separate 2D arrays.
r, g, b = np.array(im).T

# Let's make an alpha (transparency) band based on where blue is < 100
a = np.zeros_like(b)
a[b < 100] = 255

# Random math... This isn't meant to look good...
# Keep in mind that these are unsigned 8-bit integers, and will overflow.
# You may want to convert to floats for some calculations.
r = (b + g) * 5

# Put things back together and save the result...
im = Image.fromarray(np.dstack([item.T for item in (r,g,b,a)]))

im.save('output.png')



import cv2
    import numpy as np
    from PIL import ImageGrab

    out = cv2.VideoWriter('record.avi', 2, 8.0, (1366, 768))
    while (True):
       img = ImageGrab.grab(bbox=(0, 0, 1366, 768)) # x, y, w, h
       img_np = np.array(img)
       frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
       out.write(img_np)
       cv2.imshow("Recorder", frame)
       key = cv2.waitKey(1)
       if key == 27:
          break
    cv2.waitKey(0)
    cv2.destroyAllWindows()

RGB_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
vid.write(RGB_img)
"""
