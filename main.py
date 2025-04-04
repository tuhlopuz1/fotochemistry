import asyncio
import logging
import requests
from lxml import html
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
import pytesseract
import cv2
import os
import os
from dotenv import load_dotenv

load_dotenv()

typess = [
    'металл', 'основной оксид', 'основание', 'соль', 'вода', 'неметалл',
    'кислотный оксид', 'кислота'
]

metalls = [
    'Li', 'Be', 'B', 'Na', 'Mg', 'Al', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn',
    'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Nb', 'Ba', 'Au', 'Hg', 'Pb',
    'Ag', 'Sr', 'Rb', 'Cs', 'Fr', 'Ra', 'In', 'Y', 'Zr', 'Mo', 'Tc', 'Ru', 'Rh',
    'Pd', 'Cd', 'Sn', 'La', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Tl', 'Bi',
    'Po', 'Fr', 'Ra', 'Ac', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt'


]

nometalls = [
    'C', 'N', 'F', 'Ne', 'P', 'S', 'Cl', 'Ar', 'Se', 'Br', 'Kr', 'I', 'Rn', 'Si',
    'O', 'B', 'H', 'P', 'As', 'Se', 'Te', 'At', 'Ne', 'Ar', 'Xe', 'Rn', 'He'
]

valvvs1 = [
    'Li', 'Na', 'K', 'Cu', 'Rb', 'Ag', 'Cs', 'Au', 'Fr', 'Rg', 'F', 'Cl', 'Br',
    'I', 'NO3', 'NO2'
]

valvvs2 = [
    'Be', 'Mg', 'Ca', 'Zn', 'Sr', 'Cd', 'Ba', 'Hg', 'Ra', 'Cn', 'S', 'SO3',
    'SO4', 'SiO', 'CO3'
]

valvvs3 = [
    'B', 'Al', 'Sc', 'Ga', 'Y', 'In',
    'La', 'Ti', 'Ac', 'Nh', 'PO4'
]



ad_ress = [
  'F', 'Cl', 'Br', 'I', 'NO3',
  'S', 'SO3', 'SO4'
]


# функция распознавания текста на фото
def imag():

    image = Image.open('original.jpg')
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





    image.save('black_white.jpg')

    image = Image.open('black_white.jpg')

    string = pytesseract.image_to_string(image, config = r'--oem 3 --psm 6')



    image = cv2.imread('black_white.jpg')

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






    cv2.imwrite('rectangled.jpg', image)

    image = image[abs(miny-5):maxy+5, abs(minx-5):maxx+5]
    try:
        string = pytesseract.image_to_string(image, config = r'--oem 3 --psm 6')
        cv2.imwrite('cropped.jpg', image)
    except:
        pass


    image1 = cv2.imread('rectangled.jpg')

    for i, el in enumerate(data.splitlines()):
        if i == 0:
            continue

        el = el.split()

        x, y, w, h = int(el[6]), int(el[7]), int(el[8]), int(el[9])

        cv2.rectangle(image1, (x, y), (w + x, h + y), (0, 0, 255), 1)
    cv2.imwrite('rectangled.jpg', image1)




    return string



def debug(v1):




    lt = [0]*len(v1)
    v1 = [char for char in v1]

    x = 0
    while x <= len(v1)-2:
        if v1[x].isalpha() and v1[x] == v1[x].lower():
            if v1[x+1].isalpha() and v1[x+1] == v1[x+1].lower():

                v1[x] = v1[x].upper()
                x+=1
        x += 1


    for x in range(len(v1)-1):
        if v1[x].isdigit():
            v1[x+1] = v1[x+1].upper()

    v1[0] = v1[0].upper()




    v1 = ''.join(v1)
    return v1



def moreinfo(v11):

    if v11[0] == ' ':
        v11 = v11[1:len(v11)]

    if v11[-1] == ' ':
        v11 = v11[0:len(v11)-1]



    v11 = v11.replace(' ', '_')

    url = f'https://ru.wikipedia.org/wiki/{v11}'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')


    ses = requests.Session()

    log = ses.post(url, data={"search": v11})



    htc = log.text

    tree = html.fromstring(htc)

    element = tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/p[1]')
    if element != []:
        element = element[0]


    else:
        return 'error'

    eltt = element.text_content()

    element = tree.xpath('/html/body/div[3]/div[3]/div[5]/div[1]/p[2]')
    if element != []:
        element = element[0]
        eltt += element.text_content()



    return eltt


def splitv(v1):
    c = []
    k = -1
    for x in range(len(v1)):
        if (v1[x].upper() == v1[x]
            and v1[x].isalpha()) or v1[x] == '(' or v1[x] == ')':
            k += 1
            c.append('')
        c[k] += v1[x]

    if len(v1) > 3:
        for x in range(len(c) - 1):
            if c[x] == 'N' and c[x + 1] == 'O3':
                c[x] += c[x + 1]
                c.pop(x + 1)
            elif c[x] == 'C' and c[x + 1] == 'O3':
                c[x] += c[x + 1]
                c.pop(x + 1)
            elif c[x] == 'P' and c[x + 1] == 'O4':
                c[x] += c[x + 1]
                c.pop(x + 1)
            elif c[x] == 'S' and (c[x + 1] == 'O3' or c[x + 1] == 'O4'):
                c[x] += c[x + 1]
                c.pop(x + 1)
            elif c[x] == 'O' and c[x + 1] == 'H':
                c[x] += c[x + 1]
                c.pop(x + 1)
            if c[x - 1] == '(' and ')' in c[x + 1]:
                c[x] = '(' + c[x] + f'){c[x + 1][-1]}'
                c.pop(x - 1)
                c.pop(x)
                break

    return c


def typev(v1):
    for x in range(10):
        v1 = v1.replace(str(x), '')

    if v1 == 'HO':
        tv1 = typess[4]
    elif 'OH' in v1:
        tv1 = typess[2]
    elif v1 in metalls:
        tv1 = typess[0]
    elif v1 in nometalls:
        tv1 = typess[5]
    elif 'H' in splitv(v1) and ('NO' in v1 or 'SO' in v1 or 'PO' in v1
                                or 'SiO' in v1 or 'CO' in v1):
        tv1 = typess[7]
    else:
        c = splitv(v1)
        if 'H' in c and c[1] in ad_ress:
            tv1 = typess[7]
        elif len(c) == 2 and c[1] == 'O':
            if c[0] in metalls:
                tv1 = typess[1]
            elif c[0] in nometalls:
                tv1 = typess[6]
        elif 'NO' in v1 or 'SO' in v1 or 'PO' in v1 or 'SiO' in v1 or 'CO' in v1 or c[
            1] in ad_ress:
            if c[0] in metalls:
                tv1 = typess[3]
    return tv1


def vals(v1):
    if typev(v1) == typess[2]:
        if not v1[-1].isdigit():
            return [1, 1]
        else:
            return [int(v1[-1]), 1]

    if typev(v1) == typess[0]:

        if v1 in valvvs1:
            return [1]
        if v1 in valvvs2:
            return [2]
        if v1 in valvvs3:
            return [3]
        else:
            return ['-']

    if typev(v1) == typess[7]:
        if splitv(v1)[0][-1].isdigit():
            return [1, int(splitv(v1)[0][-1])]
        else:
            return [1, 1]

    if typev(v1) == typess[1] or typev(v1) == typess[6]:
        if splitv(v1)[0][-1] == '2':
            if splitv(v1)[1][-1].isalpha():
                return [1, 2]
            elif splitv(v1)[1][-1] == '3':
                return [3, 2]
            elif splitv(v1)[1][-1] == '5':
                return [5, 2]
            elif splitv(v1)[1][-1] == '7':
                return [7, 2]

        if splitv(v1)[0][-1].isalpha():
            if splitv(v1)[1][-1].isalpha():
                return [2, 2]
            elif splitv(v1)[1][-1] == '2':
                return [4, 2]
            elif splitv(v1)[1][-1] == '3':
                return [6, 2]

    if typev(v1) == typess[3]:

        valo = 0
        q1 = splitv(v1)[1]
        if '(' in splitv(v1)[1]:
            q1 = q1.replace('(', '')
            q1 = q1.replace(')', '')
            q1 = q1[0:len(q1) - 1]
        if q1 in valvvs1:
            valo = 1

        elif q1 in valvvs2:
            valo = 2
        elif q1 in valvvs3:
            valo = 3

        if q1 == splitv(v1)[1]:
            if 'O' in q1:
                cou2 = 1
            else:
                if q1[-1].isalpha():
                    cou2 = 1
                else:
                    cou2 = q1[-1]
        else:
            cou2 = int(splitv(v1)[1][-1])

        if splitv(v1)[0][-1].isalpha():
            cou1 = 1
        else:
            cou1 = int(splitv(v1)[0][-1])

        return [round(valo * cou2 / cou1), valo]
    if typev(v1) == typess[5]:
        return ['-']


def info(v1):
    an = f'type: {typev(v1)}\n' \
         f'valences: {vals(v1)}\n' \
         f'components: {splitv(v1)}'
    return an



def reaction(a):
    if a == 'H2O':
        return 'Вода'

    url = 'https://chemequations.com/ru/'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.text

    ses = requests.Session()

    log = ses.post(url, data={'s': a})

    htc = log.text

    tree = html.fromstring(htc)

    element = tree.xpath('/html/body/div[1]/section/div[1]/div/h1')
    if element != []:
        element = element[0]

    else:
        return 'error'

    eltt = element.text_content()

    if not '?' in eltt:
        if eltt != f'\n{a}':

            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')
            return eltt

        else:
            element = tree.xpath('/html/body/div[1]/section/div[1]/div/ul/li[1]/em')
            if element != []:
                element = element[0]
            else:
                return 'error'
            eltt = element.text_content()
            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')
            return eltt
    else:
        if '?' in eltt:
            element = tree.xpath(
                '/html/body/div[1]/section/div[1]/div/table/tbody/tr[1]/td[2]/a')[0]

            eltt = element.text_content()
            eltt = eltt.replace('(g)', '')
            eltt = eltt.replace('(l)', '')
            eltt = eltt.replace('(al)', '')
            eltt = eltt.replace('(aq)', '')
            eltt = eltt.replace('(s)', '')

            return eltt


def replaces(ans):

    if ans[0].isdigit() and not '=' in ans:
        ans = ans[1:len(ans)]


    ans = ans.replace(' ','')
    ans = ans.replace('W', 'H')
    ans = ans.replace('\n','')
    ans = ans.replace('$','S')
    ans = ans.replace('0','O')
    ans = ans.replace('so4','SO4')
    ans = ans.replace('Cb','Cl')
    ans = ans.replace('Ct', 'Cl')
    ans = ans.replace('No', 'Na')
    ans = ans.replace('NA', 'Na')
    ans = ans.replace('CL', 'Cl')
    ans = ans.replace('OL', 'O2')
    ans = ans.replace('OD', 'O2')
    ans = ans.replace('*', '+')
    ans = ans.replace('Me', 'Mn')
    ans = ans.replace('O1', 'O2')
    ans = ans.replace('H1', 'H2')
    ans = ans.replace('HD', 'H2')
    ans = ans.replace('|', '')
    ans = ans.replace(':', '')
    ans = ans.replace('H5', 'H2')
    ans = ans.replace(',', '2')
    ans = ans.replace('Ms', 'Mg')
    ans = ans.replace('ClL', 'Cl2')
    ans = ans.replace('ClD', 'Cl2')
    ans = ans.replace('Ha', 'H2')
    ans = ans.replace('Ho', 'H2')
    ans = ans.replace('Hr', 'H2')
    ans = ans.replace('O)', 'O2')
    ans = ans.replace('O72', 'O2')
    ans = ans.replace('s', '3')
    ans = ans.replace('HL', 'H2')




    return ans


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!\n"
                         "I am chemistry bot.\n"
                         "Send reaction or an element.\n"
                         "You also can send a photo of reaction.\n")



def replace1(v1):
    v1 = v1.replace('(I)','')
    v1 = v1.replace('(II)','')
    v1 = v1.replace('(III)','')
    v1 = v1.replace('(IV)','')
    v1 = v1.replace('(VI)','')
    v1 = v1.replace('(VII)','')
    v1 = v1.replace(' ','')
    return v1



@dp.message_handler(content_types=['text'])
async def test(message: types.Message):
    ans = message.text


    ans = debug(ans)
    print(ans)
    print(reaction(ans))
    if ans == '':
        ans = 'error'
    else:
        try:
            global ans1
            ans1 = reaction(ans)

            await message.answer(ans1)
            if replace1(ans1).isalpha() and ans1 != 'error':

                back_in_black = 1


            else:
                await message.answer(ans1)
                back_in_black = 0


        except:
            ans = 'error'

    try:
        if not '+' in ans:

            ans = info(ans)


            if back_in_black == 1:
                await message.answer(ans, reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text='More info', callback_data='in')]]))
            else:
                await message.answer(ans)
    except:
        pass



@dp.message_handler(content_types=['photo'])
async def image(message):
    file_id = message.photo[-1].file_id

    photo_file = await bot.get_file(file_id)
    file_path = "original.jpg"
    await photo_file.download(file_path)
    ans = imag()

    print(ans)

    if ans != '':
        ans = replaces(ans)
        await message.answer(ans)


    else:
        await message.answer('error')

    if ans == '':
        ans = 'error'
    else:
        try:
            global ans1
            ans1 = debug(ans1)
            ans1 = reaction(ans)

            if replace1(ans1).isalpha() and ans1 != 'error':
                back_in_black = 1
            else:
                back_in_black = 0
            await message.answer(ans1)
        except:
            ans = 'error'

    try:
        print(ans)
        if not '+' in ans:
            print(ans)

            ans = info(ans)
            print(ans)
            if back_in_black == 1:

                await message.answer(ans, reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text='More info', callback_data='in')]]))

            else:
                await message.answer(ans)
    except Exception as e:
        print('execution error')
        print(e)
    del file_path



async def main():
    await dp.start_polling(bot)




@dp.callback_query_handler(text='in')
async def send_message(callback: types.CallbackQuery):
    await callback.message.answer(moreinfo(ans1))

    await callback.answer()





if __name__ == "__main__":
    asyncio.run(main())
