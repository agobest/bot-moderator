import asyncio
import logging
from datetime import date, datetime, timedelta 

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.markdown import hlink

from config import BOT_TOKEN, ADMIN_ID
from stop_words_function import contains_profanity
from db import Database


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database('storage_bot.db')


@dp.message(F.text.startswith('бан'), F.from_user.id == ADMIN_ID, ((F.chat.type == 'group') | (F.chat.type == 'supergroup')))
async def admin_ban_user(message: types.Message):
    """Функция бана юзера администратором"""
    try:
        if message.reply_to_message:
            await message.answer("Забанил!")
            db.add_banned_userx(message.reply_to_message.from_user.id)
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        else:
            await message.answer("Для бана юзера это должен быть ответ на сообщение!")
    except Exception as e:
        print(e)


@dp.message(F.new_chat_members)
async def delete_system_message(message: types.Message):
    """Функция удаления системных сообщений"""
    await message.delete()
    try:
        for user in message.new_chat_members:
            if db.get_banned_userx(user.id):
                await bot.ban_chat_member(message.chat.id, user.id)
                await bot.send_message(message.chat.id, '<b>Обнаружен спаммер! Удаляю</b>', parse_mode="HTML")
            elif not db.get_exist_userx(user.id):
                db.add_userx(user.id)
                dt = datetime.now() + timedelta(minutes=3)
                timestamp = dt.timestamp()
                await bot.restrict_chat_member(chat_id=message.chat.id, 
                                               user_id=user.id,
                                               permissions=types.ChatPermissions(False),
                                               until_date=timestamp)
                if db.get_exist_channelx(message.chat.id):
                    channel_url = db.get_channelx(message.chat.id)[0]
                    channel_text = hlink('канал', f'{channel_url}')
                    await message.answer(f'<b>Добро пожаловать, {user.full_name}!</b>\n'
                                          f'Перед началом использования бота подпишись на наш {channel_text}\n'
                                          'Возможность писать сообщения откроется через 3 минуты.',
                                           parse_mode="HTML",
                                           disable_web_page_preview = True)
                else:
                    await message.answer(f'<b>Добро пожаловать, {user.full_name}!</b>\n'
                                          'Возможность писать сообщения откроется через 3 минуты.',
                                           parse_mode="HTML")
            elif db.get_exist_userx(user.id):
                dt = datetime.now() + timedelta(minutes=3)
                timestamp = dt.timestamp()
                await bot.restrict_chat_member(chat_id=message.chat.id, 
                                               user_id=user.id,
                                               permissions=types.ChatPermissions(MutableTelegramObject=False),
                                               until_date=timestamp)   
                if db.get_exist_channelx(message.chat.id):
                    channel_url = db.get_channelx(message.chat.id)[0]
                    channel_text = hlink('канал', f'{channel_url}')
                    await message.answer(f'<b>Добро пожаловать, {user.full_name}!</b>\n'
                                          f'Перед началом использования бота подпишись на наш {channel_text}\n'
                                          'Возможность писать сообщения откроется через 3 минуты.',
                                           parse_mode="HTML",
                                           disable_web_page_preview = True)
                else:
                    await message.answer(f'<b>Добро пожаловать, {user.full_name}!</b>\n'
                                          'Возможность писать сообщения откроется через 3 минуты.',
                                           parse_mode="HTML")

    except Exception as e:
        print(e)


@dp.message(F.left_chat_member)
async def delete_system_message(message: types.Message):
    """Функция удаления системных сообщений"""
    await message.delete()


@dp.message((F.text.lower() == 'спасибо'), ((F.chat.type == 'group') | (F.chat.type == 'supergroup')))
async def user_send_message(message: types.Message):
    """Функция для отправки благодарностей юзеру"""
    try:
        if message.reply_to_message:
            if not db.get_exist_userx(message.reply_to_message.from_user.id):
                db.add_userx(message.reply_to_message.from_user.id)
            thanks_count = db.get_thanks_userx(message.reply_to_message.from_user.id)[0]
            thanks_count += 1
            db.add_thanks_userx(message.reply_to_message.from_user.id, thanks_count)
            message = message.reply_to_message
            await message.reply(f"<b>Спасибо, что помогаете сообществу!</b>\n"
                                f"Ваше количество благодарностей - <b>{thanks_count}</b>",
                                parse_mode='HTML')
    except Exception as e:
        print(e)


@dp.message(((F.chat.type == 'group') | (F.chat.type == 'supergroup')) & F.from_user.id != ADMIN_ID)
async def user_send_message(message: types.Message):
    """Функция проверки сообщения на запрещенные слова"""
    try:
        if not db.get_exist_userx(message.from_user.id):
            db.add_userx(message.from_user.id)
        if message.forward_from_chat:
            await message.delete()
            if message.from_user.username:
                await message.answer(f'❤️‍🔥@{message.from_user.username} ваше сообщение рекламного характера, по  размещению напишите 🤡 @alina_tech')
            else:
                await message.answer(f'❤️‍🔥{message.from_user.full_name} ваше сообщение рекламного характера, по  размещению напишите 🤡 @alina_tech')
        elif contains_profanity(str(message.text).lower()):
            if message.from_user.username:
                await message.answer(f'❤️‍🔥@{message.from_user.username} ваше сообщение рекламного характера, по  размещению напишите 🤡 @alina_tech')
            else:
                await message.answer(f'❤️‍🔥{message.from_user.full_name} ваше сообщение рекламного характера, по  размещению напишите 🤡 @alina_tech')
            await message.delete()
        else:
            pass
    except Exception as e:
        print(e)
    

@dp.message(Command("channel"), F.from_user.id == ADMIN_ID)
async def cmd_add(message: types.Message):
    try:
        chat_data = message.text.split(' ')
        chat_id = message.chat.id
        channel_url = message.text.split(' ')[-1]
        if db.get_exist_channelx(chat_id):
            db.delete_channelx(chat_id)
        db.add_channelx(chat_id, channel_url)
        m = await message.reply('Установил канал для данной группы!')
        await asyncio.sleep(60)
        await message.delete()
        await m.delete()
    except Exception as e:
        print(e)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
