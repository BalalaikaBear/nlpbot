import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_token import api

from objects import Order, FoodType, Size
from menu import menu
from test1 import tokenise, read_order

bot: Bot = Bot(token=api)
dp: Dispatcher = Dispatcher()

# клавиатура
kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Пицца'),
    KeyboardButton(text='Закуски'),
    KeyboardButton(text='Напитки')]], resize_keyboard=True)

order: Order = Order()
prepared_examples: list[str] = [
    'Заказать две большие пиццы с ветчиной с грибами и беконом + 2 фри и колу',
    'Пепперони с ветчиной + стакан сока',
    'Две порции картофеля фри и американо + салат Цезарь'
]


# КОМАНДЫ ----------------------------------------------------------------------------------------------------------- *
@dp.message(Command('info', 'инфо', 'help', 'помощь'))
async def help_answer(message: types.Message) -> None:
    """Команда помощь"""
    await message.answer(
        'Здравствуйте! Я умный бот по заказу еды. Напишите что бы вы хотели заказать.\n' +
        'Например: _' + random.choice(prepared_examples) + '_',
        parse_mode='Markdown', reply_markup=kb
    )


@dp.message(Command('reset', 'сброс'))
async def reset_order(message: types.Message, order: Order) -> None:
    """Сброс заказа"""
    order.reset()
    await message.answer('Ваш заказ сброшен. Напишите что бы вы хотели заказать.')


# МЕНЮ -------------------------------------------------------------------------------------------------------------- *
@dp.message(F.text.in_({'Пицца', 'пицца'}))
async def show_menu(message: types.Message) -> None:
    """Отображает меню ресторана"""
    answer: str = ""
    for pizza in menu:
        if pizza.food_type == FoodType.PIZZA:
            # название
            answer += f'*Пицца {pizza.name}*\n'

            # описание
            if pizza.description:
                answer += f'{pizza.description}\n'

            # цена
            answer += 'Цена: '
            answer += f'малая {pizza.price[Size.S]}Р ' if isinstance(pizza.price, dict) and pizza.price.get(
                Size.S) else ''
            answer += f'средняя {pizza.price[Size.M]}Р ' if isinstance(pizza.price, dict) and pizza.price.get(
                Size.M) else ''
            answer += f'большая {pizza.price[Size.L]}Р ' if isinstance(pizza.price, dict) and pizza.price.get(
                Size.L) else ''
            answer += f'{pizza.price}Р ' if isinstance(pizza.price, int) else ''
            answer += '\n'
    await message.answer(answer, parse_mode='Markdown')


@dp.message(F.text.in_({'Закуски', 'закуски'}))
async def show_menu(message: types.Message) -> None:
    """Отображает меню ресторана"""
    answer: str = ""
    for snack in menu:
        if snack.food_type == FoodType.SNACK:
            # название
            answer += f'*{snack.name}*\n'

            # описание
            if snack.description:
                answer += f'{snack.description}\n'

            # цена
            answer += 'Цена: '
            answer += f'малая {snack.price[Size.S]}Р ' if isinstance(snack.price, dict) and snack.price.get(
                Size.S) else ''
            answer += f'средняя {snack.price[Size.M]}Р ' if isinstance(snack.price, dict) and snack.price.get(
                Size.M) else ''
            answer += f'большая {snack.price[Size.L]}Р ' if isinstance(snack.price, dict) and snack.price.get(
                Size.L) else ''
            answer += f'{snack.price}Р ' if isinstance(snack.price, int) else ''
            answer += '\n'
    await message.answer(answer, parse_mode='Markdown')


@dp.message(F.text.in_({'Напитки', 'напитки'}))
async def show_menu(message: types.Message) -> None:
    """Отображает меню ресторана"""
    answer: str = ""
    for drink in menu:
        if drink.food_type == FoodType.DRINK:
            # название
            answer += f'*{drink.name}*\n'

            # описание
            if drink.description:
                answer += f'{drink.description}\n'

            # цена
            answer += 'Цена: '
            answer += f'малая {drink.price[Size.S]}Р ' if isinstance(drink.price, dict) and drink.price.get(
                Size.S) else ''
            answer += f'средняя {drink.price[Size.M]}Р ' if isinstance(drink.price, dict) and drink.price.get(
                Size.M) else ''
            answer += f'большая {drink.price[Size.L]}Р ' if isinstance(drink.price, dict) and drink.price.get(
                Size.L) else ''
            answer += f'{drink.price}Р ' if isinstance(drink.price, int) else ''
            answer += '\n'
    await message.answer(answer, parse_mode='Markdown')


# ОПРЕДЕЛИТЕЛЬ ТЕКСТА ----------------------------------------------------------------------------------------------- *
@dp.message()
async def all_messages(message: types.Message, order: Order) -> None:
    """Определение текста пользователя и чтение заказа"""
    tokens: list[str] = tokenise(message.text)
    order, answer = read_order(tokens, order)
    if order.has_something():
        await message.answer(f'%s. Ваш заказ:\n%s' % (answer, order.to_text()), parse_mode='Markdown')
    else:
        await message.answer(answer)


async def main():
    await dp.start_polling(bot, order=order)


if __name__ == '__main__':
    asyncio.run(main())
