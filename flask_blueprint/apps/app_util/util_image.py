import os, sys
from PIL import Image
from PIL import ImageEnhance
import argparse
import ntpath

WIDTH = 30
RATIO = 1.5
HEIGHT = int(WIDTH/RATIO)
SIZE = (WIDTH, HEIGHT)
SIZE = (25, 16)    # eu (26,17) , (128, 128) for thumbnail

DEST_DIR = '/static/images/maps/flags_small/'


def resize(src, dest=None, size=None):
    """ maintain ratio
    basewidth = 300
    img = Image.open('somepic.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    """
    inpathfile = src

    if not size:
        size = SIZE

    if dest:
        outpathfile = dest
    else:
        infilepath, infilename = os.path.split(inpathfile)
        outfilename = os.path.splitext(infilename)[0] + '_icon.png'
        outpathfile = os.path.join(DEST_DIR, outfilename)

    try:
      im = Image.open(inpathfile)
      print(im.format, "%dx%d" % im.size, im.mode)  # PNG 30x19 RGB
      print('OUT size: ',size)
      #im.thumbnail(size)
      im = im.resize(size, Image.ANTIALIAS)
      im.save(outpathfile)
    except IOError:
      print("Error opening image - cannot create thumbnail for", inpathfile)


def convert_jpg():
  for infile in sys.argv[1:]:
      f, e = os.path.splitext(infile)
      outfile = f + ".jpg"
      if infile != outfile:
          try:
              Image.open(infile).save(outfile)
          except IOError:
              print("cannot convert", infile)


def darken_lighten():
    im_orig = Image.open("background_castle_fantasy.jpg")
    im_mod = im_orig.point(lambda p: p * 0.8)
    im_mod.save("background_castle_fantasy1.jpg")
    enhancer = ImageEnhance.Brightness(im_orig)

    # factor 1.0 always returns a copy of the original image
    # lower factors mean darker, and higher values brighter
    for k in range(1, 9):
        factor = k / 4.0
        print(factor),  # 0.25 0.5 0.75 1.0 1.25 1.5 1.75 2.0
        img_enhanced = enhancer.enhance(factor)
        # safe images as Audi_bright025.jpg to Audi_bright200.jpg
        # to the working directory
        img_enhanced.save("Audi_bright%03d.jpg" % (int(factor*100)) )


def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])


def filter():
    try:
      original = Image.open("Lenna.png")

      filtered_blurred = original.filter(ImageFilter.BLUR)
      filtered_contour = original.filter(ImageFilter.CONTOUR)

      # Display both images
      original.show()
      filtered_blurred.show()

      filtered_blurred.save("filtered_blurred.png")
    except:
      print("Unable to load image")


#>>> img2 = img.crop((80, 80, 520, 520))
#>>> img2.show()


def to_favicon(path_filename):
    """
    NOTE: original image needs to be square

    cd where this util_image.py is located
    $ cd ~/Agape/development/projects/fintech/flask_blueprint/apps/app_util
    (venv3) $ p3
    >>> import util_image
    >>> util_image.to_favicon('/Users/acrosspond/Agape/development/assets/tribal/hex5.png')
    """
    im = Image.open(path_filename)
    # im.size

    #os.path.splitext('/path/to/somefile.ext')
    path, filename = os.path.split(path_filename)
    #filename = os.path.basename(path_filename)
    filename_noext = os.path.splitext(filename)[0]

    icon_sizes = [(16,16), (32, 32), (48, 48), (64,64)]
    # im.save(ico, sizes=icon_sizes)
    for size in icon_sizes:
        #im.save(ico, sizes=icon_sizes)
        im2 = im.resize(size, Image.ANTIALIAS)
        ico_path_name = os.path.join(path, filename_noext + '_' + str(size[0]) + '.ico')
        #im2.save("hex5_16.ico")
        im2.save(ico_path_name)


if __name__ == "__main__":
    """ Usage:
    $ cd ~/projects/kiklearn/flask_blueprint/apps/app_util

    $ python3 util_image.py /static/images/maps/flags_big/ru.png
    $ python3 util_image.py /static/images/maps/flags_wik/200px-Flag_of_Ireland.svg.png -dest /static/images/maps/flags_small/ie_icon.png

    $ python3 ~/projects/kiklearn/flask_blueprint/apps/app_util/util_image.py /static/images/maps/flags_med/ru.png

    Ex/
    $ ~/projects/backup/backup.py -log rivercast pwd

    $ ~/projects/backup/backup.py -log target_file pwd
    $ ~/projects/backup/backup.py -log ~target_file pwd
    $ ~/projects/backup/backup.py -log target_dir/ pwd
    $ ~/projects/backup/backup.py -log ~target_dir/ pwd

    Ex/ nargs='?' means 0-or-1 arguments
        const=1 sets the default when there are 0 arguments
        type=int converts the argument to int
    parser = argparse.ArgumentParser()
    parser.add_argument('--example', nargs='?', const=1, type=int)
    args = parser.parse_args()

    parser.add_argument("thisismandatoryandinthisorder")
    parser.add_argument("-optionalandanyorder")
    parser.add_argument('-optional-butifexistwillbecow-cannotoverride', action='store_const', const='cow')
    parser.add_argument('-optional-defaultifnotexist-canoverride', '--src', default='cow')
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    parser.add_argument('-dest', '--dest', default=None)
    parser.add_argument('-size', '--size', default=None, nargs=2, type=int)
    parser.add_argument('-log','--log', action='store_true')  #, default=os.getcwd())
    # parser.add_argument('log', nargs='?')  #, default=os.getcwd())

    args = parser.parse_args()

    resize(args.src, args.dest, args.size)
