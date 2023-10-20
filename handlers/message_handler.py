from loader import bot, dp
import config as cfg

from aiogram import types

import base as db

__all__ = ['dp']


@dp.message_handler(commands = ['id'])
async def idcommand(message: types.Message):
    await message.reply(text = f"{message.chat.id}\n{message.from_user.id}\n{message.message_thread_id}")

@dp.message_handler(content_types=['text', 'voice', 'audio', 'photo', 'video', 'sticker', 'video_note'])
async def textChat(message: types.Message):
    await db.createTables()
    if message.message_thread_id == None and message.from_user.id == cfg.owner_id:
        users = await db.getAllUsers()

        for user in users:
            try:
                user = user[0]
                if message.content_type == 'text':
                    await bot.send_message(chat_id=user, text=message.text)
                elif message.content_type == 'voice':
                    await bot.send_voice(chat_id=user, voice=message.voice.file_id)
                elif message.content_type == 'audio':
                    if message.caption:
                        await bot.send_audio(chat_id=user, audio=message.audio.file_id, caption = message.caption)
                    else:
                        await bot.send_audio(chat_id=user, audio=message.audio.file_id)
                elif message.content_type == 'photo':
                    if message.caption:
                        await bot.send_photo(chat_id=user, photo=message.photo[-1].file_id, caption = message.caption)
                    else:
                        await bot.send_photo(chat_id=user, photo=message.photo[-1].file_id)
                elif message.content_type == 'video':
                    if message.caption:
                        await bot.send_video(chat_id=user, video=message.video.file_id, caption = message.caption)
                    else:
                        await bot.send_video(chat_id=user, video=message.video.file_id)
                elif message.content_type == 'sticker':
                    await bot.send_sticker(chat_id=user, sticker=message.sticker.file_id)
                elif message.content_type == 'video_note':
                    await bot.send_video_note(chat_id=user, video_note=message.video_note.file_id)
            except Exception as E:
                print(E)

    elif message.message_thread_id and message.from_user.id == cfg.owner_id:
        user = await db.getUserFromThreadId(thread_id=message.message_thread_id)
        if message.content_type == 'text':
                await bot.send_message(chat_id=user, text=message.text)
        elif message.content_type == 'voice':
                await bot.send_voice(chat_id=user, voice=message.voice.file_id)
        elif message.content_type == 'audio':
                if message.caption:
                    await bot.send_audio(chat_id=user, audio=message.audio.file_id, caption = message.caption)
                else:
                    await bot.send_audio(chat_id=user, audio=message.audio.file_id)
        elif message.content_type == 'photo':
                if message.caption:
                    await bot.send_photo(chat_id=user, photo=message.photo[-1].file_id, caption = message.caption)
                else:
                    await bot.send_photo(chat_id=user, photo=message.photo[-1].file_id)
        elif message.content_type == 'video':
                if message.caption:
                    await bot.send_video(chat_id=user, video=message.video.file_id, caption = message.caption)
                else:
                    await bot.send_video(chat_id=user, video=message.video.file_id)
        elif message.content_type == 'sticker':
                await bot.send_sticker(chat_id=user, sticker=message.sticker.file_id)
        elif message.content_type == 'video_note':
                await bot.send_video_note(chat_id=user, video_note=message.video_note.file_id)

    else:
        isExist = await db.isExist(message.from_user.id)
        if isExist is False:
            chat = await bot.create_forum_topic(chat_id=cfg.chat_id, name=f"{message.from_user.first_name} | {message.from_user.id} | @{message.from_user.username}")
            await db.insertUser(message.from_user.id, message.from_user.first_name, chat.message_thread_id)
            if message.text != '/start':
                await bot.send_message(chat_id=cfg.chat_id, text=message.text, message_thread_id=chat.message_thread_id)
        else:
            thread_id = await db.getThread(message.from_user.id)
            if message.content_type == 'text':
                await bot.send_message(chat_id=cfg.chat_id, text=message.text, message_thread_id=thread_id)
            elif message.content_type == 'voice':
                await bot.send_voice(chat_id=cfg.chat_id, voice=message.voice.file_id, message_thread_id=thread_id)
            elif message.content_type == 'audio':
                if message.caption:
                    await bot.send_audio(chat_id=cfg.chat_id, audio=message.audio.file_id, message_thread_id=thread_id, caption = message.caption)
                else:
                    await bot.send_audio(chat_id=cfg.chat_id, audio=message.audio.file_id, message_thread_id=thread_id)
            elif message.content_type == 'photo':
                if message.caption:
                    await bot.send_photo(chat_id=cfg.chat_id, photo=message.photo[-1].file_id, message_thread_id=thread_id, caption = message.caption)
                else:
                    await bot.send_photo(chat_id=cfg.chat_id, photo=message.photo[-1].file_id, message_thread_id=thread_id)
            elif message.content_type == 'video':
                if message.caption:
                    await bot.send_video(chat_id=cfg.chat_id, video=message.video.file_id, message_thread_id=thread_id, caption = message.caption)
                else:
                    await bot.send_video(chat_id=cfg.chat_id, video=message.video.file_id, message_thread_id=thread_id)
            elif message.content_type == 'sticker':
                await bot.send_sticker(chat_id=cfg.chat_id, sticker=message.sticker.file_id, message_thread_id=thread_id)
            elif message.content_type == 'video_note':
                await bot.send_video_note(chat_id=cfg.chat_id, video_note=message.video_note.file_id, message_thread_id=thread_id)

