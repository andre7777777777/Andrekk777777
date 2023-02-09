from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import platform, asyncio, subprocess

token = "6035713420:AAHLc8mmiW4dTRww7T4CTVC6B8blEmX7jVA" # Токен

time = 1 # Промежуток времени между пингами(в сек.)
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

class ips(StatesGroup):
	ip = State()

@dp.message_handler(commands=["start"])
async def message_handler(message: types.Message, state: FSMContext):
	msg = "Введите свой IP-адрес"

	await bot.send_message(message.chat.id, msg)
	await ips.ip.set()

@dp.message_handler(state=ips.ip)
async def code_telegram(message: types.Message, state: FSMContext):
	if ping(message.text) == True:
		msg = f"🟢 <b>Информация</b>\n" \
			  f"├ IP: <code>{message.text}</code>\n" \
			  f"└ IP-адрес подключён к сети\n"
		await bot.send_message(message.chat.id, msg)
		while True:
			if ping(message.text) == True:
				await asyncio.sleep(time)
			else:
				msg = f"🔴 <b>Информация</b>\n" \
					  f"├ IP: <code>{message.text}</code>\n" \
					  f"└ IP-адрес отключился от сети\n"
				await bot.send_message(message.chat.id, msg)
				break
	else:
		msg = f"🔴 <b>Информация</b>\n" \
			  f"├ IP: <code>{message.text}</code>\n" \
			  f"└ IP-адрес отключён от сети\n"
		await bot.send_message(message.chat.id, msg)
		while True:
			if ping(message.text) == True:
				msg = f"🟢 <b>Информация</b>\n" \
					  f"├ IP: <code>{message.text}</code>\n" \
					  f"└ IP-адрес подключился к сети\n"
				await bot.send_message(message.chat.id, msg)
				break
			else:
				await asyncio.sleep(time)

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0

if __name__ == '__main__':
	print("Bot started.")
	executor.start_polling(dp)