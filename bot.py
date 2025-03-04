import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "7889104731:AAGN2YRqTNZpdZlfylwQhNQmycPfQCCnwo0"
GROUP_ID = "1155525830"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Локализации
languages = {
    "ru": {
        "sections": {
            "0": "Учебная часть",
            "1": "Хозяйственная часть",
            "2": "Столовая",
            "3": "Воспитательная часть",
            "4": "Объявления"
        },
        "subcategories": {
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
        },
        "messages": {
            "choose_lang": "Выберите язык:",
            "choose_section": "Выберите адресата:",
            "choose_subcategory": "Выберите подкатегорию:",
            "enter_message": "Введите ваше сообщение:",
            "success": "✅ Ваша заявка отправлена!",
            "error": "Ошибка: не удалось определить тему.",
            "start": "Пожалуйста, начните с команды /start."
        }
    },
    "kz": {
        "sections": {
            "0": "Оқу бөлімі",
            "1": "Шаруашылық бөлімі",
            "2": "Асхана",
            "3": "Тәрбие бөлімі",
            "4": "Хабарландырулар"
        },
        "subcategories": {
            "0": {
                "0": "Сабақ кестесі",
                "1": "Оқытушылар",
                "2": "Үй тапсырмалары",
                "3": "Емтихандар мен тестілер",
                "4": "Басқа"
            },
            "1": {
                "0": "Ақаулар мен бұзылулар",
                "1": "Жарықтандыру және жылыту",
                "2": "Жиһаз және жабдық",
                "3": "Басқа"
            },
            "2": {
                "0": "Тамақ сапасы",
                "1": "Ассортимент және мәзір",
                "2": "Қызмет көрсету",
                "3": "Басқа"
            },
            "3": {
                "0": "Қақтығыстар мен мінез-құлық",
                "1": "Сыныптан тыс іс-шаралар",
                "2": "Қатысу және сабақ қалу",
                "3": "Басқа"
            }
        },
        "messages": {
            "choose_lang": "Тілді таңдаңыз:",
            "choose_section": "Алғыр таңдаңыз:",
            "choose_subcategory": "Субкатегорияны таңдаңыз:",
            "enter_message": "Хабарды енгізіңіз:",
            "success": "✅ Сіздің өтінішіңіз жіберілді!",
            "error": "Қате: тақырыпты анықтау мүмкін емес.",
            "start": "/start пәрменінен бастаңыз."
        }
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
    "Посещение и пропуски": 403,
    "Сабақ кестесі": 101,
    "Оқытушылар": 102,
    "Үй тапсырмалары": 103,
    "Емтихандар мен тестілер": 104,
    "Басқа": 105,
    "Ақаулар мен бұзылулар": 201,
    "Жарықтандыру және жылыту": 202,
    "Жиһаз және жабдық": 203,
    "Тамақ сапасы": 301,
    "Ассортимент және мәзір": 302,
    "Қызмет көрсету": 303,
    "Қақтығыстар мен мінез-құлық": 401,
    "Сыныптан тыс іс-шаралар": 402,
    "Қатысу және сабақ қалу": 403
}

user_states = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Қазақша", callback_data="lang_kz")
    keyboard.button(text="Русский", callback_data="lang_ru")
    await message.answer(languages['ru']['messages']['choose_lang'], 
                        reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def process_language(callback: types.CallbackQuery):
    lang = callback.data.split('_')[1]
    user_states[callback.from_user.id] = {'lang': lang}
    await show_sections(callback.message, lang)

async def show_sections(message: types.Message, lang: str):
    keyboard = InlineKeyboardBuilder()
    sections = languages[lang]['sections']
    for key, value in sections.items():
        keyboard.button(text=f"{key} - {value}", callback_data=f"section_{key}")
    await message.edit_text(languages[lang]['messages']['choose_section'], 
                           reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data.startswith('section_'))
async def process_section(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_states[user_id]['lang']
    section_id = callback.data.replace("section_", "")
    user_states[user_id]["section"] = section_id
    
    keyboard = InlineKeyboardBuilder()
    subcats = languages[lang]['subcategories'][section_id]
    for key, value in subcats.items():
        keyboard.button(text=f"{key} - {value}", callback_data=f"sub_{key}")
        
    await callback.message.edit_text(languages[lang]['messages']['choose_subcategory'], 
                                   reply_markup=keyboard.as_markup())

@dp.callback_query(lambda c: c.data.startswith('sub_'))
async def process_subcategory(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_states[user_id]['lang']
    section_id = user_states[user_id]["section"]
    subcat_id = callback.data.replace("sub_", "")
    
    subcat = languages[lang]['subcategories'][section_id][subcat_id]
    user_states[user_id]["subcategory"] = subcat
    await callback.message.edit_text(languages[lang]['messages']['enter_message'])

@dp.message()
async def process_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_states and "subcategory" in user_states[user_id]:
        lang = user_states[user_id]['lang']
        subcat = user_states[user_id]["subcategory"]
        topic_id = topic_ids.get(subcat)
        
        if topic_id:
            text = f"📌 {languages[lang]['messages']['success']} *{subcat}*:\n{message.text}"
            await bot.send_message(GROUP_ID, text, message_thread_id=topic_id, parse_mode="Markdown")
            await message.answer(languages[lang]['messages']['success'])
            del user_states[user_id]
        else:
            await message.answer(languages[lang]['messages']['error'])
    else:
        lang = user_states.get(user_id, {}).get('lang', 'ru')
        await message.answer(languages[lang]['messages']['start'])

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
