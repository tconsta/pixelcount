from PIL import Image
from io import BytesIO
from base64 import b64encode


def process_image(img_b, color_hex=None, precision=80):
    """Counts black, white, and specified color pixels and mask them on the image.
    Args:
        img_b (bytes): image to process
        color_hex (str): color in hex format
        precision (int): color comparison precision
    Returns:
        bytes: processed image with masked pixels,
        dict: {'blacks': str,
               'whites': str,
               'colored': str}
    """
    MAX_ERROR = 20
    MAX_PRECISION = 100

    error = (MAX_PRECISION - precision) * MAX_ERROR / 100

    black_rgb = (0, 0, 0)
    white_rgb = (255, 255, 255)

    if color_hex:
        color_rgb = tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))

    red_rgb = (255, 0, 0)       # highlight black
    blue_rgb = (0, 0, 255)      # highlight white
    green_rgb = (0, 255, 0)     # highlight user specified color

    # color counts
    blacks = whites = colored = 0

    img = Image.open(BytesIO(img_b)).convert("RGB")
    pixdata = img.load()
    width, height = img.size

    # Count and mask
    for y in range(height):
        for x in range(width):
            if color_hex and \
                 (abs(pixdata[x, y][0] - color_rgb[0]) <= error and
                  abs(pixdata[x, y][1] - color_rgb[1]) <= error and
                  abs(pixdata[x, y][2] - color_rgb[2]) <= error):
                pixdata[x, y] = green_rgb
                colored += 1
            elif (abs(pixdata[x, y][0] - black_rgb[0]) <= error and
                  abs(pixdata[x, y][1] - black_rgb[1]) <= error and
                  abs(pixdata[x, y][2] - black_rgb[2]) <= error):
                pixdata[x, y] = red_rgb
                blacks += 1
            elif (abs(pixdata[x, y][0] - white_rgb[0]) <= error and
                  abs(pixdata[x, y][1] - white_rgb[1]) <= error and
                  abs(pixdata[x, y][2] - white_rgb[2]) <= error):
                pixdata[x, y] = blue_rgb
                whites += 1

    img_io = BytesIO()
    img.save(img_io, format='PNG')
    # Return bytes containing the entire contents of the buffer
    new_img_b = img_io.getvalue()

    counts = {'blacks': f'{blacks} ({blacks/(width * height)*100:.1f}%)',
              'whites': f'{whites} ({whites/(width * height)*100:.1f}%)',
              'colored': f'{colored} ({colored/(width * height)*100:.1f}%)'}

    return new_img_b, counts


def img_to_datauri(img):
    """Convert image to data URI ACSII text
    Args:
        img (bytes): image
    Returns:
        str: data: URI - data:image/jpeg;base64
    """
    # b64encode - Encode the bytes-like objects and return the encoded bytes
    # bytes.decode(encoding="utf-8") - Return a string
    data = b64encode(img).decode()
    mime = 'image/jpeg;'
    datauri = "data:%sbase64,%s" % (mime, data)
    return datauri
