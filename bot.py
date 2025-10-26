import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Configuration ---
# Bot Token from @BotFather
TOKEN = "8443628415:AAGld9KKD0x2JStEgmkqNBJqMCkGh061JI8"
# Link for "Открыть" and "Смотреть все анкеты" buttons
SITE_LINK = "https://chmpmrm.flirt-hotlady.com/wdk2cxh"

# File paths for the 25 photos (assuming they are in the current directory)
PHOTO_FILES = [
    "IMG_4158.jpeg", "IMG_4157.jpeg", "IMG_4156.jpeg", "IMG_4155.jpeg", "IMG_4154.jpeg",
    "IMG_4153.jpeg", "IMG_4149.jpeg", "IMG_4148.jpeg", "IMG_4147.jpeg", "IMG_4075.jpeg",
    "IMG_4144.jpeg", "IMG_4145.jpeg", "IMG_4142.jpeg", "IMG_4141.jpeg", "IMG_4139.jpeg",
    "IMG_4136.jpeg", "IMG_4137.jpeg", "IMG_4138.jpeg", "IMG_4135.jpeg", "IMG_4134.jpeg",
    "IMG_4133.jpeg", "IMG_4128.jpeg", "IMG_4131.jpeg", "IMG_4132.jpeg", "IMG_4124.jpeg"
]

# The first photo will be used for the welcome screen
WELCOME_PHOTO = PHOTO_FILES[0]

# Data for the 25 profiles
PROFILE_DATA = [
    {"name": "Анна", "text": "Ты мне сразу понравился… зайди, я покажу 😉"},
    {"name": "Галина", "text": "Не ожидала, что здесь встречу такого…💦"},
    {"name": "Валерия", "text": "Я сейчас дома одна 😘"},
    {"name": "Валентина", "text": "Ты уверен, что выдержишь мой взгляд? Пиши на сайт💋"},
    {"name": "Светлана", "text": "Хочу познакомиться, но не здесь 😏"},
    {"name": "Ольга", "text": "Зайди — я покажу, что значит “взрослое внимание”💦"},
    {"name": "Елена", "text": "Посмотри, что напишу тебе сейчас…💌"},
    {"name": "Татьяна", "text": "Может, продолжим там, где потише? Моя грудь голая"},
    {"name": "Наталья", "text": "Я не кусаюсь… если не попросишь 😌"},
    {"name": "Ирина", "text": "Смотри осторожно… втянуться легко в мой 5 размер😘"},
    {"name": "Мария", "text": "Не обещаю быть скромной хочу 🍆"},
    {"name": "Маргарита", "text": "У тебя взгляд, от которого теряю контроль напиши мне😉"},
    {"name": "Екатерина", "text": "Ты точно хочешь увидеть продолжение?🍓"},
    {"name": "Марина", "text": "Просто открой и почувствуй"},
    {"name": "Юлия", "text": "Не играй с огнём, я серьёзно"},
    {"name": "Виктория", "text": "Секунду… я только халат поправлю 😏"},
    {"name": "Алёна", "text": "Ты меня ищешь — я здесь"},
    {"name": "Людмила", "text": "Внимание! Опасно для самоконтроля 😌мои формы огонь"},
    {"name": "Надюша", "text": "Не удержалась — написала тебе хочу"},
    {"name": "Инна", "text": "Мне нравится, когда мужчина первый кликает и входит🔥"},
    {"name": "Лариса", "text": "Не смотри слишком долго — привыкнешь"},
    {"name": "Вероника", "text": "Хочешь узнать, чем закончится? Пиши любимый"},
    {"name": "Ника", "text": "Мне нужен только один. Может, это ты?"},
    {"name": "Наташа", "text": "Просто зайди… я всё покажу"},
    {"name": "Яна", "text": "Я ждала, когда именно ты появишься 💫"},
]

# Cities
CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]

# Group profiles by city (5 profiles per city)
PROFILES_PER_CITY = 5
CITY_PROFILES = {}
for i, city in enumerate(CITIES):
    start_index = i * PROFILES_PER_CITY
    end_index = start_index + PROFILES_PER_CITY
    city_profiles = []
    for j in range(PROFILES_PER_CITY):
        profile_index = start_index + j
        profile = PROFILE_DATA[profile_index]
        profile["photo"] = PHOTO_FILES[profile_index]
        city_profiles.append(profile)
    CITY_PROFILES[city] = city_profiles

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and photo with the 'Start' button."""
    welcome_text_raw = (
        "🔥 ВНИМАНИЕ: Настоящие Знакомства 35+! 🔥\n\n"
        "📍 Города: Москва, Санкт-Петербург, Новосибирск, Екатеринбург, Казань.\n\n"
        "💯 Гарантия: Здесь реальные женщины 35+ без ботов и пустых анкет.\n\n"
        "Нажмите \"Старт\" и начните прямо сейчас!"
    )
    welcome_text = escape_markdown_v2(welcome_text_raw)
    keyboard = [
        [InlineKeyboardButton("Старт", callback_data="show_cities")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send photo with caption and button
    try:
        with open(WELCOME_PHOTO, "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
    except FileNotFoundError:
        logger.error(f"Welcome photo not found: {WELCOME_PHOTO}")
        await update.message.reply_text(
            f"Ошибка: Не найдено приветственное фото ({WELCOME_PHOTO}).\n\n{welcome_text}",
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'
        )

async def show_cities(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the list of cities."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(city, callback_data=f"select_city_{city}")] for city in CITIES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_caption(
        caption="Выберите город:",
        reply_markup=reply_markup
    )

def get_profile_keyboard(city: str, profile_index: int) -> InlineKeyboardMarkup:
    """Generates the keyboard for a profile."""
    keyboard = [
        [InlineKeyboardButton("🟢 Сейчас онлайн", url=SITE_LINK)],
        [InlineKeyboardButton("Открыть", url=SITE_LINK)]
    ]
    # Navigation buttons
    navigation_buttons = []
    # If not the last profile, add "Next" button
    if profile_index < PROFILES_PER_CITY - 1:
        navigation_buttons.append(
            InlineKeyboardButton("Следующая ⏭️", callback_data=f"show_profile_{city}_{profile_index + 1}")
        )
    # If it's the last profile, add "Смотреть все анкеты" button
    if profile_index == PROFILES_PER_CITY - 1:
        navigation_buttons.append(
            InlineKeyboardButton("Смотреть все анкеты на сайте", url=SITE_LINK)
        )
    keyboard.append(navigation_buttons)
    # Add button to go back to city selection
    keyboard.append([InlineKeyboardButton("⬅️ Сменить город", callback_data="show_cities")])
    return InlineKeyboardMarkup(keyboard)

def escape_markdown_v2(text: str) -> str:
    """Helper function to escape special characters in MarkdownV2."""
    # List of special characters in MarkdownV2:
    # _, *, [, ], (, ), ~, `, >, #, +, -, =, |, {, }, ., !
    special_chars = r'_*[]()~`>#+-=|{}.!'
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def get_profile_caption(profile: dict, city: str) -> str:
    """Generates the caption for a profile."""
    name = escape_markdown_v2(profile['name'])
    text = escape_markdown_v2(profile['text'])
    city_escaped = escape_markdown_v2(city)
    return (
        f"*{name}*\n"
        f"_{text}_\n\n"
        f"📍 Город: {city_escaped}"
    )

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows a specific profile."""
    query = update.callback_query
    await query.answer()
    try:
        # Parse callback data: "show_profile_{city}_{index}"
        parts = query.data.split('_')
        if len(parts) < 4:
            logger.error(f"Invalid callback data: {query.data}")
            await query.edit_message_caption(caption="❌ Ошибка: Неверные данные")
            return
        city = parts[2]
        index_str = parts[3]
        profile_index = int(index_str)
        profiles = CITY_PROFILES.get(city)
        if not profiles or profile_index >= len(profiles):
            logger.error(f"Profile not found for city {city} at index {profile_index}")
            await query.edit_message_caption(caption="❌ Ошибка: Анкета не найдена")
            return

        profile = profiles[profile_index]
        caption = get_profile_caption(profile, city)
        reply_markup = get_profile_keyboard(city, profile_index)
        # Prepare the new photo and caption
        try:
            with open(profile["photo"], "rb") as photo_file:
                new_media = InputMediaPhoto(
                    media=photo_file,
                    caption=caption,
                    parse_mode='MarkdownV2'
                )
                # Edit the message to change the photo, caption, and keyboard
                await query.edit_message_media(
                    media=new_media,
                    reply_markup=reply_markup
                )
        except FileNotFoundError:
            logger.error(f"Profile photo not found: {profile['photo']}")
            # If photo not found, just edit the caption and keyboard
            await query.edit_message_caption(
                caption=f"❌ Ошибка: Не найдено фото\n\n{caption}",
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            await query.edit_message_caption(
                caption=f"❌ Ошибка загрузки\n\n{caption}",
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
    except Exception as e:
        logger.error(f"Error in show_profile: {e}")
        await query.edit_message_caption(caption="❌ Произошла ошибка. Напишите /start")

async def select_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles city selection and shows the first profile for that city."""
    query = update.callback_query
    await query.answer()
    try:
        # Parse callback data: "select_city_{city}"
        parts = query.data.split('_')
        if len(parts) < 3:
            logger.error(f"Invalid city callback: {query.data}")
            await query.edit_message_caption(caption="❌ Ошибка выбора города")
            return
        city = parts[2]
        # Show the first profile (index 0)
        profiles = CITY_PROFILES.get(city)
        if not profiles:
            logger.error(f"City not found: {city}")
            await query.edit_message_caption(caption="❌ Город не найден")
            return
        profile = profiles[0]
        caption = get_profile_caption(profile, city)
        reply_markup = get_profile_keyboard(city, 0)
        # Send the first profile
        try:
            with open(profile["photo"], "rb") as photo_file:
                new_media = InputMediaPhoto(
                    media=photo_file,
                    caption=caption,
                    parse_mode='MarkdownV2'
                )
                await query.edit_message_media(
                    media=new_media,
                    reply_markup=reply_markup
                )
        except FileNotFoundError:
            logger.error(f"Profile photo not found: {profile['photo']}")
            await query.edit_message_caption(
                caption=f"❌ Ошибка: Не найдено фото\n\n{caption}",
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
    except Exception as e:
        logger.error(f"Error in select_city: {e}")
        await query.edit_message_caption(caption="❌ Ошибка выбора города. Напишите /start")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))

    # on callback queries - handle button presses
    application.add_handler(CallbackQueryHandler(show_cities, pattern="^show_cities$"))
    application.add_handler(CallbackQueryHandler(select_city, pattern="^select_city_"))
    application.add_handler(CallbackQueryHandler(show_profile, pattern="^show_profile_"))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
