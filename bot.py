import asyncio
import logging
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config
from datetime import datetime
from aiogram import html
from aiogram import F
from aiogram.filters import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# bot = Bot(token="5939449175:AAHzob6lv9QjjJQE0_Wwtlb4TR1xhAC6YUc")

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("<b>Hello!</b>")

# Хэндлер на команду /test1
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")

# Хэндлер на команду /dice
@dp.message(Command("dice"))
async def cmd_dice(message: types.Message, bot: Bot):
    await bot.send_dice(message.from_user.id, emoji=DiceEmoji.DICE)

# Хендлер эхо текста с указанием времени написания и сохр.форматирования
# @dp.message(F.text)
# async def echo_with_time(message: types.Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M:%S')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="HTML")

# Хендлер эхо на гифку
@dp.message(F.animation)
async def echo_gif(message: types.Message):
    await message.reply_animation(message.animation.file_id)




# КНОПКИ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        # [types.KeyboardButton(text="С пюрешкой")],
        # [types.KeyboardButton(text="Без пюрешки")]

        [
        types.KeyboardButton(text="С пюрешкой"),
        types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи")
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

    @dp.message(Text("С пюрешкой"))
    async def with_puree(message: types.Message):
        # после выбора, убирает кнопки
        await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
        # await message.reply("Отличный выбор!")

    @dp.message(lambda message: message.text == "Без пюрешки")
    async def without_puree(message: types.Message):
        # после выбора, убирает кнопки
        await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())
        # await message.reply("Так невкусно!")


# Keyboard Builder
# Для более динамической генерации кнопок можно воспользоваться сборщиком клавиатур.
# Нам пригодятся следующие методы:
# add(<KeyboardButton>) — добавляет кнопку в память сборщика;
# adjust(int1, int2, int3...) — делает строки по int1, int2, int3... кнопок;
# as_markup() — возвращает готовый объект клавиатуры;
# button(<params>) — добавляет кнопку с заданными параметрами,
# тип кнопки (Reply или Inline) определяется автоматически.
# Создадим пронумерованную клавиатуру размером 4×4:

@dp.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

# Колбэки
@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )
@dp.callback_query(Text("random_value"))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
