import asyncio
from aiogram import Bot, Dispatcher, types, filters


bot = Bot(token="6653561504:AAFwxMbOVvgjTmuJQnLf657WWGpkY84FAF4")
dp = Dispatcher(bot=bot)


@dp.message(filters.Command("start"))
async def start(message: types.Message):
    await message.answer(f"Asalomu aleykum {message.from_user.full_name} echo hushkelibsiz")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
