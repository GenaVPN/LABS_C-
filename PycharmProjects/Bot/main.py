import logging
import json
import os
import config
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove, InputFile, FSInputFile
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация бота
BOT_TOKEN = config.BOT_TOKEN
ADMINS_FILE = "admins.json"
USERS_FILE = "users.json"

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Флаг для отслеживания состояния рассылки
is_broadcasting = False


# Загрузка данных
def load_data():
    data = {"admins": set(), "users": set()}

    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "r") as f:
            data["admins"] = set(json.load(f))
    else:
        data["admins"].add(511514835)  # Ваш ID

    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data["users"] = set(json.load(f))

    return data


def save_data(data):
    with open(ADMINS_FILE, "w") as f:
        json.dump(list(data["admins"]), f)
    with open(USERS_FILE, "w") as f:
        json.dump(list(data["users"]), f)


data = load_data()
admins = data["admins"]
users = data["users"]
user_chats = {}


# Клавиатура админ-панели
def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="📩 Массовая рассылка")],
            [KeyboardButton(text="👥 Управление админами")],
            [KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="❌ Закрыть панель")]
        ],
        resize_keyboard=True
    )


async def is_admin(user_id: int):
    return user_id in admins


@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if await is_admin(message.from_user.id):
        await message.answer(
            "🔐 <b>Админ-панель</b> активирована",
            reply_markup=admin_keyboard()
        )
    else:
        await message.answer("⛔ У вас нет прав доступа к этой команде")


@dp.message(Command("start"))
async def start_command(message: types.Message):
    users.add(message.from_user.id)
    save_data({"admins": admins, "users": users})

    if await is_admin(message.from_user.id):
        await message.answer(
            "👋 <b>Привет, администратор!</b>\nИспользуй /admin для доступа к панели управления",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "👋 Привет! Напиши мне сообщение, и я перешлю его администраторам.",
            reply_markup=ReplyKeyboardRemove()
        )


# Обработчик для начала рассылки
@dp.message(F.text == "📩 Массовая рассылка")
async def start_broadcast(message: types.Message):
    global is_broadcasting

    if not await is_admin(message.from_user.id):
        return

    if is_broadcasting:
        await message.answer("❗ Рассылка уже выполняется, дождитесь завершения")
        return

    is_broadcasting = True
    await message.answer(
        "📩 <b>Начало массовой рассылки</b>\n\n"
        "Отправьте ОДНО сообщение для рассылки (текст или фото с подписью)\n"
        "Используйте /cancel для отмены",
        reply_markup=ReplyKeyboardRemove()
    )


# Обработчик контента для рассылки (только одно сообщение)
@dp.message(F.chat.id.in_(admins), F.content_type.in_({'photo', 'text'}))
async def process_broadcast(message: types.Message):
    global is_broadcasting

    if not is_broadcasting or not await is_admin(message.from_user.id):
        return

    if not message.text and not message.photo:
        is_broadcasting = False
        await message.answer("❌ Нет контента для рассылки", reply_markup=admin_keyboard())
        return

    if not users:
        is_broadcasting = False
        await message.answer("❌ Нет пользователей для рассылки", reply_markup=admin_keyboard())
        return

    await message.answer(f"⏳ Начинаю рассылку для {len(users)} пользователей...")

    success = failed = blocked = 0
    broadcast_content = {
        "type": "photo" if message.photo else "text",
        "content": message.photo[-1].file_id if message.photo else message.text,
        "caption": message.caption if message.photo else None
    }

    for user_id in list(users):
        try:
            if broadcast_content["type"] == "photo":
                await bot.send_photo(
                    chat_id=user_id,
                    photo=broadcast_content["content"],
                    caption=broadcast_content["caption"] or ""
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=broadcast_content["content"]
                )
            success += 1
        except Exception as e:
            failed += 1
            if "bot was blocked" in str(e).lower():
                blocked += 1
                users.discard(user_id)

    if blocked:
        save_data({"admins": admins, "users": users})

    is_broadcasting = False
    await message.answer(
        f"📊 <b>Результаты рассылки</b>\n\n"
        f"✅ Успешно: <b>{success}</b>\n"
        f"❌ Не удалось: <b>{failed}</b>\n"
        f"🚫 Заблокировали бота: <b>{blocked}</b>\n"
        f"👥 Осталось пользователей: <b>{len(users)}</b>",
        reply_markup=admin_keyboard()
    )


# Остальные обработчики остаются без изменений
# (show_admins, manage_admins, reply_to_user, etc.)

# Обработчик команды /cancel
@dp.message(Command("cancel"))
async def cancel_handler(message: types.Message):
    global is_broadcasting

    if await is_admin(message.from_user.id):
        is_broadcasting = False
        await message.answer(
            "❌ Текущее действие отменено",
            reply_markup=admin_keyboard()
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    if not os.path.exists(ADMINS_FILE):
        save_data({"admins": admins, "users": users})

    import asyncio

    asyncio.run(main())