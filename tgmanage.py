from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from connect_db import update_live_morning_video
import datetime
TOKEN = '5176859204:AAHj1xFktkzMaQpfB8hHxjGUH6Ta0iTV9FE'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

DELAY = 1


def repeat(coro, loop):
	asyncio.ensure_future(coro(), loop=loop)
	loop.call_later(DELAY, repeat, coro, loop)


async def update_live():
	date = datetime.datetime.now().date()
	custom_time_morning = "5:32:0"
	custom_time_daily_routine = "9:33:0"
	time = datetime.datetime.now().time()
	new_time = f"{time.hour}:{time.minute}:{time.second}"
	if new_time == custom_time_morning:
		update_live_morning_video(date, 'morningVideo')
	elif new_time == custom_time_daily_routine:
		update_live_morning_video(date, 'dailyRoutine')


if __name__ == '__main__':
	from otherHandlers import dp

	loop = asyncio.get_event_loop()
	loop.call_later(DELAY, repeat, update_live, loop)
	executor.start_polling(dp, skip_updates=True, loop=loop)
