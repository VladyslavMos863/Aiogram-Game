from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import time
import asyncio
import schedule
import requests


TOKEN = '6989176302:AAEGID1PoEQX2M3xX63-vY_egkp4fukJWg4'


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Player_one'), KeyboardButton('Player_two'), KeyboardButton('Shop'), KeyboardButton('Atack'))


kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb2.add(KeyboardButton('AK-47'), KeyboardButton('knife'), KeyboardButton('back'))


weapon_list = ['AK-47', 'KNIFE']   
    

class Form(StatesGroup):
    player1 = State()
    player2 = State()


class Player():
    hp = 100
    pay = 0
    weapon = []


player_one = Player()
player_two = Player()


async def time_to_pay():
    player_one.pay += 5
    player_two.pay += 5
    print('I working')
    print(player_one.__dict__)


async def main():
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()

async def periodic_time_to_pay():
    while True:
        await asyncio.sleep(3)
        await time_to_pay()


async def start_tasks():
    task1 = asyncio.create_task(main())
    task2 = asyncio.create_task(periodic_time_to_pay())
    await asyncio.gather(task1, task2)


@dp.message_handler(text=['AK-47'], state=Form.player1)
async def atack_player_one(message: types.Message):
    if player_one.pay == 30:
        player_one.weapon.append('AK-47')


@dp.message_handler(text=['Atack'], state=Form.player1)
async def atack_player_one(message: types.Message):
    player_two.hp -= 30
    await bot.send_message(chat_id=message.from_user.id, text=player_two.hp)
    
    
@dp.message_handler(text=['Atack'], state=Form.player2)
async def atack_player_two(message: types.Message):
    player_one.hp -= 30
    await bot.send_message(chat_id=message.from_user.id, text=player_one.hp)


@dp.message_handler(commands=['player_one'])
async def register_player_one(message: types.Message):
    await message.answer('Введи ник:')
    await Form.player1.set()
    
    
@dp.message_handler(commands=['player_two'])
async def register_player_one(message: types.Message):
    await message.answer('Введи ник:')
    await Form.player2.set()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет введи свой ник по команде player_one и player_two для второго игрока', reply_markup=kb)


@dp.message_handler(text=['Shop'], state=Form.player1)
@dp.message_handler(text=['Shop'], state=Form.player2)
async def shop(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Shop', reply_markup=kb2)


@dp.message_handler(commands=['menu'], state=Form.player1)
@dp.message_handler(commands=['menu'], state=Form.player2)
async def main_menu(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Menu', reply_markup=kb)
    
    
@dp.message_handler(text=['back'], state=Form.player1)
@dp.message_handler(text=['back'], state=Form.player2)
async def back(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='back', reply_markup=kb)
    
    
@dp.message_handler(text='Player_one', state=Form.player1)
async def player(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=player_one.hp)
    await bot.send_message(chat_id=message.from_user.id, text=player_one.pay)
    await bot.send_message(chat_id=message.from_user.id, text=player_one.weapon)
    
    
@dp.message_handler(text='Player_two', state=Form.player2)
async def player(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=player_two.hp)
    await bot.send_message(chat_id=message.from_user.id, text=player_two.pay)
    await bot.send_message(chat_id=message.from_user.id, text=player_two.weapon)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_tasks())
    executor.start_polling(dp, skip_updates=True)
    loop.run_forever()

