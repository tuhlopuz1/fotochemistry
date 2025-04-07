import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from src.parsing import moreinfo, reaction
from src.utils import debug, replace1, info, replaces
from src.image_processing import imag


load_dotenv()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!\n"
                         "I am chemistry bot.\n"
                         "Send reaction or an element.\n"
                         "You also can send a photo of reaction.\n")
    


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
    file_path = "src/images/original.jpg"
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
            
            ans1 = debug(ans)
            ans1 = reaction(ans)

            if replace1(ans1).isalpha() and ans1 != 'error':
                back_in_black = 1
            else:
                back_in_black = 0
            await message.answer(ans1)
        except Exception as e:
            print(f'error: {e}')
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



@dp.callback_query_handler(text='in')
async def send_message(callback: types.CallbackQuery):
    await callback.message.answer(moreinfo(ans1))

    await callback.answer()