from PIL import Image
import pytesseract
import cv2


def imag():

    image = Image.open('src/images/original.jpg')
    w1, h1 = image.size
    if h1 > 500:
        image = image.resize((round(w1 / 5), round(h1 / 5)))

    else:
        pass
    w1, h1 = image.size



    pix = image.load()
    av = 0

    for x in range(h1):
        for y in range(w1):
            av += sum(pix[y, x])

    av /= w1 * h1 * 3

    for x in range(h1):
        for y in range(w1):
            if sum(pix[y, x]) / 3 >= av * 5/6:
                image.putpixel((y, x), (255, 255, 255))
            else:
                image.putpixel((y, x), (0, 0, 0))





    image.save('src/images/black_white.jpg')

    image = Image.open('src/images/black_white.jpg')

    string = pytesseract.image_to_string(image, config = r'--oem 3 --psm 6')



    image = cv2.imread('src/images/black_white.jpg')

    data = pytesseract.image_to_data(image, config = r'--oem 3 --psm 6')

    maxx = 0
    maxy = 0

    minx = 9999
    miny = 9999


    for i, el in enumerate(data.splitlines()):
        if i == 0:
            continue

        el = el.split()

        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])

        # cv2.rectangle(image, (x, y), (w + x, h + y), (0, 0, 255), 1)


        if x < minx and x > 20:
            minx = x
        if y < miny and y > 20:
            miny = y

        if x + w > maxx and x + w < w1 - 20:
            maxx = x + w
        if y + h > maxy and y + h < h1 - 20:
            maxy = y + h

    if miny == 9999:
        miny = 0
    if minx == 9999:
        minx = 0






    cv2.imwrite('src/images/rectangled.jpg', image)

    image = image[abs(miny-5):maxy+5, abs(minx-5):maxx+5]
    try:
        string = pytesseract.image_to_string(image, config = r'--oem 3 --psm 6')
        cv2.imwrite('src/images/cropped.jpg', image)
    except:
        pass


    image1 = cv2.imread('src/images/rectangled.jpg')

    for i, el in enumerate(data.splitlines()):
        if i == 0:
            continue

        el = el.split()

        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])

        cv2.rectangle(image1, (x, y), (w + x, h + y), (0, 0, 255), 1)
    cv2.imwrite('src/images/rectangled.jpg', image1)




    return string
