from PIL import Image
from io import BytesIO
from base64 import b64encode


def process_image(img_b, color_hex=None):
    """Counts black, white, and specified color pixels and mask them on the image.
    Args:
        img_b (bytes): image to process
        hex_color (str): color in hex format
    Returns:
        bytes: processed image with masked pixels,
        dict: {'blacks': str,
               'whites': str,
               'colored': str}
    """
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
            if color_hex and pixdata[x, y] == color_rgb:
                pixdata[x, y] = green_rgb
                colored += 1
            elif pixdata[x, y] == black_rgb:
                pixdata[x, y] = red_rgb
                blacks += 1
            elif pixdata[x, y] == white_rgb:
                pixdata[x, y] = blue_rgb
                whites += 1

    # Debug:
    # img.save('debug.jpg')

    img_io = BytesIO()
    img.save(img_io, format='PNG')
    # Return bytes containing the entire contents of the buffer
    new_img_b = img_io.getvalue()

    counts = {'blacks': f'{blacks} ({blacks/(width * height)*100:.1f}%)',
              'whites': f'{whites} ({whites/(width * height)*100:.1f}%)',
              'colored': f'{colored} ({colored/(width * height)*100:.1f}%)'}

    return new_img_b, counts


def img_to_datauri(img):

    # b64encode - Encode the bytes-like objects and return the encoded bytes
    # bytes.decode(encoding="utf-8") - Return a string
    data = b64encode(img).decode()
    mime = 'image/jpeg;'
    datauri = "data:%sbase64,%s" % (mime, data)
    return datauri
