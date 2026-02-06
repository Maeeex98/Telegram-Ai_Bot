from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import ollama
import os

os.system("ollama create my_llama3 -f \"<<You're file>>\"")

TOKEN = "You're TOKEN"
LOG_CHAT_ID = "you're id"
bot = Bot(token=TOKEN)
dp = Dispatcher()

dialog_history = {}

def get_history(user_id):
    if user_id not in dialog_history:
        dialog_history[user_id] = []
    return dialog_history[user_id]

@dp.message(lambda m: m.chat.type in ['group', 'supergroup'], Command('ai'))
@dp.message(lambda m: m.chat.type == 'private')
async def ai_response(message: types.Message):
    user_id = message.from_user.id
    history = get_history(user_id)
    history.append({"role": "user", "content": message.text})

    await bot.send_chat_action(message.chat.id, "typing")

    response = ollama.chat(
        model='my_llama3',
        messages=history,
    )
    bot_msg = response['message']['content']
    history.append({"role": "assistant", "content": bot_msg})

    await message.answer(bot_msg)

    await bot.send_message(
        LOG_CHAT_ID,
        f"👤: {message.from_user.full_name}: {message.text}\n\n"
        f"🤖: {bot_msg}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())   