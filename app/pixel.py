from PIL import Image


def process_image():

    black_rgb = (0, 0, 0)
    white_rgb = (255, 255, 255)

    color_rgb = (1, 2, 3)

    red_rgb = (255, 0, 0)       # highlight black
    blue_rgb = (0, 0, 255)      # highlight white
    green_rgb = (0, 255, 0)     # highlight user specified color

    # color counts
    blacks = whites = colored = 0

    img = Image.open('/home/tconsta/pixelcount/app/test.jpg').convert("RGB")
    pixdata = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            if  pixdata[x, y] == color_rgb:
                pixdata[x, y] = green_rgb
                colored += 1
            elif pixdata[x, y] == black_rgb:
                pixdata[x, y] = red_rgb
                blacks += 1
            elif pixdata[x, y] == white_rgb:
                pixdata[x, y] = blue_rgb
                whites += 1

    img.save('result.jpg')


if __name__ =='__main__':

    process_image()
