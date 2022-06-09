from PIL import Image
import sys

def get_brightness(rgb: tuple) -> int:
    '''
    Gets brightness value from RGB tuple based on type value.
    Here the relative luminance formula is used.

    params: (tuple) rgb, three-tuple
    returns: (int)brightness value
    '''

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    return int((0.21 * r) + (0.71 * g) + (0.07 * b))



def rgb_to_chars(image: Image, type=None) -> None:
    '''
    Converts the values of the pixels matrix from RGB tuples to the corresponding ASCII character.
    The ASCII character depends on the brightness value of the pixel.
    Brightness formula is defined in get_brightness() function.

    params:
        (list) pixels

        optional:
            (str) type, how pixels should be printed.
                None       - white characters with a black background.
                "inverted" - black characters with a white background.
    returns: 
        None
    '''

    # these are the ASCII characters used in the drawing, from thinnest to boldest.
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    # if type is inverted, ASCII characters are used from boldest to thinnest
    if (type == "inverted"):
        ascii_chars = ascii_chars[::-1]

    # max_brightness depends on the brightness formula.
    max_brightness = 253

    # see here: https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.getdata
    pixels = list(image.getdata())

    for x in range(len(pixels)):
        # at the end of each row, go to next line
        if (x % im_width == 0):
            print()

        rgb = pixels[x]
        brightness = get_brightness(rgb)
        char_index = (brightness * len(ascii_chars)) // max_brightness

        # print each char multiple times to make image less squashed.
        for i in range(3):
            print(ascii_chars[char_index], end="")


if (__name__ == "__main__"):
    try:
        filepath = str(sys.argv[1])
        im = Image.open(filepath)

        # if image is too wide, resize it.
        # the max width of 300px was obtained through trial-and-error
        MAX_WIDTH = 300
        if (im.size[0] > MAX_WIDTH):
            height_width_ratio = im.size[1] / im.size[0]
            im = im.resize((MAX_WIDTH, int(MAX_WIDTH * height_width_ratio)))

        im_width = im.size[0]
        im_height = im.size[1]

        print("Succesfully imported image!")
        print("Image Size: " , im_width, "X", im_height)
    except:
        raise Exception("Failed to import image!")

    rgb_to_chars(im, "inverted")


