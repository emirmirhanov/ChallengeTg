from tgmanage import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from connect_db import post_one, chek_status, chek_all_status, perform_task
from aiogram.dispatcher.filters import BoundFilter
import datetime


class MorningVideo(StatesGroup):
    video = State()
    routine = State()


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()


dp.filters_factory.bind(MyFilter)


@dp.message_handler(Command('post'), is_admin=True)
async def post_publication(message: types.Message):
    post = post_one()
    await message.delete()
    if post:
        await message.answer(f"{post}")
    elif post is None:
        await message.answer("Нет активных постов")


@dp.message_handler(Command('post'))
async def post_delete(message: types.Message):
    await message.delete()


@dp.message_handler(Command('chekAllStatus'), is_admin=True)
async def chek_all_status_fn(message: types.Message):
    await message.delete()
    result = chek_all_status()
    people = ''
    if result:
        for i in result:
            people += '@' + i[0] + ': ' + '❤' * i[1] + '\n' + '\n'
        await message.answer(f"""Статистика участников:
{people}""")
    else:
        await message.answer("Пока нет участников")


@dp.message_handler(Command('chekAllStatus'))
async def status_delete(message: types.Message):
    await message.delete()


@dp.message_handler(Command('morningVideo'))
@dp.message_handler(Command('dailyRoutine'))
async def add_data(message: types.Message):
    global id_mess
    result = chek_status(message.from_user.username)
    if result and result[3] > 0 and message['date'].time() < datetime.time(15, 30, 00) and (message.text == '/morningvideo' or message.text == '/morningvideo@Challenges_test_bot'):
        id_mess = (await message.answer('Отправьте видео'))
        await message.delete()
        await MorningVideo.video.set()
    elif result and result[3] > 0 and message['date'].time() < datetime.time(15, 30, 00) and (message.text == '/dailyroutine' or message.text == '/dailyroutine@Challenges_test_bot'):
        id_mess = (await message.answer('Отправьте Текст')).message_id
        await message.delete()
        await MorningVideo.routine.set()
    else:
        await message.reply('Уже время вышло')


@dp.message_handler(state=MorningVideo.video, content_types=['video', 'video_note'])
async def get_video(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, id_mess)
    result = chek_status(message.from_user.username)
    perform_task(message['date'], result[2], 'morningVideo')
    await state.finish()


@dp.message_handler(state=MorningVideo.routine, content_types=['text'])
async def get_video(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, id_mess)
    result = chek_status(message.from_user.username)
    perform_task(message['date'], result[2], 'dailyRoutine')
    await state.finish()
