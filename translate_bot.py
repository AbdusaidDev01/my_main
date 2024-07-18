import asyncio
from aiogram import types, Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from googletrans import Translator

API_TOKEN = "6653561504:AAFwxMbOVvgjTmuJQnLf657WWGpkY84FAF4"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

translator = Translator()

# Create a keyboard for language selection
language_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="English"), KeyboardButton(text="Русский")]
], resize_keyboard=True)

class TranslationStates(StatesGroup):
    choose_language = State()
    translate_message = State()

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(TranslationStates.choose_language)
    await message.answer(f"Asalou aleykum {message.from_user.full_name}", reply_markup=language_keyboard)

@dp.message(TranslationStates.choose_language, F.text == "Русский")
async def set_language_rus(message: types.Message, state: FSMContext):
    await state.update_data(language='ru')
    await state.set_state(TranslationStates.translate_message)
    await message.answer("Вы выбрали русский язык. Теперь отправьте сообщение для перевода.", reply_markup=ReplyKeyboardRemove())

@dp.message(TranslationStates.choose_language, F.text == "English")
async def set_language_eng(message: types.Message, state: FSMContext):
    await state.update_data(language='en')
    await state.set_state(TranslationStates.translate_message)
    await message.answer("You chose English. Now send a message to translate.", reply_markup=ReplyKeyboardRemove())

@dp.message(TranslationStates.translate_message)
async def translate_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    target_language = user_data.get('language')
    translated_text = translator.translate(text=message.text, dest=target_language)
    await message.answer(f"Translated message: {translated_text.text}")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

