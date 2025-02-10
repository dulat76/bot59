import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "7889104731:AAGN2YRqTNZpdZlfylwQhNQmycPfQCCnwo0"  # Вставьте сюда токен от BotFather
GROUP_ID = "1155525830"  # Замените на ID вашей группы

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Основное меню выбора адресата
sections = {
    "0": "Учебная часть",
    "1": "Хозяйственная часть",
    "2": "Столовая",
    "3": "Воспитательная часть"
}

subcategories = {
    "0": {
        "0": "Расписание занятий",
        "1": "Преподаватели",
        "2": "Домашние задания",
        "3": "Экзамены и зачёты",
        "4": "Другое"
    },
    "1": {
        "0": "Поломки и неисправности",
        "1": "Освещение и отопление",
        "2": "Мебель и оборудование",
        "3": "Другое"
    },
    "2": {
        "0": "Качество еды",
        "1": "Ассортимент и меню",
        "2": "Обслуживание",
        "3": "Другое"
    },
    "3": {
        "0": "Конфликты и поведение",
        "1": "Внеурочные мероприятия",
        "2": "Посещение и пропуски",
        "3": "Другое"
    }
}

topic_ids = {
    "Расписание занятий": 101,
    "Преподаватели": 102,
    "Домашние задания": 103,
    "Экзамены и зачёты": 104,
    "Другое": 105,
    "Поломки и неисправности": 201,
    "Освещение и отопление": 202,
    "Мебель и оборудование": 203,
    "Качество еды": 301,
    "Ассортимент и меню": 302,
    "Обслуживание": 303,
    "Конфликты и поведение": 401,
    "Внеурочные мероприятия": 402,
    "Посещение и пропуски": 403
}

user_states = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    for key, value in sections.items():
        keyboard.button(text=f"{key} - {value}", callback_data=f"section_{key}")
    await message.answer("Выберите адресата:", reply_markup=keyboard.as_markup())

@dp.callback_query()
async def process_section(callback: types.CallbackQuery):
    section_id = callback.data.replace("section_", "")
    user_states[callback.from_user.id] = {"section": section_id}
    keyboard = InlineKeyboardBuilder()
    for key, value in subcategories[section_id].items():
        keyboard.button(text=f"{key} - {value}", callback_data=f"sub_{key}")
    await callback.message.edit_text("Выберите подкатегорию:", reply_markup=keyboard.as_markup())

@dp.callback_query()
async def process_subcategory(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    section_id = user_states[user_id]["section"]
    subcat_id = callback.data.replace("sub_", "")
    subcat = subcategories[section_id][subcat_id]
    user_states[user_id]["subcategory"] = subcat
    await callback.message.edit_text("Введите ваше сообщение:")

@dp.message()
async def process_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_states and "subcategory" in user_states[user_id]:
        subcat = user_states[user_id]["subcategory"]
        topic_id = topic_ids.get(subcat, None)
        if topic_id:
            text = f"📌 Новая заявка в разделе *{subcat}*:\n{message.text}"
            await bot.send_message(GROUP_ID, text, message_thread_id=topic_id, parse_mode="Markdown")
            await message.answer("✅ Ваша заявка отправлена!")
            del user_states[user_id]
        else:
            await message.answer("Ошибка: не удалось определить тему.")
    else:
        await message.answer("Пожалуйста, начните с команды /start.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
