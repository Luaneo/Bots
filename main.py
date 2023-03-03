import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from PIL import Image
from random import randint


async def julia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = *map(lambda string: eval (string.replace(',', '.')),
                context.args), 0, 0
    cX, cY = args[0], args[1]
    maxIter = 255

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Создание множества Жюлиа при c = {cX} + {cY}i, подождите...')

    width, height, zoom = 1920, 1080, 1
    bitmap = Image.new("RGB", (width, height), "white")

    pix = bitmap.load()

    for x in range(width):
        for y in range(height):
            zx = 1.5*(x - width/2)/(0.5*zoom*width)
            zy = 1.0*(y - height/2)/(0.5*zoom*height)
            i = maxIter
            while zx*zx + zy*zy < 4 and i > 1:
                tmp = zx*zx - zy*zy + cX
                zy, zx = 2.0*zx*zy + cY, tmp
                i -= 1
            pix[x, y] = (i << 21) + (i << 10) + (i << 3)

    id = randint(0, 1000000)
    bitmap.save(fp=f'julia{id}.png')

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f'julia{id}.png', caption=f'Множество Жюлиа при c = {cX} + {cY}i')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Этот бот создаёт множества Жюлиа.
Используйте команду /julia и укажите два аргумента после неё через пробел (значение `c` по оси Re и по оси Im соответственно), чтобы создать множество Жюлиа""")


if __name__ == '__main__':
    application = ApplicationBuilder().token(
        open('api.key').readline()).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('julia', julia))

    application.run_polling()
